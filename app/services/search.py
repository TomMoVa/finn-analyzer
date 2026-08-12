from __future__ import annotations

import html
import os
import re
from urllib.parse import urlencode, urlparse

import httpx

BRAVE_URL = "https://api.search.brave.com/res/v1/web/search"
DDG_URL = "https://html.duckduckgo.com/html/"


class SearchError(RuntimeError):
    pass


def build_query(car: dict) -> str:
    parts = ["site:finn.no/mobility/item", car.get("make", ""), car.get("model", ""), str(car.get("year", "")), car.get("fuel", "")]
    return " ".join(part.strip() for part in parts if str(part).strip())


def build_finn_url(car: dict) -> str:
    query = " ".join(x for x in [car.get("make", ""), car.get("model", "")] if x).strip()
    params = {"q": query, "registration_class": "1"}
    year = str(car.get("year", ""))
    if year.isdigit():
        params["year_from"], params["year_to"] = str(max(1950, int(year) - 2)), str(int(year) + 2)
    return "https://www.finn.no/mobility/search/car?" + urlencode(params)


def _number(text: str) -> int | None:
    match = re.search(r"(?<!\d)(\d{2,3}(?:[ .\u00a0]\d{3})+|\d{5,7})\s*(?:kr|,-)", text, re.I)
    return int(re.sub(r"\D", "", match.group(1))) if match else None


def _normalise_url(url: str) -> str | None:
    from urllib.parse import unquote
    url = html.unescape(url)
    redirect = re.search(r"uddg=([^&]+)", url)
    if redirect:
        url = unquote(redirect.group(1))
    parsed = urlparse(url)
    if parsed.netloc not in {"www.finn.no", "finn.no"} or not re.search(r"/(?:mobility/item|car/used/ad\.html)", parsed.path):
        return None
    return f"https://www.finn.no{parsed.path}" + (f"?{parsed.query}" if parsed.query else "")


def parse_results(items: list[dict], car: dict) -> list[dict]:
    seen, output = set(), []
    wanted = f"{car.get('make', '')} {car.get('model', '')}".lower().split()
    for item in items:
        title = html.unescape(re.sub(r"<[^>]+>", "", item.get("title", ""))).strip()
        description = html.unescape(re.sub(r"<[^>]+>", " ", item.get("description", ""))).strip()
        url, haystack = _normalise_url(item.get("url", "")), f"{title} {description}".lower()
        price = _number(haystack)
        if not url or url in seen or not price or not all(word in haystack for word in wanted):
            continue
        year_match = re.search(r"\b(19\d{2}|20\d{2})\b", haystack)
        found_year = int(year_match.group(1)) if year_match else None
        if found_year and car.get("year") and abs(found_year - int(car["year"])) > 3:
            continue
        seen.add(url)
        output.append({"title": title, "description": description, "url": url, "price": price, "year": found_year})
    return output[:12]


async def search_comparables(car: dict) -> list[dict]:
    headers = {"User-Agent": "FINN-Analyzer/1.0 (+personal market research)"}
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True, headers=headers) as client:
            api_key = os.getenv("BRAVE_SEARCH_API_KEY")
            if api_key:
                response = await client.get(BRAVE_URL, params={"q": build_query(car), "count": 20}, headers={**headers, "X-Subscription-Token": api_key})
                response.raise_for_status()
                items = response.json().get("web", {}).get("results", [])
            else:
                response = await client.post(DDG_URL, data={"q": build_query(car), "kl": "no-no"})
                response.raise_for_status()
                items = [{"url": u, "title": t, "description": d} for u, t, d in re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</(?:a|div)>', response.text, re.I | re.S)]
    except (httpx.HTTPError, ValueError):
        return []
    return parse_results(items, car)



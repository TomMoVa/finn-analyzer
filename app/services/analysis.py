from __future__ import annotations

import re
from statistics import median


def parse_number(value: str | int | float) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    digits = re.sub(r"[^0-9]", "", value or "")
    if not digits:
        raise ValueError("missing number")
    return int(digits)


def analyse(car: dict, listings: list[dict]) -> dict:
    prices = [int(item["price"]) for item in listings if item.get("price", 0) > 0]
    market = int(median(prices)) if prices else None
    difference = car["price"] - market if market else None
    percent = round(difference / market * 100) if market else None
    if percent is None:
        verdict, tone = "Trenger sammenligningsgrunnlag", "neutral"
    elif percent <= -10:
        verdict, tone = "Lav pris mot markedet", "good"
    elif percent >= 10:
        verdict, tone = "Høy pris mot markedet", "bad"
    else:
        verdict, tone = "Nær markedspris", "neutral"
    return {"car": car, "listings": listings, "count": len(prices), "market_price": market, "difference": difference, "percent": percent, "verdict": verdict, "tone": tone}



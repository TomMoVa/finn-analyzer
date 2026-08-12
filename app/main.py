from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.analysis import analyse, parse_number
from app.services.search import SearchError, build_finn_url, search_comparables

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="FINN Bilanalys")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"form": {}, "results": None, "search_url": None})


@app.post("/analyser", response_class=HTMLResponse)
async def analyse_car(request: Request, make: str = Form(...), model: str = Form(...), year: str = Form(...), mileage: str = Form(...), price: str = Form(...), fuel: str = Form(""), transmission: str = Form("")):
    form = {"make": make.strip(), "model": model.strip(), "year": year.strip(), "mileage": mileage.strip(), "price": price.strip(), "fuel": fuel.strip(), "transmission": transmission.strip()}
    error, results = None, []
    try:
        car = {**form, "year": int(parse_number(year)), "mileage": parse_number(mileage), "price": parse_number(price)}
        if not (1950 <= car["year"] <= 2100) or car["price"] <= 0:
            raise ValueError
        results = await search_comparables(car)
        report = analyse(car, results)
    except (ValueError, TypeError):
        error, report = "Sjekk at år, kilometer og pris er gyldige tall.", None
    except SearchError as exc:
        error, report = str(exc), analyse(car, [])
    return templates.TemplateResponse(request=request, name="index.html", context={"form": form, "results": report, "error": error, "search_url": build_finn_url(form), "has_api_key": bool(os.getenv("BRAVE_SEARCH_API_KEY"))})



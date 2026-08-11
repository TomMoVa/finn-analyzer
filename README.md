# FINN Analyzer – mobil nettapp

Dette er en mobilvennlig prototype som analyserer annonser og finner sammenlignbare FINN-treff via en søkemotor-API.

## Hvorfor ikke scrape FINN direkte?
FINN opplyser at automatisert crawling/systematisk innhenting ikke er tillatt uten skriftlig tillatelse. Derfor henter denne appen ikke FINN-sider direkte. Den bruker i stedet Brave Search API for å finne offentlig indekserte FINN-resultater.

## Kom i gang lokalt
1. Installer Python 3.11+
2. `pip install -r requirements.txt`
3. Lag miljøvariabel `BRAVE_SEARCH_API_KEY`
4. `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Åpne `http://localhost:8000`

## Mobil
Når appen ligger på Render/Railway/Fly.io eller tilsvarende, åpner du URL-en på Samsung og velger:
Chrome → meny → «Legg til på startskjermen».

## Søkemotor
Opprett en Brave Search API-nøkkel og sett:
`BRAVE_SEARCH_API_KEY=din_nøkkel`

Appen fungerer også uten nøkkel i demo/manuell modus.

## Deploy til Render
- New Web Service
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment: legg inn `BRAVE_SEARCH_API_KEY`

## Viktig
Deal Score er en prisindikasjon, ikke en takst. Bruk tilstand, servicehistorikk, utstyr og faktisk salgspris i tillegg.


## Enkel publisering fra telefon

1. Opprett et GitHub-repository, f.eks. `finn-analyzer`.
2. Last opp alle filene i denne pakken til repoet.
3. Gå til Render og velg **New + → Blueprint**.
4. Koble GitHub-repoet.
5. Render finner `render.yaml` automatisk.
6. Legg inn miljøvariabelen `BRAVE_SEARCH_API_KEY`.
7. Trykk deploy.
8. Når tjenesten er grønn får du en fast HTTPS-adresse.
9. Åpne den på Samsung og velg **Legg til på startskjermen**.

Hvis du ikke har Brave Search API-nøkkel ennå, kan appen deployes uten den, men automatisk søk etter sammenlignbare annonser vil være deaktivert.

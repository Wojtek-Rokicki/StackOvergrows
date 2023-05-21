# SV-Hackathon-AdsDetect
Repository for Supervision Hackathon for project of detecting advertisements 
## IaaC Docker contenerization
W katalogu iaac znajduje się przykładowy szablon dla api gateway (katalog apigw) i kontenerów na skrypty (katalogi skrypt1, skrypt2, ...)

W każdym z katalogów znajduje się katalog app, gdzie można wrzucić skrypty do uruchamiania w ramach serwera FastAPI, listę wymaganych blbliotek zamieszczamy w pliku requirements.txt dla właściwego katalogu kontenera.

## Uruchomienie
Wywołujemy
```bash
cd app
docker compose up --build
```

### API

1. Pobierz [Postman](https://www.postman.com/downloads/) dla zapytań API.
2. Wczytaj plik konfiguracyjny: `SuperVisionHack.postman_collection.json`
3. Wykorzystuj endpointy:

#### `/query_browser`

```
{
    "url": "https://gazeta.pl",
    "query": "Inwestycje w złoto",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    "context": "Ewentualny kontekst przeglądarki"
}
```

#### `/query_site`

Input contract:

```
{
    "url": "https://www.google.com/",
    "query": "Dochód pasywny",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "context": "Ewentualny kontekst przeglądarki"
}
```

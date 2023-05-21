<<<<<<< HEAD
### API

1. Download [Postman](https://www.postman.com/downloads/) for api calls.
2. Load configuration file: `SuperVisionHack.postman_collection.json`
3. Use endpoints:

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
=======
# SV-Hackathon-AdsDetect
Repository for Supervision Hackathon for project of detecting advertisements 
## IaaC Docker contenerization
W katalogu iaac znajduje się przykładowy szablon dla api gateway (katalog apigw) i kontenerów na skrypty (katalogi skrypt1, skrypt2, ...)

W każdym z katalogów znajduje się katalog app, gdzie można wrzucić skrypty do uruchamiania w ramach serwera FastAPI, listę wymaganych blbliotek zamieszczamy w pliku requirements.txt dla właściwego katalogu kontenera.

Przykładowy flow znajduje się w apigw pod ścieżką `/flow_test1`, który wysyła zapytanie do kontenera skrypt1 pod ścieżką /test.
>>>>>>> iaac-poc

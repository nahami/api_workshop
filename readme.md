API Workshop
============

## Setup

Voer de volgende regels uit in de terminal:

1. python -m venv .venv
2.  MacOS:
    source .venv/bin/activate 
    Windows: 
    .\.venv\Scripts\Activate
3. Install the required packages using: 
    pip install -r requirements.txt
4. Start de API:
    uvicorn app:app --reload
5. (Optioneel) Start de webapp:
    streamlit run webapp.py


## API Structuur

De REST API draait op http://127.0.0.1:8000

| Methode | Endpoint       | Beschrijving              |
|---------|----------------|---------------------------|
| GET     | /items         | Alle items ophalen        |
| GET     | /items/{id}    | Één item ophalen op ID    |
| POST    | /items         | Nieuw item aanmaken       |
| PUT     | /items/{id}    | Bestaand item bijwerken   |
| DELETE  | /items/{id}    | Item verwijderen          |

### Datamodel (Item)
- naam        : string  (verplicht)
- prijs       : float   (verplicht)
- op_voorraad : bool    (optioneel, standaard: true)

### Automatische documentatie
- Swagger UI : http://127.0.0.1:8000/docs
- ReDoc      : http://127.0.0.1:8000/redoc


## Testen

Zie [tests.md](tests.md) voor een volledig overzicht van alle testgevallen.

Tests uitvoeren:
```powershell
pytest test_app.py -v
```

## Testen vanuit PowerShell

### GET – alle items ophalen
    Invoke-RestMethod -Method GET -Uri http://127.0.0.1:8000/items

### GET – één item ophalen (bijv. ID 1)
    Invoke-RestMethod -Method GET -Uri http://127.0.0.1:8000/items/1

### POST – nieuw item aanmaken
    $body = '{"naam": "Ayakkabi", "prijs": 299.99}'
    Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/items -ContentType "application/json" -Body $body

### PUT – item bijwerken (bijv. ID 1)
    $body = '{"naam": "Laptop Pro", "prijs": 1299.99, "op_voorraad": true}'
    Invoke-RestMethod -Method PUT -Uri http://127.0.0.1:8000/items/1 -ContentType "application/json" -Body $body

### DELETE – item verwijderen (bijv. ID 1)
    Invoke-RestMethod -Method DELETE -Uri http://127.0.0.1:8000/items/1

> Let op: gebruik in PowerShell altijd Invoke-RestMethod in plaats van curl,
> omdat curl in PowerShell een alias is voor Invoke-WebRequest en anders gedrag heeft.


## Git

git config --global user.name "My Name"
git config --global user.email "myemail@example.com"

git remote add origin https://github.com/nahami/api_workshop.git
git branch -M main
git push -u origin main


## Extra

db viewer sqlite: https://sqlitebrowser.org
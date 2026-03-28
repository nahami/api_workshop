# Test Documentatie

Alle tests staan in `test_app.py` en worden uitgevoerd met pytest.

## Tests uitvoeren

```powershell
.\.venv\Scripts\Activate
pytest test_app.py -v
```

---

## GET /items – alle items ophalen

| Test | Verwacht resultaat |
|------|--------------------|
| `test_get_alle_items` | Status 200, 3 items in de response |

---

## GET /items/{id} – één item ophalen

| Test | Invoer | Verwacht resultaat |
|------|--------|--------------------|
| `test_get_item_bestaat` | ID 1 | Status 200, naam="Laptop", prijs=999.99, op_voorraad=True |
| `test_get_item_niet_gevonden` | ID 999 | Status 404, detail="Item niet gevonden" |
| `test_get_item_op_voorraad_false` | ID 3 | Status 200, op_voorraad=False |

---

## POST /items – nieuw item aanmaken

| Test | Invoer | Verwacht resultaat |
|------|--------|--------------------|
| `test_maak_nieuw_item` | naam="Monitor", prijs=299.99 | Status 201, id=4, op_voorraad=True (standaard) |
| `test_maak_item_met_alle_velden` | naam="Headset", prijs=79.99, op_voorraad=False | Status 201, op_voorraad=False |
| `test_maak_item_verhoogt_id` | 3 items achter elkaar aanmaken | Derde item krijgt id=6 |
| `test_maak_item_ontbrekend_verplicht_veld` | alleen prijs, naam ontbreekt | Status 422 (validatiefout) |

---

## PUT /items/{id} – item bijwerken

| Test | Invoer | Verwacht resultaat |
|------|--------|--------------------|
| `test_update_item` | ID 1, naam="Laptop Pro", prijs=1299.99 | Status 200, bericht="Item bijgewerkt", gewijzigde waarden terug |
| `test_update_item_niet_gevonden` | ID 999 | Status 404, detail="Item niet gevonden" |

---

## DELETE /items/{id} – item verwijderen

| Test | Invoer | Verwacht resultaat |
|------|--------|--------------------|
| `test_verwijder_item` | ID 2 | Status 200, bericht="Item verwijderd", naam="Muis"; daarna GET op ID 2 geeft 404 |
| `test_verwijder_item_niet_gevonden` | ID 999 | Status 404, detail="Item niet gevonden" |
| `test_verwijder_item_vermindert_lijst` | verwijder ID 1, dan GET /items | Nog 2 items over |

---

## Test isolatie

Elke test wordt uitgevoerd met een verse kopie van de in-memory database via de `reset_state` fixture:

```python
@pytest.fixture(autouse=True)
def reset_state():
    app_module.items = {
        1: Item(naam="Laptop", prijs=999.99),
        2: Item(naam="Muis", prijs=29.99),
        3: Item(naam="Toetsenbord", prijs=49.99, op_voorraad=False),
    }
    app_module.volgende_id = 4
    yield
```

Dit zorgt ervoor dat tests elkaar niet beïnvloeden.

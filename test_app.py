import pytest
from fastapi.testclient import TestClient

import app as app_module
from app import app, Item


@pytest.fixture(autouse=True)
def reset_state():
    """Reset de in-memory database voor elke test."""
    app_module.items = {
        1: Item(naam="Laptop", prijs=999.99),
        2: Item(naam="Muis", prijs=29.99),
        3: Item(naam="Toetsenbord", prijs=49.99, op_voorraad=False),
    }
    app_module.volgende_id = 4
    yield


client = TestClient(app)


# ── GET /items ────────────────────────────────────────────────────────────────

def test_get_alle_items():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


# ── GET /items/{id} ───────────────────────────────────────────────────────────

def test_get_item_bestaat():
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["naam"] == "Laptop"
    assert data["prijs"] == 999.99
    assert data["op_voorraad"] is True


def test_get_item_niet_gevonden():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item niet gevonden"


def test_get_item_op_voorraad_false():
    response = client.get("/items/3")
    assert response.status_code == 200
    assert response.json()["op_voorraad"] is False


# ── POST /items ───────────────────────────────────────────────────────────────

def test_maak_nieuw_item():
    nieuw = {"naam": "Monitor", "prijs": 299.99}
    response = client.post("/items", json=nieuw)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["item"]["naam"] == "Monitor"
    assert data["item"]["op_voorraad"] is True  # standaard waarde


def test_maak_item_met_alle_velden():
    nieuw = {"naam": "Headset", "prijs": 79.99, "op_voorraad": False}
    response = client.post("/items", json=nieuw)
    assert response.status_code == 201
    assert response.json()["item"]["op_voorraad"] is False


def test_maak_item_verhoogt_id():
    client.post("/items", json={"naam": "A", "prijs": 1.0})
    client.post("/items", json={"naam": "B", "prijs": 2.0})
    response = client.post("/items", json={"naam": "C", "prijs": 3.0})
    assert response.json()["id"] == 6


def test_maak_item_ontbrekend_verplicht_veld():
    response = client.post("/items", json={"prijs": 99.99})  # naam ontbreekt
    assert response.status_code == 422


# ── PUT /items/{id} ───────────────────────────────────────────────────────────

def test_update_item():
    update = {"naam": "Laptop Pro", "prijs": 1299.99, "op_voorraad": True}
    response = client.put("/items/1", json=update)
    assert response.status_code == 200
    data = response.json()
    assert data["bericht"] == "Item bijgewerkt"
    assert data["item"]["naam"] == "Laptop Pro"
    assert data["item"]["prijs"] == 1299.99


def test_update_item_niet_gevonden():
    update = {"naam": "Onbekend", "prijs": 0.0}
    response = client.put("/items/999", json=update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item niet gevonden"


# ── DELETE /items/{id} ────────────────────────────────────────────────────────

def test_verwijder_item():
    response = client.delete("/items/2")
    assert response.status_code == 200
    data = response.json()
    assert data["bericht"] == "Item verwijderd"
    assert data["item"]["naam"] == "Muis"

    # controleer dat het item echt weg is
    response = client.get("/items/2")
    assert response.status_code == 404


def test_verwijder_item_niet_gevonden():
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item niet gevonden"


def test_verwijder_item_vermindert_lijst():
    client.delete("/items/1")
    response = client.get("/items")
    assert len(response.json()) == 2

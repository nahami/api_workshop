from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Stap 1: Maak een FastAPI app aan ---
app = FastAPI(title="API Workshop Demo")


# --- Stap 2: Definieer een datamodel ---
class Item(BaseModel):
    naam: str
    prijs: float
    op_voorraad: bool = True


# --- Stap 3: In-memory "database" (gewoon een dict) ---
items: dict[int, Item] = {
    1: Item(naam="Laptop", prijs=999.99),
    2: Item(naam="Muis", prijs=29.99),
    3: Item(naam="Toetsenbord", prijs=49.99, op_voorraad=False),
}
volgende_id = 4


# --- Stap 4: Endpoints ---

# GET alle items
@app.get("/items")
def get_alle_items():
    return items


# GET één item op ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item niet gevonden")
    return items[item_id]


# POST – nieuw item aanmaken
@app.post("/items", status_code=201)
def maak_item(item: Item):
    global volgende_id
    items[volgende_id] = item
    nieuw_id = volgende_id
    volgende_id += 1
    return {"id": nieuw_id, "item": item}


# PUT – bestaand item bijwerken
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item niet gevonden")
    items[item_id] = item
    return {"bericht": "Item bijgewerkt", "item": item}


# DELETE – item verwijderen
@app.delete("/items/{item_id}")
def verwijder_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item niet gevonden")
    verwijderd = items.pop(item_id)
    return {"bericht": "Item verwijderd", "item": verwijderd}

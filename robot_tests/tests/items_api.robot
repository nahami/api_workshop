*** Settings ***
Resource        ../resources/api_keywords.robot
Suite Setup     Maak API verbinding
Suite Teardown  Sluit API verbinding

Documentation   Feature: Items beheren via de REST API
...             Als een extern systeem
...             Wil ik items kunnen ophalen, aanmaken, bijwerken en verwijderen
...             Zodat ik de voorraad kan beheren


*** Test Cases ***

# ══════════════════════════════════════════════════════════════════════════════
# GET /items
# ══════════════════════════════════════════════════════════════════════════════

Scenario: Alle items ophalen als de API beschikbaar is
    [Tags]    GET    happy-path
    Given Ik haal alle items op
    Then De statuscode is 200
    And De response bevat 3 items

# ══════════════════════════════════════════════════════════════════════════════
# GET /items/{id}
# ══════════════════════════════════════════════════════════════════════════════

Scenario: Een bestaand item ophalen op ID
    [Tags]    GET    happy-path
    Given Ik haal item 1 op
    Then De statuscode is 200
    And Het item heeft naam "Laptop"
    And Het item heeft prijs 999.99
    And Het item is op voorraad

Scenario: Een item ophalen dat niet bestaat
    [Tags]    GET    unhappy-path
    Given Ik haal item 999 op
    Then De statuscode is 404
    And De foutmelding is "Item niet gevonden"

Scenario: Een item ophalen dat niet op voorraad is
    [Tags]    GET    happy-path
    Given Ik haal item 3 op
    Then De statuscode is 200
    And Het item heeft naam "Toetsenbord"
    And Het item is niet op voorraad

# ══════════════════════════════════════════════════════════════════════════════
# POST /items
# ══════════════════════════════════════════════════════════════════════════════

Scenario: Een nieuw item aanmaken met verplichte velden
    [Tags]    POST    happy-path
    Given Ik maak een nieuw item aan met naam "Monitor" en prijs 299.99
    Then De statuscode is 201
    And Het nieuwe item heeft id 4

Scenario: Een nieuw item aanmaken met alle velden inclusief op_voorraad
    [Tags]    POST    happy-path
    Given Ik maak een nieuw item aan met naam "Headset", prijs 79.99 en op_voorraad ${False}
    Then De statuscode is 201

Scenario: Een item aanmaken zonder verplicht veld naam
    [Tags]    POST    unhappy-path    validatie
    Given Ik maak een item aan zonder naam en prijs 99.99
    Then De statuscode is 422

# ══════════════════════════════════════════════════════════════════════════════
# PUT /items/{id}
# ══════════════════════════════════════════════════════════════════════════════

Scenario: Een bestaand item bijwerken
    [Tags]    PUT    happy-path
    Given Ik update item 1 met naam "Laptop Pro" en prijs 1299.99
    Then De statuscode is 200
    And De bevestiging is "Item bijgewerkt"

Scenario: Een niet-bestaand item proberen bij te werken
    [Tags]    PUT    unhappy-path
    Given Ik update item 999 met naam "Onbekend" en prijs 0.0
    Then De statuscode is 404
    And De foutmelding is "Item niet gevonden"

# ══════════════════════════════════════════════════════════════════════════════
# DELETE /items/{id}
# ══════════════════════════════════════════════════════════════════════════════

Scenario: Een bestaand item verwijderen
    [Tags]    DELETE    happy-path
    Given Ik verwijder item 2
    Then De statuscode is 200
    And De bevestiging is "Item verwijderd"

Scenario: Een niet-bestaand item proberen te verwijderen
    [Tags]    DELETE    unhappy-path
    Given Ik verwijder item 999
    Then De statuscode is 404
    And De foutmelding is "Item niet gevonden"

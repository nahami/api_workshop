*** Settings ***
Library     RequestsLibrary
Library     Collections


*** Variables ***
${BASE_URL}     http://127.0.0.1:8000
${SESSION}      api_session


*** Keywords ***

# ── Setup / Teardown ──────────────────────────────────────────────────────────

Maak API verbinding
    Create Session    ${SESSION}    ${BASE_URL}    verify=True

Sluit API verbinding
    Delete All Sessions


# ── GET ───────────────────────────────────────────────────────────────────────

Ik haal alle items op
    ${response}=    GET On Session    ${SESSION}    /items
    Set Test Variable    ${RESPONSE}    ${response}

Ik haal item ${id} op
    ${response}=    GET On Session    ${SESSION}    /items/${id}    expected_status=any
    Set Test Variable    ${RESPONSE}    ${response}


# ── POST ──────────────────────────────────────────────────────────────────────

Ik maak een nieuw item aan met naam "${naam}" en prijs ${prijs}
    ${body}=    Create Dictionary    naam=${naam}    prijs=${prijs}
    ${response}=    POST On Session    ${SESSION}    /items    json=${body}    expected_status=any
    Set Test Variable    ${RESPONSE}    ${response}

Ik maak een nieuw item aan met naam "${naam}", prijs ${prijs} en op_voorraad ${op_voorraad}
    ${body}=    Create Dictionary    naam=${naam}    prijs=${prijs}    op_voorraad=${op_voorraad}
    ${response}=    POST On Session    ${SESSION}    /items    json=${body}    expected_status=any
    Set Test Variable    ${RESPONSE}    ${response}

Ik maak een item aan zonder naam en prijs ${prijs}
    ${body}=    Create Dictionary    prijs=${prijs}
    ${response}=    POST On Session    ${SESSION}    /items    json=${body}    expected_status=any
    Set Test Variable    ${RESPONSE}    ${response}


# ── PUT ───────────────────────────────────────────────────────────────────────

Ik update item ${id} met naam "${naam}" en prijs ${prijs}
    ${body}=    Create Dictionary    naam=${naam}    prijs=${prijs}    op_voorraad=${True}
    ${response}=    PUT On Session    ${SESSION}    /items/${id}    json=${body}    expected_status=any
    Set Test Variable    ${RESPONSE}    ${response}


# ── DELETE ────────────────────────────────────────────────────────────────────

Ik verwijder item ${id}
    ${response}=    DELETE On Session    ${SESSION}    /items/${id}    expected_status=any
    Set Test Variable    ${RESPONSE}    ${response}


# ── Assertions ────────────────────────────────────────────────────────────────

De statuscode is ${code}
    Should Be Equal As Integers    ${RESPONSE.status_code}    ${code}

De response bevat ${aantal} items
    ${data}=    Set Variable    ${RESPONSE.json()}
    Length Should Be    ${data}    ${aantal}

Het item heeft naam "${naam}"
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Be Equal    ${data}[naam]    ${naam}

Het item heeft prijs ${prijs}
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Be Equal As Numbers    ${data}[prijs]    ${prijs}

Het item is op voorraad
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Be True    ${data}[op_voorraad]

Het item is niet op voorraad
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Not Be True    ${data}[op_voorraad]

De foutmelding is "${bericht}"
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Be Equal    ${data}[detail]    ${bericht}

Het nieuwe item heeft id ${id}
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Be Equal As Integers    ${data}[id]    ${id}

De bevestiging is "${bericht}"
    ${data}=    Set Variable    ${RESPONSE.json()}
    Should Be Equal    ${data}[bericht]    ${bericht}

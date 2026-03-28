# Deployment

De API wordt automatisch gebouwd en gedeployed via GitHub Actions.

Workflow bestand: `.github/workflows/build-deploy.yml`

---

## Workflow overzicht

Trigger: elke push naar `main` of `murat`, en pull requests naar `main`.

### Stage 1 – Build & Unit Tests

| Stap | Actie |
|------|-------|
| 1 | Code checkouten |
| 2 | Python 3.12 instellen (met pip cache) |
| 3 | `pip install -r requirements.txt` |
| 4 | `pytest test_app.py` – deploy wordt geblokkeerd bij falende tests |
| 5 | ZIP-artifact aanmaken (exclusief `.venv`, `__pycache__`, db-bestanden) |
| 6 | Artifact uploaden (7 dagen bewaard) |

### Stage 2 – Deploy naar Development

Draait alleen als Stage 1 slaagt.

| Stap | Actie |
|------|-------|
| 1 | Artifact downloaden |
| 2 | Inloggen bij Azure via Service Principal |
| 3 | Deployen naar Azure Web App |
| 4 | Startup commando instellen: `uvicorn app:app --host 0.0.0.0` |
| 5 | Uitloggen bij Azure |

---

## Azure configuratie

| Instelling | Waarde |
|------------|--------|
| Azure Web App naam | `api-workshop-dev` |
| Resource Group | `rg-api-workshop-dev` |
| GitHub Environment | `development` |

---

## Vereiste GitHub Secrets

Ga naar **GitHub repo → Settings → Secrets and variables → Actions** en voeg toe:

| Secret | Beschrijving |
|--------|--------------|
| `AZURE_CREDENTIALS_DEV` | JSON output van de Service Principal (zie hieronder) |

### Service Principal aanmaken

```bash
az ad sp create-for-rbac \
  --name "sp-api-workshop-dev" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/rg-api-workshop-dev \
  --sdk-auth
```

De output ziet er zo uit:

```json
{
  "clientId": "<CLIENT_ID>",
  "clientSecret": "<CLIENT_SECRET>",
  "subscriptionId": "<SUBSCRIPTION_ID>",
  "tenantId": "<TENANT_ID>"
}
```

Kopieer de volledige JSON als waarde voor het secret `AZURE_CREDENTIALS_DEV`.

---

## Lokaal testen voor deployment

Zorg dat de unit tests slagen voordat je pusht:

```powershell
.\.venv\Scripts\Activate
pytest test_app.py -v
```

Start de API lokaal:

```powershell
uvicorn app:app --reload
```

API beschikbaar op: http://127.0.0.1:8000  
Swagger UI: http://127.0.0.1:8000/docs

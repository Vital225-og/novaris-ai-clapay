# Novaris AI Backend

Backend FastAPI du Sprint 4 pour Novaris AI, solution anti-fraude Mobile Money.

Le backend utilise maintenant SQLite via SQLAlchemy pour persister :

- les transactions analysées
- les scores de risque
- les alertes fraude
- les KPI du dashboard

## Installation

Depuis le dossier `backend/` :

```bash
pip install -r requirements.txt
```

## Configuration

La base locale par defaut est :

```text
sqlite:///./novaris_ai.db
```

La variable d environnement `DATABASE_URL` permet de surcharger cette valeur.

## Lancement local

```bash
uvicorn app.main:app --reload
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

Au demarrage, l application :

- initialise les tables SQLite
- charge les donnees de demo depuis `backend/app/data/demo_transactions.json`
- charge les alertes de demo depuis `backend/app/data/demo_alerts.json`

## Dependances

- `sqlalchemy`

## Endpoints

### Santé

- `GET /api/v1/health`

### Transactions

- `POST /api/v1/transactions/analyze`
- `GET /api/v1/transactions`
- `GET /api/v1/transactions/{transaction_id}`

### Dashboard

- `GET /api/v1/dashboard/kpis`

### Alertes

- `GET /api/v1/alerts`
- `GET /api/v1/alerts/{alert_id}`
- `POST /api/v1/alerts/{alert_id}/resolve`

## Comportement de persistance

Quand `POST /api/v1/transactions/analyze` est appelé :

- la transaction est analysee par le `Risk Orchestrator`
- la transaction est enregistree en base SQLite
- le score de risque detaille est enregistre en base SQLite
- une alerte est creee automatiquement si `risk_score >= 60`
- le contrat JSON de la reponse reste identique

Statuts d alerte :

- `OPEN`
- `IN_REVIEW`
- `RESOLVED`

Niveaux d alerte :

- `Modéré`
- `Élevé`
- `Critique`

## Dashboard KPI

Le dashboard lit directement les donnees SQLite pour retourner :

- `total_transactions`
- `total_alerts`
- `critical_alerts`
- `review_alerts`
- `allowed_transactions`
- `blocked_transactions`
- `protected_amount`
- `average_risk_score`

### Exemple de reponse

```json
{
  "total_transactions": 25,
  "total_alerts": 8,
  "critical_alerts": 3,
  "review_alerts": 5,
  "allowed_transactions": 12,
  "blocked_transactions": 3,
  "protected_amount": 2450000,
  "average_risk_score": 64
}
```

## Exemple de requete

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/transactions/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Client Demo",
    "sender_phone": "+2250700000000",
    "receiver_phone": "+2250500000000",
    "amount": 450000,
    "transaction_type": "withdrawal",
    "agent_id": "AG-044",
    "device_id": "DEV-NEW-991",
    "location": "Abidjan",
    "hour": 1,
    "transactions_last_10min": 8,
    "is_new_device": true,
    "sim_changed_recently": true,
    "agent_risk_level": "high"
  }'
```

## Commandes de test

```bash
pytest
```

## Note sur `pytest` sous Windows

Les tests passent, mais dans cet environnement Windows le runner peut rester actif apres l affichage de `passed`. J ai verifie les `TestClient`, les imports, les services et la fermeture de l engine SQLAlchemy sans trouver de thread applicatif restant actif. Si le comportement persiste, il s agit probablement d une particularite de l environnement Pytest/Windows et non d un blocage du backend.

## Structure

- `app/db`: engine, sessions, initialisation et seed SQLite
- `app/models`: ORM SQLAlchemy
- `app/repositories`: acces donnees
- `app/services`: scoring, alertes, dashboard et transaction store
- `app/data`: donnees de demo JSON
- `app/api/v1`: routes REST
- `tests`: tests pytest

## Limites restantes

- pas de PostgreSQL
- pas d Alembic
- pas de worker
- pas de modele ML reel
- pas de persistence distribuee

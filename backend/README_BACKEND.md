# Novaris AI Backend

Backend FastAPI du Sprint 1 pour Novaris AI, solution anti-fraude Mobile Money.

Le but de cette première version est de fournir une base propre, modulaire et testable pour :

- exposer un endpoint de santé
- analyser une transaction de façon déterministe
- calculer un score de risque
- produire un Novaris Trust Score
- retourner une décision lisible
- fournir une explication métier simple

## Installation

Depuis le dossier `backend/` :

```bash
pip install -r requirements.txt
```

## Lancement local

```bash
uvicorn app.main:app --reload
```

Swagger sera disponible sur :

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### GET `/api/v1/health`

Réponse :

```json
{
  "status": "ok",
  "service": "Novaris AI Backend",
  "version": "0.1.0"
}
```

### POST `/api/v1/transactions/analyze`

Analyse une transaction Mobile Money et retourne :

- `risk_score`
- `trust_score`
- `risk_level`
- `decision`
- `module_scores`
- `reasons`
- `investigation_summary`

## Exemple de requête

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

## Structure

- `app/core`: configuration, constantes, exceptions
- `app/api/v1`: routes REST
- `app/schemas`: schémas Pydantic
- `app/services`: moteur de scoring et orchestration
- `app/utils`: utilitaires
- `tests`: tests pytest

## Limites du Sprint 1

- pas de base de données
- pas de modèle ML réel
- pas de worker d’arrière-plan
- pas de scoring adaptatif en production
- pas d’historique transactionnel persistant


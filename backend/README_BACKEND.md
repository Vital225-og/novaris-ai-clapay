# Novaris AI Backend

Backend FastAPI du Sprint 2 pour Novaris AI, solution anti-fraude Mobile Money.

Le backend expose un socle modulaire avec 4 services de scoring independants :

- `TransactionMonitoringService`
- `DeviceSimIntelligenceService`
- `AgentFraudDetectionService`
- `FraudGraphService`

Le `RiskOrchestrator` coordonne ensuite ces modules pour produire :

- un `risk_score`
- un `trust_score`
- un `risk_level`
- une `decision`
- une liste de `reasons`
- un `investigation_summary`

## Installation

Depuis le dossier `backend/` :

```bash
pip install -r requirements.txt
```

## Lancement local

```bash
uvicorn app.main:app --reload
```

Swagger :

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

Analyse une transaction Mobile Money et retourne la réponse enrichie du moteur de risque.

## Modules de scoring

### 1. Transaction Monitoring

Analyse :

- `amount`
- `hour`
- `transactions_last_10min`
- `transaction_type`

Règles :

- `amount >= 300000`: `+35`
- `amount >= 100000`: `+20`
- `transactions_last_10min >= 8`: `+30`
- `transactions_last_10min >= 5`: `+20`
- `hour` entre `0` et `5`: `+15`
- `transaction_type = withdrawal`: `+10`

### 2. Device/SIM Intelligence

Analyse :

- `is_new_device`
- `sim_changed_recently`
- `device_id`
- `location`

Règles :

- `is_new_device = true`: `+35`
- `sim_changed_recently = true`: `+40`
- `location` vide ou inconnue: `+10`

### 3. Agent Fraud Detection

Analyse :

- `agent_id`
- `agent_risk_level`

Règles :

- `agent_risk_level = high`: `+75`
- `agent_risk_level = medium`: `+45`
- `agent_risk_level = low`: `+15`
- `agent_id` vide: `+10`

### 4. Fraud Graph Intelligence

Analyse simulée :

- `sender_phone`
- `receiver_phone`
- `agent_id`
- `device_id`
- `agent_risk_level`

Règles :

- `device_id` contenant `NEW` ou `RISK`: `+35`
- `receiver_phone` présent: `+10`
- `agent_id` présent et `agent_risk_level = high`: `+40`

## Formule d agrégation

Le score final est calculé avec une moyenne ponderee :

```text
risk_score =
35% transaction_monitoring
+ 25% device_sim
+ 20% agent_fraud
+ 20% fraud_graph
```

Le résultat est arrondi a l entier.

## Decision Engine

- `0` a `29`: `ALLOW` / `Faible`
- `30` a `59`: `MONITOR` / `Modere`
- `60` a `79`: `REVIEW` / `Eleve`
- `80` a `100`: `TEMPORARY_BLOCK` / `Critique`

## Trust Score

```text
trust_score = 1000 - (risk_score * 10)
```

## Exemple de réponse

```json
{
  "transaction_id": "TX-ABC123DEF456",
  "customer_name": "Client Demo",
  "amount": 450000,
  "transaction_type": "withdrawal",
  "agent_id": "AG-044",
  "device_id": "DEV-NEW-991",
  "location": "Abidjan",
  "risk_score": 82,
  "trust_score": 180,
  "risk_level": "Critique",
  "decision": "TEMPORARY_BLOCK",
  "module_scores": {
    "transaction_monitoring": 90,
    "device_sim": 75,
    "agent_fraud": 75,
    "fraud_graph": 85
  },
  "reasons": [
    "Montant tres superieur au comportement habituel",
    "Fréquence élevée sur une courte période"
  ],
  "investigation_summary": "Cette transaction présente un risque critique. Un blocage temporaire est recommandé avant validation humaine."
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

## Structure

- `app/core`: configuration, constantes, exceptions
- `app/api/v1`: routes REST
- `app/schemas`: schemas Pydantic
- `app/services`: moteurs de scoring et orchestration
- `app/utils`: utilitaires
- `tests`: tests pytest

## Limites du Sprint 2

- pas de base de donnees
- pas de modele ML reel
- pas de worker d arriere-plan
- pas de persistence transactionnelle
- pas de modele de graphe real temps


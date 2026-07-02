# Novaris AI Backend

Backend FastAPI du Sprint 3 pour Novaris AI, solution anti-fraude Mobile Money.

Le backend expose désormais :

- l analyse de transaction
- un stockage mémoire des transactions de démonstration et des analyses courantes
- un dashboard KPI
- un système d alertes fraude

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

## Comportement du stockage

Le Sprint 3 utilise un stockage mémoire simple alimenté par :

- `backend/app/data/demo_transactions.json`
- `backend/app/data/demo_alerts.json`

Les transactions analysées pendant l exécution sont ajoutées au store mémoire.

## Création automatique d alerte

Lorsqu une transaction est analysée :

- elle est ajoutée au `transaction_store`
- si `risk_score >= 60`, une alerte est créée automatiquement
- si `risk_score >= 80`, l alerte est critique et le statut initial est `OPEN`
- si `60 <= risk_score <= 79`, l alerte est de niveau élevé et le statut initial est `IN_REVIEW`
- si `risk_score < 60`, aucune alerte n est créée

Statuts d alerte :

- `OPEN`
- `IN_REVIEW`
- `RESOLVED`

Niveaux d alerte :

- `Modéré`
- `Élevé`
- `Critique`

## Dashboard KPI

Le dashboard agrège les données en mémoire pour retourner :

- `total_transactions`
- `total_alerts`
- `critical_alerts`
- `review_alerts`
- `allowed_transactions`
- `blocked_transactions`
- `protected_amount`
- `average_risk_score`

### Exemple de réponse

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

## Exemple de réponse transaction

```json
{
  "transaction_id": "TX-001",
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
    "Montant très supérieur au comportement habituel",
    "Fréquence élevée sur une courte période"
  ],
  "investigation_summary": "Cette transaction présente un risque critique. Un blocage temporaire est recommandé avant validation humaine."
}
```

## Exemple de réponse alerte

```json
{
  "alert_id": "ALT-001",
  "transaction_id": "TX-001",
  "risk_score": 92,
  "risk_level": "Critique",
  "decision": "TEMPORARY_BLOCK",
  "status": "OPEN",
  "created_at": "2026-07-02T10:00:00",
  "main_reason": "Montant inhabituel + nouvel appareil"
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

## Notes sur `pytest` sous Windows

Les tests affichent correctement leur succès, mais dans cet environnement Windows le runner peut rester actif après l exécution. Les causes les plus probables ont été limitées en utilisant des `TestClient` fermés explicitement dans les tests. Si le phénomène persiste dans un autre poste, il s agit probablement d une particularité d environnement et non d un blocage applicatif du backend.

## Structure

- `app/core`: configuration, constantes, exceptions
- `app/api/v1`: routes REST
- `app/schemas`: schémas Pydantic
- `app/services`: scoring, alertes, dashboard et stockage mémoire
- `app/data`: jeux de démonstration JSON
- `app/utils`: utilitaires
- `tests`: tests pytest

## Limites du Sprint 3

- pas de base de données
- pas de modèle ML réel
- pas de worker
- pas de persistance durable
- pas d historique au-delà du stockage mémoire


# API Design – Polling System

## 1. Overview

This document describes the **API design principles, data contracts, and validation strategy** used in the Polling System.

The goal of this design is to ensure:

* Long-term maintainability
* Strong validation at the API boundary
* Clear separation of concerns
* Forward compatibility as features evolve

This document focuses on **why** the API looks the way it does, not just what it does.

---

## 2. Design Goals

The API was designed with the following principles:

1. **Explicit over implicit** – Data meaning should never depend on array position or hidden assumptions.
2. **Validation at the boundary** – Invalid requests should be rejected before reaching business logic.
3. **Evolvability** – New fields and behaviors should be addable without breaking clients.
4. **Deterministic ordering** – Ordering must be treated as data, not an implementation detail.
5. **Layered responsibility** – Schemas validate shape, services enforce business rules, models persist state.

---

## 3. High-Level Architecture

```
Client
  ↓
FastAPI Route
  ↓
Pydantic Schemas (validation + defaults)
  ↓
Service Layer (business rules)
  ↓
Repository Layer (DB interaction)
  ↓
SQLAlchemy Models
  ↓
Database
```

Key rule:

> **If data reaches the service layer, it is already valid.**

---

## 4. Poll Creation Contract

### 4.1 Request Shape

The poll creation API accepts a **fully explicit nested structure**.

```json
{
  "title": "Best Backend Language",
  "type": "POLL",
  "description": "Vote wisely",
  "ends_at": null,
  "questions": [
    {
      "question_text": "Which language do you prefer?",
      "question_type": "SINGLE_CHOICE",
      "order_index": 0,
      "options": [
        { "option_text": "Python", "order_index": 0 },
        { "option_text": "Java", "order_index": 1 },
        { "option_text": "Go", "order_index": 2 }
      ]
    }
  ]
}
```

---

## 5. Why This Contract Was Chosen

### 5.1 Explicit Ordering

Earlier designs relied on array position for ordering:

```json
"options": ["Python", "Java", "Go"]
```

This approach was rejected because:

* Array order can be lost or altered across clients
* Partial updates become unsafe
* Reordering requires full replacement
* Meaning becomes implicit and fragile

Instead, ordering is modeled explicitly:

```json
{ "option_text": "Python", "order_index": 0 }
```

This ensures:

* Deterministic rendering
* Stable persistence
* Safe reordering

---

### 5.2 Structured Objects Over Primitive Lists

Using objects instead of strings enables:

* Strong validation (non-empty text, unique order)
* Future extensibility (images, metadata, weights)
* Clear API documentation
* Easier onboarding for new engineers

This design avoids breaking changes when the system evolves.

---

### 5.3 Validation at the API Boundary

The API enforces correctness using Pydantic schemas:

* Enum validation for poll and question types
* Minimum counts (at least 1 question, 2 options)
* Ordering constraints
* Duplicate option prevention

Invalid requests are rejected **before** any business logic or database interaction.

---

## 6. Default Behavior and Derived Fields

### 6.1 `ends_at` Default

* `ends_at` is optional in the request
* If omitted or set to `null`, it defaults to:

```
current_time + 7 days (UTC)
```

This behavior is implemented in the schema layer to:

* Keep services simple
* Make behavior explicit in API docs
* Ensure consistent defaults

---

## 7. OpenAPI Examples

### 7.1 Create Poll – Example Request

```json
{
  "title": "Team Lunch Preference",
  "type": "SURVEY",
  "description": "Help us decide",
  "questions": [
    {
      "question_text": "Preferred cuisine?",
      "question_type": "MULTI_CHOICE",
      "order_index": 0,
      "options": [
        { "option_text": "Indian", "order_index": 0 },
        { "option_text": "Italian", "order_index": 1 },
        { "option_text": "Mexican", "order_index": 2 }
      ]
    }
  ]
}
```

---

### 7.2 Successful Response

```json
{
  "poll_id": "c8b9f4a2-9d3b-4b7e-9a8f-3c2e4c5a1f9d",
  "status": "DRAFT",
  "created_at": "2026-02-09T12:30:00Z",
  "ends_at": "2026-02-16T12:30:00Z"
}
```

---

### 7.3 Validation Error Example

```json
{
  "detail": [
    {
      "loc": ["body", "questions", 0, "options"],
      "msg": "At least 2 options are required",
      "type": "value_error"
    }
  ]
}
```

---

## 8. Responsibilities by Layer

| Layer            | Responsibility                           |
| ---------------- | ---------------------------------------- |
| Pydantic Schemas | Shape, types, defaults, basic validation |
| Service Layer    | Business rules, orchestration            |
| Repository       | Persistence and transactions             |
| Models           | Database schema                          |

This separation ensures each layer remains simple and testable.

---

## 9. Anti-Patterns Avoided

* Relying on array position for meaning
* Performing validation in services
* Encoding business rules in database defaults
* Overloading ORM models with API logic

---

## 10. Summary

This API contract is designed to:

* Prevent entire classes of bugs
* Scale with feature growth
* Be clear, explicit, and review-friendly

The structure may appear verbose initially, but it significantly reduces long-term complexity and risk.

---

**Design philosophy:**

> *Make illegal states unrepresent

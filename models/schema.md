# Database Schema (Polls & Surveys)

This document describes the core database schema for polls, surveys, and voting.

```mermaid
erDiagram

    POLL {
        UUID poll_id PK
        STRING title
        STRING type "POLL | SURVEY"
        STRING status "DRAFT | ACTIVE | CLOSED"
        TIMESTAMP created_at
        TIMESTAMP ends_at
    }

    QUESTION {
        UUID question_id PK
        UUID poll_id FK
        STRING question_text
        STRING question_type "SINGLE_CHOICE | MULTI_CHOICE"
        INT order_index
    }

    OPTION {
        UUID option_id PK
        UUID question_id FK
        STRING option_text
        INT vote_count
    }

    VOTE {
        UUID vote_id PK
        UUID option_id FK
        UUID user_id
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    POLL ||--o{ QUESTION : contains
    QUESTION ||--o{ OPTION : has
    OPTION ||--o{ VOTE : chosen_in

---

# Tables

## POLL

| Column | Type | Constraints |
|--------|------|-------------|
| poll_id | UUID | PK |
| title | STRING | NOT NULL |
| type | ENUM | NOT NULL, ('POLL', 'SURVEY') |
| status | ENUM | NOT NULL, ('DRAFT', 'ACTIVE', 'CLOSED') |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |
| ends_at | TIMESTAMP | NULL |

## QUESTION

| Column | Type | Constraints |
|--------|------|-------------|
| question_id | UUID | PK |
| poll_id | UUID | FK → POLL |
| question_text | STRING | NOT NULL |
| question_type | ENUM | NOT NULL, ('SINGLE_CHOICE', 'MULTI_CHOICE') |
| order_index | INT | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

## OPTION

| Column | Type | Constraints |
|--------|------|-------------|
| option_id | UUID | PK |
| question_id | UUID | FK → QUESTION |
| option_text | STRING | NOT NULL |
| order_index | INT | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

## VOTE

| Column | Type | Constraints |
|--------|------|-------------|
| vote_id | UUID | PK |
| option_id | UUID | FK → OPTION |
| user_id | UUID | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

---

# Relationships

- POLL 1--N QUESTION
- QUESTION 1--N OPTION
- OPTION 1--N VOTE
```

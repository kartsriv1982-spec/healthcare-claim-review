# 🏥 Intelligent Healthcare Claim Review System using Agentic AI

## Overview

The **Intelligent Healthcare Claim Review System** is an AI-powered healthcare claims processing platform that automates the end-to-end claim review lifecycle using **Agentic AI**, **Retrieval-Augmented Generation (RAG)**, **LangGraph**, and **Human-in-the-Loop (HITL)** workflows.

The solution leverages multiple AI agents working collaboratively to validate healthcare claims, analyze insurance policy coverage, generate explainable recommendations, and route low-confidence or business-critical decisions for human review.

Designed using a microservices-based architecture, the platform integrates OCR, Large Language Models (LLMs), Retrieval-Augmented Generation, AWS cloud services, and enterprise-grade workflow orchestration to simulate a real-world insurance claim adjudication system.

---
## Team & Contributions

This capstone project was successfully completed through the collaborative efforts of our team. Each member contributed to specific functional and technical areas of the solution.

<img width="752" height="718" alt="image" src="https://github.com/user-attachments/assets/c9396abc-9aa1-42a6-a64a-942377a5fdd3" />

---

# Business Problem

Healthcare insurance claim processing is often:

* Manual and time-consuming
* Error-prone
* Expensive to operate
* Difficult to audit
* Challenging to scale

Traditional claim review requires human experts to:

* Verify claim documents
* Validate mandatory information
* Interpret insurance policies
* Detect exclusions
* Make approval decisions
* Maintain regulatory audit trails

This project demonstrates how **Generative AI** and **Agentic AI** can significantly reduce manual effort while keeping humans in control of critical decisions.

---

# Solution Highlights

* Multi-Agent AI Workflow using LangGraph
* Retrieval-Augmented Generation (RAG) for policy reasoning
* Human-in-the-Loop approval workflow
* Explainable AI recommendations
* OCR-based document extraction
* Enterprise audit logging
* Microservices architecture
* AWS cloud integration
* Docker-based deployment
* PostgreSQL persistence

---

# System Architecture

```
                Claim PDF
                     │
                     ▼
              AWS Textract OCR
                     │
                     ▼
             Validation Agent
                     │
          Valid? ────┴──── No
             │             │
            Yes            ▼
             │      Validation Failed
             ▼
          Policy Agent (RAG)
             │
             ▼
        Decision Agent
             │
             ▼
   Human-in-the-Loop Review
             │
             ▼
      Final Claim Decision
             │
             ▼
      PostgreSQL + Audit Trail
```

---

# AI Workflow

## Validation Agent

Responsible for:

* OCR validation
* Mandatory field verification
* Data completeness checks
* Early workflow termination for invalid claims

---

## Policy Agent (RAG)

Uses Retrieval-Augmented Generation to:

* Retrieve policy clauses
* Analyze policy coverage
* Identify exclusions
* Determine medical necessity
* Produce explainable reasoning
* Generate confidence scores

---

## Decision Agent

Consolidates outputs from previous agents to determine:

* APPROVE
* REJECT
* REQUEST_INFO

along with business justification.

---

## Human-in-the-Loop (HITL)

Claims requiring manual intervention are routed to reviewers who can:

* Accept AI recommendation
* Override AI decision
* Add review comments
* Maintain complete audit history

---

# Key Features

* AI-assisted claim adjudication
* Policy-aware recommendations
* Explainable AI reasoning
* Human review workflow
* Complete audit trail
* OCR integration
* REST APIs
* Modern Streamlit dashboard
* Modular microservices
* Cloud-ready architecture

---

# Technology Stack

## Backend

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL

## Frontend

* Streamlit

## AI & GenAI

* OpenAI GPT
* LangGraph
* LangChain
* ChromaDB
* Retrieval-Augmented Generation (RAG)

## Cloud Services

* AWS Textract
* AWS S3
* EC2
* CloudFormation
* IAM
* VPC

## DevOps

* Docker
* Docker Compose
* GitHub

---

# Project Structure

```
healthcare-claim-review/

├── app/
├── frontend/
├── authservice/
├── deployment/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

---

# Human Review Workflow

1. Upload healthcare claim.
2. Extract claim data using OCR.
3. Validate mandatory fields.
4. Retrieve insurance policy context.
5. Generate AI recommendation.
6. Route uncertain claims to human reviewer.
7. Persist final decision.
8. Maintain immutable audit trail.

---

# Enterprise Design Principles

* Agent-based architecture
* Separation of concerns
* Explainable AI
* Human governance
* Microservices
* Event-driven workflow orchestration
* Configuration-driven deployment
* Cloud-native design

---


# Learning Outcomes

This project demonstrates practical implementation of:

* Agentic AI
* Retrieval-Augmented Generation
* LangGraph orchestration
* Human-in-the-Loop systems
* Enterprise AI architecture
* FastAPI microservices
* Docker deployment
* AWS cloud integration
* Explainable AI
* Production-grade software engineering


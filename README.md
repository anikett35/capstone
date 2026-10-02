# Customer Account Microservice - DevOps Capstone Project

[![CI Build](https://github.com/anikett35/capstone/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/anikett35/capstone/actions/workflows/ci-build.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)

This repository contains the completed project for the [**IBM-CD0285EN-SkillsNetwork DevOps Capstone Project**](https://www.coursera.org/learn/devops-capstone-project?specialization=devops-and-software-engineering), part of the [**IBM DevOps and Software Engineering Professional Certificate**](https://www.coursera.org/professional-certificates/devops-and-software-engineering).

## Project Overview

The Customer Account microservice provides a complete, production-ready RESTful service for managing customer accounts in an e-commerce platform. It demonstrates modern DevOps practices including:

- **Agile Development:** Sprint planning and Kanban management using User Stories, Story Points, and Backlogs.
- **Test-Driven Development (TDD):** Full unit test suite with 95%+ code coverage using `nose` and `coverage`.
- **Code Quality:** Automated linting with `flake8` and `pylint`.
- **Continuous Integration (CI):** Automated pipelines via GitHub Actions running tests and linters on each push and pull request.
- **Application Security:** Hardened with `Flask-Talisman` for secure HTTP headers and `Flask-CORS` for cross-origin access control.
- **Containerization:** Production Docker image built with a non-root user and minimal footprint.
- **Continuous Delivery (CD):** Kubernetes deployment manifests and automated Tekton delivery pipeline.

---

## Data Model

The Account model stores the following attributes:

| Field Name | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the account |
| `name` | String(64) | Not Null | Customer's full name |
| `email` | String(64) | Not Null | Customer's email address |
| `address` | String(256) | Not Null | Customer's physical mailing address |
| `phone_number` | String(32) | Nullable | Optional phone contact number |
| `date_joined` | Date | Not Null | Date the customer registered |

---

## RESTful API Endpoints

| HTTP Method | URL Path | Status Code | Description |
|:---|:---|:---|:---|
| `GET` | `/` | `200 OK` | Service metadata and root endpoints |
| `GET` | `/health` | `200 OK` | Health check endpoint |
| `POST` | `/accounts` | `201 CREATED` | Create a new customer account |
| `GET` | `/accounts` | `200 OK` | List all customer accounts |
| `GET` | `/accounts/<id>` | `200 OK` | Retrieve details of a single account |
| `PUT` | `/accounts/<id>` | `200 OK` | Update an existing customer account |
| `DELETE` | `/accounts/<id>` | `204 NO CONTENT` | Remove an existing customer account |

---

## Running Locally

### 1. Initialize Development Environment
```bash
source bin/setup.sh
```

### 2. Start PostgreSQL Database
```bash
make db
```

### 3. Run the Microservice
```bash
honcho start
```
The service will be accessible at `http://localhost:8080`.

### 4. Run Automated Tests and Linting
```bash
# Run unit tests with coverage
make tests

# Run code linter
make lint
```

---

## Docker & Kubernetes Deployment

### Build and Run Docker Container
```bash
docker build -t accounts:1.0 .
docker run -d -p 8080:8080 --name accounts accounts:1.0
```

### Deploy to Kubernetes
```bash
kubectl apply -f deploy/deployment.yaml
kubectl apply -f deploy/service.yaml
```

---

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

### © IBM Corporation & Contributors. All rights reserved.

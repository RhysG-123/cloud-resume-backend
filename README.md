# Cloud Resume Challenge – Backend

## Overview

This is the backend API for my [Cloud Resume Challenge](https://cloudresumechallenge.dev), designed to demonstrate real-world cloud engineering and serverless development using Microsoft Azure.

It provides a serverless endpoint that tracks and updates resume page visits using an Azure Function and Cosmos DB.

🔗 **Frontend:** [rhysgoonan.com](https://www.rhysgoonan.com)

---

## Features

- Serverless Azure Function (Node.js)
- Visitor count stored in Azure Cosmos DB (Table API)
- Connected to static frontend via HTTP endpoint
- Secured and compliant with enterprise policy (tag enforcement and region restriction)
- Automated CI/CD with GitHub Actions using Azure Service Principal authentication

---

## Technologies Used

- Azure Functions (Node.js runtime)
- Azure Cosmos DB (Table API)
- Azure Storage Account (for function runtime)
- Azure App Service (Function App)
- GitHub Actions (CI/CD pipeline)
- Azure RBAC and Policy enforcement
- JavaScript (function logic)

---

## API Endpoint

The live backend function is publicly accessible at:

https://crc-function-app.azurewebsites.net/api/VisitorCounter

This endpoint is called by the frontend on each visit to increment and return the current visitor count.

---

## Project Structure

cloud-resume-backend/
  .github/
    workflows/
      deploy.yml – GitHub Actions workflow for deployment
  crc-visitor-func/ – Azure Function app folder (Node.js)
    src/
      functions/
        VisitorCounter.js
    index.js – Function entry point
    host.json – Function host config
    package.json – Node.js dependencies
    .funcignore – Files excluded from deployment

---

## Deployment & CI/CD

The backend is deployed automatically using **GitHub Actions** on pushes to the `main` branch.

Authentication is handled using a **Service Principal** stored in GitHub Secrets (`AZURE_CREDENTIALS`), with the following configuration:

- ✅ Azure login via `azure/login@v1`
- ✅ Deployment via `Azure/functions-action@v1`
- ✅ Locked to `Australia East` region
- ✅ Resources tagged with `department=Development` (enforced by policy)

---

## Skills Demonstrated

- Serverless API development with Azure Functions
- NoSQL integration with Cosmos DB Table API
- RBAC-secured CI/CD deployment pipeline
- Policy-aware resource management in Azure
- GitHub Actions for automated delivery
- JavaScript development for backend logic

---

## Licence

This project is licensed under the [MIT Licence](LICENSE).

# ADAPTIVE AI LOGISTICS OPERATIONS INTELLIGENCE PLATFORM

**SE331 Capstone Project**

An adaptive AI-powered platform designed to improve logistics, inventory management, and procurement operations through intelligent data analysis, machine learning, and decision-support capabilities.

## ACE Procurement Intelligence Module

ACE Procurement Intelligence is a procurement decision-support module within the ADAPTIVE AI LOGISTICS OPERATIONS INTELLIGENCE PLATFORM.

It is designed to help various types of organizations make smarter purchasing decisions through inventory management, demand forecasting, and procurement recommendations.

## 1. Project Overview

Organizations across different industries regularly purchase resources, equipment, supplies, and other essential items to maintain their daily operations.

Traditional procurement decisions often rely on manual calculations and assumptions, which can lead to overstocking, shortages, unnecessary expenses, and inefficient resource management.

The ACE Procurement Intelligence module aims to address these challenges by combining inventory management with machine learning-based demand forecasting and procurement recommendations.

The system helps organizations determine:
- What items need to be purchased.
- How much quantity should be purchased.
- When an item should be reordered.
- Which supplier offers the most suitable price.

## 2. Key Features

### Authentication and User Management
- Organization registration.
- Secure user login and logout.
- Role-based access control.
- Separate permissions for administrators, managers, and store officers.
- Organization-level data isolation.

### Inventory and Data Management
- Add and manage inventory items.
- Register and manage suppliers.
- Record purchases and consumption.
- Track available stock quantities.
- Edit inventory records.
- Prevent consumption beyond available stock.

### Demand Forecasting
- Predict future demand using historical consumption data.
- Compare forecasting models using historical prediction errors.
- Display forecast results with an estimated error range.
- Provide a fallback approach when historical data is insufficient.

### Procurement Recommendations
- Identify potential stock shortages and overstocking.
- Recommend purchase quantities.
- Suggest suitable purchasing times.
- Compare supplier prices.
- Provide explanations behind procurement recommendations.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Frontend Development Server | Vite |
| Backend | Python, Django |
| API Framework | Django REST Framework |
| Machine Learning | Scikit-learn |
| Numerical Processing | NumPy |
| Database | SQLite |
| Version Control | Git and GitHub |

## 4. Project Structure

```text
ADAPTIVE-AI-LOGISTICS-OPERATIONS-INTELLIGENCE-PLATFORM/
│
├── ace-procurement/
│   ├── backend/
│   │   ├── accounts/
│   │   ├── inventory/
│   │   ├── intelligence/
│   │   │   └── ml/
│   │   ├── config/
│   │   ├── manage.py
│   │   └── requirements.txt
│   │
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── pages/
│   │   │   ├── App.jsx
│   │   │   ├── api.js
│   │   │   ├── icons.jsx
│   │   │   └── styles.css
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   ├── .gitignore
│   └── README.md
│
├── app/
├── tests/
├── Reports/
└── README.md
```

## 5. Current Implementation Scope

The ACE Procurement Intelligence module currently focuses on:

- Organization registration and authentication.
- Role-based user management.
- Inventory and transaction management.
- Machine learning-based demand forecasting.
- Procurement decision recommendations.
- Supplier price comparison.

Additional features and system improvements will be developed as the project progresses.

## 6. Team Information

**Overall Project:** ADAPTIVE AI LOGISTICS OPERATIONS INTELLIGENCE PLATFORM

**Module:** ACE Procurement Intelligence

**Course:** SE331 — Capstone Project

**Team:** ACE

**Team Members:**

1. **Md Asif Raihan** — Team Lead
2. **Md Abu Musha Rony** — Team Member
3. **Md Mostahid Islam Riad** — Team Member

**Department:** Software Engineering

**Institution:** Daffodil International University

## 7. Future Improvements

Potential future developments include:

- CSV-based inventory data import.
- Recording procurement decisions and actual purchasing outcomes.
- Organizational memory for improving future recommendations.
- More advanced demand forecasting models.
- Supplier performance evaluation.
- Enhanced reporting and analytics.
- Natural-language AI assistant for procurement-related queries.

---

*Smarter Logistics. Intelligent Procurement. Data-Driven Decisions.*

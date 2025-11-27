# Organ-C-Codefest-Hackathon

# 🚀 Enterprise Predictive Analytics Platform
Real-Time IoT Ingestion • AI/ML Forecasting • Anomaly Detection • Risk Scoring • Smart Alerts

A complete AI-powered enterprise analytics solution built with FastAPI, Python, Machine Learning, and a PostgreSQL database—designed to help retail businesses make smarter, real-time decisions.

## 📌 Overview

This project delivers an end-to-end predictive analytics system that processes enterprise operational data in real-time, detects anomalies, forecasts sales, and generates actionable business insights.

The platform integrates:

⚡ Real-Time IoT Data Ingestion

🤖 Machine Learning Models (Prophet, Isolation Forest, Clustering)

🧠 Automated Risk Assessment

🚨 Smart Alerts & Recommendations

📊 KPI Dashboard & Forecast Visualization

🗄️ Cloud Database (PostgreSQL)

🔌 FastAPI REST Endpoints

## 🧱 Project Architecture
                        ┌──────────────────────┐
                        │     Frontend UI      │
                        │  (Dashboard / Login) │
                        └──────────┬───────────┘
                                   │
                                   ▼
                      ┌──────────────────────────┐
                      │     FastAPI Backend      │
                      │  • IoT Ingestion API     │
                      │  • Forecast Engine       │
                      │  • Anomaly Detection     │
                      │  • Risk Scoring          │
                      │  • Alerts System         │
                      └──────────┬──────────────┘
                                   │
                                   ▼
                   ┌──────────────────────────────┐
                   │      Machine Learning         │
                   │  • Prophet Forecasting        │
                   │  • Isolation Forest Detection │
                   │  • Clustering (KMeans)        │
                   └──────────┬───────────────────┘
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │     PostgreSQL Database    │
                    │  • anomaly_logs            │
                    │  • cluster_logs            │
                    │  • risk_logs               │
                    │  • alerts                  │
                    └────────────────────────────┘

## ✨ Key Features
🔌 1. IoT Ingestion API

Receives real-time enterprise data from a Python IoT simulator or actual devices.

📈 2. Forecasting (Prophet)

Generates future sales trends.

🔍 3. Anomaly Detection

Using Isolation Forest to detect unusual patterns.

🧩 4. Clustering

Groups stores/departments with similar behavior.

⚠️ 5. Risk Scoring & Alerts

Automatically creates alerts for high-risk events.

🗄️ 6. PostgreSQL Persistence

Stores logs for:

-anomaly_logs

-cluster_logs

-risk_logs

-alerts

## 🛠️ Tech Stack
Backend

-Python

-FastAPI

-SQLAlchemy ORM

-PostgreSQL (Render Cloud)

-Prophet (Forecasting)

-Scikit-Learn (Anomaly + Clustering)

Frontend 

-TailwindCSS

-Vite

-React 

-TypeScript

-JavaScript

Infrastructure

-Railway Web Service

-Render PostgreSQL Instance

-Python IoT Simulator 

## 📡 API Endpoints
IoT Ingestion
```
POST /api/v1/iot/
```


Sends IoT data → anomaly detection → clustering → risk scoring → database logging.

Forecasting
```
POST /api/v1/forecast/
```

Anomaly Detection
```
POST /api/v1/anomaly/
```
Risk Assessment
```
POST /api/v1/risk/
```
Alerts
```
GET /api/v1/alerts/
```

Stores
```
GET /api/v1/stores/
```
## ⚙️ Installation & Setup
1️⃣ Clone the repository
```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

2️⃣ Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3️⃣ Install dependencies
```
pip install -r requirements.txt
```

4️⃣ Set your environment variable
```
DATABASE_URL=<your_postgres_url>
```

5️⃣ Run the FastAPI backend
```
uvicorn main:app --reload
```

6️⃣ Open API docs
```
http://127.0.0.1:8000/docs
```

## 🔄 IoT Simulator

The project includes a Python script that sends random data to the API every 10 minutes.

Run it with:
```
python iot_simulator.py
```


This simulates:

-store activity

-dept behavior

-weekly sales

-temperature

-CPI / fuel price

-unemployment

## 🧪 Model Accuracy Evaluation

The system evaluates:

📈 Forecasting Accuracy

-MAE

-RMSE

-MAPE

-Coverage

🔍 Anomaly Detection Confidence

-Detection rate

-Score variance

-Model confidence

🎯 Overall Performance Score

Combines:
```
70% Forecast Accuracy
30% Anomaly Confidence
```

## 📌 Future Improvements

Real IoT hardware support

More ML models

Automated email/SMS alerts

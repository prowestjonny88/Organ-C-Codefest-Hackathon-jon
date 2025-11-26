from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ROUTES
from routes.iot import router as iot_router
from routes.forecast import router as forecast_router
from routes.anomaly import router as anomaly_router
from routes.kpi import router as kpi_router
from routes.risk import router as risk_router
from routes.alerts import router as alerts_router
from routes.cluster import router as cluster_router
from routes.stores import router as stores_router
from routes.recommendations import router as recommendations_router
from routes.websocket import router as websocket_router  # WebSocket routes
from routes.schemas import HealthResponse

# DATABASE
from database import Base, engine

# IMPORTANT: import models BEFORE create_all()
from models import Alert, AnomalyLog, ClusterLog, RiskLog


API_V1_PREFIX = "/api/v1"

app = FastAPI(
    title="Enterprise Predictive Analytics API",
    version="1.0.0",
    description="""
    ## Track 1: Intelligent Predictive Analytics for Enterprise Operations
    
    This API provides AI-powered analytics for retail operations including:

    * 📈 Forecasting
    * 🔍 Anomaly Detection
    * 📊 KPI Dashboard
    * ⚠️ Risk Assessment
    * 🚨 Alerts
    * 💡 Recommendations
    * 🏪 Store Analytics
    """
)


# ============================================
# MIDDLEWARE (must be before routes)
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# STARTUP EVENT → Create tables on Render
# ============================================
@app.on_event("startup")
def startup():
    print("🚀 Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)


# ============================================
# HEALTH CHECK
# ============================================
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return {"status": "ok"}


# ============================================
# WEBSOCKET ROUTES (no version prefix)
# ============================================
app.include_router(websocket_router, prefix="/ws", tags=["🔌 WebSocket"])

# ============================================
# API v1 ROUTES
# ============================================
app.include_router(iot_router, prefix=f"{API_V1_PREFIX}/iot", tags=["IoT Ingestion"])
app.include_router(stores_router, prefix=f"{API_V1_PREFIX}/stores", tags=["Stores"])
app.include_router(recommendations_router, prefix=f"{API_V1_PREFIX}/recommendations", tags=["Recommendations"])
app.include_router(forecast_router, prefix=f"{API_V1_PREFIX}/forecast", tags=["Forecast"])
app.include_router(kpi_router, prefix=f"{API_V1_PREFIX}/kpi", tags=["KPI Overview"])
app.include_router(anomaly_router, prefix=f"{API_V1_PREFIX}/anomaly", tags=["Anomaly Detection"])
app.include_router(risk_router, prefix=f"{API_V1_PREFIX}/risk", tags=["Risk Assessment"])
app.include_router(alerts_router, prefix=f"{API_V1_PREFIX}/alerts", tags=["Alerts"])
app.include_router(cluster_router, prefix=f"{API_V1_PREFIX}/cluster", tags=["Clustering"])

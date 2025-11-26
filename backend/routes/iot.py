from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import Alert, AnomalyLog, ClusterLog, RiskLog
from ml.model import SalesModel
import pandas as pd

router = APIRouter()
model = SalesModel()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class IoTInput(BaseModel):
    timestamp: str
    store: int
    dept: int
    Weekly_Sales: float
    Temperature: float
    Fuel_Price: float
    CPI: float
    Unemployment: float
    IsHoliday: int


@router.post("/")
def iot_ingest(data: IoTInput, db: Session = Depends(get_db)):

    # Convert IoT input to dataframe
    df = pd.DataFrame([data.dict()])

    # 🔥 CRITICAL FIX — rename to match model training columns
    df = df.rename(columns={
        "store": "Store",
        "dept": "Dept",
        "IsHoliday": "IsHoliday",
        "Weekly_Sales": "Weekly_Sales",
        "Temperature": "Temperature",
        "Fuel_Price": "Fuel_Price",
        "CPI": "CPI",
        "Unemployment": "Unemployment"
    })

    # Make sure types match training schema
    df["Store"] = df["Store"].astype(int)
    df["Dept"] = df["Dept"].astype(int)
    df["IsHoliday"] = df["IsHoliday"].astype(int)

    # 1) anomaly detection
    anomaly = model.detect_anomalies(df).iloc[0]
    anomaly_flag = int(anomaly["anomaly"])
    anomaly_score = float(anomaly["anomaly_score"])

    db.add(AnomalyLog(
        timestamp=data.timestamp,
        value=data.Weekly_Sales,
        score=anomaly_score,
        is_anomaly=(anomaly_flag == -1)
    ))

    # 2) clustering
    cluster_id = model.cluster(df)

    db.add(ClusterLog(
        store=data.store,
        dept=data.dept,
        cluster=cluster_id,
        features=data.dict()
    ))

    # 3) risk score calculation
    score = 0
    if anomaly_flag == -1:
        score += 40
    if abs(anomaly_score) > 0.15:
        score += 10
    if cluster_id in [6, 7]:
        score += 20

    level = "HIGH" if score >= 60 else "MEDIUM" if score >= 30 else "LOW"

    risk_row = RiskLog(
        store=data.store,
        dept=data.dept,
        risk_score=score,
        risk_level=level,
        anomaly=anomaly_flag,
        cluster=cluster_id
    )
    db.add(risk_row)

    # 4) auto alert
    if level == "HIGH":
        db.add(Alert(
            store=data.store,
            dept=data.dept,
            message="⚠ High risk detected from IoT update",
            risk_score=score
        ))

    db.commit()

    return {
        "status": "success",
        "anomaly": anomaly_flag,
        "anomaly_score": anomaly_score,
        "cluster": cluster_id,
        "risk_level": level,
        "risk_score": score
    }

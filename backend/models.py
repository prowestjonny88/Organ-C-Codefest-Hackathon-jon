from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

# ============================
# ALERTS TABLE
# ============================
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    store = Column(Integer)
    dept = Column(Integer)
    message = Column(String)
    risk_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================
# ANOMALY LOG TABLE
# ============================
class AnomalyLog(Base):
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String)
    value = Column(Float)
    score = Column(Float)

    # IMPORTANT — Render DB expects integer, not boolean
    is_anomaly = Column(Integer)      # 0 = normal, 1 = anomaly

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================
# CLUSTER LOG TABLE
# ============================
class ClusterLog(Base):
    __tablename__ = "cluster_logs"

    id = Column(Integer, primary_key=True, index=True)
    store = Column(Integer)
    dept = Column(Integer)
    cluster = Column(Integer)
    features = Column(JSON)  # store all IoT input as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================
# RISK LOG TABLE
# ============================
class RiskLog(Base):
    __tablename__ = "risk_logs"

    id = Column(Integer, primary_key=True, index=True)
    store = Column(Integer)
    dept = Column(Integer)
    risk_score = Column(Float)
    risk_level = Column(String)

    # Keep integers to match DB schema
    anomaly = Column(Integer)
    cluster = Column(Integer)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

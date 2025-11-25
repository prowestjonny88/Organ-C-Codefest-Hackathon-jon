import { Router } from "express";

const router = Router();

// POST /api/detect_anomaly
// Body: AnomalyInput model with fields:
// Weekly_Sales, Temperature, Fuel_Price, CPI, Unemployment, Store, Dept, IsHoliday
router.post("/detect_anomaly", (req, res) => {
  const {
    Weekly_Sales,
    Temperature,
    Fuel_Price,
    CPI,
    Unemployment,
    Store,
    Dept,
    IsHoliday
  } = req.body;

  // Validate required fields
  if (Weekly_Sales === undefined) {
    return res.status(400).json({ error: "Weekly_Sales is required" });
  }

  // TODO: Replace with actual anomaly detection model
  // This should call your trained isolation forest or anomaly detection model
  
  // Demo response matching your backend structure
  // anomaly: -1 (anomaly detected) or 0 (normal)
  // anomaly_score: float between 0.0 and 1.0
  
  const anomalyScore = Math.random() * 0.3;
  const isAnomaly = anomalyScore > 0.15 ? -1 : 0;

  res.json({
    anomaly: isAnomaly,
    anomaly_score: parseFloat(anomalyScore.toFixed(4))
  });
});

// GET /api/anomalies (optional: get all detected anomalies)
router.get("/anomalies", (req, res) => {
  const { store_id, dept } = req.query;

  // TODO: Query database for historical anomalies
  
  // Demo response
  const anomalies = [
    {
      date: "2024-01-15",
      store: "1",
      dept: "Electronics",
      weekly_sales: 45231.50,
      anomaly: -1,
      anomaly_score: 0.23
    },
    {
      date: "2024-02-03",
      store: "2",
      dept: "Apparel",
      weekly_sales: 12450.75,
      anomaly: -1,
      anomaly_score: 0.31
    }
  ];

  res.json(anomalies);
});

export default router;

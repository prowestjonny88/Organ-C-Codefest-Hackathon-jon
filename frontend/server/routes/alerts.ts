import { Router } from "express";

const router = Router();

// GET /api/alerts
// Query params: store_id (optional), severity (optional: HIGH, MEDIUM, LOW)
router.get("/alerts", (req, res) => {
  const { store_id, severity } = req.query;

  // TODO: Replace with actual alert generation from your risk analysis
  // This should generate alerts based on:
  // - High risk scores (>= 60)
  // - Anomaly detection (anomaly_flag == -1)
  // - High-risk clusters (6, 7)
  
  // Demo alerts data matching your frontend structure
  const alerts = [
    {
      id: "alert-001",
      store: "Store-1",
      severity: "HIGH",
      messages: [
        "⚠ High operational risk detected",
        "⚠ Anomaly detected in sales behavior",
        "⚠ Store belongs to high-risk behavior group"
      ],
      risk_score: 70,
      cluster: 7,
      anomaly_flag: -1,
      timestamp: new Date().toISOString()
    },
    {
      id: "alert-002",
      store: "Store-5",
      severity: "MEDIUM",
      messages: [
        "⚠ Anomaly detected in sales behavior"
      ],
      risk_score: 40,
      cluster: 4,
      anomaly_flag: -1,
      timestamp: new Date().toISOString()
    },
    {
      id: "alert-003",
      store: "Store-12",
      severity: "HIGH",
      messages: [
        "⚠ High operational risk detected",
        "⚠ Store belongs to high-risk behavior group"
      ],
      risk_score: 60,
      cluster: 6,
      anomaly_flag: 0,
      timestamp: new Date().toISOString()
    }
  ];

  // Filter by store_id if provided
  let filtered = alerts;
  if (store_id) {
    filtered = filtered.filter(alert => alert.store === `Store-${store_id}`);
  }
  if (severity && typeof severity === 'string') {
    filtered = filtered.filter(alert => alert.severity === severity.toUpperCase());
  }

  res.json(filtered);
});

export default router;

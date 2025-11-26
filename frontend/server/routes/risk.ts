import { Router } from "express";

const router = Router();

// GET /api/risk_analysis
// Query params: store_id (optional), dept (optional)
router.get("/risk_analysis", (req, res) => {
  const { store_id, dept } = req.query;

  // TODO: Replace with actual risk analysis from your models
  // This should integrate: anomaly detection + cluster analysis + risk scoring
  
  // Demo risk analysis data matching your frontend structure
  const riskItems = [
    {
      store: "Store-1",
      risk_score: 70,
      risk_level: "HIGH",
      cluster: 7,
      anomaly: -1,
      days_to_stockout: 3
    },
    {
      store: "Store-2",
      risk_score: 45,
      risk_level: "MEDIUM",
      cluster: 5,
      anomaly: 0,
      days_to_stockout: 8
    },
    {
      store: "Store-3",
      risk_score: 15,
      risk_level: "LOW",
      cluster: 2,
      anomaly: 0,
      days_to_stockout: 15
    }
  ];

  // Filter by store_id or dept if provided
  let filtered = riskItems;
  if (store_id) {
    filtered = filtered.filter(item => item.store === `Store-${store_id}`);
  }

  res.json(filtered);
});

// Risk scoring logic (matching your backend):
// score = 0
// if anomaly_flag == -1: score += 40
// if abs(anomaly_score) > 0.15: score += 10
// if cluster_id >= 6: score += 20
// 
// Risk levels:
// score >= 60: HIGH
// score >= 30: MEDIUM
// score < 30: LOW

export default router;

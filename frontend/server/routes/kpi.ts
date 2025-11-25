import { Router } from "express";

const router = Router();

// GET /api/kpi_overview
// Query params: store_id (optional), dept (optional)
router.get("/kpi_overview", (req, res) => {
  const { store_id, dept } = req.query;

  // TODO: Replace with actual data from your ML model/database
  // This should call: load_raw_data() and calculate KPIs
  // For now, returning demo structure matching your backend
  
  const kpiData = {
    avg_weekly_sales: 15981.26,
    max_sales: 693099.36,
    min_sales: 209.96,
    volatility: 22786.18,
    holiday_sales_avg: 17413.10
  };

  res.json(kpiData);
});

export default router;

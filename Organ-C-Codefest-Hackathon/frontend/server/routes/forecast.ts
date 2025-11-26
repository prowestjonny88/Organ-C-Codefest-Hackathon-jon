import { Router } from "express";

const router = Router();

// GET /api/forecast
// Query params: store_id (optional), periods (default=6, range 1-26)
router.get("/forecast", (req, res) => {
  const store_id = req.query.store_id ? parseInt(req.query.store_id as string) : null;
  const periods = req.query.periods ? parseInt(req.query.periods as string) : 6;

  // Validate periods range
  if (periods < 1 || periods > 26) {
    return res.status(400).json({ error: "periods must be between 1 and 26" });
  }

  // TODO: Replace with actual forecast from your ML model
  // This should call: get_time_series(store_id) and model.forecast()
  
  // Demo forecast data matching your backend structure
  const forecastData = [];
  const baseDate = new Date();
  
  for (let i = 0; i < periods; i++) {
    const date = new Date(baseDate);
    date.setDate(date.getDate() + (i * 7)); // Weekly forecast
    
    forecastData.push({
      timestamp: date.toISOString().split('T')[0],
      forecast: 15000 + Math.random() * 5000,
      lower_bound: 12000 + Math.random() * 3000,
      upper_bound: 17000 + Math.random() * 5000
    });
  }

  res.json(forecastData);
});

export default router;

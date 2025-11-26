import { Router } from "express";

const router = Router();

// Simple recommendations generator — for a real app, use forecasting/optimization logic
router.get("/recommendations", (_req, res) => {
  // Example dynamic suggestions — in production you would compute from DB/forecasts
  const today = new Date().toISOString().split('T')[0];
  const recommendations = [
    {
      id: "rec-001",
      title: "Increase inventory — Beverages (Store 5)",
      details: "Increase inventory of Beverages in Store 5 next week to meet predicted demand.",
      productId: "prod-bev-05",
      storeId: "store-5",
      date: today,
      action: "order",
      severity: "high",
    },
    {
      id: "rec-002",
      title: "Reduce stock — Apparel (Store 2)",
      details: "Reduce stock levels for Apparel in Store 2 due to expected low demand.",
      productId: "prod-app-02",
      storeId: "store-2",
      date: today,
      action: "reduce",
      severity: "medium",
    },
    {
      id: "rec-003",
      title: "Staff scheduling — Store 8",
      details: "Schedule more staff on weekends for Store 8 owing to an expected rise in weekend traffic.",
      storeId: "store-8",
      date: today,
      action: "schedule_staff",
      severity: "low",
    },
  ];

  return res.json(recommendations);
});

export default router;

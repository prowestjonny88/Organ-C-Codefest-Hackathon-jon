import "dotenv/config";
import express from "express";
import cors from "cors";
import { handleDemo } from "./routes/demo";
import uploadRouter from "./routes/upload";
import recommendationsRouter from "./routes/recommendations";
import kpiRouter from "./routes/kpi";
import forecastRouter from "./routes/forecast";
import anomalyRouter from "./routes/anomaly";
import riskRouter from "./routes/risk";
import alertsRouter from "./routes/alerts";

export function createServer() {
  const app = express();

  // Middleware
  app.use(cors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Example API routes
  app.get("/api/ping", (_req, res) => {
    const ping = process.env.PING_MESSAGE ?? "ping";
    res.json({ message: ping });
  });

  app.get("/api/demo", handleDemo);
  app.use("/api", uploadRouter);
  app.use("/api", recommendationsRouter);
  app.use("/api", kpiRouter);
  app.use("/api", forecastRouter);
  app.use("/api", anomalyRouter);
  app.use("/api", riskRouter);
  app.use("/api", alertsRouter);

  return app;
}

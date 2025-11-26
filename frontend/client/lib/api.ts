import type { BusinessMetrics, InventorySnapshot, ForecastDetail, KPIMetrics } from "@/lib/types";
import { demoMetrics, demoInventories, demoForecast, demoKPIMetrics } from "./demo-data";
import { demoRecommendations } from "./demo-data";

const USE_MOCK = import.meta.env.VITE_USE_MOCK_API === "true";

export async function fetchKPIMetrics(storeId?: number, dept?: number): Promise<KPIMetrics> {
  if (USE_MOCK) return demoKPIMetrics();
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId.toString());
    if (dept) params.append('dept', dept.toString());
    
    const res = await fetch(`/api/kpi_overview?${params.toString()}`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    
    // Map backend response to frontend format
    return {
      avgWeeklySales: json.avg_weekly_sales,
      maxSales: json.max_sales,
      minSales: json.min_sales,
      volatility: json.volatility,
      holidaySalesAvg: json.holiday_sales_avg
    };
  } catch (err) {
    console.warn("fetchKPIMetrics failed, falling back to demo data", err);
    return demoKPIMetrics();
  }
}

export async function fetchMetrics(): Promise<BusinessMetrics> {
  if (USE_MOCK) return demoMetrics();
  try {
    const res = await fetch("/api/metrics");
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json as BusinessMetrics;
  } catch (err) {
    // Fall back to demo data if API unavailable
    console.warn("fetchMetrics failed, falling back to demo data", err);
    return demoMetrics();
  }
}

export async function fetchInventories(): Promise<InventorySnapshot[]> {
  if (USE_MOCK) return demoInventories();
  try {
    const res = await fetch(`/api/inventories`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json as InventorySnapshot[];
  } catch (err) {
    console.warn("fetchInventories failed, falling back to demo data", err);
    return demoInventories();
  }
}

export async function fetchForecast(storeId?: number, periods = 6): Promise<any[]> {
  if (USE_MOCK) return demoForecast("demo", periods);
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId.toString());
    params.append('periods', periods.toString());
    
    const res = await fetch(`/api/forecast?${params.toString()}`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    
    // Map backend response to frontend format
    return json.map((item: any) => ({
      date: item.timestamp,
      forecast: item.forecast,
      lowerInterval: item.lower_bound,
      upperInterval: item.upper_bound,
      historicalSales: 0, // Not provided by forecast endpoint
      anomalyFlag: false
    }));
  } catch (err) {
    console.warn("fetchForecast failed, falling back to demo data", err);
    return demoForecast("demo", periods);
  }
}

export async function fetchRecommendations(): Promise<any[]> {
  if (USE_MOCK) return demoRecommendations();
  try {
    const res = await fetch(`/api/recommendations`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json as any[];
  } catch (err) {
    console.warn("fetchRecommendations failed, falling back to demo data", err);
    return demoRecommendations();
  }
}

export async function fetchAnomalies(storeId?: number, dept?: number): Promise<any[]> {
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId.toString());
    if (dept) params.append('dept', dept.toString());
    
    const res = await fetch(`/api/anomalies?${params.toString()}`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json;
  } catch (err) {
    console.warn("fetchAnomalies failed", err);
    return [];
  }
}

export async function detectAnomaly(data: {
  Weekly_Sales: number;
  Temperature?: number;
  Fuel_Price?: number;
  CPI?: number;
  Unemployment?: number;
  Store?: number;
  Dept?: number;
  IsHoliday?: number;
}): Promise<{ anomaly: number; anomaly_score: number }> {
  try {
    const res = await fetch(`/api/detect_anomaly`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json;
  } catch (err) {
    console.warn("detectAnomaly failed", err);
    return { anomaly: 0, anomaly_score: 0 };
  }
}

export async function fetchRiskAnalysis(storeId?: number, dept?: number): Promise<any[]> {
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId.toString());
    if (dept) params.append('dept', dept.toString());
    
    const res = await fetch(`/api/risk_analysis?${params.toString()}`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json;
  } catch (err) {
    console.warn("fetchRiskAnalysis failed", err);
    return [];
  }
}

export async function fetchAlerts(storeId?: number, severity?: string): Promise<any[]> {
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId.toString());
    if (severity) params.append('severity', severity);
    
    const res = await fetch(`/api/alerts?${params.toString()}`);
    if (!res.ok) throw new Error("API error");
    const json = await res.json();
    return json;
  } catch (err) {
    console.warn("fetchAlerts failed", err);
    return [];
  }
}

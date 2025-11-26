// Data type definitions for Retail

export interface SalesRecord {
  date: string;
  storeId: string;
  state: string;
  category: string;
  productId: string;
  productName: string;
  actualSales: number;
  forecastSales: number;
  lowerConfidence: number;
  upperConfidence: number;
}

export interface SupplierDimension {
  productId: string;
  supplierId: string;
  avgLeadTime: number;
  leadTimeStd: number;
  reliabilityScore: number;
  unitCost: number;
  retailPrice: number;
  holdingCostPercent: number;
  orderingCost: number;
}

export interface InventorySnapshot {
  productId: string;
  productName: string;
  storeId: string;
  category: string;
  currentStock: number;
  reorderPoint: number;
  safetyStock: number;
  economicOrderQuantity: number;
  daysUntilStockout: number;
  riskLevel: "low" | "medium" | "high" | "critical";
  recommendedOrderQty: number;
  lastOrder: string;
  avgDailyDemand: number;
}

export interface ForecastDetail {
  productId: string;
  date: string;
  historicalSales: number;
  forecast: number;
  lowerInterval: number;
  upperInterval: number;
  anomalyFlag: boolean;
  anomalyReason?: string;
}

export interface BusinessMetrics {
  forecastAccuracy: number;
  costSavings: number;
  inventoryTurnover: number;
  leadTime: number;
  serviceLevel: number;
  excessInventoryValue: number;
  potentialLostRevenue: number;
}

export interface KPIMetrics {
  avgWeeklySales: number;
  maxSales: number;
  minSales: number;
  volatility: number;
  holidaySalesAvg: number;
}

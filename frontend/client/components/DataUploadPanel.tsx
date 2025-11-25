import { useState } from "react";
import Papa from "papaparse";
import type {
  SalesRecord,
  InventorySnapshot,
  SupplierDimension,
} from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, Database, TrendingUp, AlertTriangle } from "lucide-react";

export interface UploadResult {
  sales?: SalesRecord[];
  products?: InventorySnapshot[];
  suppliers?: SupplierDimension[];
}

interface DataUploadPanelProps {
  // onDataLoaded receives parsed objects extracted from CSVs
  onDataLoaded: (result?: UploadResult) => void;
}

export default function DataUploadPanel({ onDataLoaded }: DataUploadPanelProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    setIsLoading(true);
    setUploadError(null);
    const uploads: UploadResult = {};

    const filePromises = files.map((file) =>
      new Promise<void>(async (resolve) => {
        try {
          const fd = new FormData();
          fd.append("file", file);
          const resp = await fetch("/api/upload", { method: "POST", body: fd });
          if (resp.ok) {
            const json = await resp.json();
            if (json.sales) uploads.sales = (uploads.sales || []).concat(json.sales);
            if (json.products) uploads.products = (uploads.products || []).concat(json.products);
            if (json.suppliers) uploads.suppliers = (uploads.suppliers || []).concat(json.suppliers);
            return resolve();
          }
        } catch (err) {
          // ignore and fallback to client parsing
        }

        // Client-side parsing with PapaParse
        Papa.parse(file, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
          complete: (results) => {
            try {
              const rows = results.data as any[];
              const headers = (results.meta.fields || Object.keys(rows[0] || {})).map((h) => String(h));
              const headerSet = new Set(headers.map((h) => h.toLowerCase()));
              const isSales = headerSet.has("actualsales") || headerSet.has("forecastsales") || headerSet.has("date");
              const isSupplier = headerSet.has("supplierid") || headerSet.has("avgleadtime");
              const isProduct = headerSet.has("productid") && headerSet.has("productname") && headerSet.has("currentstock");

              if (isSales) {
                uploads.sales = (uploads.sales || []).concat(
                  rows.map((r) => ({
                    date: r["date"] || r["Date"] || "",
                    storeId: r["storeId"] || r["StoreId"] || r["store_id"] || "",
                    state: r["state"] || "",
                    category: r["category"] || "",
                    productId: r["productId"] || r["ProductId"] || r["product_id"] || "",
                    productName: r["productName"] || r["ProductName"] || "",
                    actualSales: Number(r["actualSales"] || r["ActualSales"] || r["quantity"] || 0),
                    forecastSales: Number(r["forecastSales"] || 0),
                    lowerConfidence: Number(r["lowerConfidence"] || 0),
                    upperConfidence: Number(r["upperConfidence"] || 0),
                  })) as SalesRecord[]
                );
              } else if (isSupplier) {
                uploads.suppliers = (uploads.suppliers || []).concat(
                  rows.map((r) => ({
                    productId: r["productId"] || r["ProductId"] || r["product_id"] || "",
                    supplierId: r["supplierId"] || r["SupplierId"] || "",
                    avgLeadTime: Number(r["avgLeadTime"] || 0),
                    leadTimeStd: Number(r["leadTimeStd"] || 0),
                    reliabilityScore: Number(r["reliabilityScore"] || 0),
                    unitCost: Number(r["unitCost"] || 0),
                    retailPrice: Number(r["retailPrice"] || 0),
                    holdingCostPercent: Number(r["holdingCostPercent"] || 0),
                    orderingCost: Number(r["orderingCost"] || 0),
                  })) as SupplierDimension[]
                );
              } else if (isProduct) {
                uploads.products = (uploads.products || []).concat(
                  rows.map((r) => ({
                    productId: r["productId"] || r["ProductId"] || r["product_id"] || "",
                    productName: r["productName"] || r["ProductName"] || "",
                    storeId: r["storeId"] || r["StoreId"] || "",
                    category: r["category"] || "",
                    currentStock: Number(r["currentStock"] || r["stock"] || 0),
                    reorderPoint: Number(r["reorderPoint"] || 0),
                    safetyStock: Number(r["safetyStock"] || 0),
                    economicOrderQuantity: Number(r["economicOrderQuantity"] || 0),
                    daysUntilStockout: Number(r["daysUntilStockout"] || 0),
                    riskLevel: (r["riskLevel"] as any) || "low",
                    recommendedOrderQty: Number(r["recommendedOrderQty"] || 0),
                    lastOrder: r["lastOrder"] || "",
                    avgDailyDemand: Number(r["avgDailyDemand"] || 0),
                  })) as InventorySnapshot[]
                );
              }
              resolve();
            } catch (err) {
              setUploadError(err instanceof Error ? err.message : "Failed to parse file");
              resolve();
            }
          },
          error: (err) => {
            setUploadError(err.message);
            resolve();
          },
        });
      })
    );

    Promise.all(filePromises)
      .then(() => {
        setIsLoading(false);
        onDataLoaded(uploads);
      })
      .catch((err) => {
        setUploadError(err instanceof Error ? err.message : String(err));
        setIsLoading(false);
      });
  };

  // Demo data loader: call the callback with synthesized sample datasets
  const handleDemoData = () => {
    setIsLoading(true);
    setTimeout(() => {
      const demoSales: SalesRecord[] = [
        {
          date: new Date().toISOString().split("T")[0],
          storeId: "store-1",
          state: "CA",
          category: "Apparel",
          productId: "prod-001",
          productName: "Blue T-Shirt",
          actualSales: 15,
          forecastSales: 14,
          lowerConfidence: 12,
          upperConfidence: 17,
        },
        {
          date: new Date().toISOString().split("T")[0],
          storeId: "store-1",
          state: "CA",
          category: "Apparel",
          productId: "prod-002",
          productName: "Green Hoodie",
          actualSales: 7,
          forecastSales: 8,
          lowerConfidence: 6,
          upperConfidence: 10,
        },
      ];
      const demoProducts: InventorySnapshot[] = [
        {
          productId: "prod-001",
          productName: "Blue T-Shirt",
          storeId: "store-1",
          category: "Apparel",
          currentStock: 120,
          reorderPoint: 20,
          safetyStock: 10,
          economicOrderQuantity: 240,
          daysUntilStockout: 8,
          riskLevel: "medium",
          recommendedOrderQty: 180,
          lastOrder: new Date().toISOString().split("T")[0],
          avgDailyDemand: 2,
        },
        {
          productId: "prod-002",
          productName: "Green Hoodie",
          storeId: "store-2",
          category: "Apparel",
          currentStock: 40,
          reorderPoint: 10,
          safetyStock: 8,
          economicOrderQuantity: 50,
          daysUntilStockout: 5,
          riskLevel: "high",
          recommendedOrderQty: 30,
          lastOrder: new Date().toISOString().split("T")[0],
          avgDailyDemand: 1,
        },
      ];
      setIsLoading(false);
      onDataLoaded({ sales: demoSales, products: demoProducts });
    }, 700);
  };


  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 flex items-center justify-center px-4 pt-20">
      <div className="max-w-2xl w-full">
        {/* Welcome Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-secondary mb-6">
            <Database className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-4">
            👋 WELCOME 👋
          </h1>
          <p className="text-foreground/60">
            Powered by ML demand forecasting, statistical anomaly detection,
            and operations research optimization
          </p>
        </div>

        {/* Upload Panel */}
        <Card className="border-0 shadow-xl mb-8">
          <CardContent className="p-8">
            <div className="space-y-6">
              {/* Instructions */}
              <div>
                <h2 className="text-xl font-semibold text-foreground mb-4">
                  Get Started
                </h2>
                <p className="text-foreground/70 mb-6">
                  Upload your CSV files or try our demo data to see the platform in action.
                </p>
              </div>

              {/* File Upload Area */}
              <div className="relative">
                <input
                  type="file"
                  multiple
                  accept=".csv,.json"
                  onChange={handleFileUpload}
                  disabled={isLoading}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className={`block p-8 border-2 border-dashed rounded-xl text-center cursor-pointer transition-all ${
                    isLoading
                      ? "border-border bg-slate-50 cursor-not-allowed opacity-75"
                      : "border-primary/30 bg-primary/5 hover:border-primary hover:bg-primary/10"
                  }`}
                >
                  <Upload className="w-8 h-8 text-primary mx-auto mb-3" />
                  <p className="font-semibold text-foreground mb-1">
                    {isLoading ? "Processing files..." : "Drag and drop files here"}
                  </p>
                  <p className="text-sm text-foreground/60">
                    {isLoading
                      ? "Please wait..."
                      : "or click to select CSV or JSON files"}
                  </p>
                </label>
              </div>

              {/* Error Message */}
              {uploadError && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-red-900">Upload Failed</p>
                    <p className="text-sm text-red-800">{uploadError}</p>
                  </div>
                </div>
              )}

              {/* Demo Data Option */}
              <div className="border-t border-border pt-6">
                <p className="text-sm text-foreground/70 mb-4">
                  Don't have data ready? Start with sample data to explore features.
                </p>
                <Button
                  onClick={handleDemoData}
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-primary to-secondary font-semibold"
                  size="lg"
                >
                  <TrendingUp className="w-4 h-4 mr-2" />
                  {isLoading ? "Loading Demo Data..." : "Load Demo Data"}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Features Highlight */}
        <div className="grid md:grid-cols-3 gap-4">
          {[
            {
              icon: TrendingUp,
              title: "Smart Forecasting",
              desc: "With high accuracy",
            },
            {
              icon: AlertTriangle,
              title: "Anomaly Detection",
              desc: "Real-time alerts for stockouts, spikes, and irregularities",
            },
            {
              icon: Database,
              title: "Optimization",
              desc: "Dynamic and safety recommendations",
            },
          ].map((feature) => {
            const Icon = feature.icon;
            return (
              <Card key={feature.title} className="border-0 text-center">
                <CardContent className="p-6">
                  <Icon className="w-8 h-8 text-primary mx-auto mb-3" />
                  <h3 className="font-semibold text-foreground mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-xs text-foreground/60">{feature.desc}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}

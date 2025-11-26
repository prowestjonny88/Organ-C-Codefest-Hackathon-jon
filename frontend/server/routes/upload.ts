import { RequestHandler, Router } from "express";
import multer from "multer";
import Papa from "papaparse";
import type { UploadResult } from "@/components/DataUploadPanel";

const upload = multer({ storage: multer.memoryStorage() });

const router = Router();

router.post("/upload", upload.single("file"), (req, res) => {
  try {
    const file = (req as any).file as any | undefined;
    if (!file) return res.status(400).json({ message: "No file uploaded" });
    const text = file.buffer.toString("utf8");
    const results = Papa.parse(text, { header: true, dynamicTyping: true, skipEmptyLines: true });
    const rows = results.data as any[];
    console.log("UPLOAD ROUTE: parsed rows count:", rows.length);
    const headers = (results.meta.fields || Object.keys(rows[0] || {})).map((h) => String(h));
    console.log("UPLOAD ROUTE: parsed headers:", headers);
    const headerSet = new Set(headers.map((h) => h.toLowerCase()));
    console.log("UPLOAD ROUTE: headerSet contains:\n", Array.from(headerSet).join(", "));
    const uploads: UploadResult = {};
    const isSales = headerSet.has("date") || headerSet.has("actualsales");
    const isSupplier = headerSet.has("supplierid") || headerSet.has("avgleadtime");
    const isProduct = headerSet.has("productid") && headerSet.has("productname") && headerSet.has("currentstock");

    console.log("UPLOAD ROUTE: flags", { isSales, isSupplier, isProduct });

    if (isSales) {
      uploads.sales = rows.map((r) => ({
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
      }));
    } else if (isSupplier) {
      uploads.suppliers = rows.map((r) => ({
        productId: r["productId"] || r["ProductId"] || r["product_id"] || "",
        supplierId: r["supplierId"] || r["SupplierId"] || "",
        avgLeadTime: Number(r["avgLeadTime"] || 0),
        leadTimeStd: Number(r["leadTimeStd"] || 0),
        reliabilityScore: Number(r["reliabilityScore"] || 0),
        unitCost: Number(r["unitCost"] || 0),
        retailPrice: Number(r["retailPrice"] || 0),
        holdingCostPercent: Number(r["holdingCostPercent"] || 0),
        orderingCost: Number(r["orderingCost"] || 0),
      }));
    } else if (isProduct) {
      uploads.products = rows.map((r) => ({
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
      }));
    }

    return res.json(uploads);
  } catch (err) {
    return res.status(500).json({ message: err instanceof Error ? err.message : "Server error" });
  }
});

export default router;

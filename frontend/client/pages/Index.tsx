import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Navigation from "@/components/Navigation";
import { Link } from "react-router-dom";
import {
  TrendingUp,
  AlertTriangle,
  Zap,
  BarChart3,
  Brain,
  Shield,
  ArrowRight,
  CheckCircle,
} from "lucide-react";

export default function Index() {
  return (
    <>
      <Navigation />
      <main>
        {/* Hero Section */}
        <section className="pt-20 pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block mb-4 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20">
                <span className="text-sm font-medium text-primary">
                  🚀 Powered by AI & Advanced Analytics
                </span>
              </div>
              <h1 className="text-5xl sm:text-6xl font-bold mb-6 text-foreground">
                Intelligent{" "}
                <span className="gradient-text">Inventory Optimization</span>
              </h1>
              <p className="text-lg text-foreground/70 mb-8 leading-relaxed">
                Leverage machine learning for accurate demand forecasting,
                statistical anomaly detection, and operations research heuristics
                to optimize your inventory in real-time.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/dashboard">
                  <Button
                    size="lg"
                    className="bg-gradient-to-r from-primary to-secondary w-full sm:w-auto"
                  >
                    View Dashboard
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </Link>
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-2xl blur-3xl" />
              <div className="relative bg-gradient-to-br from-primary/5 to-secondary/5 rounded-2xl border border-primary/10 p-8">
                <div className="space-y-4">
                  <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-border">
                    <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                      <TrendingUp className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-xs text-foreground/50">Forecast</p>
                      <p className="font-semibold">+23.5%</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-border">
                    <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                      <AlertTriangle className="w-5 h-5 text-secondary" />
                    </div>
                    <div>
                      <p className="text-xs text-foreground/50">Anomalies</p>
                      <p className="font-semibold">2 Alerts</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-border">
                    <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
                      <Zap className="w-5 h-5 text-green-600" />
                    </div>
                    <div>
                      <p className="text-xs text-foreground/50">Optimized</p>
                      <p className="font-semibold">-18% Cost</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-transparent to-primary/5">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4 text-foreground">
                Powerful Features for Modern Supply Chains
              </h2>
              <p className="text-lg text-foreground/60 max-w-2xl mx-auto">
                Our platform combines cutting-edge AI, statistical analysis, and
                optimization algorithms to transform your inventory management.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Demand Forecasting */}
              <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center mb-4">
                    <Brain className="w-6 h-6 text-primary" />
                  </div>
                  <CardTitle className="text-xl">ML Demand Forecasting</CardTitle>
                </CardHeader>
                <CardContent className="text-foreground/70">
                  Advanced machine learning models that predict demand patterns
                  with high accuracy, accounting for seasonality, trends, and
                  external factors.
                </CardContent>
              </Card>

              {/* Anomaly Detection */}
              <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-purple-100 flex items-center justify-center mb-4">
                    <Shield className="w-6 h-6 text-secondary" />
                  </div>
                  <CardTitle className="text-xl">Anomaly Detection</CardTitle>
                </CardHeader>
                <CardContent className="text-foreground/70">
                  Statistical process control algorithms that detect unusual
                  patterns in your inventory, supply chain, and demand data in
                  real-time.
                </CardContent>
              </Card>

              {/* Inventory Optimization */}
              <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center mb-4">
                    <Zap className="w-6 h-6 text-green-600" />
                  </div>
                  <CardTitle className="text-xl">Inventory Optimization</CardTitle>
                </CardHeader>
                <CardContent className="text-foreground/70">
                  Operations research heuristics that optimize stock levels, order
                  quantities, and reorder points to minimize costs while
                  maintaining service levels.
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-4 text-foreground">
                Why Choose Us
              </h2>
              <div className="space-y-4">
                {[
                  "Real-time analytics and insights",
                  "Reduce inventory carrying costs",
                  "Improve inventory turnover",
                  "Forecast accuracy",
                  "Automated anomaly alerts",
                  "Enterprise-grade security",
                ].map((benefit) => (
                  <div key={benefit} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-secondary flex-shrink-0 mt-1" />
                    <p className="text-foreground/80">{benefit}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-6">
              {[
                { icon: BarChart3, label: "Real-time Analytics" },
                { icon: TrendingUp, label: "Forecast Accuracy" },
                { icon: Zap, label: "Cost Reduction" },
                { icon: AlertTriangle, label: "Anomaly Detection" },
              ].map(({ icon: Icon, label }) => (
                <Card key={label} className="border-0">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <Icon className="w-8 h-8 text-primary/60" />
                    </div>
                    <p className="text-sm text-foreground/60">{label}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

      </main>
    </>
  );
}

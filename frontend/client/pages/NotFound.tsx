import Navigation from "@/components/Navigation";
import useDocumentTitle from "@/hooks/use-document-title";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

export default function NotFound() {
  useDocumentTitle("Retail — Page Not Found");
  return (
    <>
      <Navigation />
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-white to-slate-50 px-4">
        <div className="text-center max-w-md">
          <div className="mb-6">
            <div className="text-6xl font-bold text-foreground mb-2">404</div>
            <h1 className="text-2xl font-bold text-foreground mb-2">
              Page Not Found
            </h1>
            <p className="text-foreground/60">
              The page you're looking for doesn't exist or hasn't been built yet.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link to="/">
              <Button variant="outline" className="gap-2">
                <ArrowLeft className="w-4 h-4" />
                Back to Home
              </Button>
            </Link>
            <Link to="/dashboard">
              <Button className="bg-gradient-to-r from-primary to-secondary">
                Go to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </main>
    </>
  );
}

import { Link } from "react-router-dom";
// Auth CTAs removed; Button import not required here
import { Menu, X } from "lucide-react";
import { useState } from "react";

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-border z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center gap-2 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
                <span className="text-white font-bold text-lg">I</span>
              </div>
            </Link>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center gap-8">
              <Link
                to="/"
                className="text-sm font-medium text-foreground/70 hover:text-foreground transition-colors"
              >
                Home
              </Link>
              <Link
                to="/dashboard"
                className="text-sm font-medium text-foreground/70 hover:text-foreground transition-colors"
              >
                Dashboard
              </Link>
              {/* Features & Pricing removed */}
            </div>


            {/* Mobile Menu Button */}
            <button
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t border-border py-4 space-y-3">
              <Link
                to="/"
                className="block text-sm font-medium text-foreground/70 hover:text-foreground transition-colors py-2"
              >
                Home
              </Link>
              <Link
                to="/dashboard"
                className="block text-sm font-medium text-foreground/70 hover:text-foreground transition-colors py-2"
              >
                Dashboard
              </Link>

            </div>
          )}
        </div>
      </nav>
      <div className="h-16" />
    </>
  );
}

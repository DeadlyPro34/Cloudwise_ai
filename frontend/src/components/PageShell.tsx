import { Link } from "react-router-dom";
import { useState } from "react";
import { Zap, Menu, X } from "lucide-react";

/* ─────────────────────────────────────────────
   Shared Navbar  (used by all public info pages)
───────────────────────────────────────────── */
function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav
      style={{
        position: "sticky",
        top: 0,
        zIndex: 100,
        background: "rgba(7,8,15,0.88)",
        backdropFilter: "blur(18px)",
        WebkitBackdropFilter: "blur(18px)",
        borderBottom: "1px solid rgba(255,255,255,0.07)",
      }}
    >
      <div
        style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "0 24px",
          height: 60,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {/* Logo */}
        <Link
          to="/"
          style={{ textDecoration: "none", display: "flex", alignItems: "center", gap: "0.5rem", flexShrink: 0 }}
        >
          <div
            style={{
              width: 30,
              height: 30,
              borderRadius: 8,
              background: "linear-gradient(135deg,#5B52F0,#7B75FF)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Zap size={15} color="#fff" />
          </div>
          <span style={{ fontSize: "1.05rem", fontWeight: 700, color: "#EEF2FF", letterSpacing: "-0.01em" }}>
            CloudWise AI
          </span>
        </Link>

        {/* Desktop nav links — hidden on mobile via CSS class */}
        <div className="landing-nav-links">
          {[
            { label: "Features", href: "/#features" },
            { label: "Why Us", href: "/#why-us" },
            { label: "Docs", href: "/docs" },
          ].map(({ label, href }) => (
            <a
              key={label}
              href={href}
              style={{ fontSize: "0.92rem", fontWeight: 500, color: "#8B93B5", textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = "#EEF2FF")}
              onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = "#8B93B5")}
            >
              {label}
            </a>
          ))}
        </div>

        {/* Desktop CTA buttons — hidden on mobile via CSS class */}
        <div className="landing-nav-ctas">
          <Link
            to="/login"
            style={{ fontSize: "0.88rem", fontWeight: 500, color: "#8B93B5", textDecoration: "none", padding: "0.4rem 0.9rem", transition: "color 0.2s" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = "#EEF2FF")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = "#8B93B5")}
          >
            Log In
          </Link>
          <Link
            to="/signup"
            style={{
              fontSize: "0.85rem",
              fontWeight: 600,
              color: "#fff",
              textDecoration: "none",
              padding: "0.48rem 1.15rem",
              background: "linear-gradient(135deg,#5B52F0,#7B75FF)",
              borderRadius: 8,
              transition: "opacity 0.2s",
            }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.opacity = "0.85")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.opacity = "1")}
          >
            Get Started
          </Link>
        </div>

        {/* Hamburger — shown only on mobile via CSS class */}
        <button
          className="landing-hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
          aria-expanded={menuOpen}
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile dropdown menu */}
      {menuOpen && (
        <div
          style={{
            background: "#0e0f1a",
            borderTop: "1px solid rgba(255,255,255,0.07)",
            padding: "1rem 24px 1.5rem",
            display: "flex",
            flexDirection: "column",
            gap: "0.85rem",
          }}
        >
          {[
            { label: "Features", href: "/#features" },
            { label: "Why Us", href: "/#why-us" },
            { label: "Docs", href: "/docs" },
          ].map(({ label, href }) => (
            <a
              key={label}
              href={href}
              onClick={() => setMenuOpen(false)}
              style={{ color: "#8B93B5", textDecoration: "none", fontSize: "1rem", padding: "0.35rem 0" }}
            >
              {label}
            </a>
          ))}
          <div style={{ height: 1, background: "rgba(255,255,255,0.07)", margin: "0.25rem 0" }} />
          <Link
            to="/login"
            onClick={() => setMenuOpen(false)}
            style={{ color: "#8B93B5", textDecoration: "none", fontSize: "1rem", padding: "0.35rem 0" }}
          >
            Log In
          </Link>
          <Link
            to="/signup"
            onClick={() => setMenuOpen(false)}
            style={{
              color: "#fff",
              textDecoration: "none",
              fontSize: "0.95rem",
              background: "linear-gradient(135deg,#5B52F0,#7B75FF)",
              padding: "0.65rem 1rem",
              borderRadius: 8,
              textAlign: "center",
              fontWeight: 600,
              marginTop: "0.25rem",
            }}
          >
            Get Started
          </Link>
        </div>
      )}
    </nav>
  );
}

/* ─────────────────────────────────────────────
   Shared Footer
───────────────────────────────────────────── */
function FooterCol({ heading, links }: { heading: string; links: { label: string; href: string }[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.8rem" }}>
      <p
        style={{
          fontSize: "0.7rem",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          color: "#4b5563",
          fontWeight: 700,
          margin: "0 0 0.1rem",
        }}
      >
        {heading}
      </p>
      {links.map(({ label, href }) =>
        href.startsWith("/") && !href.startsWith("/#") ? (
          <Link
            key={label}
            to={href}
            style={{ fontSize: "0.875rem", color: "#9ca3af", textDecoration: "none", transition: "color 0.2s" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = "#EEF2FF")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = "#9ca3af")}
          >
            {label}
          </Link>
        ) : (
          <a
            key={label}
            href={href}
            style={{ fontSize: "0.875rem", color: "#9ca3af", textDecoration: "none", transition: "color 0.2s" }}
            onMouseEnter={(e) => ((e.currentTarget as HTMLElement).style.color = "#EEF2FF")}
            onMouseLeave={(e) => ((e.currentTarget as HTMLElement).style.color = "#9ca3af")}
          >
            {label}
          </a>
        )
      )}
    </div>
  );
}

function PageFooter() {
  return (
    <footer style={{ background: "#07080f", borderTop: "1px solid rgba(255,255,255,0.07)", padding: "56px 32px 32px" }}>
      <div
        className="footer-grid"
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr 1fr 1fr",
          gap: "2.5rem",
          maxWidth: 1100,
          margin: "0 auto",
        }}
      >
        {/* Brand */}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <div
              style={{
                width: 28,
                height: 28,
                borderRadius: 8,
                background: "linear-gradient(135deg,#5B52F0,#7B75FF)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
              }}
            >
              <Zap size={13} color="#fff" />
            </div>
            <span style={{ fontSize: "1rem", fontWeight: 700, color: "#EEF2FF", letterSpacing: "-0.01em" }}>
              CloudWise AI
            </span>
          </div>
          <p style={{ color: "#6b7280", fontSize: "0.85rem", lineHeight: 1.65, maxWidth: 220, margin: 0 }}>
            Actionable FinOps intelligence for modern engineering teams.
          </p>
        </div>

        <FooterCol
          heading="Quick Links"
          links={[
            { label: "Features", href: "/#features" },
            { label: "Why Us", href: "/#why-us" },
            { label: "Documentation", href: "/docs" },
          ]}
        />
        <FooterCol
          heading="Company"
          links={[
            { label: "About Us", href: "/about" },
            { label: "Contact", href: "/contact" },
          ]}
        />
        <FooterCol
          heading="Legal"
          links={[
            { label: "Privacy Policy", href: "/privacy" },
            { label: "Terms of Service", href: "/terms" },
            { label: "Security (SOC 2)", href: "/security" },
            { label: "Cookie Policy", href: "/cookies" },
          ]}
        />
      </div>

      {/* Bottom bar */}
      <div
        style={{
          borderTop: "1px solid rgba(255,255,255,0.06)",
          marginTop: "2.5rem",
          paddingTop: "1.25rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "0.75rem",
          maxWidth: 1100,
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        <p style={{ fontSize: "0.82rem", color: "#6b7280", margin: 0 }}>
          {String.fromCharCode(169)} 2026 CloudWise AI {String.fromCharCode(183)} All rights reserved
        </p>
        <div style={{ display: "flex", gap: "1.25rem" }}>
          {["Twitter", "GitHub", "LinkedIn"].map((s) => (
            <a
              key={s}
              href="#"
              style={{ fontSize: "0.82rem", color: "#6b7280", textDecoration: "none", transition: "color 0.2s" }}
              onMouseEnter={(e) => ((e.target as HTMLElement).style.color = "#9ca3af")}
              onMouseLeave={(e) => ((e.target as HTMLElement).style.color = "#6b7280")}
            >
              {s}
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}

/* ─────────────────────────────────────────────
   PageShell — wraps any public page
───────────────────────────────────────────── */
export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", background: "#07080f" }}>
      <Navbar />
      <main style={{ flex: 1 }}>{children}</main>
      <PageFooter />
    </div>
  );
}

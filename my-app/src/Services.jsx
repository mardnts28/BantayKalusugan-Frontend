import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Stethoscope, Home, PhoneCall, Database, BarChart2, Shield,
  Activity, CheckCircle, ArrowRight, Clock, Users, Monitor,
  Heart, FileText, Bell, Search, Lock, Zap, MapPin, Phone,
  Mail, Menu, X,
} from "lucide-react";
import logo from "./assets/logo.png";
import "./services.css";

// ── Images ────────────────────────────────────────────────────────────────────
const analyticsImage =
  "https://images.unsplash.com/photo-1551288049-bebda4e38f71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080";
const clinicServiceImage =
  "https://images.unsplash.com/photo-1758206523670-67343d3b27eb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080";
const bpImage =
  "https://images.unsplash.com/photo-1623658045230-605cb00c80d6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080";

// ── Static Data ───────────────────────────────────────────────────────────────
const coreServices = [
  {
    icon: <Stethoscope size={28} />,
    title: "Vital Signs Monitoring",
    tagline: "Complete patient assessment",
    description:
      "Capture and store a comprehensive set of vital signs for every community patient — including blood pressure, heart rate, body temperature, SpO₂ (oxygen saturation), respiratory rate, height, weight, and BMI.",
    features: [
      "Blood pressure readings (systolic/diastolic)",
      "Heart rate and pulse oximetry (SpO₂)",
      "Body temperature logging",
      "Respiratory rate tracking",
      "BMI calculation from height/weight",
      "Historical trend charts per patient",
    ],
    color: "#2E5895",
    iconBg: "rgba(46,88,149,0.1)",
    image: bpImage,
    reverse: false,
  },
  {
    icon: <Database size={28} />,
    title: "Digital Patient Records",
    tagline: "Paperless health management",
    description:
      "Replace paper-based logbooks with a secure, centralized digital system. Each patient gets a comprehensive health profile accessible to authorized barangay staff — with complete visit history and data.",
    features: [
      "Complete patient registration and profiling",
      "Full visit history with timestamps",
      "Searchable patient database",
      "Secure data storage with access control",
      "Easy data retrieval and editing",
      "Offline data entry support via BHWs",
    ],
    color: "#C23B21",
    iconBg: "rgba(194,59,33,0.1)",
    image: clinicServiceImage,
    reverse: true,
  },
  {
    icon: <BarChart2 size={28} />,
    title: "Health Analytics & Reports",
    tagline: "Data-driven community insights",
    description:
      "Generate community-wide health reports and visualize trends across your barangay. Track which conditions are most prevalent, identify at-risk populations, and plan interventions using real data.",
    features: [
      "Community health trend visualizations",
      "Barangay-wide vital signs statistics",
      "Patient risk stratification reports",
      "Monthly and annual health summaries",
      "Exportable PDF and data reports",
      "Recharts-powered interactive dashboards",
    ],
    color: "#b8820a",
    iconBg: "rgba(255,195,43,0.15)",
    image: analyticsImage,
    reverse: false,
  },
];

const additionalServices = [
  { icon: <Home      size={22} />, title: "Home Visit Tracking",    description: "Log and schedule home visits for community members, ensuring consistent coverage and no household is missed during BHW rounds.", color: "#2E5895", iconBg: "rgba(46,88,149,0.1)"   },
  { icon: <PhoneCall size={22} />, title: "Referral Management",    description: "Efficiently manage and document patient referrals to local health centers, hospitals, and specialist facilities.",             color: "#C23B21", iconBg: "rgba(194,59,33,0.1)"   },
  { icon: <Monitor   size={22} />, title: "Admin Dashboard",        description: "A comprehensive control panel for barangay staff to manage patients, review records, and oversee all health monitoring activities.", color: "#b8820a", iconBg: "rgba(255,195,43,0.15)" },
  { icon: <Activity  size={22} />, title: "Patient Portal",         description: "Patients can view their own health records, vital sign history, and track health trends through a dedicated personal dashboard.", color: "#2E5895", iconBg: "rgba(46,88,149,0.1)"   },
  { icon: <FileText  size={22} />, title: "Appointment Scheduling", description: "Book, manage, and track check-up appointments — with filtering by status and easy cancellation for both staff and patients.",    color: "#C23B21", iconBg: "rgba(194,59,33,0.1)"   },
  { icon: <Bell      size={22} />, title: "Risk Alerts",            description: "Automatically flag patients with abnormal vital signs for immediate follow-up by barangay staff or BHW coordinators.",           color: "#b8820a", iconBg: "rgba(255,195,43,0.15)" },
  { icon: <Search    size={22} />, title: "Patient Search & Filter",description: "Quickly find any patient record using name, date, condition, or vital sign readings through the admin's advanced search tools.",   color: "#2E5895", iconBg: "rgba(46,88,149,0.1)"   },
  { icon: <Lock      size={22} />, title: "Secure Access Control",  description: "Role-based login ensures only authorized barangay staff access admin features, while patients see only their own health data.",     color: "#C23B21", iconBg: "rgba(194,59,33,0.1)"   },
  { icon: <Zap       size={22} />, title: "Fast Data Entry",        description: "Streamlined data entry forms designed for speed — allowing barangay staff to quickly input BHW-collected vital signs with minimal clicks.", color: "#b8820a", iconBg: "rgba(255,195,43,0.15)" },
];

const benefits = [
  { icon: <Clock        size={18} />, label: "Saves Time",    color: "#2E5895" },
  { icon: <Heart        size={18} />, label: "Better Care",   color: "#C23B21" },
  { icon: <CheckCircle  size={18} />, label: "Accuracy",      color: "#b8820a" },
  { icon: <Users        size={18} />, label: "Accessibility", color: "#2E5895" },
];

// ── Navbar ────────────────────────────────────────────────────────────────────
function Navbar() {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <>
      <nav className={`services-navbar${scrolled ? " services-navbar--scrolled" : ""}`}>
        <div className="services-navbar-brand">
          <img src={logo} alt="logo" className="services-navbar-logo" />
          <span className="services-navbar-name">BantayKalusugan</span>
        </div>

        <div className="services-navbar-links">
          <Link to="/"         className="services-navbar-link">Home</Link>
          <Link to="/services" className="services-navbar-link services-navbar-link--active">Services</Link>
          <Link to="/aboutus"    className="services-navbar-link">About Us</Link>
          <button onClick={() => navigate("/login")} className="services-navbar-btn">
            Log In
          </button>
        </div>

        <button className="services-navbar-hamburger" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </nav>

      {menuOpen && (
        <div className="services-navbar-mobile">
          {[["Home", "/"], ["Services", "/services"], ["About Us", "/about"]].map(([label, path]) => (
            <Link
              key={label}
              to={path}
              onClick={() => setMenuOpen(false)}
              className="services-navbar-mobile-link"
            >
              {label}
            </Link>
          ))}
          <button onClick={() => navigate("/login")} className="services-navbar-mobile-btn">
            Log In
          </button>
        </div>
      )}
    </>
  );
}

// ── Footer ────────────────────────────────────────────────────────────────────
function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-grid">

          {/* Brand Column */}
          <div className="footer-brand">
                <div className="footer-brand-logo">
                        <img src={logo} alt="logo" style={{ width: "24px", height: "24px", objectFit: "contain" }} />
                    <div className="footer-brand-name">
                        <span className="brand-primary">Bantay</span>
                        <span className="brand-accent">Kalusugan</span>
                    </div>
                </div>
                <p className="footer-brand-desc">
                    A web-based patient monitoring platform for barangay-level health
                    data management and community wellness tracking.
                </p>
          </div>

          {/* Our Services Column */}
          <div>
            <p className="footer-col-title">Our Services</p>
            <ul className="footer-link-list">
              {["Blood Pressure Monitoring", "Health Record Management", "Health Trend Analysis"].map((l) => (
                <li key={l}><a href="#">{l}</a></li>
              ))}
            </ul>
          </div>

          {/* Quick Links Column */}
          <div>
            <p className="footer-col-title">Quick Links</p>
            <ul className="footer-link-list">
              {["Home", "Services", "About Us", "Contact"].map((l) => (
                <li key={l}><a href="#">{l}</a></li>
              ))}
            </ul>
          </div>

          {/* Contact Column */}
          <div>
            <p className="footer-col-title">Contact Us</p>
            <ul className="footer-contact-list">
              <li className="footer-contact-item">
                <MapPin size={15} className="footer-contact-icon" />
                <span className="footer-contact-text">
                  Barangay Health Center,<br />Sample Barangay, City, Philippines
                </span>
              </li>
              <li className="footer-contact-item">
                <Phone size={15} className="footer-contact-icon" />
                <span className="footer-contact-text">+63 912 345 6789</span>
              </li>
              <li className="footer-contact-item">
                <Mail size={15} className="footer-contact-icon" />
                <span className="footer-contact-text">info@bantaykalusugan.ph</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Divider + Copyright */}
        <div className="footer-divider">
          <p className="footer-copyright">
            © {new Date().getFullYear()} BantayKalusugan. All rights reserved.
          </p>
          <div className="footer-bottom-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

// ── Services Page ─────────────────────────────────────────────────────────────
export function Services() {
  return (
    <div className="services-page">
      <Navbar />

      {/* ── HERO ── */}
      <section className="services-hero">
        <div className="services-hero-decorative-circle-right" />
        <div className="services-hero-decorative-circle-left" />
        <div className="services-hero-content">
          <div className="services-hero-badge">
            <Zap size={14} />
            <span>Platform Services</span>
          </div>
          <h1 className="services-hero-heading">
            Everything Your Barangay Needs
            <span className="services-hero-heading-highlight"> for Better Health</span>
          </h1>
          <p className="services-hero-description">
            BantayKalusugan offers a complete suite of health monitoring and management tools —
            designed specifically for barangay-level healthcare operations in the Philippines.
          </p>
          <div className="services-hero-benefits">
            {benefits.map((b) => (
              <div key={b.label} className="services-hero-benefit-pill">
                <span style={{ color: b.color }}>{b.icon}</span>
                {b.label}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CORE SERVICES ── */}
      <section className="services-core-section">
        <div className="services-core-header">
          <span className="services-section-tag services-core-tag">Core Services</span>
          <h2 className="services-section-heading">
            The Heart of <span className="services-section-heading-highlight">BantayKalusugan</span>
          </h2>
          <p className="services-section-description">
            Three flagship services that form the foundation of barangay digital health monitoring.
          </p>
        </div>

        <div className="services-core-list">
          {coreServices.map((service) => (
            <div
              key={service.title}
              className={`services-core-item${service.reverse ? " services-core-item-reverse" : ""}`}
            >
              <div className="services-core-image-wrapper">
                <img
                  src={service.image}
                  alt={service.title}
                  className="services-core-image"
                  onError={(e) => { e.target.style.backgroundColor = "#e5e7eb"; e.target.src = ""; }}
                />
              </div>

              <div className="services-core-content">
                <div
                  className="services-core-icon-wrapper"
                  style={{ backgroundColor: service.iconBg, color: service.color }}
                >
                  {service.icon}
                </div>
                <span
                  className="services-core-tagline"
                  style={{ backgroundColor: service.iconBg, color: service.color }}
                >
                  {service.tagline}
                </span>
                <h3 className="services-core-title">{service.title}</h3>
                <p className="services-core-description">{service.description}</p>
                <div className="services-core-features">
                  {service.features.map((f) => (
                    <div key={f} className="services-core-feature">
                      <CheckCircle size={14} className="services-core-feature-icon" style={{ color: service.color }} />
                      <span className="services-core-feature-text">{f}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── ADDITIONAL SERVICES ── */}
      <section className="services-additional-section">
        <div className="services-additional-header">
          <span className="services-section-tag services-additional-tag">Additional Features</span>
          <h2 className="services-section-heading">
            More Tools to{" "}
            <span className="services-additional-heading-highlight">Support Your Work</span>
          </h2>
        </div>

        <div className="services-additional-grid">
          {additionalServices.map((s) => (
            <div key={s.title} className="services-additional-card">
              <div
                className="services-additional-icon"
                style={{ backgroundColor: s.iconBg, color: s.color }}
              >
                {s.icon}
              </div>
              <h4 className="services-additional-title">{s.title}</h4>
              <p className="services-additional-description">{s.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="services-cta-section">
        <div className="services-cta-content">
          <h2 className="services-cta-heading">
            Ready to Digitize Your
            <span className="services-cta-heading-highlight"> Barangay&apos;s Health System?</span>
          </h2>
          <p className="services-cta-description">
            Join 500+ patients and 62+ BHWs already experiencing better community health
            management through BantayKalusugan.
          </p>
          <div className="services-cta-buttons">
            <Link to="/register" className="services-cta-button-primary">
              Get Started Free
            </Link>
            <Link to="/aboutus" className="services-cta-button-secondary">
              Learn About Us <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
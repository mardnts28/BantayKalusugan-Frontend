import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Shield, Heart, Users, Target, Eye, Award, CheckCircle,
  ArrowRight, Activity, Globe, Lightbulb, TrendingUp,
  MapPin, Phone, Mail, Menu, X,
} from "lucide-react";
import logo from "./assets/logo.png";
import "./AboutUs.css";

// ── Images ────────────────────────────────────────────────────────────────────
const teamImage =
  "https://images.unsplash.com/photo-1653508311277-1ecf6ee52c5e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080";
const clinicImage =
  "https://images.unsplash.com/photo-1759860002248-356d31d06195?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1080";

// ── Static Data ───────────────────────────────────────────────────────────────
const stats = [
  { value: "500+",   label: "Patients Registered", icon: <Users    size={18} /> },
  { value: "4,800+", label: "Vital Records Logged", icon: <Activity size={18} /> },
  { value: "15+",    label: "Barangays Served",      icon: <Globe    size={18} /> },
  { value: "62",     label: "Active BHWs",           icon: <Heart    size={18} /> },
];

const values = [
  { icon: <Shield     size={20} />, title: "Integrity",   description: "We are committed to honest, transparent management of community health data — safeguarding patient privacy and ensuring accurate, reliable records at every level.",  iconBg: "rgba(46,88,149,0.1)",   iconColor: "#2E5895" },
  { icon: <Heart      size={20} />, title: "Compassion",  description: "Every feature of BantayKalusugan is built with the patient in mind — making healthcare more accessible, understandable, and personal for each community member.",  iconBg: "rgba(194,59,33,0.1)",   iconColor: "#C23B21" },
  { icon: <Lightbulb  size={20} />, title: "Innovation",  description: "We embrace digital technology to replace inefficient paper-based methods, turning raw health data into actionable insights for barangay health management.",       iconBg: "rgba(255,195,43,0.15)", iconColor: "#b8820a" },
  { icon: <Users      size={20} />, title: "Community",   description: "BantayKalusugan is built on collaboration — connecting BHWs, barangay administrators, and patients into a unified health monitoring ecosystem.",                   iconBg: "rgba(46,88,149,0.1)",   iconColor: "#2E5895" },
  { icon: <Award      size={20} />, title: "Excellence",  description: "We strive to provide barangay health workers and staff with tools that meet the highest standards of accuracy, usability, and reliability.",                        iconBg: "rgba(194,59,33,0.1)",   iconColor: "#C23B21" },
  { icon: <TrendingUp size={20} />, title: "Progress",    description: "Our platform evolves alongside the healthcare needs of the community — continuously improving to serve every barangay resident better.",                             iconBg: "rgba(255,195,43,0.15)", iconColor: "#b8820a" },
];

const milestones = [
  {
    year: "2026",
    title: "Concept & Idea",
    description: "The idea for BantayKalusugan was born out of observing the challenges BHWs and barangay staff face managing paper health records during community rounds.",
    color: "#2E5895",
  },
  {
    year: "2026",
    title: "Platform Development",
    description: "Development of the core platform began — designing the patient monitoring system, vital signs logging, and secure admin dashboard tailored for barangay use.",
    color: "#C23B21",
  },
  {
    year: "2026",
    title: "Full Deployment",
    description: "Full-scale rollout across 15+ barangays, with 62 active BHWs and 500+ registered patients benefiting from the digitized health monitoring system.",
    color: "#FFC32B",
  },
];

const checklistItems = [
  "Digitizes BHW-collected vital signs data",
  "Enables patients to track their own health records",
  "Empowers admins with analytics and reports",
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
      <nav className={`about-navbar${scrolled ? " about-navbar--scrolled" : ""}`}>
        <div className="about-navbar-brand">
          <img src={logo} alt="logo" className="about-navbar-logo" />
          <span className="about-navbar-name">BantayKalusugan</span>
        </div>

        <div className="about-navbar-links">
          <Link to="/"         className="about-navbar-link">Home</Link>
          <Link to="/services" className="about-navbar-link">Services</Link>
          <Link to="/aboutus"    className="about-navbar-link about-navbar-link--active">About Us</Link>
          <button onClick={() => navigate("/login")} className="about-navbar-btn">
            Log In
          </button>
        </div>

        <button className="about-navbar-hamburger" onClick={() => setMenuOpen(!menuOpen)}>
          {menuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </nav>

      {menuOpen && (
        <div className="about-navbar-mobile">
          {[["Home", "/"], ["Services", "/services"], ["About Us", "/about"]].map(([label, path]) => (
            <Link
              key={label}
              to={path}
              onClick={() => setMenuOpen(false)}
              className="about-navbar-mobile-link"
            >
              {label}
            </Link>
          ))}
          <button onClick={() => navigate("/login")} className="about-navbar-mobile-btn">
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

// ── Main Page ─────────────────────────────────────────────────────────────────
export function AboutUs() {
  return (
    <div className="about-page">
      <Navbar />

      {/* ── HERO ── */}
      <section className="about-hero">
        <div className="about-hero-decorative-circle-right" />
        <div className="about-hero-decorative-circle-left" />
        <div className="about-hero-content">
          <div className="about-hero-badge">
            <Shield size={14} />
            <span>About BantayKalusugan</span>
          </div>
          <h1 className="about-hero-heading">
            Built for Barangays,{" "}
            <span className="about-hero-heading-highlight">Powered by Purpose</span>
          </h1>
          <p className="about-hero-description">
            BantayKalusugan is a web-based patient monitoring platform designed to digitize
            and streamline community health management at the barangay level across the Philippines.
          </p>
          <div className="about-hero-cta">
            <Link to="/register" className="about-hero-cta-primary">
              Join the Platform
            </Link>
            <Link to="/services" className="about-hero-cta-secondary">
              Our Services <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section className="about-stats-section">
        <div className="about-stats-grid">
          {stats.map((stat) => (
            <div key={stat.label} className="about-stat-item">
              <div className="about-stat-icon">{stat.icon}</div>
              <div className="about-stat-value">{stat.value}</div>
              <div className="about-stat-label">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── OUR STORY ── */}
      <section className="about-story-section">
        <div className="about-story-grid">
          <div className="about-story-image-wrapper">
            <div className="about-story-image-rounded">
              <img
                src={teamImage}
                alt="BantayKalusugan community healthcare"
                onError={(e) => { e.target.style.backgroundColor = "#e5e7eb"; e.target.src = ""; }}
              />
            </div>
            <div className="about-story-image-badge">
              <div className="about-story-badge-year">Est. 2023</div>
              <div className="about-story-badge-text">Serving Filipino communities since inception</div>
            </div>
          </div>

          <div>
            <span className="about-section-tag">Our Story</span>
            <h2 className="about-section-heading">
              From Paper Logbooks to{" "}
              <span className="about-section-heading-highlight">Digital Health Records</span>
            </h2>
            <p className="about-story-paragraph">
              BantayKalusugan was born out of a real challenge observed in barangay-level healthcare
              across the Philippines. Barangay Health Workers (BHWs) and local health staff were
              spending valuable time managing rows of paper logbooks, manually transcribing vital signs,
              and trying to track hundreds of patients with limited resources.
            </p>
            <p className="about-story-paragraph">
              The result? Missed records, data inconsistencies, and delayed interventions for at-risk
              community members. We knew there had to be a better way — one that respected the reality
              of barangay resources while still delivering the power of modern digital health management.
            </p>
            <p className="about-story-paragraph">
              BantayKalusugan was developed as a web-based platform that serves as the digital backbone
              of barangay health operations — connecting BHWs, administrators, and patients in one
              organized, accessible system.
            </p>
            <ul className="about-story-checklist">
              {checklistItems.map((item) => (
                <li key={item} className="about-story-checklist-item">
                  <CheckCircle size={16} className="about-story-checklist-icon" />
                  <span className="about-story-checklist-text">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* ── MISSION & VISION ── */}
      <section className="about-mission-vision-section">
        <div className="about-mission-vision-header">
          <span className="about-mission-vision-tag">Our Purpose</span>
          <h2 className="about-section-heading">
            Mission &amp; <span className="about-section-heading-highlight">Vision</span>
          </h2>
        </div>

        <div className="about-mission-vision-grid">
          <div className="about-mission-card">
            <div className="about-card-decorative-circle" style={{ backgroundColor: "#2E5895" }} />
            <div className="about-mission-icon"><Target size={24} /></div>
            <h3 className="about-mission-heading">Our Mission</h3>
            <p className="about-card-description">
              To provide barangay-level health workers and administrators with an accessible,
              efficient, and reliable web-based platform that digitizes patient health monitoring —
              enabling better health outcomes for Filipino communities through organized data
              management and real-time health tracking.
            </p>
            <div className="about-card-footer about-mission-footer">
              <p className="about-card-quote">
                &ldquo;Empowering every barangay to protect and monitor the health of its community.&rdquo;
              </p>
            </div>
          </div>

          <div className="about-vision-card">
            <div className="about-card-decorative-circle" style={{ backgroundColor: "#FFC32B" }} />
            <div className="about-vision-icon"><Eye size={24} /></div>
            <h3 className="about-vision-heading">Our Vision</h3>
            <p className="about-card-description">
              A Philippines where every barangay operates a fully digitized, BHW-supported health
              monitoring system — where no patient record is lost, no health risk goes undetected,
              and every community member has transparent access to their own health journey through
              BantayKalusugan.
            </p>
            <div className="about-card-footer about-vision-footer">
              <p className="about-card-quote">
                &ldquo;A healthier Philippines, one barangay at a time.&rdquo;
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── CORE VALUES ── */}
      <section className="about-values-section">
        <div className="about-values-header">
          <span className="about-section-tag">What We Stand For</span>
          <h2 className="about-section-heading">
            Our Core <span className="about-section-heading-highlight">Values</span>
          </h2>
          <p className="about-team-header-description">
            The principles that guide every decision we make in building and operating BantayKalusugan.
          </p>
        </div>

        <div className="about-values-grid">
          {values.map((val) => (
            <div key={val.title} className="about-value-card">
              <div
                className="about-value-icon"
                style={{ backgroundColor: val.iconBg, color: val.iconColor }}
              >
                {val.icon}
              </div>
              <h3 className="about-value-title">{val.title}</h3>
              <p className="about-value-description">{val.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── TIMELINE ── */}
      <section className="about-timeline-section">
        <div className="about-timeline-grid">
          <div>
            <span className="about-section-tag about-timeline-content-tag">Our Journey</span>
            <h2 className="about-section-heading">
              How We Got{" "}
              <span className="about-timeline-content-heading-highlight">Here</span>
            </h2>
            <p className="about-story-paragraph">
              From identifying the problem in barangay health operations to deploying a full-scale
              platform — here&apos;s a look at the BantayKalusugan journey.
            </p>

            <div className="about-timeline-wrapper">
              <div className="about-timeline-line" />
              <ul className="about-timeline-list">
                {milestones.map((m) => (
                  <li key={m.year} className="about-timeline-item">
                    <div
                      className="about-timeline-year-badge"
                      style={{ backgroundColor: m.color }}
                    >
                      {m.year.slice(2)}
                    </div>
                    <div>
                      <div className="about-timeline-item-header">
                        <span
                          className="about-timeline-year-pill"
                          style={{ backgroundColor: m.color }}
                        >
                          {m.year}
                        </span>
                        <span className="about-timeline-item-title">{m.title}</span>
                      </div>
                      <p className="about-timeline-item-description">{m.description}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="about-timeline-image">
            <img
              src={clinicImage}
              alt="Barangay health mission"
              onError={(e) => { e.target.style.backgroundColor = "#e5e7eb"; e.target.src = ""; }}
            />
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="about-cta-section">
        <div className="about-cta-content">
          <div className="about-cta-icon-wrapper">
            <Heart size={28} color="#FFC32B" />
          </div>
          <h2 className="about-cta-heading">
            Be Part of the{" "}
            <span className="about-cta-heading-highlight">BantayKalusugan</span>{" "}
            Community
          </h2>
          <p className="about-cta-description">
            Join hundreds of patients and barangay health workers already benefiting from
            digitized community health monitoring across the Philippines.
          </p>
          <div className="about-cta-buttons">
            <Link to="/register" className="about-cta-button-primary">
              Register as Patient
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
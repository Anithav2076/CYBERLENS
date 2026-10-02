import { useEffect, useState } from "react";
import axios from "axios";
import {
  ShieldCheck,
  LayoutDashboard,
  Server,
  History,
  ShieldAlert,
  Activity,
  AlertTriangle,
  CircleCheck,
  RefreshCw,
  Monitor,
  ArrowLeft,
  Search,
  Lightbulb,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [currentPage, setCurrentPage] = useState("dashboard");

  const [stats, setStats] = useState(null);
  const [systems, setSystems] = useState([]);

  const [selectedSystem, setSelectedSystem] = useState(null);
  const [riskDetails, setRiskDetails] = useState(null);

  const [loading, setLoading] = useState(true);
  const [systemsLoading, setSystemsLoading] = useState(false);
  const [riskDetailsLoading, setRiskDetailsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const [error, setError] = useState("");

  // Mitigation simulation
  const [selectedMitigation, setSelectedMitigation] = useState("");
  const [mitigationResult, setMitigationResult] = useState(null);
  const [mitigationLoading, setMitigationLoading] = useState(false);

  // Mitigation prioritization
  const [prioritizedMitigations, setPrioritizedMitigations] = useState([]);
  const [prioritizationLoading, setPrioritizationLoading] = useState(false);

  // ============================================================
  // LOAD DASHBOARD STATISTICS
  // ============================================================

  const loadDashboardStats = async () => {
    try {
      setError("");
      const response = await axios.get(
  `${API_URL}/dashboard-stats`
);

const data = response.data;

setStats({
  total_assessments: data.total_assessments ?? 0,

  risk_distribution: {
    critical: data.risk_distribution?.critical ?? 0,
    high: data.risk_distribution?.high ?? 0,
    medium: data.risk_distribution?.medium ?? 0,
    low: data.risk_distribution?.low ?? 0,
  },

  average_risk:
    data.risk_statistics?.average_risk ?? 0,

  highest_risk:
    data.risk_statistics?.highest_risk ?? 0,

  lowest_risk:
    data.risk_statistics?.lowest_risk ?? 0,
});

setStats({
  ...data,
  average_risk:
    data.average_risk ??
    data.risk_statistics?.average_risk ??
    0,
  highest_risk:
    data.highest_risk ??
    data.risk_statistics?.highest_risk ??
    0,
  lowest_risk:
    data.lowest_risk ??
    data.risk_statistics?.lowest_risk ??
    0,
});

    } catch (err) {
      console.error("Dashboard API error:", err);

      setError(
        "Unable to connect to the FastAPI backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // LOAD SYSTEMS
  // ============================================================

  const loadSystems = async () => {
    try {
      setSystemsLoading(true);
      setError("");

      const response = await axios.get(
        `${API_URL}/systems`
      );

      setSystems(response.data.systems || []);
    } catch (err) {
      console.error("Systems API error:", err);

      setError(
        "Unable to load registered systems."
      );
    } finally {
      setSystemsLoading(false);
    }
  };

  // ============================================================
  // LOAD SYSTEM RISK DETAILS
  // ============================================================

  const loadRiskDetails = async (systemId) => {
    try {
      setRiskDetailsLoading(true);
      setError("");

      const response = await axios.get(
        `${API_URL}/systems/${systemId}/risk`
      );

      setRiskDetails(response.data);
    } catch (err) {
      console.error("Risk details API error:", err);

      setError(
        "Unable to load risk details for this system."
      );
    } finally {
      setRiskDetailsLoading(false);
    }
  };

  // ============================================================
  // SIMULATE MITIGATION
  // ============================================================

  const simulateMitigation = async () => {
    if (!selectedMitigation || !selectedSystem) {
      setError("Please select a mitigation first.");
      return;
    }

    try {
      setMitigationLoading(true);
      setError("");
      setMitigationResult(null);

      const observationResponse = await axios.get(
        `${API_URL}/systems/${selectedSystem.system_id}/observation`
      );

      const observation = observationResponse.data.observation;

      const response = await axios.post(
        `${API_URL}/simulate-mitigation`,
        {
          system_id: selectedSystem.system_id,
          observation,
          feature: selectedMitigation,
        }
      );

      setMitigationResult(response.data);
    } catch (err) {
      console.error("Mitigation simulation error:", err);
      setError(
        err.response?.data?.detail ||
        "Unable to simulate mitigation."
      );
    } finally {
      setMitigationLoading(false);
    }
  };

  // ============================================================
  // PRIORITIZE MITIGATIONS
  // ============================================================

  const loadMitigationPriorities = async () => {
    if (!selectedSystem) {
      setError("No system selected.");
      return;
    }

    try {
      setPrioritizationLoading(true);
      setError("");

      const observationResponse = await axios.get(
        `${API_URL}/systems/${selectedSystem.system_id}/observation`
      );

      const observation = observationResponse.data.observation;

      const response = await axios.post(
        `${API_URL}/prioritize-mitigations`,
        {
          system_id: selectedSystem.system_id,
          observation,
        }
      );

      setPrioritizedMitigations(
        response.data.prioritized_mitigations || []
      );
    } catch (err) {
      console.error("Mitigation prioritization error:", err);
      setError(
        err.response?.data?.detail ||
        "Unable to prioritize mitigations."
      );
    } finally {
      setPrioritizationLoading(false);
    }
  };

  // ============================================================
  // OPEN SYSTEM DETAILS
  // ============================================================

  const handleSystemClick = async (system) => {
    setSelectedSystem(system);
    setRiskDetails(null);
    setSelectedMitigation("");
    setMitigationResult(null);
    setPrioritizedMitigations([]);
    setCurrentPage("risk-details");

    await loadRiskDetails(system.system_id);
  };

  // ============================================================
  // BACK TO SYSTEMS
  // ============================================================

  const handleBackToSystems = () => {
    setSelectedSystem(null);
    setRiskDetails(null);
    setSelectedMitigation("");
    setMitigationResult(null);
    setPrioritizedMitigations([]);
    setCurrentPage("systems");
    setError("");
  };

  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {
    const loadInitialData = async () => {
      await loadDashboardStats();
    };

    loadInitialData();
  }, []);

  // ============================================================
  // PAGE NAVIGATION
  // ============================================================

  const handlePageChange = (page) => {
    setCurrentPage(page);
    setError("");

    if (page === "dashboard") {
      setSelectedSystem(null);
      setRiskDetails(null);
      setSelectedMitigation("");
      setMitigationResult(null);
      setPrioritizedMitigations([]);
    }

    if (page === "systems") {
      setSelectedSystem(null);
      setRiskDetails(null);
      setSelectedMitigation("");
      setMitigationResult(null);
      setPrioritizedMitigations([]);
      loadSystems();
    }
  };

  // ============================================================
  // REFRESH
  // ============================================================

  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      setError("");

      if (currentPage === "dashboard") {
        await loadDashboardStats();
      }

      if (currentPage === "systems") {
        await loadSystems();
      }

      if (
        currentPage === "risk-details" &&
        selectedSystem
      ) {
        await loadRiskDetails(
          selectedSystem.system_id
        );
      }
    } finally {
      setRefreshing(false);
    }
  };

  // ============================================================
  // RISK PERCENTAGE
  // ============================================================

  const getRiskPercentage = (riskCount) => {
    if (!stats || !stats.total_assessments) {
      return 0;
    }

    return (
      (riskCount / stats.total_assessments) * 100
    );
  };

  // ============================================================
  // RISK BADGE
  // ============================================================

  const getRiskClass = (riskLevel) => {
    switch (riskLevel) {
      case "CRITICAL":
        return "risk-badge critical-badge";

      case "HIGH":
        return "risk-badge high-badge";

      case "MEDIUM":
        return "risk-badge medium-badge";

      case "LOW":
        return "risk-badge low-badge";

      default:
        return "risk-badge unknown-badge";
    }
  };

  // ============================================================
  // SHAP VALUE FORMAT
  // ============================================================

  const formatShapValue = (value) => {
    const number = Number(value || 0);

    return number >= 0
      ? `+${number.toFixed(4)}`
      : number.toFixed(4);
  };

  // ============================================================
  // LOADING SCREEN
  // ============================================================

  if (loading) {
    return (
      <div className="app">
        <aside className="sidebar">

          <div className="logo-section">

            <div className="logo-icon">
              <ShieldCheck size={28} />
            </div>

            <div>
              <h2>CyberLens</h2>
              <span>CYBER RISK INTELLIGENCE</span>
            </div>

          </div>

          <div className="sidebar-footer">
            <div className="status-dot"></div>

            <span>
              Connecting to backend...
            </span>
          </div>

        </aside>

        <main className="main-content">

          <div className="loading">

            <Activity size={28} />

            <p>
              Loading cybersecurity dashboard...
            </p>

          </div>

        </main>
      </div>
    );
  }

  // ============================================================
  // MAIN APPLICATION
  // ============================================================

  return (
    <div className="app">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        {/* Logo */}

        <div className="logo-section">

          <div className="logo-icon">
            <ShieldCheck size={28} />
          </div>

          <div>
            <h2>CyberLens</h2>

            <span>
              CYBER RISK INTELLIGENCE
            </span>
          </div>

        </div>

        {/* Navigation */}

        <nav className="navigation">

          {/* Dashboard */}

          <div
            className={`nav-item ${
              currentPage === "dashboard"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handlePageChange("dashboard")
            }
          >

            <LayoutDashboard size={20} />

            <span>
              Dashboard
            </span>

          </div>

          {/* Systems */}

          <div
            className={`nav-item ${
              currentPage === "systems" ||
              currentPage === "risk-details"
                ? "active"
                : ""
            }`}
            onClick={() =>
              handlePageChange("systems")
            }
          >

            <Server size={20} />

            <span>
              Systems
            </span>

          </div>

          {/* Future pages */}

          <div className="nav-item">

            <History size={20} />

            <span>
              Risk History
            </span>

          </div>

          <div className="nav-item">

            <ShieldAlert size={20} />

            <span>
              Mitigation
            </span>

          </div>

        </nav>

        {/* Backend status */}

        <div className="sidebar-footer">

          <div className="status-dot"></div>

          <span>
            Backend Connected
          </span>

        </div>

      </aside>


      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <main className="main-content">

        {/* ====================================================
            HEADER
        ==================================================== */}

        <header className="topbar">

          <div>

            <h1>

              {currentPage === "dashboard"
                ? "Cyber Risk Dashboard"
                : currentPage === "systems"
                ? "Registered Systems"
                : "System Risk Details"}

            </h1>

            <p>

              {currentPage === "dashboard"
                ? "AI-powered cybersecurity risk assessment and decision support"
                : currentPage === "systems"
                ? "Authorized endpoint systems monitored by the platform"
                : selectedSystem
                ? `Detailed AI risk analysis for ${selectedSystem.system_id}`
                : "System risk analysis"}

            </p>

          </div>

          <button
            className="refresh-button"
            onClick={handleRefresh}
            disabled={refreshing}
          >

            <RefreshCw
              size={17}
              className={
                refreshing
                  ? "refresh-spin"
                  : ""
              }
            />

            {refreshing
              ? "Refreshing..."
              : "Refresh"}

          </button>

        </header>


        {/* ====================================================
            ERROR
        ==================================================== */}

        {error && (

          <div className="error-box">

            <AlertTriangle size={20} />

            <span>
              {error}
            </span>

          </div>

        )}


        {/* ====================================================
            DASHBOARD PAGE
        ==================================================== */}

        {currentPage === "dashboard" &&
          stats && (

          <>

            {/* STAT CARDS */}

            <section className="stats-grid">

              {/* Total */}

              <div className="stat-card">

                <div className="stat-icon">
                  <Activity size={24} />
                </div>

                <div>

                  <p>
                    Total Assessments
                  </p>

                  <h2>
                    {stats.total_assessments ?? 0}
                  </h2>

                </div>

              </div>


              {/* Critical */}

              <div className="stat-card critical-card">

                <div className="stat-icon">
                  <ShieldAlert size={24} />
                </div>

                <div>

                  <p>
                    Critical Risk
                  </p>

                  <h2>
                    {stats.risk_distribution?.critical ?? 0}
                  </h2>

                </div>

              </div>


              {/* High */}

              <div className="stat-card high-card">

                <div className="stat-icon">
                  <AlertTriangle size={24} />
                </div>

                <div>

                  <p>
                    High Risk
                  </p>

                  <h2>
                    {stats.risk_distribution?.high ?? 0}
                  </h2>

                </div>

              </div>


              {/* Average */}

              <div className="stat-card">

                <div className="stat-icon">
                  <CircleCheck size={24} />
                </div>

                <div>

                  <p>
                    Average Risk
                  </p>

                  <h2>
                    {Number(
                      stats.average_risk ?? 0
                    ).toFixed(2)}
                  </h2>

                  <span className="score-label">
                    / 100
                  </span>

                </div>

              </div>

            </section>


            {/* RISK OVERVIEW */}

            <section className="content-grid">

              <div className="panel">

                <div className="panel-header">

                  <div>

                    <h2>
                      Risk Overview
                    </h2>

                    <p>
                      Current assessment distribution
                    </p>

                  </div>

                  <ShieldCheck size={24} />

                </div>


                <div className="risk-list">

                  {/* Critical */}

                  <div className="risk-row">

                    <span>
                      Critical
                    </span>

                    <strong>
                      {stats.risk_distribution?.critical ?? 0}
                    </strong>

                  </div>

                  <div className="risk-bar">

                    <div
                      className="risk-fill critical-fill"
                      style={{
                        width: `${getRiskPercentage(
                          stats.risk_distribution?.critical ?? 0
                        )}%`,
                      }}
                    ></div>

                  </div>


                  {/* High */}

                  <div className="risk-row">

                    <span>
                      High
                    </span>

                    <strong>
                      {stats.risk_distribution?.high ?? 0}
                    </strong>

                  </div>

                  <div className="risk-bar">

                    <div
                      className="risk-fill high-fill"
                      style={{
                        width: `${getRiskPercentage(
                          stats.risk_distribution?.high ?? 0
                        )}%`,
                      }}
                    ></div>

                  </div>


                  {/* Medium */}

                  <div className="risk-row">

                    <span>
                      Medium
                    </span>

                    <strong>
                      {stats.risk_distribution?.medium ?? 0}
                    </strong>

                  </div>

                  <div className="risk-bar">

                    <div
                      className="risk-fill medium-fill"
                      style={{
                        width: `${getRiskPercentage(
                          stats.risk_distribution?.medium ?? 0
                        )}%`,
                      }}
                    ></div>

                  </div>


                  {/* Low */}

                  <div className="risk-row">

                    <span>
                      Low
                    </span>

                    <strong>
                      {stats.risk_distribution?.low ?? 0}
                    </strong>

                  </div>

                  <div className="risk-bar">

                    <div
                      className="risk-fill low-fill"
                      style={{
                        width: `${getRiskPercentage(
                          stats.risk_distribution?.low ?? 0
                        )}%`,
                      }}
                    ></div>

                  </div>

                </div>

              </div>


              {/* RISK STATISTICS */}

              <div className="panel">

                <div className="panel-header">

                  <div>

                    <h2>
                      Risk Statistics
                    </h2>

                    <p>
                      Assessment score summary
                    </p>

                  </div>

                  <Activity size={24} />

                </div>


                <div className="big-score">

                  <span>
                    Highest Risk
                  </span>

                  <strong>
                    {Number(
                      stats.highest_risk ?? 0
                    ).toFixed(2)}
                  </strong>

                  <small>
                    / 100
                  </small>

                </div>


                <div className="divider"></div>


                <div className="score-row">

                  <span>
                    Lowest Risk
                  </span>

                  <strong>
                    {Number(
                      stats.lowest_risk ?? 0
                    ).toFixed(2)}
                  </strong>

                </div>


                <div className="score-row">

                  <span>
                    Average Risk
                  </span>

                  <strong>
                    {Number(
                      stats.average_risk ?? 0
                    ).toFixed(2)}
                  </strong>

                </div>

              </div>

            </section>


            {/* ASSESSMENT SUMMARY */}

            <section className="panel system-panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Assessment Summary
                  </h2>

                  <p>
                    Latest cybersecurity assessment statistics
                  </p>

                </div>

                <Server size={24} />

              </div>


              <div className="assessment-summary">

                <div>

                  <span>
                    Total Assessments
                  </span>

                  <strong>
                    {stats.total_assessments ?? 0}
                  </strong>

                </div>


                <div>

                  <span>
                    Critical Assessments
                  </span>

                  <strong className="critical-text">

                    {stats.risk_distribution?.critical ?? 0}

                  </strong>

                </div>


                <div>

                  <span>
                    High Risk Assessments
                  </span>

                  <strong className="high-text">

                    {stats.risk_distribution?.high ?? 0}

                  </strong>

                </div>

              </div>

            </section>

          </>

        )}


        {/* ====================================================
            SYSTEMS PAGE
        ==================================================== */}

        {currentPage === "systems" && (

          <section className="panel systems-panel">

            <div className="panel-header">

              <div>

                <h2>
                  Registered Endpoint Systems
                </h2>

                <p>
                  Systems registered with the AI Cyber Risk platform
                </p>

              </div>

              <Monitor size={24} />

            </div>


            {/* Loading */}

            {systemsLoading && (

              <div className="loading">

                <Activity size={24} />

                <p>
                  Loading systems...
                </p>

              </div>

            )}


            {/* No systems */}

            {!systemsLoading &&
              systems.length === 0 && (

              <div className="empty-state">

                <Server size={40} />

                <h3>
                  No systems registered
                </h3>

                <p>
                  Register an authorized endpoint
                  to begin risk assessment.
                </p>

              </div>

            )}


            {/* Systems table */}

            {!systemsLoading &&
              systems.length > 0 && (

              <div className="systems-table-container">

                <table className="systems-table">

                  <thead>

                    <tr>

                      <th>
                        System
                      </th>

                      <th>
                        Hostname
                      </th>

                      <th>
                        Operating System
                      </th>

                      <th>
                        Agent
                      </th>

                      <th>
                        Risk Score
                      </th>

                      <th>
                        Risk Level
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {systems.map((system) => (

                      <tr
                        key={system.system_id}
                        className="system-row"
                        onClick={() =>
                          handleSystemClick(system)
                        }
                        title="Click to view risk details"
                      >

                        {/* System */}

                        <td>

                          <div className="system-name">

                            <div className="system-icon">
                              <Monitor size={18} />
                            </div>

                            <div>

                              <strong>
                                {system.system_id}
                              </strong>

                            </div>

                          </div>

                        </td>


                        {/* Hostname */}

                        <td>
                          {system.hostname}
                        </td>


                        {/* OS */}

                        <td>
                          {system.operating_system}
                        </td>


                        {/* Agent */}

                        <td>
                          {system.agent_version}
                        </td>


                        {/* Risk score */}

                        <td>

                          <strong>

                            {Number(
                              system.latest_risk?.risk_score ?? 0
                            ).toFixed(2)}

                          </strong>

                        </td>


                        {/* Risk level */}

                        <td>

                          <span
                            className={getRiskClass(
                              system.latest_risk?.risk_level
                            )}
                          >

                            {system.latest_risk?.risk_level ??
                              "UNKNOWN"}

                          </span>

                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            )}

          </section>

        )}


        {/* ====================================================
            RISK DETAILS PAGE
        ==================================================== */}

        {currentPage === "risk-details" && (

          <section className="risk-details-page">

            {/* Back button */}

            <button
              className="back-button"
              onClick={handleBackToSystems}
            >

              <ArrowLeft size={18} />

              Back to Systems

            </button>


            {riskDetailsLoading && (

              <div className="loading">

                <Activity size={28} />

                <p>
                  Loading AI risk analysis...
                </p>

              </div>

            )}


            {!riskDetailsLoading &&
              riskDetails && (

              <>

                {/* ==================================================
                    RISK OVERVIEW
                ================================================== */}

                <section className="risk-detail-grid">

                  {/* Risk Score */}

                  <div className="risk-detail-card">

                    <div className="detail-icon">
                      <ShieldAlert size={24} />
                    </div>

                    <span>
                      Risk Score
                    </span>

                    <strong className="risk-score-large">

                      {Number(
                        riskDetails.risk_assessment?.risk_score ?? 0
                      ).toFixed(2)}

                    </strong>

                    <small>
                      / 100
                    </small>

                  </div>


                  {/* Risk Level */}

                  <div className="risk-detail-card">

                    <div className="detail-icon">
                      <AlertTriangle size={24} />
                    </div>

                    <span>
                      Risk Level
                    </span>

                    <div>

                      <span
                        className={getRiskClass(
                          riskDetails.risk_assessment?.risk_level
                        )}
                      >

                        {riskDetails.risk_assessment?.risk_level ??
                          "UNKNOWN"}

                      </span>

                    </div>

                  </div>


                  {/* Attack Probability */}

                  <div className="risk-detail-card">

                    <div className="detail-icon">
                      <Activity size={24} />
                    </div>

                    <span>
                      Attack Probability
                    </span>

                    <strong className="risk-score-large">

                      {(
                        Number(
                          riskDetails.risk_assessment
                            ?.attack_probability ?? 0
                        ) * 100
                      ).toFixed(2)}

                      %

                    </strong>

                  </div>

                </section>


                {/* ==================================================
                    SHAP EXPLANATION
                ================================================== */}

                <section className="panel">

                  <div className="panel-header">

                    <div>

                      <h2>
                        AI Risk Explanation
                      </h2>

                      <p>
                        Features contributing to the model's risk prediction
                      </p>

                    </div>

                    <Search size={24} />

                  </div>


                  <div className="shap-list">

                    {riskDetails.shap_explanations?.map(
                      (item, index) => (

                      <div
                        className="shap-item"
                        key={`${item.feature}-${index}`}
                      >

                        <div className="shap-main">

                          <strong>
                            {item.feature}
                          </strong>

                          <span>
                            Feature value:{" "}
                            {Number(
                              item.feature_value ?? 0
                            ).toLocaleString()}
                          </span>

                        </div>


                        <div
                          className={
                            Number(item.shap_value) >= 0
                              ? "shap-positive"
                              : "shap-negative"
                          }
                        >

                          {formatShapValue(
                            item.shap_value
                          )}

                        </div>

                      </div>

                    ))}

                  </div>


                  <div className="shap-note">

                    <AlertTriangle size={17} />

                    <span>
                      SHAP values explain how each feature
                      influenced the model prediction. They
                      represent model contribution, not proof
                      of causality.
                    </span>

                  </div>

                </section>


                {/* ==================================================
                    RECOMMENDATIONS
                ================================================== */}

                <section className="panel">

                  <div className="panel-header">

                    <div>

                      <h2>
                        Security Recommendations
                      </h2>

                      <p>
                        AI-generated investigation and mitigation guidance
                      </p>

                    </div>

                    <Lightbulb size={24} />

                  </div>


                  <div className="recommendation-list">

                    {riskDetails.recommendations?.map(
                      (item, index) => (

                      <div
                        className="recommendation-card"
                        key={`${item.feature}-${index}`}
                      >

                        <div className="recommendation-icon">

                          <ShieldCheck size={20} />

                        </div>

                        <div>

                          <h3>
                            {item.feature}
                          </h3>

                          <p>
                            {item.recommendation}
                          </p>

                          <small>
                            {item.security_rationale}
                          </small>

                          <div className="recommendation-meta">

                            <span>
                              {item.contribution}
                            </span>

                            <span>
                              {item.simulation_change}
                            </span>

                          </div>

                        </div>

                      </div>

                    ))}

                  </div>

                </section>

                {/* ==================================================
                    MITIGATION SIMULATION
                ================================================== */}

                <section className="panel">

                  <div className="panel-header">
                    <div>
                      <h2>Mitigation Simulation</h2>
                      <p>
                        Estimate how a selected mitigation could change the AI risk score
                      </p>
                    </div>
                    <ShieldAlert size={24} />
                  </div>

                  <div className="mitigation-simulation">
                    <div className="mitigation-control">
                      <label htmlFor="mitigation-select">
                        Select Mitigation
                      </label>

                      <select
                        id="mitigation-select"
                        value={selectedMitigation}
                        onChange={(e) => {
                          setSelectedMitigation(e.target.value);
                          setMitigationResult(null);
                        }}
                      >
                        <option value="">
                          Select a feature
                        </option>

                        {riskDetails.recommendations?.map((item, index) => (
                          <option
                            key={`${item.feature}-${index}`}
                            value={item.feature}
                          >
                            Reduce {item.feature} by 20%
                          </option>
                        ))}
                      </select>

                      <button
                        className="simulate-button"
                        onClick={simulateMitigation}
                        disabled={mitigationLoading || !selectedMitigation}
                      >
                        {mitigationLoading
                          ? "Simulating..."
                          : "Simulate Mitigation"}
                      </button>
                    </div>

                    {mitigationResult && (
                      <div className="mitigation-result">
                        <h3>Simulation Result</h3>

                        <div className="mitigation-result-grid">
                          <div>
                            <span>Current Risk</span>
                            <strong>
                              {Number(
                                mitigationResult.current_risk?.risk_score ?? 0
                              ).toFixed(2)}
                            </strong>
                          </div>

                          <div>
                            <span>New Risk</span>
                            <strong>
                              {Number(
                                mitigationResult.mitigation_simulation?.new_risk ?? 0
                              ).toFixed(2)}
                            </strong>
                          </div>

                          <div>
                            <span>Estimated Reduction</span>
                            <strong>
                              {Number(
                                mitigationResult.mitigation_simulation
                                  ?.estimated_reduction ?? 0
                              ).toFixed(2)}
                            </strong>
                          </div>

                          <div>
                            <span>New Risk Level</span>
                            <span
                              className={getRiskClass(
                                mitigationResult.mitigation_simulation
                                  ?.new_risk_level
                              )}
                            >
                              {mitigationResult.mitigation_simulation
                                ?.new_risk_level ?? "UNKNOWN"}
                            </span>
                          </div>
                        </div>

                        <div className="mitigation-rationale">
                          <strong>Security Rationale</strong>
                          <p>
                            {mitigationResult.mitigation_simulation
                              ?.security_rationale}
                          </p>
                          <small>
                            This is a model-based estimate, not a guaranteed real-world risk reduction.
                          </small>
                        </div>
                      </div>
                    )}
                  </div>

                </section>

                {/* ==================================================
                    MITIGATION PRIORITIZATION
                ================================================== */}

                <section className="panel">

                  <div className="panel-header">
                    <div>
                      <h2>Mitigation Prioritization</h2>
                      <p>
                        Compare model-estimated risk reduction and prioritize mitigations
                      </p>
                    </div>
                    <ShieldAlert size={24} />
                  </div>

                  <button
                    className="simulate-button"
                    onClick={loadMitigationPriorities}
                    disabled={prioritizationLoading}
                  >
                    {prioritizationLoading
                      ? "Analyzing Mitigations..."
                      : "Prioritize Mitigations"}
                  </button>

                  {prioritizedMitigations.length > 0 && (
                    <div className="prioritization-list">
                      {prioritizedMitigations.map((item, index) => (
                        <div
                          className="recommendation-card"
                          key={`${item.feature}-${index}`}
                        >
                          <div className="recommendation-icon">
                            <strong>#{item.priority ?? index + 1}</strong>
                          </div>

                          <div>
                            <h3>{item.feature}</h3>
                            <p>{item.mitigation}</p>

                            <div className="recommendation-meta">
                              <span>
                                Risk Reduction: {Number(
                                  item.estimated_reduction ?? 0
                                ).toFixed(2)} points
                              </span>
                              <span>
                                New Risk: {Number(
                                  item.new_risk ?? 0
                                ).toFixed(2)}
                              </span>
                            </div>

                            <small>
                              {item.security_rationale}
                            </small>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {prioritizedMitigations.length === 0 && !prioritizationLoading && (
                    <div className="empty-state">
                      <p>
                        Click &quot;Prioritize Mitigations&quot; to compare available mitigation options.
                      </p>
                    </div>
                  )}

                  {prioritizedMitigations.length > 0 && (
                    <div className="shap-note">
                      <AlertTriangle size={17} />
                      <span>
                        Priorities are based on model-estimated risk reduction. They are decision-support estimates, not guaranteed real-world outcomes.
                      </span>
                    </div>
                  )}

                </section>

              </>

            )}

          </section>

        )}

      </main>

    </div>
  );
}

export default App;
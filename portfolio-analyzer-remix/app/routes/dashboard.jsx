// app/routes/dashboard.jsx
import { useState } from "react";

export default function Dashboard() {
  // Portfolio Analysis State
  const [url, setUrl] = useState("");
  const [urlReport, setUrlReport] = useState(null);
  const [urlError, setUrlError] = useState("");

  // Resume Analysis State
  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeReport, setResumeReport] = useState(null);
  const [resumeError, setResumeError] = useState("");

  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  // Handle portfolio analysis via URL
  const handleAnalyzeUrl = async (e) => {
    e.preventDefault();
    try {
      const payload = JSON.stringify({ url });
      const endpoints = [
        "/portfolio/analyze",   // Metadata & content analysis
        "/portfolio/evaluate",  // AI evaluation (e.g., sentiment, readability)
        "/portfolio/score",     // Dynamic scoring
        "/portfolio/enhance",   // Enhancement suggestions
        "/gamification/gamify", // Gamification level
        "/gamification/career", // Career/job insights
      ];

      const requests = endpoints.map((endpoint) =>
        fetch(window.ENV.API_URL + endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: payload,
        }).then((res) => res.json())
      );

      const results = await Promise.all(requests);
      const aggregatedReport = {
        analysis: results[0],
        evaluation: results[1],
        scoring: results[2],
        enhancements: results[3],
        gamification: results[4],
        career: results[5],
      };

      setUrlReport(aggregatedReport);
      setUrlError("");
    } catch (err) {
      console.error(err);
      setUrlError("An error occurred during URL analysis.");
    }
  };

  // Handle resume analysis via file upload
  const handleAnalyzeResume = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setResumeError("Please select a resume file to upload.");
      return;
    }
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const res = await fetch(window.ENV.API_URL + "/resume/analyze", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
      if (!res.ok) {
        const errData = await res.json();
        setResumeError(errData.detail || "Resume analysis failed");
        return;
      }
      const data = await res.json();
      setResumeReport(data);
      setResumeError("");
    } catch (err) {
      console.error(err);
      setResumeError("An error occurred during resume analysis.");
    }
  };

  return (
    <>
      <style>{`
        /* Global container */
        .dashboard-container {
          background-color: #f5f5f5;
          padding: 2rem;
          font-family: 'Arial, sans-serif';
          min-height: 100vh;
        }
        /* Section card styling */
        .section-card {
          background-color: #fff;
          border-radius: 12px;
          padding: 2rem;
          margin-bottom: 2rem;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        /* Input and button styling */
        .input-field {
          width: 100%;
          padding: 0.75rem;
          margin-bottom: 1rem;
          border: 1px solid #ccc;
          border-radius: 6px;
          font-size: 1rem;
        }
        .action-button {
          background-color: #66a6ff;
          color: #fff;
          border: none;
          border-radius: 6px;
          padding: 0.75rem 1.5rem;
          font-size: 1rem;
          cursor: pointer;
          width: 100%;
          transition: background-color 0.2s ease;
        }
        .action-button:hover {
          background-color: #559de6;
        }
        /* Grid container for report cards */
        .grid-container {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1rem;
          margin-top: 1rem;
        }
        /* Report card styling */
        .report-card {
          border: 1px solid #ccc;
          border-radius: 12px;
          padding: 1rem;
          background: #fafafa;
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .report-card:hover {
          transform: scale(1.02);
          box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .report-heading {
          margin-bottom: 0.5rem;
          color: #333;
          font-size: 1.2rem;
        }
        @media (max-width: 600px) {
          .section-card {
            padding: 1.5rem;
          }
        }
      `}</style>
      <div className="dashboard-container">
        <h2 style={{ marginBottom: "1rem" }}>Dashboard</h2>
        <p>
          Analyze your portfolio by entering a URL or upload your resume (PDF/DOCX) for resume analysis.
        </p>

        {/* Portfolio Analysis Section */}
        <section className="section-card">
          <h3>Analyze Portfolio by URL</h3>
          <form onSubmit={handleAnalyzeUrl}>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="input-field"
              placeholder="Enter portfolio URL"
              required
            />
            <button type="submit" className="action-button">
              Analyze URL
            </button>
          </form>
          {urlError && <p style={{ color: "red", marginTop: "1rem" }}>{urlError}</p>}
          {urlReport && (
            <div style={{ marginTop: "1rem" }}>
              <h4>Aggregated Portfolio Analysis Report</h4>
              <div className="grid-container">
                <div className="report-card">
                  <h5 className="report-heading">📝 Analysis</h5>
                  <p><strong>Title:</strong> {urlReport.analysis.metadata.title}</p>
                  <p><strong>Authors:</strong> {urlReport.analysis.metadata.authors.join(", ") || "N/A"}</p>
                  <p><strong>Publish Date:</strong> {urlReport.analysis.metadata.publish_date}</p>
                  <p><strong>Summary:</strong> {urlReport.analysis.metadata.summary || "N/A"}</p>
                  <p><strong>Content:</strong> {urlReport.analysis.content_analysis}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">🔍 Evaluation</h5>
                  <p>
                    <strong>Sentiment:</strong> {`Neg: ${urlReport.evaluation.sentiment.neg}, Neu: ${urlReport.evaluation.sentiment.neu}, Pos: ${urlReport.evaluation.sentiment.pos}, Compound: ${urlReport.evaluation.sentiment.compound}`}
                  </p>
                  <p><strong>Readability:</strong> {urlReport.evaluation.readability}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">📊 Scoring</h5>
                  <p><strong>Design:</strong> {urlReport.scoring.design}</p>
                  <p><strong>Technical Depth:</strong> {urlReport.scoring.technical_depth}</p>
                  <p><strong>Impact:</strong> {urlReport.scoring.impact}</p>
                  <p><strong>Clarity:</strong> {urlReport.scoring.clarity}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">🚀 Enhancements</h5>
                  <ul>
                    {urlReport.enhancements.suggestions.map((s, index) => (
                      <li key={index}>{s}</li>
                    ))}
                  </ul>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">🎮 Gamification</h5>
                  <p><strong>Level:</strong> {urlReport.gamification.level}</p>
                  <p><strong>Aggregate Score:</strong> {urlReport.gamification.aggregate_score}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">💼 Career Insights</h5>
                  <ul>
                    {urlReport.career.recommendations.map((r, index) => (
                      <li key={index}>{r}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </section>

        <hr style={{ margin: "2rem 0" }} />

        {/* Resume Analysis Section */}
        <section className="section-card">
          <h3>Analyze Resume by File Upload</h3>
          <form onSubmit={handleAnalyzeResume} encType="multipart/form-data">
            <input
              type="file"
              onChange={(e) => setSelectedFile(e.target.files[0])}
              className="input-field"
              required
            />
            <button type="submit" className="action-button">
              Analyze Resume
            </button>
          </form>
          {resumeError && (
            <p style={{ color: "red", marginTop: "1rem" }}>{resumeError}</p>
          )}
          {resumeReport && (
            <div style={{ marginTop: "1rem" }}>
              <h4>Resume Analysis Report</h4>
              <div className="grid-container">
                <div className="report-card">
                  <h5 className="report-heading">📄 Metadata</h5>
                  <p><strong>Filename:</strong> {resumeReport.metadata.filename}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">🗒️ Content Analysis</h5>
                  <p>{resumeReport.content_analysis}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">🔍 Evaluation</h5>
                  <p>
                    <strong>Sentiment:</strong> {`Neg: ${resumeReport.evaluation.sentiment.neg}, Neu: ${resumeReport.evaluation.sentiment.neu}, Pos: ${resumeReport.evaluation.sentiment.pos}, Compound: ${resumeReport.evaluation.sentiment.compound}`}
                  </p>
                  <p><strong>Readability:</strong> {resumeReport.evaluation.readability}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">📊 Scoring</h5>
                  <p><strong>Design:</strong> {resumeReport.scoring.design}</p>
                  <p><strong>Technical Depth:</strong> {resumeReport.scoring.technical_depth}</p>
                  <p><strong>Impact:</strong> {resumeReport.scoring.impact}</p>
                  <p><strong>Clarity:</strong> {resumeReport.scoring.clarity}</p>
                </div>
                <div className="report-card">
                  <h5 className="report-heading">🚀 Enhancements</h5>
                  <ul>
                    {resumeReport.enhancements.suggestions.map((s, index) => (
                      <li key={index}>{s}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </>
  );
}

import React from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-app">
      <h1 className="home-title">AI Engagement Analyst</h1>

      <div className="dashboard-grid">
        <div
          className="dashboard-card"
          onClick={() => navigate("/timeline")}
        >
          <h2>Post Timeline</h2>
          <p>
            Review prioritized posts, analyze engagement patterns,
            and optimize weak-performing content.
          </p>
        </div>

        <div
          className="dashboard-card"
          onClick={() => navigate("/workbench")}
        >
          <h2>Signal Workbench</h2>
          <p>
            Experiment with engagement signals and generate
            structured AI insights for content improvement.
          </p>
        </div>
      </div>
    </div>
  );
}

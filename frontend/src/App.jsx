import "./App.css";
import { useEffect, useState } from "react";
import {
  fetchLinks,
  fetchContentByLink,
  analyzeRaw
} from "./api";

import EngagementChart from "./components/EngagementChart";
import MomentumChart from "./components/MomentumChart";
import InsightCard from "./components/InsightCard";

export default function App() {
  const [links, setLinks] = useState([]);
  const [selectedLink, setSelectedLink] = useState("");
  const [signals, setSignals] = useState(null);
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLinks().then(d => setLinks(d.links || []));
  }, []);

  async function loadSignals(link) {
    setInsight(null);
    const data = await fetchContentByLink(link);
    setSignals(data);
  }

  function update(path, value) {
    setSignals(prev => {
      const next = structuredClone(prev);
      let ref = next;
      path.slice(0, -1).forEach(k => (ref = ref[k]));
      ref[path.at(-1)] = value;
      return next;
    });
  }

  async function analyze() {
    setLoading(true);
    const res = await analyzeRaw(signals);
    setInsight(res.llm_insight);
    setLoading(false);
  }

  return (
    <div className="app">
      <header>
        <h1>Content Insight Engine</h1>
        <p>Edit signals → Generate AI insight → Understand performance</p>
      </header>

      <select
        value={selectedLink}
        onChange={e => {
          setSelectedLink(e.target.value);
          loadSignals(e.target.value);
        }}
      >
        <option value="">Select content link</option>
        {links.map(l => (
          <option key={l}>{l}</option>
        ))}
      </select>

      {signals && (
        <section className="editor">
          <h2>Signal Editor</h2>

          <div className="grid">
            <label>
              Performance Status
              <select
                value={signals.performance_status}
                onChange={e =>
                  update(["performance_status"], e.target.value)
                }
              >
                {["excellent", "good", "average", "poor", "underperforming"].map(v => (
                  <option key={v}>{v}</option>
                ))}
              </select>
            </label>

            <label>
              Engagement Rate
              <input
                type="number"
                step="0.001"
                value={signals.engagement_profile.engagement_rate}
                onChange={e =>
                  update(["engagement_profile", "engagement_rate"], +e.target.value)
                }
              />
            </label>

            <label>
              Retention Rate
              <input
                type="number"
                step="0.001"
                value={signals.engagement_profile.save_rate}
                onChange={e =>
                  update(["engagement_profile", "save_rate"], +e.target.value)
                }
              />
            </label>

            <label>
              Amplification Rate
              <input
                type="number"
                step="0.001"
                value={signals.engagement_profile.share_rate}
                onChange={e =>
                  update(["engagement_profile", "share_rate"], +e.target.value)
                }
              />
            </label>

            <label>
              Primary Interaction
              <select
                value={signals.engagement_profile.dominant_engagement}
                onChange={e =>
                  update(["engagement_profile", "dominant_engagement"], e.target.value)
                }
              >
                {["likes", "shares", "comments", "reposts", "saves"].map(v => (
                  <option key={v}>{v}</option>
                ))}
              </select>
            </label>
          </div>

          <button className="analyze-btn" onClick={analyze}>
            {loading ? "Analyzing..." : "Generate AI Insight"}
          </button>
        </section>
      )}

      {insight && (
        <>
          <section className="insight">
            <InsightCard title="Why it underperformed" value={insight.failure_reason} />
            <InsightCard title="What worked" value={insight.success_driver} />
            <InsightCard title="Recommended actions" list={insight.recommended_actions} />
            <InsightCard
              title="Confidence score"
              value={`${Math.round(insight.confidence_score * 100)}%`}
            />
          </section>

          <section className="charts">
            <EngagementChart engagement={signals.engagement_profile} />
            <MomentumChart engagement={signals.engagement_profile} />
          </section>
        </>
      )}
    </div>
  );
}

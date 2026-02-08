import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function EngagementChart({ engagement }) {
  const data = [
    { name: "Engagement", value: engagement.engagement_rate },
    { name: "Retention", value: engagement.save_rate },
    { name: "Amplification", value: engagement.share_rate }
  ];

  return (
    <div className="chart-card">
      <h3>Engagement Signals</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

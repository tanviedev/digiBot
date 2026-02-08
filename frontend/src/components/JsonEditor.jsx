export default function JsonEditor({ value, onChange }) {
  return (
    <div className="card">
      <h3>Base Engine Input (Editable)</h3>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={18}
        spellCheck={false}
      />
    </div>
  );
}

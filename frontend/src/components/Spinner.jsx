export default function Spinner({ label = "Loading..." }) {
  return (
    <div className="spinner">
      <div className="spinner-circle" />
      <span>{label}</span>
    </div>
  );
}

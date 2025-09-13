// src/components/MachineCard.jsx
import React from "react";

// ساده‌ترین gauge با رنگ‌بندی بر اساس RUL
const getRULColor = (rul) => {
  if (rul < 50) return "red";
  if (rul < 200) return "orange";
  return "green";
};

const MachineCard = ({ machine }) => {
  const {
    machine_id,
    temperature,
    vibration,
    pressure,
    run_hours,
    rul_hours,
    predicted_failure_date,
  } = machine;

  const rulPercent = rul_hours ? Math.min((rul_hours / 1000) * 100, 100) : 0;
  const rulColor = getRULColor(rul_hours);

  return (
    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "16px",
        width: "220px",
        boxShadow: "2px 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      <h3>Machine {machine_id}</h3>
      <p>Temperature: {temperature.toFixed(1)} °C</p>
      <p>Vibration: {vibration.toFixed(2)}</p>
      <p>Pressure: {pressure.toFixed(1)} PSI</p>
      <p>Run Hours: {run_hours}</p>

      <div style={{ marginTop: "10px" }}>
        <p>RUL: {rul_hours ? rul_hours.toFixed(0) : "-"} hours</p>
        <div
          style={{
            background: "#eee",
            borderRadius: "8px",
            height: "16px",
            width: "100%",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${rulPercent}%`,
              background: rulColor,
              height: "100%",
              transition: "width 0.5s ease",
            }}
          ></div>
        </div>
        <small>Predicted Failure: {predicted_failure_date || "-"}</small>
      </div>
    </div>
  );
};

export default MachineCard;

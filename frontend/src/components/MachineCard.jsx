// src/components/MachineGauge.jsx
import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

const MachineGauge = ({ label, value, max = 100, unit = "" }) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100); // محدود کردن 0 تا 100%

  return (
    <div style={{ width: 100, margin: "10px" }}>
      <CircularProgressbar
        value={percentage}
        text={`${value}${unit}`}
        styles={buildStyles({
          textSize: "16px",
          pathColor: "#4caf50",
          textColor: "#333",
          trailColor: "#eee",
        })}
      />
      <div style={{ textAlign: "center", marginTop: 5 }}>{label}</div>
    </div>
  );
};

export default MachineGauge;

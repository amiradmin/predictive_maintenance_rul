// src/components/MachineCardCircular.jsx
import React from "react";
import "./MachineCardCircular.css";

const MachineCardCircular = ({ machine }) => {
  // Safe parsing
  const rul = parseFloat(machine.rul_hours) || 0;
  const temp = parseFloat(machine.temperature) || 0;
  const vib = parseFloat(machine.vibration) || 0;
  const pres = parseFloat(machine.pressure) || 0;

  // درصد برای گِیج‌ها
  const tempPercent = Math.min((temp / 100) * 100, 100);
  const vibPercent = Math.min((vib / 1) * 100, 100);
  const presPercent = Math.min((pres / 100) * 100, 100);
  const rulPercent = Math.min((rul / 1000) * 100, 100);

  // وضعیت RUL
  const getStatus = () => {
    if (rul < 48) return "critical";
    if (rul < 168) return "warning";
    return "normal";
  };
  const status = getStatus();

  return (
    <div className={`machine-card ${status}`}>
      <div className="card-header">
        <h3>Machine {machine.machine_id}</h3>
        <div className={`status-indicator ${status}`}>
          {status.toUpperCase()}
        </div>
      </div>

      <div className="rul-gauge">
        <div className="gauge-container">
          <div className="gauge">
            <div className="gauge-background"></div>
            <div
              className="gauge-fill"
              style={{ transform: `rotate(${rulPercent * 1.8 - 90}deg)` }}
            ></div>
            <div className="gauge-center">
              <span className="rul-value">{rul.toFixed(0)}</span>
              <span className="rul-label">RUL Hours</span>
            </div>
          </div>
        </div>
        <br />
        <h3 className="failure-date">
          Predicted Failure: {machine.predicted_failure_date ?? "N/A"}
        </h3>
      </div>

      <div className="sensor-gauges">
        <div className="sensor-gauge">
          <div className="sensor-title">Temperature</div>
          <div className="sensor-value">{temp.toFixed(1)}°C</div>
          <div className="sensor-visual">
            <div className="gauge-bar">
              <div className="gauge-fill temp" style={{ width: `${tempPercent}%` }}></div>
            </div>
          </div>
        </div>

        <div className="sensor-gauge">
          <div className="sensor-title">Vibration</div>
          <div className="sensor-value">{vib.toFixed(2)}</div>
          <div className="sensor-visual">
            <div className="gauge-bar">
              <div className="gauge-fill vib" style={{ width: `${vibPercent}%` }}></div>
            </div>
          </div>
        </div>

        <div className="sensor-gauge">
          <div className="sensor-title">Pressure</div>
          <div className="sensor-value">{pres.toFixed(1)}</div>
          <div className="sensor-visual">
            <div className="gauge-bar">
              <div className="gauge-fill pres" style={{ width: `${presPercent}%` }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MachineCardCircular;

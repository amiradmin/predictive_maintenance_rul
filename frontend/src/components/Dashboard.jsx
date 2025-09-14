// src/components/Dashboard.jsx
import React, { useState, useEffect } from "react";
import MachineCardCircular from "./MachineCardCircular";

// مقادیر اولیه برای هر ماشین
const initialMachines = [
  { machine_id: 1, temperature: 70, vibration: 0.5, pressure: 30, run_hours: 100, rul_hours: 300 },
  { machine_id: 2, temperature: 68, vibration: 0.6, pressure: 28, run_hours: 200, rul_hours: 400 },
  { machine_id: 3, temperature: 72, vibration: 0.55, pressure: 32, run_hours: 150, rul_hours: 350 },
  { machine_id: 4, temperature: 69, vibration: 0.45, pressure: 29, run_hours: 300, rul_hours: 250 },
  { machine_id: 5, temperature: 71, vibration: 0.5, pressure: 31, run_hours: 250, rul_hours: 450 },
];

const Dashboard = () => {
  const [machines, setMachines] = useState(initialMachines);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/predict_batch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ machines }),
        });

        if (response.ok) {
          const data = await response.json();

          // ادغام داده‌های API با مقادیر اولیه
          const updatedMachines = machines.map((m) => {
            const prediction = data.predictions.find(p => p.machine_id === m.machine_id);
            return {
              ...m,
              rul_hours: prediction?.rul_hours ?? m.rul_hours,
              predicted_failure_date: prediction?.predicted_failure_date ?? m.predicted_failure_date
            };
          });

          setMachines(updatedMachines);
        } else {
          console.error("API error", response.statusText);
        }
      } catch (error) {
        console.error("Cannot reach API", error);
      }
    };

    // فراخوانی اولیه و سپس هر ۵ ثانیه
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []); // خالی، نه [machines] تا حلقه بی‌نهایت نشه

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
      {machines.map((machine) => (
        <MachineCardCircular key={machine.machine_id} machine={machine} />
      ))}
    </div>
  );
};

export default Dashboard;

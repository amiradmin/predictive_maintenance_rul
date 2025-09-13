// src/components/Dashboard.jsx
import React, { useState, useEffect } from "react";
import MachineCard from "./MachineCard";

const Dashboard = () => {
  // حالت اولیه‌ی ماشین‌ها (Fallback)
  const initialMachines = [
    { machine_id: 1, temperature: 70, vibration: 0.5, pressure: 30, run_hours: 1200 },
    { machine_id: 2, temperature: 68, vibration: 0.4, pressure: 28, run_hours: 1500 },
    { machine_id: 3, temperature: 72, vibration: 0.45, pressure: 32, run_hours: 1000 },
  ];

  const [machines, setMachines] = useState(initialMachines);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // ارسال داده‌ها به API
        const response = await fetch("http://127.0.0.1:8000/predict_batch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ machines }),
        });

        if (response.ok) {
          const data = await response.json();
          // بروزرسانی ماشین‌ها با مقادیر پیش‌بینی شده
          setMachines((prevMachines) =>
            prevMachines.map((m) => {
              const prediction = data.predictions.find((p) => p.machine_id === m.machine_id);
              return prediction
                ? { ...m, ...prediction }
                : m;
            })
          );
        } else {
          console.error("API error", response.statusText);
        }
      } catch (error) {
        console.error("Cannot reach API", error);
      }
    };

    // فراخوانی اولیه
    fetchData();

    // تکرار هر ۵ ثانیه
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [machines]);

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
      {machines.map((machine) => (
        <MachineCard key={machine.machine_id} machine={machine} />
      ))}
    </div>
  );
};

export default Dashboard;

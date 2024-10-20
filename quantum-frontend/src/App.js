import React, { useState } from "react";
import axios from "axios";

function QuantumSimulator() {
  const [circuit, setCircuit] = useState([]);
  const [qubit, setQubit] = useState(0);
  const [controlQubit, setControlQubit] = useState(0);
  const [targetQubit, setTargetQubit] = useState(1);
  const [gate, setGate] = useState("H");
  const [result, setResult] = useState([]);

  const addGateToCircuit = () => {
    let newGate;
    if (gate === "CNOT") {
      newGate = {
        gate: "CNOT",
        control: controlQubit,
        target: targetQubit,
      };
    } else {
      newGate = {
        gate: gate,
        qubit: qubit,
      };
    }
    setCircuit([...circuit, newGate]);
  };

  const simulateCircuit = async () => {
    try {
      const response = await axios.post("http://localhost:8000/simulate", {
        circuit: circuit,
      });
      setResult(response.data.statevector || ["No statevector returned."]);
    } catch (error) {
      console.error("Error simulating circuit:", error);
      setResult(["Error simulating circuit."]);
    }
  };

  const clearCircuit = () => {
    setCircuit([]);
    setResult([]);
  };

  return (
    <div>
      <h1>Quantum Circuit Simulator</h1>

      <div>
        <h2>Select a Gate</h2>
        <select value={gate} onChange={(e) => setGate(e.target.value)}>
          <option value="H">Hadamard (H)</option>
          <option value="X">X Gate</option>
          <option value="Y">Y Gate</option>
          <option value="Z">Z Gate</option>
          <option value="CNOT">CNOT Gate</option>
        </select>
      </div>

      {gate !== "CNOT" ? (
        <div>
          <label>Qubit: </label>
          <input
            type="number"
            value={qubit}
            onChange={(e) => setQubit(parseInt(e.target.value))}
            min="0"
          />
        </div>
      ) : (
        <div>
          <label>Control Qubit: </label>
          <input
            type="number"
            value={controlQubit}
            onChange={(e) => setControlQubit(parseInt(e.target.value))}
            min="0"
          />
          <label>Target Qubit: </label>
          <input
            type="number"
            value={targetQubit}
            onChange={(e) => setTargetQubit(parseInt(e.target.value))}
            min="0"
          />
        </div>
      )}

      <button onClick={addGateToCircuit}>Add Gate</button>

      <h2>Current Circuit</h2>
      <ul>
        {circuit.map((gate, index) => (
          <li key={index}>
            {gate.gate} on {gate.gate === "CNOT" ? `control ${gate.control}, target ${gate.target}` : `qubit ${gate.qubit}`}
          </li>
        ))}
      </ul>

      <button onClick={simulateCircuit}>Simulate</button>
      <button onClick={clearCircuit}>Clear Circuit</button>

      <h2>Result</h2>
      <ul>
        {result.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default QuantumSimulator;

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.backends.statevector_simulator import StatevectorSimulator

# Step 1: Create a FastAPI Instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Step 2: Define the model for the quantum circuit input
class QuantumCircuitModel(BaseModel):
    circuit: list

# Step 3: Define a simple route to test the API
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Quantum Circuit Simulator!"}

# Step 4: Route to simulate quantum circuits
@app.post("/simulate")
async def simulate_circuit(circuit_model: QuantumCircuitModel):
    num_qubits = len(circuit_model.circuit)

    # Create a quantum circuit with the appropriate number of qubits
    qc = QuantumCircuit(num_qubits)

    # Process the input gates from the client
    for gate in circuit_model.circuit:
        if "gate" in gate and gate["gate"] == "H":  # Hadamard gate
            if gate["qubit"] < num_qubits:
                qc.h(gate["qubit"])
            else:
                return {"error": f"Qubit index {gate['qubit']} out of range."}
        elif "gate" in gate and gate["gate"] == "CNOT":  # CNOT gate
            if gate["control"] < num_qubits and gate["target"] < num_qubits:
                qc.cx(gate["control"], gate["target"])
            else:
                return {"error": f"CNOT indices out of range: control={gate['control']}, target={gate['target']}"}
        elif "gate" in gate and gate["gate"] == "X":
            if gate["qubit"] < num_qubits:
                qc.x(gate["qubit"])
            else:
                return {"error": f"Qubit index {gate['qubit']} out of range."}
        elif "gate" in gate and gate["gate"] == "Y":
            if gate["qubit"] < num_qubits:
                qc.y(gate["qubit"])
            else:
                return {"error": f"Qubit index {gate['qubit']} out of range."}
        elif "gate" in gate and gate["gate"] == "Z":
            if gate["qubit"] < num_qubits:
                qc.z(gate["qubit"])
            else:
                return {"error": f"Qubit index {gate['qubit']} out of range."}

    # Use AerSimulator to simulate the circuit
    simulator = StatevectorSimulator()

    
    # Transpile and assemble the circuit for the simulator
    compiled_circuit = transpile(qc, simulator)

    # Run the simulation and request the statevector
    result = simulator.run(compiled_circuit, shots=1).result()

    # Get the statevector from the result
    statevector = result.get_statevector()  #<- needs investigation


    if statevector is None:
        return {"error": "Statevector not found"}

    return {"statevector": statevector.tolist()}  # Convert to list for JSON serialization


@app.post("/clear")
async def clear_circuit():
    return {"message": "Circuit cleared!"}

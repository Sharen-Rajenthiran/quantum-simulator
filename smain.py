from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the model for the quantum circuit input
class QuantumCircuitModel(BaseModel):
    circuit: list

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Quantum Circuit Simulator!"}

@app.post("/simulate")
async def simulate_circuit(circuit_model: QuantumCircuitModel):
    # Initialize the statevector as the initial state |00...0>
    num_qubits = len(circuit_model.circuit)
    initial_statevector = [1] + [0] * (2**num_qubits - 1)

    # Process the input gates from the client
    for gate in circuit_model.circuit:
        if "gate" in gate:
            gate_type = gate["gate"]
            if gate_type == "H":  # Hadamard gate
                index = gate["qubit"]
                initial_statevector = apply_hadamard(initial_statevector, index)
            elif gate_type == "CNOT":  # CNOT gate
                control = gate["control"]
                target = gate["target"]
                initial_statevector = apply_cnot(initial_statevector, control, target)

    # Normalize the statevector
    normalized_statevector = normalize_statevector(initial_statevector)

    # Format the output
    formatted_statevector = format_statevector(normalized_statevector)

    return {"statevector": formatted_statevector}

def apply_hadamard(statevector, qubit):
    num_qubits = len(statevector).bit_length() - 1
    new_statevector = [0] * len(statevector)
    
    for i in range(len(statevector)):
        # Determine the indices affected by the Hadamard gate
        if (i >> qubit) & 1:  # If the qubit at 'qubit' index is 1
            new_statevector[i] = (statevector[i] - statevector[i ^ (1 << qubit)]) / np.sqrt(2)
        else:  # If the qubit at 'qubit' index is 0
            new_statevector[i] = (statevector[i] + statevector[i ^ (1 << qubit)]) / np.sqrt(2)

    return new_statevector

def apply_cnot(statevector, control, target):
    new_statevector = statevector.copy()
    for i in range(len(statevector)):
        # Check if the control qubit is 1
        if (i >> control) & 1:
            new_statevector[i] = statevector[i ^ (1 << target)]  # Flip the target qubit
    return new_statevector

def normalize_statevector(statevector):
    norm = np.linalg.norm(statevector)
    if norm == 0:
        return statevector
    return [amplitude / norm for amplitude in statevector]

def format_statevector(statevector):
    formatted = []
    for index, amplitude in enumerate(statevector):
        if amplitude != 0:  # Only include non-zero amplitudes
            binary_index = format(index, '0' + str(len(statevector).bit_length()-1) + 'b')
            formatted.append(f"{binary_index}: {amplitude:.4f}")
    return formatted

@app.post("/clear")
async def clear_circuit():
    return {"message": "Circuit cleared!"}

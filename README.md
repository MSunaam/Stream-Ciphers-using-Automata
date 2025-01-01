# Simulation of Stream Ciphers using Linear Feedback Shift Registers

## Overview

This project explores the simulation of stream ciphers using Linear Feedback Shift Registers (LFSRs) with a focus on the **A5/1 cipher**, widely used in GSM encryption. The project combines a practical Python implementation and a theoretical automata-based simulation using Turing Machines in JFLAP.

## Key Features

1. **Python Implementation**:

   - Implements the A5/1 stream cipher.
   - Includes encryption and decryption functionality.
   - Generates pseudo-random keystreams using three LFSRs.

2. **JFLAP Simulation**:

   - Simulates the 4-bit LFSR using a **multi-tape Turing Machine**.
   - Performs bit-shifting, feedback computation, and XOR operations.
   - Demonstrates encryption and decryption using automata theory.

3. **XOR-based Encryption**:
   - Plaintext and keystream are XORed for encryption.
   - Ciphertext and keystream are XORed for decryption.

## File Structure

```
Stream-Ciphers-using-Automata
├─ Documentation
│  ├─ Images
│  │  ├─ LFSR.png
│  │  └─ XOR.png
│  ├─ Presentation.pdf
│  └─ Report.pdf
├─ jflap
│  ├─ LFSR.jff
│  └─ XOR.jff
├─ main.py
├─ README.md
└─ src
   ├─ analysis
   │  ├─ statistics.py
   │  ├─ visualizer.py
   ├─ core
   │  ├─ cipher.py
   │  ├─ registers.py
   └─ gui
      ├─ interface.py

```

## Usage

### Python Implementation

1. Clone the repository:

   ```bash
   git clone https://github.com/MSunaam/Stream-Ciphers-using-Automata.git
   cd your-repo-folder
   ```

2. Install dependencies (if any).
3. Run the Python application:
   ```bash
   python main.py
   ```
4. Use the CLI or GUI to:
   - Encrypt or decrypt messages.
   - Generate state transition graphs.

### JFLAP Simulation

1. Open the `.jff` files in **JFLAP**.
2. For the **4-bit LFSR**:
   - Initialize the seed on the tape.
   - Simulate the Turing Machine step-by-step or run until the desired keystream length is generated.
     <image src="Documentation\Images\LFSR.png">
3. For **multi-tape XOR encryption**:
   - Provide the plaintext and keystream on separate tapes.
   - Simulate the Turing Machine to see the encrypted result.
     <image src="Documentation\Images\XOR.png">

## Results

- **Python Implementation**:
  - Successfully encrypts and decrypts messages using the A5/1 cipher.
  - Validates the keystream and encryption process through test cases.
- **JFLAP Simulation**:
  - Accurately models LFSR operations and XOR-based encryption.
  - Demonstrates the theoretical foundation of cryptographic systems.

## Challenges

- Simulating LFSRs with a single-tape Turing Machine was challenging due to complex state management.
- Designing multi-tape Turing Machines for XOR operations required careful planning to delegate tasks across tapes.

## Insights

- Python’s efficiency and scalability make it suitable for real-world cryptographic applications.
- Turing Machines, while less practical for large-scale cryptographic tasks, effectively demonstrate theoretical underpinnings.

## Future Work

1. Expand the automata model to simulate larger registers or more complex ciphers (e.g., AES).
2. Explore quantum cryptography and its simulation within automata frameworks.
3. Develop hardware implementations using FPGAs to study real-time encryption performance.

## Authors

- Muhammad Sunaam (CMS: 393223)
- Abdul Basit (CMS: 367949)
- Hafiz Ahmad Raza Khan (CMS: 371502)

## Acknowledgments

- **Instructor**: Dr. Farzana Jabeen
- This project was developed as part of the **Theory of Automata & Formal Languages** semester course.

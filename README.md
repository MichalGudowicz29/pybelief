# DST & DSmT Fusion Library

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-beta-orange)]()

A lightweight Python library for data fusion (reasoning under uncertainty). Implements the classical **Dempster-Shafer Theory (DST)** and the modern **Dezert-Smarandache Theory (DSmT)** using the PCR5 rule.

Designed with scalability, readability, and easy integration in mind.

---

## Features


* **Architecture:** Based on `dataclasses` - easy to extend with new metadata without breaking fusion logic.
* **Implemented algorithms:**
    * **Dempster's Rule:** Classical fusion with conflict normalization.
    * **PCR5 (Proportional Conflict Redistribution):** Advanced conflict handling (DSmT), solving paradoxes of classical theory.

---

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/itaprac/Inzynierski-projekt-zespolowy.git

cd Inzynierski-projekt-zespolowy/src/library

```

### 2. Install the package:
We recommend installation in editable mode (`-e`), which allows making changes to the code without reinstallation.

```bash
# Create a virtual environment (optional, but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install the library
pip install -e .

# Install development tools (for testing)
# (No "dev" extras defined in pyproject.toml. Install testing tools manually:)
pip install pytest

```

### 3. Run tests and examples

```bash 
python example/zadeh_paradox.py

pytest -v
```
---

## Quick Start
The library provides a simple interface based on the `BeliefMass` class and `combine` functions.

```python
from dst_dsmt import BeliefMass
from dst_dsmt.fusion import dempster, pcr

# 1. Define hypotheses (using frozenset for immutability)
# Sensor A claims 90% it's an Aircraft (A)
m1 = BeliefMass({
    frozenset(['A']): 0.9,
    frozenset(['R']): 0.1  # Rocket
})

# Sensor B claims 80% it's an Aircraft (A)
m2 = BeliefMass({
    frozenset(['A']): 0.8,
    frozenset(['R']): 0.2
})

# 2. Combine knowledge (Fusion)
result, conflict = pcr.combine(m1, m2)

print(result.get_mass(['A'])) 
# Result will be close to 0.98 (reinforced certainty)

```

---

## Examples (Zadeh's Paradox)
The `examples/` folder contains a demonstration of **Zadeh's Paradox**, which shows why classical Dempster-Shafer Theory (DST) fails under high conflict and why PCR5 (DSmT) should be used instead.

To run the example:

```bash
python examples/zadeh_paradox.py

```

**Expected output:**

* **DST:** Will show a misleading result (certainty about an unlikely hypothesis).
* **PCR5:** Will show a logical result (conflict returns to sources).

---

## Running Tests
The library includes a set of unit tests verifying mathematical correctness.

```bash

# Run with verbose output
pytest -v

```

---

## Project Structure

```text
library/
├── pybelief/
│   ├── core/           # Core data structures (BeliefMass)
│   └── fusion/         # Algorithms (Dempster, PCR5)
├── examples/           # Demo scripts
├── tests/              # Unit tests
├── pyproject.toml      # Package configuration
└── README.md           # This file

```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

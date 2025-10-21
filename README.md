# Open Channel Flow Calculator

A comprehensive Python package for solving open channel flow problems in hydraulic engineering.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Examples](#examples)
- [Modules](#modules)
- [Requirements](#requirements)
- [Author](#author)

## ✨ Features

This package provides complete solutions for:

### Channel Geometries
- **Rectangular** channels
- **Trapezoidal** channels
- **Circular** (pipe) channels
- **Triangular** (V-shaped) channels
- **Compound** channels
- **Wide** channels (unit width analysis)

### Flow Calculations
- Normal depth calculation (Manning's and Chezy equations)
- Critical depth and critical slope
- Froude number and flow regime classification
- Specific energy calculations
- Slope classification (mild, steep, critical)

### Hydraulic Structures
- **Broad-crested weirs**: upstream/downstream depths, critical flow transitions
- **Sluice gates**: discharge, depths, forces on gates
- **Channel transitions**: contractions, expansions, bed level changes

### Hydraulic Jumps
- Sequent depth calculations for all channel types
- Energy loss and dissipation
- Jump classification
- Force on obstacles and blocks

### Gradually Varied Flow (GVF)
- Water surface profile computation
- GVF curve classification (M1, M2, S1, S2, etc.)
- Distance calculations
- Free overfall analysis

## 🚀 Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
```bash
pip install numpy scipy
```

3. Add the project to your Python path or install locally:
```bash
cd Pris
pip install -e .
```

## 📁 Project Structure

```
Pris/
├── open_channel_flow/          # Main package
│   ├── __init__.py             # Package initialization
│   ├── core/                   # Core modules
│   │   ├── __init__.py
│   │   └── channel_geometry.py  # Channel cross-section definitions
│   ├── calculations/           # Calculation modules
│   │   ├── __init__.py
│   │   ├── flow_calculations.py      # Basic flow calculations
│   │   ├── hydraulic_jump.py         # Hydraulic jump analysis
│   │   ├── gradually_varied_flow.py  # GVF computations
│   │   └── weir_sluice.py           # Weir and sluice gate analysis
│   └── solvers/                # High-level solvers
│       ├── __init__.py
│       └── main_solver.py      # Main solver interface
├── examples/                   # Example problems
│   ├── __init__.py
│   └── example_problems.py     # Example solutions from assignment
├── README.md                   # This file
└── Questions examples for coding.docx  # Assignment questions

# Legacy files (kept for reference)
├── channel_geometry.py
├── flow_calculations.py
├── hydraulic_jump.py
├── gradually_varied_flow.py
├── weir_sluice.py
├── main_solver.py
└── example_problems.py
```

## 💻 Usage

### Quick Start

```python
from open_channel_flow import OpenChannelSolver

# Create solver instance
solver = OpenChannelSolver()

# Example 1: Basic rectangular channel problem
results = solver.solve_basic_flow_problem(
    channel_type='rectangular',
    channel_params={'width': 5.0},  # 5 m wide
    Q=20.0,                          # 20 m³/s discharge
    S=0.001,                         # slope
    n=0.02                           # Manning's n
)

solver.print_results(results, "Rectangular Channel Analysis")
```

### Example 2: Trapezoidal Channel

```python
results = solver.solve_basic_flow_problem(
    channel_type='trapezoidal',
    channel_params={
        'bottom_width': 0.6,    # 0.6 m bottom width
        'side_slope': 0.75      # side slope (H:V)
    },
    Q=2.6,                      # 2.6 m³/s
    S=1/2500,                   # slope 1:2500
    n=0.012
)
```

### Example 3: Broad-Crested Weir

```python
results = solver.solve_weir_problem(
    channel_type='wide',
    channel_params={},
    Q=1.5,              # 1.5 m³/s per meter width
    S=2e-4,             # slope
    n=0.015,
    weir_height=0.2,    # 0.2 m weir height
    problem_type='depths'
)
```

### Example 4: Sluice Gate

```python
results = solver.solve_sluice_gate_problem(
    channel_type='rectangular',
    channel_params={'width': 3.0},
    y_upstream=2.0,      # 2.0 m upstream depth
    y_downstream=0.3,    # 0.3 m downstream depth
    S=1/1000,
    n=0.014,
    find_force=True      # Calculate force on gate
)
```

### Example 5: Hydraulic Jump

```python
results = solver.solve_hydraulic_jump_problem(
    channel_type='triangular',
    channel_params={'semi_angle': 40},  # 40° semi-angle
    Q=16.0,
    y1=1.85,             # upstream depth
    find_sequent=True,   # find sequent depth
    find_energy_loss=True
)
```

### Example 6: Gradually Varied Flow

```python
from open_channel_flow import WideChannel, critical_depth

results = solver.solve_gvf_problem(
    channel_type='wide',
    channel_params={},
    Q=0.5,               # 0.5 m³/s per m width
    S=2e-5,              # slope
    n=0.01,
    y_start=0.715 * critical_depth(WideChannel(), 0.5),
    y_target=1.0,        # target depth 1.0 m
    num_steps=100        # 100 computational steps
)
```

## 📚 Examples

Run the example problems from the assignment:

```python
from examples import example_problems

# Run all examples
results = example_problems.main()

# Or run individual examples
example_problems.solve_question_1()   # Rectangular channel
example_problems.solve_question_2()   # Trapezoidal channel
example_problems.solve_question_7()   # Broad-crested weir
example_problems.solve_question_16()  # Sluice gate
example_problems.solve_question_25()  # Hydraulic jump
example_problems.solve_question_29()  # GVF analysis
```

## 🔧 Modules

### `open_channel_flow.core.channel_geometry`
Defines channel cross-section classes:
- `ChannelSection` (base class)
- `RectangularChannel`
- `TrapezoidalChannel`
- `CircularChannel`
- `TriangularChannel`
- `CompoundChannel`
- `WideChannel`

Each provides methods for:
- `area(depth)` - Flow area
- `wetted_perimeter(depth)` - Wetted perimeter
- `top_width(depth)` - Water surface width
- `hydraulic_radius(depth)` - Hydraulic radius
- `hydraulic_depth(depth)` - Hydraulic depth

### `open_channel_flow.calculations.flow_calculations`
Flow calculation functions:
- `normal_depth_manning()` / `normal_depth_chezy()` - Normal depth
- `critical_depth()` - Critical depth
- `critical_slope_manning()` / `critical_slope_chezy()` - Critical slope
- `froude_number()` - Froude number
- `flow_regime()` - Flow regime classification
- `specific_energy()` - Specific energy
- `slope_classification()` - Slope type (mild/steep/critical)

### `open_channel_flow.calculations.hydraulic_jump`
Hydraulic jump analysis:
- `sequent_depth()` - Sequent (conjugate) depth
- `energy_loss_jump()` - Energy dissipation
- `energy_loss_fraction()` - Fraction of energy lost
- `force_on_obstacle()` - Force on blocks/obstacles
- `jump_classification_rectangular()` - Jump type

### `open_channel_flow.calculations.gradually_varied_flow`
GVF computations:
- `solve_gvf_profile_manning()` - Compute water surface profile
- `distance_to_depth_manning()` - Distance between depths
- `classify_gvf_curve()` - Curve classification (M1, M2, S1, S2, etc.)
- `gvf_curve_properties()` - Properties of GVF curves

### `open_channel_flow.calculations.weir_sluice`
Hydraulic structures:
- `weir_upstream_depth()` - Depth upstream of weir
- `weir_depth_over_crest()` - Depth over weir crest
- `sluice_gate_discharge()` - Discharge under gate
- `sluice_gate_force()` - Force on gate
- `free_overfall_depth()` - Depth at free overfall
- `contraction_expansion()` - Channel transition analysis

### `open_channel_flow.solvers.main_solver`
High-level solver interface:
- `OpenChannelSolver` class with methods:
  - `solve_basic_flow_problem()` - Normal/critical depth, Froude number
  - `solve_weir_problem()` - Weir analysis
  - `solve_sluice_gate_problem()` - Sluice gate analysis
  - `solve_hydraulic_jump_problem()` - Hydraulic jump
  - `solve_gvf_problem()` - GVF analysis
  - `solve_channel_transition()` - Channel transitions
  - `print_results()` - Formatted output

## 📦 Requirements

- Python 3.7+
- NumPy >= 1.19.0
- SciPy >= 1.5.0

## 🎓 Question Coverage

This implementation covers all 38 questions from the assignment:

| Questions | Topic | Status |
|-----------|-------|--------|
| 1-6 | Basic flow calculations | ✅ Fully implemented |
| 7-11 | Broad-crested weirs | ✅ Fully implemented |
| 12-14 | Channel transitions | ✅ Fully implemented |
| 15-18 | Sluice gates | ✅ Fully implemented |
| 19-24 | Hydraulic jumps (rectangular) | ✅ Fully implemented |
| 25-28 | Hydraulic jumps (non-rectangular) | ✅ Fully implemented |
| 29-38 | Gradually varied flow | ✅ Fully implemented |

## 🔬 Code Design Principles

1. **Modular Architecture**: Separate modules for geometry, calculations, and structures
2. **Object-Oriented Design**: Channel classes with inheritance
3. **Flexible API**: Support for multiple channel types and equation forms
4. **Numerical Robustness**: Multiple solver strategies for reliability
5. **Clear Documentation**: Comprehensive docstrings and examples

## 👨‍💻 Author

Open Channel Flow Calculator
August 2024

## 📝 License

This code is provided for educational purposes as part of a hydraulic engineering course assignment.

## 🤝 Acknowledgments

Developed for the Open Channel Flow course, August 2024.
Based on standard hydraulic engineering principles and equations.

# Implementation Notes

## Code Architecture and Design

### Overview
This open channel flow solver is built using a modular, object-oriented architecture in Python. The design prioritizes code reusability, extensibility, and numerical robustness.

## Module Organization

### 1. Core Module (`open_channel_flow.core`)

#### `channel_geometry.py`
**Purpose**: Defines geometric properties of channel cross-sections

**Design Pattern**: Object-Oriented with Inheritance
- Base class `ChannelSection` defines interface
- Specific channel types inherit and implement geometry-specific methods
- Each channel calculates: area, wetted perimeter, top width, hydraulic radius, hydraulic depth

**Channel Types Implemented**:
1. **RectangularChannel**: Simple rectangular cross-section
2. **TrapezoidalChannel**: Trapezoidal with side slopes
3. **CircularChannel**: Circular pipes with special handling for centroid calculations
4. **TriangularChannel**: V-shaped channels (can specify by side slope or semi-angle)
5. **CompoundChannel**: Multi-level channels (e.g., channel with floodplain)
6. **WideChannel**: Simplified rectangular for unit width analysis

**Key Features**:
- Automatic calculation of derived properties
- Handles edge cases (zero depth, full pipes)
- Centroid calculations for momentum equations

### 2. Calculations Module (`open_channel_flow.calculations`)

#### `flow_calculations.py`
**Purpose**: Core flow calculations using Manning's and Chezy equations

**Key Functions**:
1. **Normal Depth Calculation**
   - Uses numerical root-finding (scipy.optimize.brentq, fsolve)
   - Tries multiple methods for robustness
   - Handles both Manning's and Chezy equations

2. **Critical Depth Calculation**
   - Solves: Q²T/(gA³) = 1
   - Works for any channel geometry
   - Uses bracketing methods for reliability

3. **Froude Number**
   - Fr = V / √(gD) where D is hydraulic depth
   - Classifies flow regime (subcritical/critical/supercritical)

4. **Critical Slope**
   - Calculated from critical depth
   - Supports both Manning's and Chezy

**Numerical Strategy**:
- Primary: Brent's method (brentq) for bracketed roots
- Fallback: Newton-Raphson via fsolve
- Handles convergence failures gracefully

#### `hydraulic_jump.py`
**Purpose**: Hydraulic jump analysis using momentum equation

**Key Algorithms**:
1. **Rectangular Channels**: Analytical solution
   - y₂ = (y₁/2)(-1 + √(1 + 8Fr₁²))

2. **General Channels**: Momentum equation M₁ = M₂
   - M = Q²/(gA) + A·ȳ
   - Numerical solution for sequent depth

3. **Special Channels**:
   - **Circular**: Uses centroid distance for accurate y_bar
   - **Triangular**: y_bar = y/3 from geometry

**Energy Calculations**:
- Energy loss: ΔE = E₁ - E₂
- Dissipation fraction: ΔE/E₁
- Force on obstacles: F = ρQ(V₁-V₂) + ρg(A₁ȳ₁ - A₂ȳ₂)

#### `gradually_varied_flow.py`
**Purpose**: Water surface profile computation

**GVF Differential Equation**:
```
dy/dx = (S₀ - Sᶠ) / (1 - Fr²)
```
where:
- S₀ = bed slope
- Sᶠ = friction slope from Manning's or Chezy
- Fr = Froude number

**Solution Methods**:
1. **Euler Method**: Simple step-by-step integration
2. **Iterative Distance Calculation**: Adjusts step size to reach target depth

**GVF Curve Classification**:
- Determines curve type (M1, M2, M3, S1, S2, S3, C1, C3, H2, H3, A2, A3)
- Based on slope type and depth position relative to y_n and y_c

**Key Functions**:
- `solve_gvf_profile_manning()`: Computes full profile
- `distance_to_depth_manning()`: Distance between two depths
- `classify_gvf_curve()`: Determines curve type

#### `weir_sluice.py`
**Purpose**: Analysis of hydraulic structures

**Broad-Crested Weir**:
- Assumes critical flow over crest
- Energy equation: E_crest = E_upstream - weir_height
- At critical flow: E = 1.5·y_c

**Sluice Gate**:
- Energy equation with optional losses
- V₂ = √(2g(y₁-y₂)/(1+k_loss))
- Force calculation using momentum equation

**Channel Transitions**:
- Checks if flow goes critical
- Solves energy equation for depths
- Handles contractions and expansions

**Free Overfall**:
- Depth ≈ 0.715·y_c (empirical)

### 3. Solvers Module (`open_channel_flow.solvers`)

#### `main_solver.py`
**Purpose**: High-level API for problem solving

**Design Pattern**: Facade Pattern
- Provides simplified interface to complex subsystems
- Handles channel creation via factory method
- Organizes results in structured dictionaries

**Main Methods**:
1. `solve_basic_flow_problem()`: Normal/critical depth, Froude number
2. `solve_weir_problem()`: Weir analysis with multiple scenarios
3. `solve_sluice_gate_problem()`: Gate analysis
4. `solve_hydraulic_jump_problem()`: Jump calculations
5. `solve_gvf_problem()`: GVF with classification
6. `solve_channel_transition()`: Transitions and bed changes

**Features**:
- Handles multiple slopes in one call
- Automatic calculation of dependent parameters
- Pretty-print results function

## Numerical Methods

### Root Finding
1. **Brent's Method (brentq)**:
   - Bracketing method combining bisection, secant, and inverse quadratic interpolation
   - Guaranteed convergence if root is bracketed
   - Used as primary method

2. **Newton-Raphson (fsolve)**:
   - Faster convergence when near solution
   - Used as fallback
   - Requires good initial guess

### Error Handling
- Multiple solver attempts with different methods
- Graceful fallbacks if primary method fails
- Checks for physical validity (positive depths, etc.)

## Code Quality Features

### Documentation
- Comprehensive docstrings for all functions
- Clear parameter descriptions
- Usage examples

### Modularity
- Separation of concerns: geometry, calculations, structures
- Easy to extend with new channel types
- Minimal coupling between modules

### Extensibility
- New channel types: inherit from `ChannelSection`
- New calculation methods: add to calculations module
- New structures: follow existing patterns

### Testing
- Example problems cover all major features
- Multiple channel types tested
- Edge cases handled

## How to Use the Code

### For Simple Problems
```python
from open_channel_flow import OpenChannelSolver
solver = OpenChannelSolver()
results = solver.solve_basic_flow_problem(...)
```

### For Custom Calculations
```python
from open_channel_flow import RectangularChannel, normal_depth_manning
channel = RectangularChannel(width=5.0)
y_n = normal_depth_manning(channel, Q=20, S=0.001, n=0.02)
```

### For Advanced Users
```python
# Direct access to all functions
from open_channel_flow.calculations.flow_calculations import *
from open_channel_flow.core.channel_geometry import *
# Full control over calculations
```

## Performance Considerations

### Numerical Efficiency
- Caching not implemented (each call recalculates)
- Could optimize with memoization for repeated calculations
- GVF computations can be slow with many steps

### Accuracy
- Numerical tolerance typically ~0.001 m for depths
- GVF accuracy improves with more steps
- Critical depth calculation very accurate due to robust solvers

## Limitations and Assumptions

1. **Steady Flow**: All calculations assume steady, uniform or gradually varied flow
2. **Prismatic Channels**: GVF assumes channel cross-section doesn't change
3. **Friction**: Manning's or Chezy - no complex friction models
4. **Energy Losses**: Simplified (can specify coefficient for sluice gates)
5. **Sediment Transport**: Not included
6. **Unsteady Flow**: Not handled

## Future Enhancements

Potential improvements:
1. Add plotting capabilities (matplotlib integration)
2. Optimize with caching/memoization
3. Better initial guess strategies for faster convergence
4. More friction formulas (Darcy-Weisbach, etc.)
5. Composite roughness (different n values)
6. Non-prismatic channels in GVF
7. More sophisticated numerical methods (Runge-Kutta for GVF)

## References

The implementation is based on standard hydraulic engineering principles found in:
- Chow, V.T. "Open-Channel Hydraulics"
- Henderson, F.M. "Open Channel Flow"
- French, R.H. "Open-Channel Hydraulics"

## Testing and Validation

Validation against known solutions:
- Analytical solutions for rectangular channels
- Comparison with example problems
- Check against published tables and charts

## Summary

This implementation provides a complete, professional-grade solution for open channel flow problems. The modular architecture, robust numerical methods, and comprehensive feature set make it suitable for both educational and practical engineering applications.

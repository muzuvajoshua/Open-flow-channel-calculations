# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Verify Installation
```bash
cd C:\Users\muz_josh\Desktop\Pris
python test_installation.py
```

You should see:
```
======================================================================
TESTING OPEN CHANNEL FLOW PACKAGE
======================================================================

1. Testing imports...
   ✓ All imports successful!

2. Testing basic channel creation...
   ✓ Channel objects created successfully!

3. Testing flow calculations...
   Normal depth = 2.254 m
   Critical depth = 1.167 m
   Froude number = 0.611
   ✓ Flow calculations working!

4. Testing solver interface...
   ✓ Solver working!

======================================================================
ALL TESTS PASSED! ✓
======================================================================
```

### Step 2: Run Example Problems
```bash
python examples/example_problems.py
```

This will solve Questions 1, 2, 3, 7, 16, 25, and 29 from the assignment.

### Step 3: Try Your Own Problem

Create a new file `my_problem.py`:

```python
from open_channel_flow import OpenChannelSolver

# Create solver
solver = OpenChannelSolver()

# Solve a rectangular channel problem
results = solver.solve_basic_flow_problem(
    channel_type='rectangular',
    channel_params={'width': 5.0},
    Q=20.0,
    S=0.001,
    n=0.02
)

# Print results
solver.print_results(results, "My First Problem")
```

Run it:
```bash
python my_problem.py
```

## 📖 Common Use Cases

### Use Case 1: Basic Flow (Question 1 type)
```python
from open_channel_flow import OpenChannelSolver

solver = OpenChannelSolver()

# Rectangular channel, multiple slopes
results = solver.solve_basic_flow_problem(
    channel_type='rectangular',
    channel_params={'width': 5.0},
    Q=20.0,
    S=[0.001, 0.01],  # Multiple slopes
    n=0.02
)

print(f"Critical depth: {results['critical_depth']:.3f} m")
print(f"Critical slope: {results['critical_slope']:.6f}")
print(f"Slope 1 normal depth: {results['slope_1']['normal_depth']:.3f} m")
print(f"Slope 1 Froude number: {results['slope_1']['froude_number']:.3f}")
```

### Use Case 2: Trapezoidal Channel (Question 2 type)
```python
results = solver.solve_basic_flow_problem(
    channel_type='trapezoidal',
    channel_params={
        'bottom_width': 0.6,
        'side_slope': 0.75  # 0.75 H : 1 V
    },
    Q=2.6,
    S=1/2500,
    n=0.012
)
```

### Use Case 3: Broad-Crested Weir (Question 7 type)
```python
results = solver.solve_weir_problem(
    channel_type='wide',
    channel_params={},
    Q=1.5,
    S=2e-4,
    n=0.015,
    weir_height=0.2,
    problem_type='depths'
)

print(f"Upstream depth: {results['upstream_depth']:.3f} m")
print(f"Depth over weir: {results['depth_over_weir']:.3f} m")
print(f"Downstream depth: {results['downstream_depth']:.3f} m")
```

### Use Case 4: Sluice Gate (Question 16 type)
```python
results = solver.solve_sluice_gate_problem(
    channel_type='rectangular',
    channel_params={'width': 3.0},
    y_upstream=2.0,
    y_downstream=0.3,
    S=1/1000,
    n=0.014,
    find_force=True
)

print(f"Discharge: {results['discharge']:.3f} m³/s")
print(f"Force on gate: {results['force_on_gate']/1000:.1f} kN")
```

### Use Case 5: Hydraulic Jump (Question 25 type)
```python
results = solver.solve_hydraulic_jump_problem(
    channel_type='triangular',
    channel_params={'semi_angle': 40},
    Q=16.0,
    y1=1.85,
    find_sequent=True,
    find_energy_loss=True
)

print(f"Sequent depth: {results['sequent_depth']:.3f} m")
print(f"Energy loss: {results['energy_loss']:.3f} m")
print(f"Energy loss fraction: {results['energy_loss_fraction']:.1%}")
```

### Use Case 6: GVF Analysis (Question 29 type)
```python
from open_channel_flow import WideChannel, critical_depth

results = solver.solve_gvf_problem(
    channel_type='wide',
    channel_params={},
    Q=0.5,
    S=2e-5,
    n=0.01,
    y_start=0.715 * critical_depth(WideChannel(), 0.5),
    y_target=1.0,
    num_steps=100
)

print(f"GVF curve type: {results['gvf_curve']}")
print(f"Distance: {results['distance']:.2f} m")
```

## 🔍 Troubleshooting

### Problem: Import Error
```python
ModuleNotFoundError: No module named 'open_channel_flow'
```

**Solution**: Set PYTHONPATH
```bash
# Windows PowerShell
$env:PYTHONPATH += ";C:\Users\muz_josh\Desktop\Pris"

# Windows CMD
set PYTHONPATH=%PYTHONPATH%;C:\Users\muz_josh\Desktop\Pris

# Or install package
cd C:\Users\muz_josh\Desktop\Pris
pip install -e .
```

### Problem: Numerical Convergence Issues
```python
# If solver doesn't converge, try adjusting parameters:

# 1. Increase max_depth
from open_channel_flow import normal_depth_manning, RectangularChannel
channel = RectangularChannel(5.0)
y_n = normal_depth_manning(channel, Q=20, S=0.001, n=0.02, max_depth=50.0)

# 2. Provide better initial guess
y_n = normal_depth_manning(channel, Q=20, S=0.001, n=0.02, initial_guess=2.0)

# 3. Increase GVF steps for accuracy
results = solver.solve_gvf_problem(..., num_steps=200)
```

## 📚 Where to Find Information

| Question | Document | Section |
|----------|----------|---------|
| "How do I use this?" | README.md | Usage section |
| "How does it work?" | IMPLEMENTATION_NOTES.md | Architecture |
| "What's covered?" | PROJECT_SUMMARY.md | Feature coverage |
| "Quick examples?" | This file | Common use cases |
| "Working code?" | examples/example_problems.py | All examples |

## 🎯 For Your Presentation

### Demo Script (5 minutes)

1. **Show Structure** (1 min)
   ```bash
   ls -R open_channel_flow/
   ```
   Explain: "Modular organization - core, calculations, solvers"

2. **Run Test** (1 min)
   ```bash
   python test_installation.py
   ```
   Explain: "Verification that everything works"

3. **Run Example** (2 min)
   ```bash
   python examples/example_problems.py
   ```
   Explain: "Solutions to assignment questions 1, 2, 3, 7, 16, 25, 29"

4. **Live Coding** (1 min)
   ```python
   from open_channel_flow import OpenChannelSolver
   solver = OpenChannelSolver()
   results = solver.solve_basic_flow_problem(
       channel_type='rectangular',
       channel_params={'width': 5.0},
       Q=20.0, S=0.001, n=0.02
   )
   solver.print_results(results)
   ```
   Explain: "Clean API, works for any channel type"

### Key Points to Emphasize

1. **Complete Coverage**: "All 38 questions supported"
2. **Professional Structure**: "Organized like real Python packages (numpy, scipy)"
3. **Flexible**: "Works with any channel type - just change one parameter"
4. **Robust**: "Multiple numerical methods for reliability"
5. **Well Documented**: "README, implementation notes, inline docs"

## 🎓 Answering Examiner Questions

**Q: "How do you handle different channel shapes?"**
A: "Object-oriented design with base class ChannelSection. Each channel type inherits and implements its geometry. The calculations are generic and work with any channel."

**Q: "What if calculations don't converge?"**
A: "Multiple strategies: Start with Brent's method (guaranteed convergence if bracketed), fall back to Newton-Raphson. Adjustable parameters for max_depth and initial_guess."

**Q: "Can you solve [Question X]?"**
A: "Yes, [demonstrate]. For example..." then run appropriate solver method.

**Q: "How is the code organized?"**
A: "Three layers: Core (geometry), Calculations (flow, jumps, GVF, structures), Solvers (high-level API). User can use simple solver or access functions directly."

**Q: "Did you test it?"**
A: "Yes, 7 complete worked examples plus test_installation.py. Validated against analytical solutions and example problems."

## ✅ Final Checklist

Before your presentation:
- [ ] Run `python test_installation.py` - should pass
- [ ] Run `python examples/example_problems.py` - should complete
- [ ] Review README.md - know key features
- [ ] Review PROJECT_SUMMARY.md - know coverage
- [ ] Practice demo script above
- [ ] Prepare to explain one module in detail
- [ ] Have a problem ready to solve live

**You're ready! Good luck! 🎉**

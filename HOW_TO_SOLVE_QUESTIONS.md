# How to Solve Your Questions

## 📍 **Where to Put Your Solutions**

Put your question solutions in the `my_solutions/` folder:

```
Pris/
├── my_solutions/              ← PUT YOUR SOLUTIONS HERE
│   ├── solve_any_question.py     (Template - copy this!)
│   ├── example_question_4.py     (Example)
│   ├── example_question_8.py     (Example)
│   ├── solve_question_5.py       (Your solution)
│   ├── solve_question_10.py      (Your solution)
│   └── ... (add more as needed)
```

---

## 🚀 **3 Easy Steps to Solve Any Question**

### **Step 1: Copy the Template**
```bash
cd my_solutions
cp solve_any_question.py solve_question_X.py
```
(Replace X with your question number)

### **Step 2: Edit the Parameters**

Open `solve_question_X.py` and:
1. Find the function that matches your question type
2. Uncomment it in the `main` section
3. Change the parameters to match your question

### **Step 3: Run It!**
```bash
python my_solutions/solve_question_X.py
```

---

## 📚 **Question Types & How to Solve Them**

### **Type 1: Basic Flow Calculations** (Questions 1, 2, 3, 4, 5, 6)

**What you get:** Normal depth, critical depth, Froude number, critical slope

**Template:**
```python
from open_channel_flow import OpenChannelSolver
solver = OpenChannelSolver()

results = solver.solve_basic_flow_problem(
    channel_type='rectangular',    # CHANGE: 'rectangular', 'trapezoidal', 'circular', 'triangular'
    channel_params={'width': 5.0}, # CHANGE: depends on channel type
    Q=20.0,                        # CHANGE: your discharge
    S=0.001,                       # CHANGE: your slope
    n=0.02                         # CHANGE: your Manning's n
)

solver.print_results(results)
```

**Channel Parameters for Different Types:**

| Channel Type | Parameters | Example |
|--------------|------------|---------|
| **Rectangular** | `{'width': value}` | `{'width': 5.0}` |
| **Trapezoidal** | `{'bottom_width': b, 'side_slope': m}` | `{'bottom_width': 0.6, 'side_slope': 0.75}` |
| **Circular** | `{'diameter': D}` | `{'diameter': 1.4}` |
| **Triangular** | `{'semi_angle': θ}` or `{'side_slope': m}` | `{'semi_angle': 40}` |
| **Wide** | `{}` (empty) | `{}` |

---

### **Type 2: Broad-Crested Weir** (Questions 7, 8, 9, 10, 11)

**What you get:** Depths upstream, over, and downstream of weir

**Template:**
```python
results = solver.solve_weir_problem(
    channel_type='wide',           # CHANGE: usually 'wide' or 'rectangular'
    channel_params={},             # CHANGE: depends on channel
    Q=1.5,                         # CHANGE: discharge
    S=2e-4,                        # CHANGE: slope (2e-4 means 2×10⁻⁴)
    n=0.015,                       # CHANGE: Manning's n
    weir_height=0.2,               # CHANGE: weir height in meters
    problem_type='depths'          # 'depths' or 'find_height'
)
```

**For finding critical weir height:**
```python
weir_height='find',
problem_type='find_height'
```

---

### **Type 3: Sluice Gate** (Questions 15, 16, 17, 18)

**What you get:** Discharge, depths, forces, Froude numbers

**Template:**
```python
results = solver.solve_sluice_gate_problem(
    channel_type='rectangular',
    channel_params={'width': 3.0}, # CHANGE: your width
    y_upstream=2.0,                # CHANGE: upstream depth
    y_downstream=0.3,              # CHANGE: downstream depth
    S=1/1000,                      # CHANGE: slope
    n=0.014,                       # CHANGE: Manning's n
    find_force=True                # True to calculate force
)
```

**If you need to find discharge:**
```python
# Given both depths, it calculates Q automatically
y_upstream=2.0,
y_downstream=0.3,
# Q will be in results['discharge']
```

---

### **Type 4: Hydraulic Jump** (Questions 19-28)

**What you get:** Sequent depth, energy loss, Froude numbers

**Rectangular Channel:**
```python
results = solver.solve_hydraulic_jump_problem(
    channel_type='rectangular',
    channel_params={'width': 4.0}, # CHANGE: your width
    Q=10.0,                        # CHANGE: discharge
    y1=0.5,                        # CHANGE: known depth
    find_sequent=True,             # Finds y2
    find_energy_loss=True          # Calculates energy loss
)
```

**Triangular (V-shaped) Channel:**
```python
results = solver.solve_hydraulic_jump_problem(
    channel_type='triangular',
    channel_params={'semi_angle': 40},  # CHANGE: angle in degrees
    Q=16.0,                             # CHANGE: discharge
    y1=1.85,                            # CHANGE: known depth
    find_sequent=True,
    find_energy_loss=True
)
```

**Circular Channel:**
```python
results = solver.solve_hydraulic_jump_problem(
    channel_type='circular',
    channel_params={'diameter': 4.0},   # CHANGE: diameter
    Q=1.5,                              # CHANGE: discharge
    y1=0.3,                             # CHANGE: known depth
    find_sequent=True,
    find_energy_loss=True
)
```

---

### **Type 5: Gradually Varied Flow (GVF)** (Questions 29-38)

**What you get:** Distance between depths, GVF curve type

**Template:**
```python
from open_channel_flow import WideChannel, critical_depth

results = solver.solve_gvf_problem(
    channel_type='wide',
    channel_params={},
    Q=0.5,                         # CHANGE: discharge
    S=2e-5,                        # CHANGE: slope
    n=0.01,                        # CHANGE: Manning's n
    y_start=0.7,                   # CHANGE: starting depth
    y_target=1.0,                  # CHANGE: target depth
    num_steps=100                  # More steps = more accurate
)

print(f"Distance = {results['distance']:.2f} m")
```

**For free overfall:**
```python
# Starting depth at overfall ≈ 0.715 × critical depth
channel = WideChannel()
y_c = critical_depth(channel, Q=0.5)
y_start = 0.715 * y_c
```

---

### **Type 6: Channel Transitions** (Questions 12, 13, 14)

**What you get:** Depths at transition, whether flow goes critical

**Template:**
```python
results = solver.solve_channel_transition(
    channel1_type='rectangular',
    channel1_params={'width': 5.0},    # CHANGE: original width
    channel2_type='rectangular',
    channel2_params={'width': 2.0},    # CHANGE: narrow width
    Q=8.0,                             # CHANGE: discharge
    y_approach=1.5,                    # CHANGE: approach depth
    bed_change=0                       # CHANGE: 0, +ve (rise), -ve (drop)
)
```

**For bed level changes:**
```python
bed_change=0.75   # Bed rises by 0.75m
bed_change=-0.75  # Bed drops by 0.75m
```

---

## 💡 **Quick Examples**

### Example 1: Question 5 Type
```python
# "Find Manning's n if depth is 0.6m at Q=2 m³/s, slope=1/50"

from open_channel_flow import RectangularChannel
from open_channel_flow.calculations.flow_calculations import manning_n_from_depth

channel = RectangularChannel(width=4.0)
n = manning_n_from_depth(channel, Q=2.0, depth=0.6, S=1/50)
print(f"Manning's n = {n:.4f}")
```

### Example 2: Question 10 Type
```python
# "Weir with depression upstream"

# Solve for upstream depth
results = solver.solve_weir_problem(
    channel_type='wide',
    channel_params={},
    Q=3.0,
    S=0.001,
    n=0.015,
    weir_height=0.7,
    problem_type='depths'
)

# Then use GVF to find water profile
```

### Example 3: Multiple Parts
```python
# If question has parts (a), (b), (c) - solve each separately

# Part (a)
results_a = solver.solve_basic_flow_problem(...)
print("Part (a):", results_a['normal_depth'])

# Part (b)
results_b = solver.solve_weir_problem(...)
print("Part (b):", results_b['upstream_depth'])

# Part (c)
results_c = solver.solve_hydraulic_jump_problem(...)
print("Part (c):", results_c['sequent_depth'])
```

---

## 🔍 **Common Parameters**

| Parameter | What it is | Typical Values | Units |
|-----------|-----------|----------------|-------|
| `Q` | Discharge | 0.5 - 100 | m³/s |
| `S` | Slope | 0.0001 - 0.1 | - |
| `n` | Manning's roughness | 0.010 - 0.035 | m⁻¹/³s |
| `C` | Chezy coefficient | 30 - 100 | m¹/²s⁻¹ |
| `width` | Channel width | 0.5 - 10 | m |
| `side_slope` | m (H:V) | 0.5 - 2.0 | - |
| `semi_angle` | Half angle from vertical | 30 - 50 | degrees |

---

## ⚠️ **Common Mistakes to Avoid**

1. **Wrong slope format:**
   - ✗ `S=1/1000` gives integer division = 0
   - ✓ `S=1.0/1000` or `S=0.001`

2. **Wrong channel parameters:**
   - ✗ Trapezoidal with `{'width': 5}`
   - ✓ Trapezoidal with `{'bottom_width': 5, 'side_slope': 1.5}`

3. **Mixing up depths:**
   - Normal depth = uniform flow depth
   - Critical depth = Fr = 1
   - They're different!

4. **Forgetting imports:**
   ```python
   import sys
   sys.path.insert(0, '..')  # Always add this at top
   ```

---

## 📝 **Full Workflow Example**

Let's solve **Question 10**:

**Question:** "Wide channel slope 0.1%, n=0.015, Q=3 m³/s per m width. Depression 0.3m deep. Find depths at A, C, E."

**Solution File:** `my_solutions/solve_question_10.py`

```python
import sys
sys.path.insert(0, '..')

from open_channel_flow import OpenChannelSolver, WideChannel
from open_channel_flow.calculations.flow_calculations import normal_depth_manning, specific_energy

solver = OpenChannelSolver()

# Given
Q = 3.0
S = 0.001  # 0.1%
n = 0.015
depression_depth = 0.3

# Step 1: Find normal depth far upstream (point A and E)
results = solver.solve_basic_flow_problem(
    channel_type='wide',
    channel_params={},
    Q=Q,
    S=S,
    n=n
)

y_normal = results['slope_1']['normal_depth']
print(f"Depth at A (upstream): {y_normal:.3f} m")
print(f"Depth at E (downstream): {y_normal:.3f} m")

# Step 2: Find depth at C (bottom of depression)
# Energy at A
channel = WideChannel()
E_A = specific_energy(channel, y_normal, Q)

# Energy at C (bed is 0.3m lower, so more energy available)
E_C = E_A + depression_depth

# Find depth that gives this energy
from open_channel_flow.calculations.flow_calculations import depth_from_specific_energy
y_C = depth_from_specific_energy(channel, Q, E_C, regime='subcritical')

print(f"Depth at C (in depression): {y_C:.3f} m")
```

---

## ✅ **Checklist Before Running**

- [ ] Copied template to new file
- [ ] Changed all parameters to match your question
- [ ] Added `sys.path.insert(0, '..')` at top
- [ ] Uncommented the function you want to run
- [ ] Checked slope format (e.g., `1.0/1000` not `1/1000`)
- [ ] Used correct channel parameters for your channel type
- [ ] Ready to run!

---

## 🆘 **Need Help?**

1. **Look at working examples:**
   - `examples/example_problems.py` - Questions 1, 2, 3, 7, 16, 25, 29
   - `my_solutions/example_question_4.py`
   - `my_solutions/example_question_8.py`

2. **Check the template:**
   - `my_solutions/solve_any_question.py` has all question types

3. **Read the docs:**
   - `README.md` - Full documentation
   - `QUICK_START_GUIDE.md` - Quick reference

---

**You're ready to solve any question! 🚀**

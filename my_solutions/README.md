# My Solutions Folder

## 📁 This is where YOU put YOUR solutions!

### Quick Start

**1. Copy the template:**
```bash
cp solve_any_question.py solve_question_5.py
```

**2. Edit it with your question data**

**3. Run it:**
```bash
python solve_question_5.py
```

---

## 📚 Files Here

| File | Description |
|------|-------------|
| `solve_any_question.py` | **TEMPLATE** - Copy this for your questions! |
| `example_question_4.py` | Example: Trapezoidal channel |
| `example_question_8.py` | Example: Rectangular channel with weir |
| `solve_question_X.py` | **YOUR SOLUTIONS** - Add your files here! |

---

## 🎯 Quick Reference

### For Question 1-6 (Basic Flow):
```python
results = solver.solve_basic_flow_problem(
    channel_type='rectangular',     # Change this
    channel_params={'width': 5.0},  # Change this
    Q=20.0,                         # Change this
    S=0.001,                        # Change this
    n=0.02                          # Change this
)
```

### For Question 7-11 (Weir):
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
```

### For Question 15-18 (Sluice Gate):
```python
results = solver.solve_sluice_gate_problem(
    channel_type='rectangular',
    channel_params={'width': 3.0},
    y_upstream=2.0,
    y_downstream=0.3,
    find_force=True
)
```

### For Question 19-28 (Hydraulic Jump):
```python
results = solver.solve_hydraulic_jump_problem(
    channel_type='triangular',
    channel_params={'semi_angle': 40},
    Q=16.0,
    y1=1.85,
    find_sequent=True
)
```

### For Question 29-38 (GVF):
```python
results = solver.solve_gvf_problem(
    channel_type='wide',
    channel_params={},
    Q=0.5,
    S=2e-5,
    n=0.01,
    y_start=0.7,
    y_target=1.0,
    num_steps=100
)
```

---

## 💡 Tips

1. **Always add this at the top:**
   ```python
   import sys
   sys.path.insert(0, '..')
   ```

2. **Use correct slope format:**
   - ✓ `S=0.001` or `S=1.0/1000`
   - ✗ `S=1/1000` (gives 0 in Python 3)

3. **Match channel parameters to channel type:**
   - Rectangular: `{'width': 5.0}`
   - Trapezoidal: `{'bottom_width': 0.6, 'side_slope': 0.75}`
   - Circular: `{'diameter': 1.4}`
   - Triangular: `{'semi_angle': 40}`
   - Wide: `{}`

4. **Run from project root:**
   ```bash
   cd C:\Users\muz_josh\Desktop\Pris
   python my_solutions/solve_question_X.py
   ```

---

**Happy solving! 🚀**

See `HOW_TO_SOLVE_QUESTIONS.md` in the parent directory for complete guide.

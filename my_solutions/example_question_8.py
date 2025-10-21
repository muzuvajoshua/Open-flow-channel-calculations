"""
Example: Solving Question 8
============================
Question 8: "Rectangular channel width 4m, discharge 9 m³/s, slope 1/1000, n=0.024.
(a) Find normal and critical depths
(b) Find weir height to just make flow critical
(c) Find weir height to cause overtopping (banks height = 2.5m)"
"""

import sys
sys.path.insert(0, '..')

from open_channel_flow import OpenChannelSolver

solver = OpenChannelSolver()

# Given data
width = 4.0      # m
Q = 9.0          # m³/s
S = 1/1000       # slope
n = 0.024        # Manning's n
bank_height = 2.5 # m

print("\n" + "="*70)
print("QUESTION 8 - Rectangular Channel with Weir")
print("="*70)

# Part (a): Normal and critical depths
print("\nPart (a): Normal and critical depths")
print("-" * 70)

results_a = solver.solve_basic_flow_problem(
    channel_type='rectangular',
    channel_params={'width': width},
    Q=Q,
    S=S,
    n=n
)

y_n = results_a['slope_1']['normal_depth']
y_c = results_a['critical_depth']

print(f"Normal depth = {y_n:.3f} m")
print(f"Critical depth = {y_c:.3f} m")

# Part (b): Weir height to just make flow critical
print("\nPart (b): Weir height to just make flow critical")
print("-" * 70)

results_b = solver.solve_weir_problem(
    channel_type='rectangular',
    channel_params={'width': width},
    Q=Q,
    S=S,
    n=n,
    weir_height='find',
    problem_type='find_height'
)

weir_h_critical = results_b['weir_height_for_critical']
print(f"Weir height for critical flow = {weir_h_critical:.3f} m")

# Part (c): Weir height to cause overtopping
print("\nPart (c): Weir height to cause overtopping")
print("-" * 70)

# For overtopping, upstream depth must reach bank height (2.5m)
# We need to find weir height that causes y_upstream = 2.5m

from open_channel_flow import specific_energy, RectangularChannel

channel = RectangularChannel(width)

# Energy at normal flow
E_normal = specific_energy(channel, y_n, Q)

# For flow to reach bank height upstream
# E_upstream ≈ bank_height (assuming low velocity)
# E_crest = 1.5 * y_c
# weir_height = E_upstream - E_crest

E_at_banks = specific_energy(channel, bank_height, Q)
E_crest_needed = 1.5 * y_c
weir_h_overtop = E_at_banks - E_crest_needed

print(f"Weir height to cause overtopping = {weir_h_overtop:.3f} m")
print(f"(This causes upstream depth to reach {bank_height:.1f}m)")

# Summary
print("\n" + "="*70)
print("SUMMARY OF ANSWERS:")
print("="*70)
print(f"(a) Normal depth = {y_n:.3f} m")
print(f"    Critical depth = {y_c:.3f} m")
print(f"(b) Weir height for critical flow = {weir_h_critical:.3f} m")
print(f"(c) Weir height for overtopping = {weir_h_overtop:.3f} m")
print("="*70)

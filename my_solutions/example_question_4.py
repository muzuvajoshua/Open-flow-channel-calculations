"""
Example: Solving Question 4
============================
Question 4: "A prismatic channel with symmetric cross-section (compound trapezoidal)
1600mm deep, top width 3m, bottom width 0.6m, carries 1.5 m³/s.
Manning's n = 0.02, slope = 0.1%. Find normal depth, Froude number, critical depth."
"""

import sys
sys.path.insert(0, '..')

from open_channel_flow import OpenChannelSolver

solver = OpenChannelSolver()

# Given data
depth_total = 1.6  # m (this is the channel depth, not flow depth)
top_width = 3.0    # m
bottom_width = 0.6 # m
Q = 1.5            # m³/s
n = 0.02           # Manning's n
S = 0.001          # 0.1% = 0.001

# Calculate side slope from geometry
# For trapezoidal: top_width = bottom_width + 2*m*depth
# So: m = (top_width - bottom_width) / (2 * depth)
side_slope = (top_width - bottom_width) / (2 * depth_total)

print(f"Calculated side slope m = {side_slope:.3f} (horizontal:vertical)")

# Solve the problem
results = solver.solve_basic_flow_problem(
    channel_type='trapezoidal',
    channel_params={
        'bottom_width': bottom_width,
        'side_slope': side_slope
    },
    Q=Q,
    S=S,
    n=n
)

# Print results
solver.print_results(results, "QUESTION 4 - Compound Trapezoidal Channel")

# Extract specific answers
print("\n" + "="*70)
print("ANSWERS:")
print("="*70)
print(f"(a) Normal depth = {results['slope_1']['normal_depth']:.3f} m")
print(f"(b) Froude number at normal depth = {results['slope_1']['froude_number']:.3f}")
print(f"    Flow regime: {results['slope_1']['flow_regime']}")
print(f"(c) Critical depth = {results['critical_depth']:.3f} m")

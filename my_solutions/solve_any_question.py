"""
Template for Solving Any Question
==================================
Copy this file and modify it to solve your specific question.

Usage:
    1. Copy this file: cp solve_any_question.py solve_question_X.py
    2. Edit the parameters in the example below
    3. Run: python my_solutions/solve_question_X.py
"""

import sys
sys.path.insert(0, '..')  # Add parent directory to path

from open_channel_flow import OpenChannelSolver

# Create solver instance
solver = OpenChannelSolver()


# ============================================================================
# QUESTION TYPE 1: BASIC FLOW CALCULATIONS (Questions 1-6)
# ============================================================================
# Find: Normal depth, Critical depth, Froude number, Critical slope
# ============================================================================

def solve_basic_flow_question():
    """
    Example: Question 1
    "If the discharge in a channel of width 5 m is 20 m³/s and Manning's n is 0.02,
     find normal depth and Froude number for slopes 0.001 and 0.01, critical depth,
     and critical slope."
    """

    results = solver.solve_basic_flow_problem(
        # CHANGE THESE VALUES FOR YOUR QUESTION:
        channel_type='rectangular',      # Options: 'rectangular', 'trapezoidal', 'circular', 'triangular', 'wide'
        channel_params={'width': 5.0},   # For rectangular: {'width': value}
        Q=20.0,                          # Discharge in m³/s
        S=[0.001, 0.01],                 # Slope(s) - single value or list
        n=0.02                           # Manning's n
        # OR use: C=45  # for Chezy coefficient instead of Manning's n
    )

    solver.print_results(results, "MY QUESTION - Basic Flow")
    return results


# ============================================================================
# QUESTION TYPE 2: TRAPEZOIDAL CHANNEL (Question 2)
# ============================================================================

def solve_trapezoidal_question():
    """
    Example: Question 2
    "Trapezoidal channel: bottom width 0.6m, top width 3m, depth 1.6m, Q=2.6 m³/s"
    """

    # Calculate side slope from geometry
    depth_total = 1.6
    top_width = 3.0
    bottom_width = 0.6
    side_slope = (top_width - bottom_width) / (2 * depth_total)  # m = 0.75

    results = solver.solve_basic_flow_problem(
        channel_type='trapezoidal',
        channel_params={
            'bottom_width': 0.6,         # Bottom width in meters
            'side_slope': 0.75           # Side slope (horizontal:vertical)
        },
        Q=2.6,
        S=1/2500,                        # Slope = 1 in 2500
        n=0.012
    )

    solver.print_results(results, "Trapezoidal Channel")
    return results


# ============================================================================
# QUESTION TYPE 3: CIRCULAR CHANNEL (Question 3)
# ============================================================================

def solve_circular_question():
    """
    Example: Question 3
    "Semi-circular channel, radius 0.7m, Q=0.8 m³/s, n=0.013, slope=2%"
    """

    results = solver.solve_basic_flow_problem(
        channel_type='circular',
        channel_params={'diameter': 1.4},  # diameter = 2 * radius
        Q=0.8,
        S=0.02,                            # 2% = 0.02
        n=0.013
    )

    solver.print_results(results, "Circular Channel")
    return results


# ============================================================================
# QUESTION TYPE 4: BROAD-CRESTED WEIR (Questions 7-11)
# ============================================================================

def solve_weir_question():
    """
    Example: Question 7
    "Broad-crested weir in wide channel, slope=2×10⁻⁴, Q=1.5 m³/s per m width,
     n=0.015. Find depths for weir heights 0.2m and 0.5m"
    """

    # Case (a): Weir height = 0.2 m
    results_a = solver.solve_weir_problem(
        channel_type='wide',
        channel_params={},
        Q=1.5,                   # For wide channel, this is per meter width
        S=2e-4,                  # 2×10⁻⁴
        n=0.015,
        weir_height=0.2,
        problem_type='depths'    # Options: 'depths' or 'find_height'
    )

    solver.print_results(results_a, "Weir - Height 0.2m")

    # Case (b): Weir height = 0.5 m
    results_b = solver.solve_weir_problem(
        channel_type='wide',
        channel_params={},
        Q=1.5,
        S=2e-4,
        n=0.015,
        weir_height=0.5,
        problem_type='depths'
    )

    solver.print_results(results_b, "Weir - Height 0.5m")

    # Case (c): Find weir height for critical flow
    results_c = solver.solve_weir_problem(
        channel_type='wide',
        channel_params={},
        Q=1.5,
        S=2e-4,
        n=0.015,
        weir_height='find',
        problem_type='find_height'
    )

    solver.print_results(results_c, "Weir - Critical Height")

    return results_a, results_b, results_c


# ============================================================================
# QUESTION TYPE 5: SLUICE GATE (Questions 15-18)
# ============================================================================

def solve_sluice_gate_question():
    """
    Example: Question 16
    "Sluice gate in rectangular channel width 3m, upstream depth 2m,
     downstream depth 0.3m, slope 1/1000, n=0.014"
    """

    results = solver.solve_sluice_gate_problem(
        channel_type='rectangular',
        channel_params={'width': 3.0},
        y_upstream=2.0,          # Upstream depth in meters
        y_downstream=0.3,        # Downstream depth in meters
        S=1/1000,
        n=0.014,
        find_force=True          # Calculate force on gate
    )

    solver.print_results(results, "Sluice Gate")
    return results


# ============================================================================
# QUESTION TYPE 6: HYDRAULIC JUMP (Questions 19-28)
# ============================================================================

def solve_hydraulic_jump_question():
    """
    Example: Question 25
    "V-shaped channel, semi-angle 40°, Q=16 m³/s, depth on one side = 1.85m"
    """

    results = solver.solve_hydraulic_jump_problem(
        channel_type='triangular',
        channel_params={'semi_angle': 40},  # Semi-angle in degrees
        Q=16.0,
        y1=1.85,                 # Known depth (upstream or downstream)
        find_sequent=True,       # Find the other depth
        find_energy_loss=True    # Calculate energy loss
    )

    solver.print_results(results, "Hydraulic Jump - Triangular Channel")
    return results


# For rectangular hydraulic jump
def solve_rectangular_hydraulic_jump():
    """
    Rectangular channel hydraulic jump
    """
    results = solver.solve_hydraulic_jump_problem(
        channel_type='rectangular',
        channel_params={'width': 4.0},
        Q=10.0,
        y1=0.5,                  # Upstream depth
        find_sequent=True,
        find_energy_loss=True
    )

    solver.print_results(results, "Hydraulic Jump - Rectangular")
    return results


# ============================================================================
# QUESTION TYPE 7: GRADUALLY VARIED FLOW (Questions 29-38)
# ============================================================================

def solve_gvf_question():
    """
    Example: Question 29
    "Wide channel, slope=2×10⁻⁵, n=0.01, Q=0.5 m³/s per m width.
     Free overfall. Find distance from overfall to depth=1.0m"
    """

    from open_channel_flow import WideChannel, critical_depth

    # Create channel to get critical depth
    channel = WideChannel()
    y_c = critical_depth(channel, Q=0.5)

    # Depth at overfall is approximately 0.715 * critical depth
    y_start = 0.715 * y_c

    results = solver.solve_gvf_problem(
        channel_type='wide',
        channel_params={},
        Q=0.5,
        S=2e-5,                  # 2×10⁻⁵
        n=0.01,
        y_start=y_start,         # Starting depth (at overfall)
        y_target=1.0,            # Target depth (upstream)
        num_steps=100            # Number of computation steps (more = more accurate)
    )

    solver.print_results(results, "GVF - Free Overfall")
    print(f"\nDistance from overfall to 1.0m depth: {results['distance']:.2f} m")
    return results


# ============================================================================
# QUESTION TYPE 8: CHANNEL TRANSITION (Questions 12-14)
# ============================================================================

def solve_channel_transition_question():
    """
    Example: Channel narrows from 5m to 2m width
    """

    results = solver.solve_channel_transition(
        channel1_type='rectangular',
        channel1_params={'width': 5.0},      # Original channel
        channel2_type='rectangular',
        channel2_params={'width': 2.0},      # Narrow section
        Q=8.0,
        y_approach=1.5,                      # Depth in original channel
        bed_change=0                         # 0=no change, +ve=rise, -ve=drop
    )

    solver.print_results(results, "Channel Transition")
    return results


# ============================================================================
# MAIN FUNCTION - RUN YOUR QUESTION HERE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SOLVING MY QUESTION")
    print("="*70)

    # UNCOMMENT THE QUESTION TYPE YOU WANT TO SOLVE:

    # solve_basic_flow_question()
    # solve_trapezoidal_question()
    # solve_circular_question()
    # solve_weir_question()
    # solve_sluice_gate_question()
    # solve_hydraulic_jump_question()
    # solve_rectangular_hydraulic_jump()
    # solve_gvf_question()
    # solve_channel_transition_question()

    # OR SOLVE YOUR OWN CUSTOM QUESTION:
    # Copy one of the functions above and modify the parameters

    print("\n" + "="*70)
    print("INSTRUCTIONS:")
    print("1. Uncomment the function for your question type")
    print("2. Modify the parameters to match your question")
    print("3. Run this script: python my_solutions/solve_any_question.py")
    print("="*70)

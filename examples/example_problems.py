"""
Example Problems Solver
========================
This file demonstrates how to use the open channel flow modules to solve
various types of problems from the assignment.

Author: Open Channel Flow Calculator
Date: August 2024
"""

import math
import numpy as np
from open_channel_flow.core.channel_geometry import *
from open_channel_flow.calculations.flow_calculations import *
from open_channel_flow.calculations.hydraulic_jump import *
from open_channel_flow.calculations.gradually_varied_flow import *
from open_channel_flow.calculations.weir_sluice import *


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(title)
    print("="*70)


def solve_question_1():
    """
    Question 1: Rectangular channel with varying slopes
    If the discharge in a channel of width 5 m is 20 m³/s and Manning's n is 0.02 m^(-1/3) s
    """
    print_section("QUESTION 1: Rectangular Channel - Normal and Critical Depths")

    # Given data
    width = 5.0  # m
    Q = 20.0  # m³/s
    n = 0.02  # m^(-1/3) s

    # Create channel
    channel = RectangularChannel(width)

    print(f"\nGiven:")
    print(f"  Width = {width} m")
    print(f"  Discharge = {Q} m³/s")
    print(f"  Manning's n = {n} m^(-1/3) s")

    # Part (a): Slope = 0.001
    S1 = 0.001
    print(f"\n(a) For slope S = {S1}:")

    y_n1 = normal_depth_manning(channel, Q, S1, n)
    Fr1 = froude_number(channel, y_n1, Q)

    print(f"  Normal depth = {y_n1:.3f} m")
    print(f"  Froude number = {Fr1:.3f}")
    print(f"  Flow regime: {flow_regime(Fr1)}")

    # Part (b): Slope = 0.01
    S2 = 0.01
    print(f"\n(b) For slope S = {S2}:")

    y_n2 = normal_depth_manning(channel, Q, S2, n)
    Fr2 = froude_number(channel, y_n2, Q)

    print(f"  Normal depth = {y_n2:.3f} m")
    print(f"  Froude number = {Fr2:.3f}")
    print(f"  Flow regime: {flow_regime(Fr2)}")

    # Part (c): Critical depth
    print(f"\n(c) Critical depth:")
    y_c = critical_depth(channel, Q)
    print(f"  Critical depth = {y_c:.3f} m")

    # Part (d): Critical slope
    print(f"\n(d) Critical slope:")
    S_c = critical_slope_manning(channel, Q, n, y_c)
    print(f"  Critical slope = {S_c:.6f}")

    return {
        'y_n1': y_n1, 'Fr1': Fr1,
        'y_n2': y_n2, 'Fr2': Fr2,
        'y_c': y_c, 'S_c': S_c
    }


def solve_question_2():
    """
    Question 2: Trapezoidal channel
    1600 mm deep, top width 3 m, bottom width 0.6 m, Q = 2.6 m³/s
    """
    print_section("QUESTION 2: Trapezoidal Channel")

    # Given data
    depth_total = 1.6  # m
    top_width = 3.0  # m
    bottom_width = 0.6  # m
    Q = 2.6  # m³/s
    n = 0.012  # m^(-1/3) s
    S = 1/2500  # slope

    # Calculate side slope: m = (T - b) / (2 * depth)
    side_slope = (top_width - bottom_width) / (2 * depth_total)

    # Create channel
    channel = TrapezoidalChannel(bottom_width, side_slope)

    print(f"\nGiven:")
    print(f"  Bottom width = {bottom_width} m")
    print(f"  Top width = {top_width} m")
    print(f"  Total depth = {depth_total} m")
    print(f"  Side slope m = {side_slope:.3f} (H:V)")
    print(f"  Discharge = {Q} m³/s")
    print(f"  Manning's n = {n} m^(-1/3) s")
    print(f"  Slope = 1/{int(1/S)}")

    # Part (a): Normal depth
    print(f"\n(a) Normal depth:")
    y_n = normal_depth_manning(channel, Q, S, n)
    print(f"  Normal depth = {y_n:.3f} m")

    # Part (b): Froude number at normal depth
    print(f"\n(b) Froude number at normal depth:")
    Fr_n = froude_number(channel, y_n, Q)
    print(f"  Froude number = {Fr_n:.3f}")
    print(f"  Flow regime: {flow_regime(Fr_n)}")

    # Part (c): Critical depth
    print(f"\n(c) Critical depth:")
    y_c = critical_depth(channel, Q)
    print(f"  Critical depth = {y_c:.3f} m")

    # Part (d): Critical slope
    print(f"\n(d) Critical slope:")
    S_c = critical_slope_manning(channel, Q, n, y_c)
    print(f"  Critical slope = {S_c:.6f} = 1/{int(1/S_c):.0f}")

    return {
        'y_n': y_n, 'Fr_n': Fr_n,
        'y_c': y_c, 'S_c': S_c
    }


def solve_question_3():
    """
    Question 3: Semi-circular channel
    Radius 0.7 m, Q = 0.8 m³/s, n = 0.013, slope = 2%
    """
    print_section("QUESTION 3: Circular Channel")

    # Given data
    radius = 0.7  # m
    diameter = 2 * radius
    Q = 0.8  # m³/s
    n = 0.013  # m^(-1/3) s
    S = 0.02  # 2%

    # Create channel
    channel = CircularChannel(diameter)

    print(f"\nGiven:")
    print(f"  Diameter = {diameter} m")
    print(f"  Radius = {radius} m")
    print(f"  Discharge = {Q} m³/s")
    print(f"  Manning's n = {n} m^(-1/3) s")
    print(f"  Slope = {S*100}%")

    # Part (a): Normal depth at slope 2%
    print(f"\n(a) Normal depth at slope {S*100}%:")
    y_n = normal_depth_manning(channel, Q, S, n)
    print(f"  Normal depth = {y_n:.3f} m")

    # Part (b): Froude number at normal depth
    print(f"\n(b) Froude number at normal depth:")
    Fr_n = froude_number(channel, y_n, Q)
    print(f"  Froude number = {Fr_n:.3f}")
    print(f"  Flow regime: {flow_regime(Fr_n)}")

    # Part (c): Critical depth
    print(f"\n(c) Critical depth:")
    y_c = critical_depth(channel, Q)
    print(f"  Critical depth = {y_c:.3f} m")

    return {
        'y_n': y_n, 'Fr_n': Fr_n,
        'y_c': y_c
    }


def solve_question_7():
    """
    Question 7: Broad-crested weir in wide channel
    """
    print_section("QUESTION 7: Broad-Crested Weir")

    # Given data
    S = 2e-4
    Q_per_width = 1.5  # m³/s per m width
    n = 0.015  # m^(-1/3) s

    # Wide channel (unit width)
    channel = WideChannel()
    Q = Q_per_width  # For unit width

    print(f"\nGiven:")
    print(f"  Slope = {S}")
    print(f"  Discharge = {Q_per_width} m³/s per m width")
    print(f"  Manning's n = {n} m^(-1/3) s")

    # Normal depth
    y_n = normal_depth_manning(channel, Q, S, n)
    print(f"  Normal depth = {y_n:.3f} m")

    # Critical depth
    y_c = critical_depth(channel, Q)
    print(f"  Critical depth = {y_c:.3f} m")

    # Part (a): Weir height = 0.2 m
    weir_h1 = 0.2
    print(f"\n(a) Weir height = {weir_h1} m:")

    # Upstream depth (assuming approach velocity negligible)
    # E_upstream = y_upstream
    # Over weir: E = y_upstream - weir_h
    # Critical flow: E = 1.5 * y_c
    E_over_weir = 1.5 * y_c
    y_upstream_1 = E_over_weir + weir_h1
    y_over_weir_1 = y_c

    print(f"  Upstream depth = {y_upstream_1:.3f} m")
    print(f"  Depth over weir = {y_over_weir_1:.3f} m")
    print(f"  Downstream depth = {y_n:.3f} m (returns to normal)")

    # Part (b): Weir height = 0.5 m
    weir_h2 = 0.5
    print(f"\n(b) Weir height = {weir_h2} m:")

    y_upstream_2 = E_over_weir + weir_h2
    y_over_weir_2 = y_c

    print(f"  Upstream depth = {y_upstream_2:.3f} m")
    print(f"  Depth over weir = {y_over_weir_2:.3f} m")
    print(f"  Downstream depth = {y_n:.3f} m (returns to normal)")

    # Part (c): Weir height for just critical flow
    print(f"\n(c) Weir height for just critical flow:")
    # When flow just goes critical, y_upstream = y_n
    # E_upstream = y_n + V_n²/(2g)
    E_upstream_normal = specific_energy(channel, y_n, Q)
    weir_h_critical = E_upstream_normal - 1.5 * y_c

    print(f"  Critical weir height = {weir_h_critical:.3f} m")

    return {
        'y_n': y_n, 'y_c': y_c,
        'case_a': {'y_upstream': y_upstream_1, 'y_over': y_over_weir_1},
        'case_b': {'y_upstream': y_upstream_2, 'y_over': y_over_weir_2},
        'weir_h_critical': weir_h_critical
    }


def solve_question_16():
    """
    Question 16: Sluice gate with hydraulic jump
    """
    print_section("QUESTION 16: Sluice Gate")

    # Given data
    width = 3.0  # m
    y1_upstream = 2.0  # m
    y2_downstream_gate = 0.3  # m

    # Create channel
    channel = RectangularChannel(width)

    print(f"\nGiven:")
    print(f"  Channel width = {width} m")
    print(f"  Upstream depth = {y1_upstream} m")
    print(f"  Downstream depth (at gate) = {y2_downstream_gate} m")

    # Part (a): Calculate discharge
    print(f"\n(a) Discharge:")
    Q = sluice_gate_discharge(channel, y1_upstream, y2_downstream_gate)
    print(f"  Discharge = {Q:.3f} m³/s")

    # Part (b): Normal depth
    S = 1/1000
    n = 0.014
    print(f"\n(b) Normal depth (slope = 1/{int(1/S)}, n = {n}):")
    y_n = normal_depth_manning(channel, Q, S, n)
    print(f"  Normal depth = {y_n:.3f} m")

    # Part (c): Force on blocks for hydraulic jump to normal depth
    print(f"\n(c) Hydraulic jump from gate to normal depth:")

    # Sequent depth without blocks
    y3_sequent = sequent_depth(channel, y2_downstream_gate, Q)
    print(f"  Natural sequent depth = {y3_sequent:.3f} m")

    # If blocks force jump to normal depth
    if y_n != y3_sequent:
        F_blocks = force_on_obstacle(channel, y2_downstream_gate, y_n, Q)
        print(f"  Force on blocks = {F_blocks/1000:.1f} kN")
    else:
        print(f"  No force needed (natural jump to normal depth)")

    return {
        'Q': Q, 'y_n': y_n,
        'y_sequent': y3_sequent
    }


def solve_question_25():
    """
    Question 25: Triangular channel with hydraulic jump
    """
    print_section("QUESTION 25: Triangular (V-shaped) Channel")

    # Given data
    semi_angle = 40  # degrees
    Q = 16.0  # m³/s

    # Create channel
    channel = TriangularChannel(semi_angle=semi_angle)

    print(f"\nGiven:")
    print(f"  Semi-angle = {semi_angle}°")
    print(f"  Discharge = {Q} m³/s")

    # Part (a): Critical depth
    print(f"\n(a) Critical depth:")
    y_c = critical_depth(channel, Q)
    print(f"  Critical depth = {y_c:.3f} m")

    # Part (b): Hydraulic jump
    y1 = 1.85  # m
    print(f"\n(b) Hydraulic jump with y1 = {y1} m:")

    y2 = sequent_depth_triangular(channel, y1, Q)
    print(f"  Sequent depth y2 = {y2:.3f} m")

    # Check which is upstream/downstream
    Fr1 = froude_number(channel, y1, Q)
    Fr2 = froude_number(channel, y2, Q)

    print(f"  Froude number at y1 = {Fr1:.3f} ({flow_regime(Fr1)})")
    print(f"  Froude number at y2 = {Fr2:.3f} ({flow_regime(Fr2)})")

    return {
        'y_c': y_c,
        'y1': y1, 'y2': y2,
        'Fr1': Fr1, 'Fr2': Fr2
    }


def solve_question_29():
    """
    Question 29: GVF - Free overfall with gradually varied flow
    """
    print_section("QUESTION 29: Gradually Varied Flow - Free Overfall")

    # Given data
    S = 2e-5
    n = 0.01
    Q_per_width = 0.5  # m³/s per m width

    # Wide channel
    channel = WideChannel()
    Q = Q_per_width

    print(f"\nGiven:")
    print(f"  Slope = {S}")
    print(f"  Manning's n = {n} m^(-1/3) s")
    print(f"  Discharge = {Q_per_width} m³/s per m width")

    # Normal depth
    y_n = normal_depth_manning(channel, Q, S, n)
    print(f"  Normal depth = {y_n:.3f} m")

    # Critical depth
    y_c = critical_depth(channel, Q)
    print(f"  Critical depth = {y_c:.3f} m")

    # Depth at overfall (approximately 0.715 * y_c)
    y_overfall = 0.715 * y_c
    print(f"  Depth at overfall = {y_overfall:.3f} m")

    # Distance from overfall to y = 1.0 m
    y_target = 1.0
    print(f"\nCalculating distance from overfall to depth = {y_target} m")

    # Using 2 steps
    print(f"\nUsing 2 steps:")
    dist_2 = distance_to_depth_manning(channel, Q, S, n, y_overfall, y_target, num_steps=2)
    print(f"  Distance = {dist_2:.2f} m")

    # Using different number of steps
    for num_steps in [5, 10, 50, 100]:
        dist = distance_to_depth_manning(channel, Q, S, n, y_overfall, y_target, num_steps=num_steps)
        print(f"Using {num_steps} steps: Distance = {dist:.2f} m")

    return {
        'y_n': y_n, 'y_c': y_c,
        'y_overfall': y_overfall,
        'distance_2_steps': dist_2
    }


def main():
    """Run example problems"""
    print("\n" + "="*70)
    print("OPEN CHANNEL FLOW - EXAMPLE PROBLEMS")
    print("="*70)

    # Solve selected questions
    results = {}

    results['q1'] = solve_question_1()
    results['q2'] = solve_question_2()
    results['q3'] = solve_question_3()
    results['q7'] = solve_question_7()
    results['q16'] = solve_question_16()
    results['q25'] = solve_question_25()
    results['q29'] = solve_question_29()

    print("\n" + "="*70)
    print("ALL EXAMPLE PROBLEMS COMPLETED")
    print("="*70)

    return results


if __name__ == "__main__":
    results = main()

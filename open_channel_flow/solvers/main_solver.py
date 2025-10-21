"""
Main Open Channel Flow Solver
==============================
Comprehensive solver for all types of open channel flow problems.
This is the main entry point for solving problems from the assignment.

Author: Open Channel Flow Calculator
Date: August 2024

Usage:
    python main_solver.py

"""

import math
import numpy as np
from open_channel_flow.core.channel_geometry import *
from open_channel_flow.calculations.flow_calculations import *
from open_channel_flow.calculations.hydraulic_jump import *
from open_channel_flow.calculations.gradually_varied_flow import *
from open_channel_flow.calculations.weir_sluice import *


class OpenChannelSolver:
    """Main solver class for open channel flow problems"""

    def __init__(self):
        self.g = 9.81  # m/s²

    def solve_basic_flow_problem(self, channel_type, channel_params, Q, S, n=None, C=None):
        """
        Solve basic flow problem: normal depth, critical depth, Froude number, etc.

        Parameters:
        -----------
        channel_type : str
            'rectangular', 'trapezoidal', 'circular', 'triangular', 'wide'
        channel_params : dict
            Parameters specific to channel type
        Q : float
            Discharge (m³/s)
        S : float or list
            Slope(s) (dimensionless)
        n : float, optional
            Manning's roughness coefficient (m^(-1/3) s)
        C : float, optional
            Chezy coefficient (m^(1/2) s^(-1))

        Returns:
        --------
        dict : Results containing depths, Froude numbers, slopes, etc.
        """
        # Create channel
        channel = self._create_channel(channel_type, channel_params)

        results = {
            'channel_type': channel_type,
            'discharge': Q
        }

        # Critical depth (independent of slope)
        y_c = critical_depth(channel, Q)
        results['critical_depth'] = y_c

        # Process slopes (can be single value or list)
        if not isinstance(S, list):
            S = [S]

        for i, slope in enumerate(S):
            slope_results = {}

            # Normal depth
            if n is not None:
                y_n = normal_depth_manning(channel, Q, slope, n)
                slope_results['normal_depth'] = y_n

                # Froude number at normal depth
                Fr_n = froude_number(channel, y_n, Q)
                slope_results['froude_number'] = Fr_n
                slope_results['flow_regime'] = flow_regime(Fr_n)

            elif C is not None:
                y_n = normal_depth_chezy(channel, Q, slope, C)
                slope_results['normal_depth'] = y_n

                Fr_n = froude_number(channel, y_n, Q)
                slope_results['froude_number'] = Fr_n
                slope_results['flow_regime'] = flow_regime(Fr_n)

            results[f'slope_{i+1}'] = slope_results

        # Critical slope
        if n is not None:
            S_c = critical_slope_manning(channel, Q, n, y_c)
        elif C is not None:
            S_c = critical_slope_chezy(channel, Q, C, y_c)
        else:
            S_c = None

        results['critical_slope'] = S_c

        return results

    def solve_weir_problem(self, channel_type, channel_params, Q, S, n,
                           weir_height, problem_type='depths'):
        """
        Solve broad-crested weir problems

        Parameters:
        -----------
        channel_type : str
            Channel type
        channel_params : dict
            Channel parameters
        Q : float
            Discharge (m³/s)
        S : float
            Channel slope
        n : float
            Manning's roughness coefficient
        weir_height : float or str
            Weir height (m) or 'find' to calculate height for critical flow
        problem_type : str
            'depths' or 'find_height'

        Returns:
        --------
        dict : Results
        """
        channel = self._create_channel(channel_type, channel_params)

        results = {}

        # Normal and critical depths
        y_n = normal_depth_manning(channel, Q, S, n)
        y_c = critical_depth(channel, Q)
        S_c = critical_slope_manning(channel, Q, n, y_c)

        results['normal_depth'] = y_n
        results['critical_depth'] = y_c
        results['slope_classification'] = slope_classification(S, S_c)

        if problem_type == 'find_height':
            # Find weir height for critical flow
            E_normal = specific_energy(channel, y_n, Q)
            E_critical = 1.5 * y_c
            weir_height = E_normal - E_critical
            results['weir_height_for_critical'] = weir_height
        else:
            # Calculate depths for given weir height
            y_upstream = weir_upstream_depth(channel, Q, weir_height, y_n)
            y_over_weir = weir_depth_over_crest(channel, Q, weir_height,
                                                 specific_energy(channel, y_upstream, Q))
            y_downstream = y_n  # Returns to normal flow

            results['weir_height'] = weir_height
            results['upstream_depth'] = y_upstream
            results['depth_over_weir'] = y_over_weir
            results['downstream_depth'] = y_downstream

        return results

    def solve_sluice_gate_problem(self, channel_type, channel_params,
                                   y_upstream=None, y_downstream=None, Q=None,
                                   S=None, n=None, find_force=False):
        """
        Solve sluice gate problems

        Parameters:
        -----------
        channel_type : str
            Channel type
        channel_params : dict
            Channel parameters
        y_upstream : float, optional
            Upstream depth (m)
        y_downstream : float, optional
            Downstream depth at gate (m)
        Q : float, optional
            Discharge (m³/s)
        S : float, optional
            Channel slope
        n : float, optional
            Manning's roughness coefficient
        find_force : bool
            Whether to calculate force on gate

        Returns:
        --------
        dict : Results
        """
        channel = self._create_channel(channel_type, channel_params)

        results = {}

        # Calculate discharge if not given
        if Q is None and y_upstream is not None and y_downstream is not None:
            Q = sluice_gate_discharge(channel, y_upstream, y_downstream)
            results['discharge'] = Q

        # Calculate depths if not fully specified
        if y_upstream is None and Q is not None and y_downstream is not None:
            y_upstream = sluice_gate_upstream_depth(channel, Q, y_downstream)
            results['upstream_depth'] = y_upstream

        if y_downstream is None and Q is not None and y_upstream is not None:
            y_downstream = sluice_gate_downstream_depth(channel, Q, y_upstream)
            results['downstream_depth'] = y_downstream

        # Calculate Froude numbers
        if Q is not None and y_upstream is not None:
            Fr_up = froude_number(channel, y_upstream, Q)
            results['froude_upstream'] = Fr_up

        if Q is not None and y_downstream is not None:
            Fr_down = froude_number(channel, y_downstream, Q)
            results['froude_downstream'] = Fr_down

        # Calculate force on gate if requested
        if find_force and Q is not None and y_upstream is not None and y_downstream is not None:
            F = sluice_gate_force(channel, y_upstream, y_downstream, Q)
            results['force_on_gate'] = F

        # Calculate normal and critical depths if slope given
        if S is not None and n is not None and Q is not None:
            y_n = normal_depth_manning(channel, Q, S, n)
            y_c = critical_depth(channel, Q)
            results['normal_depth'] = y_n
            results['critical_depth'] = y_c

        return results

    def solve_hydraulic_jump_problem(self, channel_type, channel_params, Q,
                                     y1=None, y2=None, find_sequent=True,
                                     find_energy_loss=True):
        """
        Solve hydraulic jump problems

        Parameters:
        -----------
        channel_type : str
            Channel type
        channel_params : dict
            Channel parameters
        Q : float
            Discharge (m³/s)
        y1 : float, optional
            Upstream depth (m)
        y2 : float, optional
            Downstream depth (m)
        find_sequent : bool
            Calculate sequent depth
        find_energy_loss : bool
            Calculate energy loss

        Returns:
        --------
        dict : Results
        """
        channel = self._create_channel(channel_type, channel_params)

        results = {
            'discharge': Q
        }

        if y1 is not None:
            results['depth_1'] = y1
            Fr1 = froude_number(channel, y1, Q)
            results['froude_1'] = Fr1

            if find_sequent:
                y2_calc = sequent_depth(channel, y1, Q)
                results['sequent_depth'] = y2_calc

                if find_energy_loss:
                    dE = energy_loss_jump(channel, y1, y2_calc, Q)
                    frac = energy_loss_fraction(channel, y1, y2_calc, Q)
                    results['energy_loss'] = dE
                    results['energy_loss_fraction'] = frac

        if y2 is not None and 'sequent_depth' not in results:
            results['depth_2'] = y2
            Fr2 = froude_number(channel, y2, Q)
            results['froude_2'] = Fr2

        return results

    def solve_gvf_problem(self, channel_type, channel_params, Q, S, n,
                          y_start, y_target, num_steps=100):
        """
        Solve gradually varied flow problem

        Parameters:
        -----------
        channel_type : str
            Channel type
        channel_params : dict
            Channel parameters
        Q : float
            Discharge (m³/s)
        S : float
            Bed slope
        n : float
            Manning's roughness coefficient
        y_start : float
            Starting depth (m)
        y_target : float
            Target depth (m)
        num_steps : int
            Number of computation steps

        Returns:
        --------
        dict : Results including distance
        """
        channel = self._create_channel(channel_type, channel_params)

        results = {
            'discharge': Q,
            'slope': S,
            'manning_n': n,
            'start_depth': y_start,
            'target_depth': y_target
        }

        # Normal and critical depths
        y_n = normal_depth_manning(channel, Q, S, n)
        y_c = critical_depth(channel, Q)
        S_c = critical_slope_manning(channel, Q, n, y_c)

        results['normal_depth'] = y_n
        results['critical_depth'] = y_c
        results['critical_slope'] = S_c
        results['slope_classification'] = slope_classification(S, S_c)

        # GVF curve classification
        gvf_curve = classify_gvf_curve(S, S_c, y_start, y_n, y_c)
        results['gvf_curve'] = gvf_curve

        # Calculate distance
        distance = distance_to_depth_manning(channel, Q, S, n, y_start, y_target, num_steps)
        results['distance'] = distance

        return results

    def solve_channel_transition(self, channel1_type, channel1_params,
                                  channel2_type, channel2_params,
                                  Q, y_approach, bed_change=0):
        """
        Solve channel transition (contraction/expansion) problem

        Parameters:
        -----------
        channel1_type : str
            Upstream channel type
        channel1_params : dict
            Upstream channel parameters
        channel2_type : str
            Transition section channel type
        channel2_params : dict
            Transition section channel parameters
        Q : float
            Discharge (m³/s)
        y_approach : float
            Approach depth (m)
        bed_change : float
            Change in bed level (positive = rise, negative = drop)

        Returns:
        --------
        dict : Results
        """
        channel1 = self._create_channel(channel1_type, channel1_params)
        channel2 = self._create_channel(channel2_type, channel2_params)

        results = {
            'discharge': Q,
            'approach_depth': y_approach
        }

        # Energy at approach
        E_approach = specific_energy(channel1, y_approach, Q)
        results['approach_energy'] = E_approach

        # Available energy in transition
        E_transition = E_approach - bed_change

        # Critical conditions in transition
        y_c2 = critical_depth(channel2, Q)
        E_c2 = specific_energy(channel2, y_c2, Q)

        results['critical_depth_transition'] = y_c2
        results['critical_energy_transition'] = E_c2

        # Check if flow goes critical
        if E_transition >= E_c2:
            results['flow_goes_critical'] = True
            results['depth_in_transition'] = y_c2
        else:
            results['flow_goes_critical'] = False
            # Flow remains subcritical
            from scipy.optimize import brentq
            def eq(y):
                return specific_energy(channel2, y, Q) - E_transition
            try:
                y_transition = brentq(eq, y_c2, E_transition*2)
                results['depth_in_transition'] = y_transition
            except:
                results['depth_in_transition'] = None

        return results

    def _create_channel(self, channel_type, params):
        """
        Factory method to create channel object

        Parameters:
        -----------
        channel_type : str
            Type of channel
        params : dict
            Channel parameters

        Returns:
        --------
        ChannelSection : Channel object
        """
        if channel_type == 'rectangular':
            return RectangularChannel(params['width'])

        elif channel_type == 'trapezoidal':
            return TrapezoidalChannel(params['bottom_width'], params['side_slope'])

        elif channel_type == 'circular':
            return CircularChannel(params['diameter'])

        elif channel_type == 'triangular':
            if 'side_slope' in params:
                return TriangularChannel(side_slope=params['side_slope'])
            else:
                return TriangularChannel(semi_angle=params['semi_angle'])

        elif channel_type == 'wide':
            return WideChannel()

        elif channel_type == 'compound':
            return CompoundChannel(
                params['bottom_section_type'],
                params['bottom_params'],
                params['break_depth'],
                params.get('top_section_type'),
                params.get('top_params')
            )

        else:
            raise ValueError(f"Unknown channel type: {channel_type}")

    def print_results(self, results, title="Results"):
        """Pretty print results"""
        print("\n" + "="*70)
        print(title)
        print("="*70)

        for key, value in results.items():
            if isinstance(value, dict):
                print(f"\n{key}:")
                for k, v in value.items():
                    if isinstance(v, (int, float)):
                        print(f"  {k}: {v:.4f}")
                    else:
                        print(f"  {k}: {v}")
            elif isinstance(value, (int, float)):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")


# Example usage functions for each problem type
def example_rectangular_channel():
    """Example: Basic rectangular channel problem"""
    solver = OpenChannelSolver()

    results = solver.solve_basic_flow_problem(
        channel_type='rectangular',
        channel_params={'width': 5.0},
        Q=20.0,
        S=[0.001, 0.01],
        n=0.02
    )

    solver.print_results(results, "Rectangular Channel - Question 1")
    return results


def example_trapezoidal_channel():
    """Example: Trapezoidal channel problem"""
    solver = OpenChannelSolver()

    results = solver.solve_basic_flow_problem(
        channel_type='trapezoidal',
        channel_params={'bottom_width': 0.6, 'side_slope': 0.75},
        Q=2.6,
        S=1/2500,
        n=0.012
    )

    solver.print_results(results, "Trapezoidal Channel - Question 2")
    return results


def example_weir():
    """Example: Broad-crested weir problem"""
    solver = OpenChannelSolver()

    results = solver.solve_weir_problem(
        channel_type='wide',
        channel_params={},
        Q=1.5,
        S=2e-4,
        n=0.015,
        weir_height=0.2,
        problem_type='depths'
    )

    solver.print_results(results, "Broad-Crested Weir - Question 7")
    return results


def example_sluice_gate():
    """Example: Sluice gate problem"""
    solver = OpenChannelSolver()

    results = solver.solve_sluice_gate_problem(
        channel_type='rectangular',
        channel_params={'width': 3.0},
        y_upstream=2.0,
        y_downstream=0.3,
        S=1/1000,
        n=0.014,
        find_force=True
    )

    solver.print_results(results, "Sluice Gate - Question 16")
    return results


def example_hydraulic_jump():
    """Example: Hydraulic jump problem"""
    solver = OpenChannelSolver()

    results = solver.solve_hydraulic_jump_problem(
        channel_type='triangular',
        channel_params={'semi_angle': 40},
        Q=16.0,
        y1=1.85,
        find_sequent=True,
        find_energy_loss=True
    )

    solver.print_results(results, "Hydraulic Jump - Question 25")
    return results


def example_gvf():
    """Example: Gradually varied flow problem"""
    solver = OpenChannelSolver()

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

    solver.print_results(results, "Gradually Varied Flow - Question 29")
    return results


def main():
    """Main function to demonstrate solver capabilities"""
    print("\n" + "="*70)
    print("OPEN CHANNEL FLOW SOLVER - COMPREHENSIVE TOOL")
    print("="*70)
    print("\nThis solver can handle:")
    print("  1. Basic flow calculations (normal depth, critical depth, Froude number)")
    print("  2. Broad-crested weir problems")
    print("  3. Sluice gate problems")
    print("  4. Hydraulic jump calculations")
    print("  5. Gradually varied flow (GVF) analysis")
    print("  6. Channel transitions")
    print("\nRunning example problems...")

    # Run examples
    example_rectangular_channel()
    example_trapezoidal_channel()
    example_weir()
    example_sluice_gate()
    example_hydraulic_jump()
    example_gvf()

    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()

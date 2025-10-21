"""
Open Channel Flow Analysis Package
====================================

A comprehensive Python package for open channel flow calculations.

Modules:
--------
- core: Channel geometry definitions
- calculations: Flow calculations, hydraulic jumps, GVF
- solvers: High-level solver interfaces

Author: Open Channel Flow Calculator
Date: August 2024
"""

__version__ = "1.0.0"
__author__ = "Open Channel Flow Calculator"

# Import main classes and functions for easy access
from open_channel_flow.core.channel_geometry import (
    ChannelSection,
    RectangularChannel,
    TrapezoidalChannel,
    CircularChannel,
    TriangularChannel,
    CompoundChannel,
    WideChannel
)

from open_channel_flow.calculations.flow_calculations import (
    normal_depth_manning,
    normal_depth_chezy,
    critical_depth,
    critical_slope_manning,
    critical_slope_chezy,
    froude_number,
    flow_regime,
    specific_energy,
    slope_classification
)

from open_channel_flow.calculations.hydraulic_jump import (
    sequent_depth,
    energy_loss_jump,
    energy_loss_fraction,
    force_on_obstacle
)

from open_channel_flow.calculations.gradually_varied_flow import (
    solve_gvf_profile_manning,
    distance_to_depth_manning,
    classify_gvf_curve
)

from open_channel_flow.calculations.weir_sluice import (
    weir_upstream_depth,
    weir_depth_over_crest,
    sluice_gate_discharge,
    sluice_gate_force,
    free_overfall_depth
)

from open_channel_flow.solvers.main_solver import OpenChannelSolver

__all__ = [
    # Channel classes
    'ChannelSection',
    'RectangularChannel',
    'TrapezoidalChannel',
    'CircularChannel',
    'TriangularChannel',
    'CompoundChannel',
    'WideChannel',

    # Flow calculations
    'normal_depth_manning',
    'normal_depth_chezy',
    'critical_depth',
    'critical_slope_manning',
    'critical_slope_chezy',
    'froude_number',
    'flow_regime',
    'specific_energy',
    'slope_classification',

    # Hydraulic jump
    'sequent_depth',
    'energy_loss_jump',
    'energy_loss_fraction',
    'force_on_obstacle',

    # GVF
    'solve_gvf_profile_manning',
    'distance_to_depth_manning',
    'classify_gvf_curve',

    # Weir and sluice
    'weir_upstream_depth',
    'weir_depth_over_crest',
    'sluice_gate_discharge',
    'sluice_gate_force',
    'free_overfall_depth',

    # Solver
    'OpenChannelSolver',
]

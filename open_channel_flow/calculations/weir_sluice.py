"""
Weir and Sluice Gate Module
============================
This module provides functions for analyzing flow over weirs and under sluice gates:
- Broad-crested weir calculations
- Sluice gate flow
- Critical flow transitions
- Energy calculations

Author: Open Channel Flow Calculator
Date: August 2024
"""

import math
import numpy as np
from scipy.optimize import fsolve, brentq
from open_channel_flow.core.channel_geometry import ChannelSection
from open_channel_flow.calculations.flow_calculations import critical_depth, specific_energy


# Physical constants
g = 9.81  # Acceleration due to gravity (m/s^2)


def broad_crested_weir_discharge(channel, y_upstream, weir_height):
    """
    Calculate discharge over a broad-crested weir
    Assumes critical flow over the weir

    For wide channels: Q = (2/3) * sqrt(2*g/3) * b * H^(3/2)
    where H = y_upstream - weir_height

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y_upstream : float
        Depth upstream of weir (m)
    weir_height : float
        Height of weir above channel bed (m)

    Returns:
    --------
    float : Discharge (m^3/s)
    """
    # Energy upstream
    E_upstream = y_upstream  # Assuming velocity head negligible upstream

    # Energy over weir (relative to weir crest)
    E_crest = E_upstream - weir_height

    # At critical flow: E = (3/2) * y_c
    # So: y_c = (2/3) * E
    y_c_crest = (2/3) * E_crest

    # Critical flow equation for discharge
    # This is approximate - actual calculation should use channel geometry
    from flow_calculations import specific_energy

    def find_Q(Q_trial):
        y_c = critical_depth(channel, Q_trial)
        E_c = specific_energy(channel, y_c, Q_trial)
        return E_c - E_crest

    try:
        Q = brentq(find_Q, 0.001, 100)
        return Q
    except:
        result = fsolve(find_Q, 1.0)
        return abs(result[0])


def weir_depth_over_crest(channel, Q, weir_height, E_upstream):
    """
    Calculate depth over the crest of a broad-crested weir

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    weir_height : float
        Height of weir above channel bed (m)
    E_upstream : float
        Specific energy upstream (relative to channel bed) (m)

    Returns:
    --------
    float : Depth over crest (m)
    """
    # Energy over crest (relative to weir top)
    E_crest = E_upstream - weir_height

    # Find depth that gives this energy
    y_c = critical_depth(channel, Q)

    # For critical flow over weir, depth should be approximately y_c
    # But we need to satisfy energy equation
    def equation(y):
        if y <= 0:
            return 1e10
        E = specific_energy(channel, y, Q)
        return E - E_crest

    try:
        y_over_crest = brentq(equation, 0.001, E_crest)
        return y_over_crest
    except:
        result = fsolve(equation, y_c)
        return abs(result[0])


def weir_upstream_depth(channel, Q, weir_height, normal_depth=None):
    """
    Calculate upstream depth for flow over a broad-crested weir

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    weir_height : float
        Height of weir above channel bed (m)
    normal_depth : float, optional
        Normal depth in channel (m)

    Returns:
    --------
    float : Upstream depth (m)
    """
    # Critical depth
    y_c = critical_depth(channel, Q)

    # Energy at critical depth (relative to weir crest)
    E_c = (3/2) * y_c

    # Energy upstream (relative to channel bed)
    E_upstream = E_c + weir_height

    # Find subcritical depth that gives this energy
    def equation(y):
        if y <= weir_height:
            return 1e10
        E = specific_energy(channel, y, Q)
        return E - E_upstream

    try:
        # Subcritical depth is > y_c
        y_upstream = brentq(equation, weir_height + y_c, E_upstream * 2)
        return y_upstream
    except:
        initial_guess = weir_height + y_c * 1.5
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def weir_downstream_depth(channel, Q, weir_height, normal_depth):
    """
    Calculate downstream depth after flow over a broad-crested weir
    (when returning to normal flow or based on downstream control)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    weir_height : float
        Height of weir above channel bed (m)
    normal_depth : float
        Normal depth in downstream channel (m)

    Returns:
    --------
    float : Downstream depth (m)
    """
    # Typically downstream depth is normal depth if no other control
    return normal_depth


def sluice_gate_discharge(channel, y_upstream, y_downstream, gate_opening=None,
                           energy_loss_coeff=0.0):
    """
    Calculate discharge under a sluice gate
    Uses Bernoulli equation with energy loss

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y_upstream : float
        Upstream depth (m)
    y_downstream : float
        Downstream depth (just after gate) (m)
    gate_opening : float, optional
        Gate opening height (m) - if None, uses y_downstream
    energy_loss_coeff : float
        Energy loss coefficient (typically 0-0.1)

    Returns:
    --------
    float : Discharge (m^3/s)
    """
    A_up = channel.area(y_upstream)
    A_down = channel.area(y_downstream)

    # Energy equation (neglecting upstream velocity)
    # y1 = y2 + V2^2/(2g) * (1 + loss_coeff)
    # Q = A2 * V2

    # Solving for V2:
    # V2 = sqrt(2*g*(y1 - y2) / (1 + loss_coeff))

    if y_upstream <= y_downstream:
        return 0

    V2 = math.sqrt(2 * g * (y_upstream - y_downstream) / (1 + energy_loss_coeff))
    Q = A_down * V2

    return Q


def sluice_gate_upstream_depth(channel, Q, y_downstream):
    """
    Calculate upstream depth for given discharge and downstream depth

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    y_downstream : float
        Downstream depth (m)

    Returns:
    --------
    float : Upstream depth (m)
    """
    # Energy equation: E1 = E2 (assuming no energy loss)
    E2 = specific_energy(channel, y_downstream, Q)

    # Find subcritical depth upstream that gives same energy
    def equation(y):
        if y <= y_downstream:
            return 1e10
        E1 = specific_energy(channel, y, Q)
        return E1 - E2

    try:
        y_c = critical_depth(channel, Q)
        y_upstream = brentq(equation, max(y_c, y_downstream), E2 * 2)
        return y_upstream
    except:
        initial_guess = y_downstream * 3
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def sluice_gate_downstream_depth(channel, Q, y_upstream):
    """
    Calculate downstream depth (just after gate) for given discharge and upstream depth

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    y_upstream : float
        Upstream depth (m)

    Returns:
    --------
    float : Downstream depth (m)
    """
    # Energy equation: E1 = E2 (assuming no energy loss)
    E1 = specific_energy(channel, y_upstream, Q)

    # Find supercritical depth downstream that gives same energy
    def equation(y):
        if y <= 0 or y >= y_upstream:
            return 1e10
        E2 = specific_energy(channel, y, Q)
        return E2 - E1

    try:
        y_c = critical_depth(channel, Q)
        y_downstream = brentq(equation, 0.001, y_c)
        return y_downstream
    except:
        initial_guess = y_upstream * 0.3
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def sluice_gate_force(channel, y_upstream, y_downstream, Q):
    """
    Calculate force on sluice gate
    Uses momentum equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y_upstream : float
        Upstream depth (m)
    y_downstream : float
        Downstream depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Force on gate (N)
    """
    rho = 1000  # Water density (kg/m^3)

    A1 = channel.area(y_upstream)
    A2 = channel.area(y_downstream)

    V1 = Q / A1 if A1 > 0 else 0
    V2 = Q / A2 if A2 > 0 else 0

    # Momentum equation
    # F = rho*Q*(V1 - V2) + rho*g*(A1*ybar1 - A2*ybar2)

    momentum_change = rho * Q * (V1 - V2)

    # Pressure force (using hydraulic depth approximation)
    D1 = channel.hydraulic_depth(y_upstream)
    D2 = channel.hydraulic_depth(y_downstream)

    pressure_change = rho * g * (A1 * D1/2 - A2 * D2/2)

    F = momentum_change + pressure_change
    return F


def critical_flow_over_obstacle(channel, Q, obstacle_height, E_upstream):
    """
    Check if flow goes critical over an obstacle (weir or rise in bed)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    obstacle_height : float
        Height of obstacle (m)
    E_upstream : float
        Specific energy upstream (m)

    Returns:
    --------
    tuple : (is_critical, y_over_obstacle)
        is_critical : bool - True if flow is critical over obstacle
        y_over_obstacle : float - depth over obstacle (m)
    """
    y_c = critical_depth(channel, Q)
    E_c = specific_energy(channel, y_c, Q)

    # Energy over obstacle (relative to obstacle top)
    E_over = E_upstream - obstacle_height

    # Minimum energy for critical flow
    E_c_min = (3/2) * y_c

    if E_over >= E_c_min:
        # Flow can go critical
        # Depth over obstacle is critical depth
        return True, y_c
    else:
        # Flow cannot go critical - depth increases
        # Find subcritical depth that satisfies energy
        def equation(y):
            if y <= 0:
                return 1e10
            E = specific_energy(channel, y, Q)
            return E - E_over

        try:
            y_over = brentq(equation, 0.001, E_over * 2)
            return False, y_over
        except:
            return False, None


def free_overfall_depth(channel, Q):
    """
    Calculate depth at a free overfall (end of channel)
    At overfall, depth is approximately 71.5% of critical depth

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Depth at overfall (m)
    """
    y_c = critical_depth(channel, Q)
    y_overfall = 0.715 * y_c
    return y_overfall


def drowned_condition(y_downstream, y_sequent):
    """
    Check if a hydraulic structure (weir, gate) is drowned

    Parameters:
    -----------
    y_downstream : float
        Actual downstream depth (m)
    y_sequent : float
        Sequent depth for hydraulic jump (m)

    Returns:
    --------
    bool : True if structure is drowned
    """
    return y_downstream > y_sequent


def contraction_expansion(channel1, channel2, Q, y_approach, transition_type='contraction'):
    """
    Calculate flow through contraction or expansion

    Parameters:
    -----------
    channel1 : ChannelSection
        Upstream channel object
    channel2 : ChannelSection
        Contracted/expanded channel object
    Q : float
        Discharge (m^3/s)
    y_approach : float
        Approach depth (m)
    transition_type : str
        'contraction' or 'expansion'

    Returns:
    --------
    tuple : (y_in_transition, is_critical)
    """
    E_approach = specific_energy(channel1, y_approach, Q)

    # Check if flow goes critical in transition
    y_c2 = critical_depth(channel2, Q)
    E_c2 = specific_energy(channel2, y_c2, Q)

    if E_approach >= E_c2:
        # Flow can go critical
        return y_c2, True
    else:
        # Flow remains subcritical
        def equation(y):
            if y <= 0:
                return 1e10
            E = specific_energy(channel2, y, Q)
            return E - E_approach

        try:
            y_transition = brentq(equation, y_c2, E_approach * 2)
            return y_transition, False
        except:
            result = fsolve(equation, y_approach)
            return abs(result[0]), False

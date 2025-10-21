"""
Gradually Varied Flow (GVF) Module
===================================
This module provides functions for analyzing gradually varied flow:
- GVF differential equation solver
- Water surface profile computation
- GVF curve classification (M1, M2, S1, S2, etc.)

Author: Open Channel Flow Calculator
Date: August 2024
"""

import math
import numpy as np
from open_channel_flow.core.channel_geometry import ChannelSection
from open_channel_flow.calculations.flow_calculations import (froude_number, manning_discharge, chezy_discharge,
                                                               normal_depth_manning, critical_depth)


# Physical constants
g = 9.81  # Acceleration due to gravity (m/s^2)


def gvf_derivative_manning(channel, y, Q, S0, n):
    """
    Calculate dy/dx for gradually varied flow using Manning's equation

    dy/dx = (S0 - Sf) / (1 - Fr^2)

    where:
    - S0 is bed slope
    - Sf is friction slope (from Manning's equation)
    - Fr is Froude number

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y : float
        Current depth (m)
    Q : float
        Discharge (m^3/s)
    S0 : float
        Bed slope (dimensionless)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)

    Returns:
    --------
    float : dy/dx (dimensionless)
    """
    if y <= 0:
        return 0

    A = channel.area(y)
    R = channel.hydraulic_radius(y)
    T = channel.top_width(y)

    if A == 0 or T == 0:
        return 0

    V = Q / A

    # Friction slope from Manning's equation
    # Sf = (n*V / R^(2/3))^2
    Sf = (n * V / (R ** (2/3))) ** 2

    # Froude number
    D = channel.hydraulic_depth(y)
    if D <= 0:
        Fr = float('inf')
    else:
        Fr = V / math.sqrt(g * D)

    # GVF equation
    numerator = S0 - Sf
    denominator = 1 - Fr**2

    if abs(denominator) < 1e-10:  # Near critical depth
        return 0

    return numerator / denominator


def gvf_derivative_chezy(channel, y, Q, S0, C):
    """
    Calculate dy/dx for gradually varied flow using Chezy equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y : float
        Current depth (m)
    Q : float
        Discharge (m^3/s)
    S0 : float
        Bed slope (dimensionless)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))

    Returns:
    --------
    float : dy/dx (dimensionless)
    """
    if y <= 0:
        return 0

    A = channel.area(y)
    R = channel.hydraulic_radius(y)
    T = channel.top_width(y)

    if A == 0 or T == 0:
        return 0

    V = Q / A

    # Friction slope from Chezy equation
    # Sf = V^2 / (C^2 * R)
    Sf = V**2 / (C**2 * R)

    # Froude number
    D = channel.hydraulic_depth(y)
    if D <= 0:
        Fr = float('inf')
    else:
        Fr = V / math.sqrt(g * D)

    # GVF equation
    numerator = S0 - Sf
    denominator = 1 - Fr**2

    if abs(denominator) < 1e-10:  # Near critical depth
        return 0

    return numerator / denominator


def solve_gvf_profile_manning(channel, Q, S0, n, y_start, distance, num_steps,
                               direction='downstream'):
    """
    Solve water surface profile using gradually varied flow equation
    Uses simple step method (Euler method)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    S0 : float
        Bed slope (dimensionless)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)
    y_start : float
        Starting depth (m)
    distance : float
        Total distance to compute (m)
    num_steps : int
        Number of computation steps
    direction : str
        'downstream' or 'upstream'

    Returns:
    --------
    tuple : (x_array, y_array) - arrays of positions and depths
    """
    dx = distance / num_steps

    if direction == 'upstream':
        dx = -dx

    x = np.zeros(num_steps + 1)
    y = np.zeros(num_steps + 1)

    x[0] = 0
    y[0] = y_start

    for i in range(num_steps):
        dy_dx = gvf_derivative_manning(channel, y[i], Q, S0, n)

        y[i+1] = y[i] + dy_dx * dx
        x[i+1] = x[i] + dx

        # Ensure depth stays positive
        if y[i+1] < 0.001:
            y[i+1] = 0.001

    return x, y


def solve_gvf_profile_chezy(channel, Q, S0, C, y_start, distance, num_steps,
                             direction='downstream'):
    """
    Solve water surface profile using Chezy equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    S0 : float
        Bed slope (dimensionless)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))
    y_start : float
        Starting depth (m)
    distance : float
        Total distance to compute (m)
    num_steps : int
        Number of computation steps
    direction : str
        'downstream' or 'upstream'

    Returns:
    --------
    tuple : (x_array, y_array) - arrays of positions and depths
    """
    dx = distance / num_steps

    if direction == 'upstream':
        dx = -dx

    x = np.zeros(num_steps + 1)
    y = np.zeros(num_steps + 1)

    x[0] = 0
    y[0] = y_start

    for i in range(num_steps):
        dy_dx = gvf_derivative_chezy(channel, y[i], Q, S0, C)

        y[i+1] = y[i] + dy_dx * dx
        x[i+1] = x[i] + dx

        # Ensure depth stays positive
        if y[i+1] < 0.001:
            y[i+1] = 0.001

    return x, y


def distance_to_depth_manning(channel, Q, S0, n, y_start, y_target, num_steps=100,
                               max_distance=10000):
    """
    Calculate distance from y_start to y_target using GVF equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    S0 : float
        Bed slope (dimensionless)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)
    y_start : float
        Starting depth (m)
    y_target : float
        Target depth (m)
    num_steps : int
        Number of computation steps
    max_distance : float
        Maximum distance to search (m)

    Returns:
    --------
    float : Distance to target depth (m)
    """
    if abs(y_start - y_target) < 0.001:
        return 0

    # Determine direction
    if y_target > y_start:
        direction = 'upstream'
    else:
        direction = 'downstream'

    # Initial distance estimate
    distance = abs(y_target - y_start) * 100  # Initial guess

    for iteration in range(10):  # Iterative refinement
        x, y = solve_gvf_profile_manning(channel, Q, S0, n, y_start, distance,
                                          num_steps, direction)

        y_end = y[-1]

        if abs(y_end - y_target) < 0.01:  # Converged
            return abs(x[-1])

        # Adjust distance estimate
        if direction == 'upstream':
            if y_end < y_target:
                distance *= 1.5
            else:
                distance *= 0.7
        else:
            if y_end > y_target:
                distance *= 1.5
            else:
                distance *= 0.7

        if distance > max_distance:
            distance = max_distance
            break

    return abs(x[-1])


def distance_to_depth_chezy(channel, Q, S0, C, y_start, y_target, num_steps=100,
                             max_distance=10000):
    """
    Calculate distance from y_start to y_target using Chezy equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    S0 : float
        Bed slope (dimensionless)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))
    y_start : float
        Starting depth (m)
    y_target : float
        Target depth (m)
    num_steps : int
        Number of computation steps
    max_distance : float
        Maximum distance to search (m)

    Returns:
    --------
    float : Distance to target depth (m)
    """
    if abs(y_start - y_target) < 0.001:
        return 0

    # Determine direction
    if y_target > y_start:
        direction = 'upstream'
    else:
        direction = 'downstream'

    # Initial distance estimate
    distance = abs(y_target - y_start) * 100

    for iteration in range(10):
        x, y = solve_gvf_profile_chezy(channel, Q, S0, C, y_start, distance,
                                        num_steps, direction)

        y_end = y[-1]

        if abs(y_end - y_target) < 0.01:
            return abs(x[-1])

        # Adjust distance estimate
        if direction == 'upstream':
            if y_end < y_target:
                distance *= 1.5
            else:
                distance *= 0.7
        else:
            if y_end > y_target:
                distance *= 1.5
            else:
                distance *= 0.7

        if distance > max_distance:
            distance = max_distance
            break

    return abs(x[-1])


def classify_gvf_curve(S0, S_c, y, y_n, y_c):
    """
    Classify GVF curve type (M1, M2, S1, S2, etc.)

    M = Mild slope (S0 < S_c)
    S = Steep slope (S0 > S_c)
    C = Critical slope (S0 = S_c)
    H = Horizontal (S0 = 0)
    A = Adverse (S0 < 0)

    Zones:
    1 = y > y_n and y > y_c
    2 = y between y_n and y_c
    3 = y < y_n and y < y_c

    Parameters:
    -----------
    S0 : float
        Bed slope
    S_c : float
        Critical slope
    y : float
        Current depth (m)
    y_n : float
        Normal depth (m)
    y_c : float
        Critical depth (m)

    Returns:
    --------
    str : GVF curve classification
    """
    # Slope type
    if abs(S0) < 1e-10:
        slope_type = 'H'
    elif S0 < 0:
        slope_type = 'A'
    elif abs(S0 - S_c) < S_c * 0.01:
        slope_type = 'C'
    elif S0 < S_c:
        slope_type = 'M'
    else:
        slope_type = 'S'

    # Zone determination
    if slope_type == 'M':
        # Mild slope: y_n > y_c
        if y > y_n:
            zone = '1'
        elif y > y_c:
            zone = '2'
        else:
            zone = '3'
    elif slope_type == 'S':
        # Steep slope: y_n < y_c
        if y > y_c:
            zone = '1'
        elif y > y_n:
            zone = '2'
        else:
            zone = '3'
    elif slope_type == 'C':
        if y > y_c:
            zone = '1'
        else:
            zone = '3'
    elif slope_type == 'H':
        if y > y_c:
            zone = '2'
        else:
            zone = '3'
    elif slope_type == 'A':
        if y > y_c:
            zone = '2'
        else:
            zone = '3'
    else:
        zone = '?'

    return slope_type + zone


def gvf_curve_properties(curve_type):
    """
    Get properties of GVF curve type

    Parameters:
    -----------
    curve_type : str
        GVF curve classification (e.g., 'M1', 'S2')

    Returns:
    --------
    dict : Properties including slope of water surface, flow regime
    """
    properties = {
        'M1': {'surface_slope': 'Mild', 'regime': 'Subcritical',
               'direction': 'Backwater', 'description': 'Drawdown to normal'},
        'M2': {'surface_slope': 'Mild', 'regime': 'Subcritical',
               'direction': 'Drawdown', 'description': 'Acceleration to critical'},
        'M3': {'surface_slope': 'Steep', 'regime': 'Supercritical',
               'direction': 'Backwater', 'description': 'Rise to critical'},
        'S1': {'surface_slope': 'Mild', 'regime': 'Subcritical',
               'direction': 'Backwater', 'description': 'Rise to critical'},
        'S2': {'surface_slope': 'Steep', 'regime': 'Supercritical',
               'direction': 'Drawdown', 'description': 'Drop to normal'},
        'S3': {'surface_slope': 'Steep', 'regime': 'Supercritical',
               'direction': 'Backwater', 'description': 'Acceleration'},
        'C1': {'surface_slope': 'Uniform', 'regime': 'Subcritical',
               'direction': 'Backwater', 'description': 'Approach to critical'},
        'C3': {'surface_slope': 'Uniform', 'regime': 'Supercritical',
               'direction': 'Backwater', 'description': 'Acceleration from critical'},
        'H2': {'surface_slope': 'Horizontal', 'regime': 'Subcritical',
               'direction': 'Drawdown', 'description': 'Horizontal channel subcritical'},
        'H3': {'surface_slope': 'Horizontal', 'regime': 'Supercritical',
               'direction': 'Backwater', 'description': 'Horizontal channel supercritical'},
        'A2': {'surface_slope': 'Adverse', 'regime': 'Subcritical',
               'direction': 'Drawdown', 'description': 'Adverse slope subcritical'},
        'A3': {'surface_slope': 'Adverse', 'regime': 'Supercritical',
               'direction': 'Backwater', 'description': 'Adverse slope supercritical'},
    }

    return properties.get(curve_type, {'description': 'Unknown curve type'})

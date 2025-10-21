"""
Flow Calculations Module
========================
This module provides functions for calculating flow parameters in open channels:
- Manning's equation for normal depth
- Critical depth and critical slope
- Froude number and flow regime classification
- Specific energy
- Flow velocity

Author: Open Channel Flow Calculator
Date: August 2024
"""

import math
import numpy as np
from scipy.optimize import fsolve, brentq, minimize_scalar
from open_channel_flow.core.channel_geometry import ChannelSection


# Physical constants
g = 9.81  # Acceleration due to gravity (m/s^2)


def manning_velocity(R, S, n):
    """
    Calculate velocity using Manning's equation
    V = (1/n) * R^(2/3) * S^(1/2)

    Parameters:
    -----------
    R : float
        Hydraulic radius (m)
    S : float
        Channel slope (dimensionless)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)

    Returns:
    --------
    float : Velocity (m/s)
    """
    return (1.0 / n) * (R ** (2/3)) * (S ** 0.5)


def chezy_velocity(R, S, C):
    """
    Calculate velocity using Chezy equation
    V = C * sqrt(R * S)

    Parameters:
    -----------
    R : float
        Hydraulic radius (m)
    S : float
        Channel slope (dimensionless)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))

    Returns:
    --------
    float : Velocity (m/s)
    """
    return C * math.sqrt(R * S)


def manning_discharge(channel, depth, S, n):
    """
    Calculate discharge using Manning's equation
    Q = (1/n) * A * R^(2/3) * S^(1/2)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    depth : float
        Flow depth (m)
    S : float
        Channel slope (dimensionless)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)

    Returns:
    --------
    float : Discharge (m^3/s)
    """
    A = channel.area(depth)
    R = channel.hydraulic_radius(depth)
    V = manning_velocity(R, S, n)
    return A * V


def chezy_discharge(channel, depth, S, C):
    """
    Calculate discharge using Chezy equation
    Q = A * C * sqrt(R * S)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    depth : float
        Flow depth (m)
    S : float
        Channel slope (dimensionless)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))

    Returns:
    --------
    float : Discharge (m^3/s)
    """
    A = channel.area(depth)
    R = channel.hydraulic_radius(depth)
    V = chezy_velocity(R, S, C)
    return A * V


def normal_depth_manning(channel, Q, S, n, initial_guess=1.0, max_depth=20.0):
    """
    Calculate normal depth using Manning's equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    S : float
        Channel slope (dimensionless)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)
    initial_guess : float
        Initial guess for depth (m)
    max_depth : float
        Maximum depth to search (m)

    Returns:
    --------
    float : Normal depth (m)
    """
    def equation(y):
        if y <= 0:
            return 1e10
        Q_calc = manning_discharge(channel, y, S, n)
        return Q_calc - Q

    try:
        # Try fsolve first
        result = fsolve(equation, initial_guess, full_output=True)
        if result[2] == 1 and result[0][0] > 0:  # Solution converged
            return result[0][0]
    except:
        pass

    try:
        # Try brentq for more robust solution
        y_n = brentq(equation, 0.001, max_depth)
        return y_n
    except:
        # If brentq fails, use fsolve with different initial guess
        result = fsolve(equation, max_depth/2)
        return abs(result[0])


def normal_depth_chezy(channel, Q, S, C, initial_guess=1.0, max_depth=20.0):
    """
    Calculate normal depth using Chezy equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    S : float
        Channel slope (dimensionless)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))
    initial_guess : float
        Initial guess for depth (m)
    max_depth : float
        Maximum depth to search (m)

    Returns:
    --------
    float : Normal depth (m)
    """
    def equation(y):
        if y <= 0:
            return 1e10
        Q_calc = chezy_discharge(channel, y, S, C)
        return Q_calc - Q

    try:
        y_n = brentq(equation, 0.001, max_depth)
        return y_n
    except:
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def critical_depth(channel, Q, initial_guess=1.0, max_depth=20.0):
    """
    Calculate critical depth where Froude number = 1
    This occurs when specific energy is minimum for a given discharge

    For critical flow: Q^2 * T / (g * A^3) = 1

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    initial_guess : float
        Initial guess for depth (m)
    max_depth : float
        Maximum depth to search (m)

    Returns:
    --------
    float : Critical depth (m)
    """
    def equation(y):
        if y <= 0:
            return 1e10
        A = channel.area(y)
        T = channel.top_width(y)
        if A <= 0 or T <= 0:
            return 1e10
        # Q^2 * T / (g * A^3) = 1 at critical depth
        return Q**2 * T / (g * A**3) - 1.0

    try:
        y_c = brentq(equation, 0.001, max_depth)
        return y_c
    except:
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def froude_number(channel, depth, Q):
    """
    Calculate Froude number Fr = V / sqrt(g * D)
    where D is hydraulic depth (A/T)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    depth : float
        Flow depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Froude number (dimensionless)
    """
    A = channel.area(depth)
    if A == 0:
        return 0
    V = Q / A
    D = channel.hydraulic_depth(depth)
    if D == 0:
        return float('inf')
    return V / math.sqrt(g * D)


def flow_regime(Fr):
    """
    Determine flow regime from Froude number

    Parameters:
    -----------
    Fr : float
        Froude number

    Returns:
    --------
    str : Flow regime ('subcritical', 'critical', or 'supercritical')
    """
    if Fr < 0.99:
        return 'subcritical'
    elif Fr > 1.01:
        return 'supercritical'
    else:
        return 'critical'


def specific_energy(channel, depth, Q):
    """
    Calculate specific energy E = y + V^2/(2g)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    depth : float
        Flow depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Specific energy (m)
    """
    A = channel.area(depth)
    if A == 0:
        return float('inf')
    V = Q / A
    return depth + V**2 / (2 * g)


def critical_slope_manning(channel, Q, n, y_c=None):
    """
    Calculate critical slope (slope at which normal depth = critical depth)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    n : float
        Manning's roughness coefficient (m^(-1/3) s)
    y_c : float, optional
        Critical depth (if already calculated)

    Returns:
    --------
    float : Critical slope (dimensionless)
    """
    if y_c is None:
        y_c = critical_depth(channel, Q)

    A = channel.area(y_c)
    R = channel.hydraulic_radius(y_c)
    V = Q / A

    # From Manning's equation: V = (1/n) * R^(2/3) * S^(1/2)
    # S = (V * n / R^(2/3))^2
    S_c = (V * n / (R ** (2/3))) ** 2
    return S_c


def critical_slope_chezy(channel, Q, C, y_c=None):
    """
    Calculate critical slope using Chezy equation

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    C : float
        Chezy coefficient (m^(1/2) s^(-1))
    y_c : float, optional
        Critical depth (if already calculated)

    Returns:
    --------
    float : Critical slope (dimensionless)
    """
    if y_c is None:
        y_c = critical_depth(channel, Q)

    A = channel.area(y_c)
    R = channel.hydraulic_radius(y_c)
    V = Q / A

    # From Chezy equation: V = C * sqrt(R * S)
    # S = (V / (C * sqrt(R)))^2
    S_c = (V / (C * math.sqrt(R))) ** 2
    return S_c


def slope_classification(S, S_c):
    """
    Classify channel slope as mild, critical, or steep

    Parameters:
    -----------
    S : float
        Actual channel slope
    S_c : float
        Critical slope

    Returns:
    --------
    str : Slope classification ('mild', 'critical', or 'steep')
    """
    if S < S_c * 0.99:
        return 'mild'
    elif S > S_c * 1.01:
        return 'steep'
    else:
        return 'critical'


def velocity_from_discharge(channel, depth, Q):
    """
    Calculate velocity from discharge and depth

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    depth : float
        Flow depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Velocity (m/s)
    """
    A = channel.area(depth)
    if A == 0:
        return 0
    return Q / A


def depth_from_specific_energy(channel, Q, E, regime='subcritical', initial_guess=None):
    """
    Calculate depth for given specific energy and discharge
    For a given E and Q, there are typically two possible depths
    (subcritical and supercritical)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    E : float
        Specific energy (m)
    regime : str
        'subcritical' or 'supercritical' - which solution to return
    initial_guess : float, optional
        Initial guess for depth (m)

    Returns:
    --------
    float : Depth (m)
    """
    y_c = critical_depth(channel, Q)

    if initial_guess is None:
        if regime == 'subcritical':
            initial_guess = E * 0.8
        else:
            initial_guess = y_c * 0.5

    def equation(y):
        if y <= 0:
            return 1e10
        E_calc = specific_energy(channel, y, Q)
        return E_calc - E

    try:
        if regime == 'subcritical':
            # Subcritical solution is between y_c and E
            y = brentq(equation, y_c, E * 1.5)
        else:
            # Supercritical solution is between 0 and y_c
            y = brentq(equation, 0.001, y_c)
        return y
    except:
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def manning_n_from_depth(channel, Q, depth, S):
    """
    Calculate Manning's n from known depth, discharge, and slope

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    Q : float
        Discharge (m^3/s)
    depth : float
        Flow depth (m)
    S : float
        Channel slope (dimensionless)

    Returns:
    --------
    float : Manning's n (m^(-1/3) s)
    """
    A = channel.area(depth)
    R = channel.hydraulic_radius(depth)
    V = Q / A

    # From Manning's equation: V = (1/n) * R^(2/3) * S^(1/2)
    # n = R^(2/3) * S^(1/2) / V
    n = (R ** (2/3)) * (S ** 0.5) / V
    return n

"""
Hydraulic Jump Module
=====================
This module provides functions for analyzing hydraulic jumps in open channels:
- Sequent (conjugate) depths
- Energy loss in hydraulic jump
- Hydraulic jump in various channel shapes

Author: Open Channel Flow Calculator
Date: August 2024
"""

import math
import numpy as np
from scipy.optimize import fsolve, brentq
from open_channel_flow.core.channel_geometry import (ChannelSection, RectangularChannel, CircularChannel,
                                                      TriangularChannel)


# Physical constants
g = 9.81  # Acceleration due to gravity (m/s^2)


def sequent_depth_rectangular(y1, Q, width):
    """
    Calculate sequent (conjugate) depth for hydraulic jump in rectangular channel
    Uses analytical solution: y2 = (y1/2) * (-1 + sqrt(1 + 8*Fr1^2))

    Parameters:
    -----------
    y1 : float
        Initial depth (m)
    Q : float
        Discharge (m^3/s)
    width : float
        Channel width (m)

    Returns:
    --------
    float : Sequent depth y2 (m)
    """
    A1 = width * y1
    V1 = Q / A1
    Fr1 = V1 / math.sqrt(g * y1)

    # Analytical solution for rectangular channel
    y2 = (y1 / 2) * (-1 + math.sqrt(1 + 8 * Fr1**2))
    return y2


def sequent_depth_general(channel, y1, Q, initial_guess=None):
    """
    Calculate sequent depth for hydraulic jump in general channel shape
    Uses momentum equation: M1 = M2
    where M = Q^2/(g*A) + A*y_bar

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y1 : float
        Initial depth (m)
    Q : float
        Discharge (m^3/s)
    initial_guess : float, optional
        Initial guess for y2 (m)

    Returns:
    --------
    float : Sequent depth y2 (m)
    """
    def momentum(y):
        """Calculate specific momentum"""
        if y <= 0:
            return 0
        A = channel.area(y)
        if A == 0:
            return 0
        # For general shape, y_bar is centroid of area below water surface
        # For simple shapes, approximate as y/2 or use hydraulic depth
        y_bar = channel.hydraulic_depth(y) / 2  # Approximation
        M = Q**2 / (g * A) + A * y_bar
        return M

    M1 = momentum(y1)

    if initial_guess is None:
        # Use rectangular approximation for initial guess
        A1 = channel.area(y1)
        T1 = channel.top_width(y1)
        if T1 > 0:
            equiv_width = T1
            equiv_y1 = A1 / T1
            y2_guess = sequent_depth_rectangular(equiv_y1, Q, equiv_width)
            initial_guess = y2_guess
        else:
            initial_guess = y1 * 2

    def equation(y2):
        if y2 <= 0:
            return 1e10
        M2 = momentum(y2)
        return M2 - M1

    try:
        # Try to find solution greater than y1 (for subcritical -> supercritical)
        # or less than y1 (for supercritical -> subcritical)
        result = fsolve(equation, initial_guess, full_output=True)
        if result[2] == 1:  # Solution converged
            return abs(result[0][0])
    except:
        pass

    # Alternative approach: search for solution
    try:
        if initial_guess > y1:
            y2 = brentq(equation, y1 * 1.01, y1 * 10)
        else:
            y2 = brentq(equation, 0.001, y1 * 0.99)
        return y2
    except:
        result = fsolve(equation, initial_guess)
        return abs(result[0])


def sequent_depth_circular(channel, y1, Q):
    """
    Calculate sequent depth for hydraulic jump in circular channel
    Uses momentum equation with proper centroid calculations

    Parameters:
    -----------
    channel : CircularChannel
        Circular channel object
    y1 : float
        Initial depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Sequent depth y2 (m)
    """
    def momentum_circular(y):
        """Calculate specific momentum for circular section"""
        if y <= 0:
            return 0
        A = channel.area(y)
        if A == 0:
            return 0

        # Distance from chord to centroid
        d_bar = channel.centroid_distance(y)

        # Distance from bottom to centroid
        y_bar = y - d_bar

        M = Q**2 / (g * A) + A * y_bar
        return M

    M1 = momentum_circular(y1)

    # Initial guess based on rectangular approximation
    A1 = channel.area(y1)
    T1 = channel.top_width(y1)
    if T1 > 0:
        equiv_y1 = A1 / T1
        y2_guess = sequent_depth_rectangular(equiv_y1, Q, T1)
    else:
        y2_guess = y1 * 2

    def equation(y2):
        if y2 <= 0 or y2 >= channel.diameter:
            return 1e10
        M2 = momentum_circular(y2)
        return M2 - M1

    try:
        result = fsolve(equation, y2_guess, full_output=True)
        if result[2] == 1:  # Solution converged
            y2 = result[0][0]
            if 0 < y2 < channel.diameter:
                return y2
    except:
        pass

    # Try brentq
    try:
        if y2_guess > y1:
            y2 = brentq(equation, y1 * 1.01, channel.diameter * 0.99)
        else:
            y2 = brentq(equation, 0.001, y1 * 0.99)
        return y2
    except:
        result = fsolve(equation, y2_guess)
        return abs(result[0])


def sequent_depth_triangular(channel, y1, Q):
    """
    Calculate sequent depth for hydraulic jump in triangular (V-shaped) channel
    Uses momentum equation

    Parameters:
    -----------
    channel : TriangularChannel
        Triangular channel object
    y1 : float
        Initial depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Sequent depth y2 (m)
    """
    m = channel.side_slope

    def momentum_triangular(y):
        """Calculate specific momentum for triangular section"""
        if y <= 0:
            return 0
        A = m * y**2
        if A == 0:
            return 0
        # Centroid of triangle is at y/3 from bottom
        y_bar = y / 3
        M = Q**2 / (g * A) + A * y_bar
        return M

    M1 = momentum_triangular(y1)

    # Initial guess
    y2_guess = y1 * 2

    def equation(y2):
        if y2 <= 0:
            return 1e10
        M2 = momentum_triangular(y2)
        return M2 - M1

    result = fsolve(equation, y2_guess)
    return abs(result[0])


def sequent_depth(channel, y1, Q, initial_guess=None):
    """
    Calculate sequent depth for hydraulic jump
    Automatically selects appropriate method based on channel type

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y1 : float
        Initial depth (m)
    Q : float
        Discharge (m^3/s)
    initial_guess : float, optional
        Initial guess for y2 (m)

    Returns:
    --------
    float : Sequent depth y2 (m)
    """
    if isinstance(channel, RectangularChannel):
        return sequent_depth_rectangular(y1, Q, channel.width)
    elif isinstance(channel, CircularChannel):
        return sequent_depth_circular(channel, y1, Q)
    elif isinstance(channel, TriangularChannel):
        return sequent_depth_triangular(channel, y1, Q)
    else:
        return sequent_depth_general(channel, y1, Q, initial_guess)


def energy_loss_jump(channel, y1, y2, Q):
    """
    Calculate energy loss in hydraulic jump
    ΔE = E1 - E2

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y1 : float
        Upstream depth (m)
    y2 : float
        Downstream depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Energy loss (m)
    """
    A1 = channel.area(y1)
    A2 = channel.area(y2)

    V1 = Q / A1
    V2 = Q / A2

    E1 = y1 + V1**2 / (2 * g)
    E2 = y2 + V2**2 / (2 * g)

    return E1 - E2


def energy_loss_fraction(channel, y1, y2, Q):
    """
    Calculate fraction of energy dissipated in hydraulic jump
    f = ΔE / E1

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y1 : float
        Upstream depth (m)
    y2 : float
        Downstream depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Fraction of energy dissipated (dimensionless)
    """
    A1 = channel.area(y1)
    V1 = Q / A1
    E1 = y1 + V1**2 / (2 * g)

    delta_E = energy_loss_jump(channel, y1, y2, Q)

    return delta_E / E1


def head_loss_jump(channel, y1, y2, Q):
    """
    Same as energy_loss_jump - alternate name for clarity
    """
    return energy_loss_jump(channel, y1, y2, Q)


def hydraulic_jump_length_rectangular(y1, y2):
    """
    Estimate length of hydraulic jump in rectangular channel
    Empirical formula: L ≈ 6 * (y2 - y1)

    Parameters:
    -----------
    y1 : float
        Upstream depth (m)
    y2 : float
        Downstream depth (m)

    Returns:
    --------
    float : Jump length (m)
    """
    return 6 * (y2 - y1)


def jump_classification_rectangular(y1, Q, width):
    """
    Classify hydraulic jump based on upstream Froude number
    (for rectangular channels)

    Parameters:
    -----------
    y1 : float
        Upstream depth (m)
    Q : float
        Discharge (m^3/s)
    width : float
        Channel width (m)

    Returns:
    --------
    str : Jump classification
    """
    A1 = width * y1
    V1 = Q / A1
    Fr1 = V1 / math.sqrt(g * y1)

    if Fr1 < 1.0:
        return "No jump (subcritical flow)"
    elif 1.0 <= Fr1 < 1.7:
        return "Undular jump"
    elif 1.7 <= Fr1 < 2.5:
        return "Weak jump"
    elif 2.5 <= Fr1 < 4.5:
        return "Oscillating jump"
    elif 4.5 <= Fr1 < 9.0:
        return "Steady jump"
    else:
        return "Strong jump"


def force_on_obstacle(channel, y1, y2, Q):
    """
    Calculate force on obstacle (e.g., blocks, gate) causing hydraulic jump
    F = ρ*g*(M1 - M2)

    For rectangular channel:
    F = ρ*Q*(V1 - V2) + ρ*g*(A1*ybar1 - A2*ybar2)

    Parameters:
    -----------
    channel : ChannelSection
        Channel cross-section object
    y1 : float
        Upstream depth (m)
    y2 : float
        Downstream depth (m)
    Q : float
        Discharge (m^3/s)

    Returns:
    --------
    float : Force per unit width (N or N/m depending on channel)
    """
    rho = 1000  # Water density (kg/m^3)

    A1 = channel.area(y1)
    A2 = channel.area(y2)

    V1 = Q / A1
    V2 = Q / A2

    # Momentum change
    momentum_change = rho * Q * (V1 - V2)

    # Pressure force change
    # For rectangular: pressure force = rho * g * A * ybar = rho * g * A * (y/2)
    # For general: use hydraulic depth as approximation
    if isinstance(channel, RectangularChannel):
        pressure_change = rho * g * (A1 * y1/2 - A2 * y2/2)
    else:
        D1 = channel.hydraulic_depth(y1)
        D2 = channel.hydraulic_depth(y2)
        pressure_change = rho * g * (A1 * D1/2 - A2 * D2/2)

    F = momentum_change + pressure_change
    return F


def drag_coefficient_force(cd, V, A, rho=1000):
    """
    Calculate drag force on obstacle
    F = (1/2) * cd * rho * V^2 * A

    Parameters:
    -----------
    cd : float
        Drag coefficient (dimensionless)
    V : float
        Velocity (m/s)
    A : float
        Frontal area (m^2)
    rho : float
        Fluid density (kg/m^3), default 1000 for water

    Returns:
    --------
    float : Drag force (N)
    """
    return 0.5 * cd * rho * V**2 * A

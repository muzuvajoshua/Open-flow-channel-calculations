"""
Channel Geometry Module
=======================
This module defines classes for different open channel cross-sections.
Each class provides methods to calculate geometric properties needed for
open channel flow analysis.

Author: Open Channel Flow Calculator
Date: August 2024
"""

import math
import numpy as np


class ChannelSection:
    """Base class for channel cross-sections"""

    def __init__(self):
        pass

    def area(self, depth):
        """Calculate flow area for given depth"""
        raise NotImplementedError

    def wetted_perimeter(self, depth):
        """Calculate wetted perimeter for given depth"""
        raise NotImplementedError

    def hydraulic_radius(self, depth):
        """Calculate hydraulic radius R = A/P"""
        A = self.area(depth)
        P = self.wetted_perimeter(depth)
        if P == 0:
            return 0
        return A / P

    def top_width(self, depth):
        """Calculate top width of water surface"""
        raise NotImplementedError

    def hydraulic_depth(self, depth):
        """Calculate hydraulic depth D = A/T"""
        A = self.area(depth)
        T = self.top_width(depth)
        if T == 0:
            return 0
        return A / T


class RectangularChannel(ChannelSection):
    """Rectangular channel cross-section"""

    def __init__(self, width):
        """
        Parameters:
        -----------
        width : float
            Channel width (m)
        """
        super().__init__()
        self.width = width

    def area(self, depth):
        """Flow area A = b*y"""
        return self.width * depth

    def wetted_perimeter(self, depth):
        """Wetted perimeter P = b + 2*y"""
        return self.width + 2 * depth

    def top_width(self, depth):
        """Top width T = b"""
        return self.width


class TrapezoidalChannel(ChannelSection):
    """Trapezoidal channel cross-section"""

    def __init__(self, bottom_width, side_slope):
        """
        Parameters:
        -----------
        bottom_width : float
            Bottom width (m)
        side_slope : float
            Side slope (horizontal:vertical), e.g., 1.5 means 1.5H:1V
        """
        super().__init__()
        self.bottom_width = bottom_width
        self.side_slope = side_slope  # m = horizontal/vertical

    def area(self, depth):
        """Flow area A = (b + m*y)*y"""
        return (self.bottom_width + self.side_slope * depth) * depth

    def wetted_perimeter(self, depth):
        """Wetted perimeter P = b + 2*y*sqrt(1 + m^2)"""
        return self.bottom_width + 2 * depth * math.sqrt(1 + self.side_slope**2)

    def top_width(self, depth):
        """Top width T = b + 2*m*y"""
        return self.bottom_width + 2 * self.side_slope * depth


class CircularChannel(ChannelSection):
    """Circular channel cross-section (pipe)"""

    def __init__(self, diameter):
        """
        Parameters:
        -----------
        diameter : float
            Pipe diameter (m)
        """
        super().__init__()
        self.diameter = diameter
        self.radius = diameter / 2

    def _theta(self, depth):
        """Calculate central angle theta from depth"""
        y = depth
        R = self.radius
        if y <= 0:
            return 0
        if y >= 2 * R:
            return math.pi
        # theta is the half-angle from vertical to water surface
        # y = R(1 - cos(theta))
        # cos(theta) = 1 - y/R
        cos_theta = 1 - y / R
        cos_theta = max(-1, min(1, cos_theta))  # Clamp to [-1, 1]
        theta = math.acos(cos_theta)
        return theta

    def area(self, depth):
        """Flow area A = R^2(theta - sin(theta)*cos(theta))"""
        theta = self._theta(depth)
        R = self.radius
        A = R**2 * (theta - math.sin(theta) * math.cos(theta))
        return A

    def wetted_perimeter(self, depth):
        """Wetted perimeter P = 2*R*theta"""
        theta = self._theta(depth)
        R = self.radius
        return 2 * R * theta

    def top_width(self, depth):
        """Top width T = 2*R*sin(theta)"""
        theta = self._theta(depth)
        R = self.radius
        return 2 * R * math.sin(theta)

    def centroid_distance(self, depth):
        """
        Distance from chord to centroid of circular segment
        Used for hydraulic jump calculations in circular channels
        """
        theta = self._theta(depth)
        R = self.radius

        if theta == 0:
            return 0

        numerator = (2/3) * (math.sin(theta))**3
        denominator = theta - 0.5 * math.sin(2*theta)

        if denominator == 0:
            return 0

        d_bar = R * numerator / denominator
        return d_bar


class TriangularChannel(ChannelSection):
    """V-shaped triangular channel cross-section"""

    def __init__(self, side_slope=None, semi_angle=None):
        """
        Parameters:
        -----------
        side_slope : float, optional
            Side slope (horizontal:vertical)
        semi_angle : float, optional
            Semi-angle from vertical in degrees

        Note: Provide either side_slope or semi_angle
        """
        super().__init__()
        if side_slope is not None:
            self.side_slope = side_slope
        elif semi_angle is not None:
            # Convert semi-angle to side slope
            # tan(semi_angle) = horizontal/vertical = side_slope
            self.side_slope = math.tan(math.radians(semi_angle))
        else:
            raise ValueError("Must provide either side_slope or semi_angle")

    def area(self, depth):
        """Flow area A = m*y^2"""
        return self.side_slope * depth**2

    def wetted_perimeter(self, depth):
        """Wetted perimeter P = 2*y*sqrt(1 + m^2)"""
        return 2 * depth * math.sqrt(1 + self.side_slope**2)

    def top_width(self, depth):
        """Top width T = 2*m*y"""
        return 2 * self.side_slope * depth


class CompoundChannel(ChannelSection):
    """Compound channel with main section and different geometry below a breakpoint"""

    def __init__(self, bottom_section_type, bottom_params, break_depth,
                 top_section_type=None, top_params=None):
        """
        Parameters:
        -----------
        bottom_section_type : str
            Type of bottom section ('rectangular', 'trapezoidal', 'triangular', 'circular')
        bottom_params : dict
            Parameters for bottom section
        break_depth : float
            Depth at which geometry changes
        top_section_type : str, optional
            Type of top section (if None, uses same as bottom)
        top_params : dict, optional
            Parameters for top section
        """
        super().__init__()
        self.bottom_section = self._create_section(bottom_section_type, bottom_params)
        self.break_depth = break_depth

        if top_section_type is not None and top_params is not None:
            self.top_section = self._create_section(top_section_type, top_params)
        else:
            self.top_section = None

    def _create_section(self, section_type, params):
        """Factory method to create channel section"""
        if section_type == 'rectangular':
            return RectangularChannel(params['width'])
        elif section_type == 'trapezoidal':
            return TrapezoidalChannel(params['bottom_width'], params['side_slope'])
        elif section_type == 'triangular':
            if 'side_slope' in params:
                return TriangularChannel(side_slope=params['side_slope'])
            else:
                return TriangularChannel(semi_angle=params['semi_angle'])
        elif section_type == 'circular':
            return CircularChannel(params['diameter'])
        else:
            raise ValueError(f"Unknown section type: {section_type}")

    def area(self, depth):
        """Calculate area for compound section"""
        if depth <= self.break_depth:
            return self.bottom_section.area(depth)
        else:
            A_bottom = self.bottom_section.area(self.break_depth)
            if self.top_section is not None:
                A_top = self.top_section.area(depth - self.break_depth)
            else:
                A_top = self.bottom_section.area(depth) - A_bottom
            return A_bottom + A_top

    def wetted_perimeter(self, depth):
        """Calculate wetted perimeter for compound section"""
        if depth <= self.break_depth:
            return self.bottom_section.wetted_perimeter(depth)
        else:
            # For compound sections, wetted perimeter calculation depends on geometry
            # This is a simplified version
            if self.top_section is not None:
                P_bottom = self.bottom_section.wetted_perimeter(self.break_depth)
                P_top = self.top_section.wetted_perimeter(depth - self.break_depth)
                # Subtract the interface width that's counted twice
                T_break = self.bottom_section.top_width(self.break_depth)
                return P_bottom + P_top - T_break
            else:
                return self.bottom_section.wetted_perimeter(depth)

    def top_width(self, depth):
        """Calculate top width for compound section"""
        if depth <= self.break_depth:
            return self.bottom_section.top_width(depth)
        else:
            if self.top_section is not None:
                return self.top_section.top_width(depth - self.break_depth)
            else:
                return self.bottom_section.top_width(depth)


class WideChannel(RectangularChannel):
    """Wide rectangular channel (unit width analysis)"""

    def __init__(self):
        """Wide channel has unit width"""
        super().__init__(width=1.0)

    def hydraulic_radius(self, depth):
        """For wide channels, R ≈ y"""
        return depth

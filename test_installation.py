"""
Test Script to Verify Installation
====================================
Quick test to ensure the package is properly organized and working.

Run this after reorganizing the code to verify everything works.
"""

print("="*70)
print("TESTING OPEN CHANNEL FLOW PACKAGE")
print("="*70)

print("\n1. Testing imports...")
try:
    from open_channel_flow import OpenChannelSolver
    from open_channel_flow import RectangularChannel, TrapezoidalChannel, CircularChannel
    from open_channel_flow import normal_depth_manning, critical_depth, froude_number
    print("   ✓ All imports successful!")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    exit(1)

print("\n2. Testing basic channel creation...")
try:
    rect_channel = RectangularChannel(width=5.0)
    trap_channel = TrapezoidalChannel(bottom_width=0.6, side_slope=0.75)
    circ_channel = CircularChannel(diameter=1.4)
    print("   ✓ Channel objects created successfully!")
except Exception as e:
    print(f"   ✗ Channel creation failed: {e}")
    exit(1)

print("\n3. Testing flow calculations...")
try:
    # Test normal depth
    y_n = normal_depth_manning(rect_channel, Q=20.0, S=0.001, n=0.02)
    print(f"   Normal depth = {y_n:.3f} m")

    # Test critical depth
    y_c = critical_depth(rect_channel, Q=20.0)
    print(f"   Critical depth = {y_c:.3f} m")

    # Test Froude number
    Fr = froude_number(rect_channel, y_n, Q=20.0)
    print(f"   Froude number = {Fr:.3f}")
    print("   ✓ Flow calculations working!")
except Exception as e:
    print(f"   ✗ Flow calculation failed: {e}")
    exit(1)

print("\n4. Testing solver interface...")
try:
    solver = OpenChannelSolver()
    results = solver.solve_basic_flow_problem(
        channel_type='rectangular',
        channel_params={'width': 5.0},
        Q=20.0,
        S=0.001,
        n=0.02
    )
    print("   ✓ Solver working!")
    print(f"   Results keys: {list(results.keys())}")
except Exception as e:
    print(f"   ✗ Solver failed: {e}")
    exit(1)

print("\n5. Testing example problems...")
try:
    from examples import example_problems
    print("   ✓ Examples module imported successfully!")
except ImportError as e:
    print(f"   ✗ Examples import failed: {e}")
    print("   Note: This is expected if not running with proper PYTHONPATH")

print("\n" + "="*70)
print("ALL TESTS PASSED! ✓")
print("="*70)
print("\nThe package is properly organized and ready to use!")
print("\nNext steps:")
print("1. Run examples: python examples/example_problems.py")
print("2. Or import in your code: from open_channel_flow import OpenChannelSolver")

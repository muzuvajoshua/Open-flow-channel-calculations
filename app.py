"""
Flask Web Application for Open Channel Flow Calculator
Uses the existing open_channel_flow module for all calculations
"""

from flask import Flask, request, render_template, jsonify
from open_channel_flow import OpenChannelSolver
from open_channel_flow import (
    RectangularChannel,
    TrapezoidalChannel,
    CircularChannel,
    TriangularChannel,
    WideChannel,
    CompoundChannel,
    critical_depth,
    froude_number,
    flow_regime,
    specific_energy
)

app = Flask(__name__)
solver = OpenChannelSolver()


@app.route('/')
def home():
    """Main page with calculation type selection"""
    return render_template('index.html')


@app.route('/calculate/normal', methods=['POST'])
def calculate_normal():
    """Calculate normal and critical depth"""
    try:
        # Get form data
        channel_type = request.form['channel_type']
        Q = float(request.form['Q'])
        S = float(request.form['S'])
        n = float(request.form['n'])

        # Build channel parameters
        channel_params = {}
        if channel_type == 'rectangular':
            channel_params['width'] = float(request.form['width'])
        elif channel_type == 'trapezoidal':
            channel_params['bottom_width'] = float(request.form['bottom_width'])
            channel_params['side_slope'] = float(request.form['side_slope'])
        elif channel_type == 'circular':
            channel_params['diameter'] = float(request.form['diameter'])
        elif channel_type == 'triangular':
            channel_params['side_slope'] = float(request.form['side_slope'])
        elif channel_type == 'compound':
            # Bottom section parameters
            bottom_section_type = request.form['bottom_section_type']
            bottom_params = {}
            if bottom_section_type == 'rectangular':
                bottom_params['width'] = float(request.form['bottom_width'])
            elif bottom_section_type == 'trapezoidal':
                bottom_params['bottom_width'] = float(request.form['bottom_bottom_width'])
                bottom_params['side_slope'] = float(request.form['bottom_side_slope'])
            elif bottom_section_type == 'triangular':
                bottom_params['side_slope'] = float(request.form['bottom_side_slope'])
            elif bottom_section_type == 'circular':
                bottom_params['diameter'] = float(request.form['bottom_diameter'])

            channel_params['bottom_section_type'] = bottom_section_type
            channel_params['bottom_params'] = bottom_params
            channel_params['break_depth'] = float(request.form['break_depth'])

            # Top section parameters (optional)
            if request.form.get('use_top_section') == 'yes':
                top_section_type = request.form['top_section_type']
                top_params = {}
                if top_section_type == 'rectangular':
                    top_params['width'] = float(request.form['top_width'])
                elif top_section_type == 'trapezoidal':
                    top_params['bottom_width'] = float(request.form['top_bottom_width'])
                    top_params['side_slope'] = float(request.form['top_side_slope'])
                elif top_section_type == 'triangular':
                    top_params['side_slope'] = float(request.form['top_side_slope'])

                channel_params['top_section_type'] = top_section_type
                channel_params['top_params'] = top_params

        # Use existing solver
        calc_results = solver.solve_basic_flow_problem(
            channel_type=channel_type,
            channel_params=channel_params,
            Q=Q,
            S=S,
            n=n
        )

        # Format inputs for display
        inputs = {
            'Channel Type': channel_type.capitalize(),
            'Discharge (Q)': f"{Q} m³/s",
            'Slope (S)': f"{S}",
            'Manning\'s n': f"{n}"
        }
        inputs.update({k.replace('_', ' ').title(): f"{v}" for k, v in channel_params.items()})

        # Format results for display
        y_n = calc_results['slope_1']['normal_depth']
        y_c = calc_results['critical_depth']
        Fr = calc_results['slope_1']['froude_number']
        regime = calc_results['slope_1']['flow_regime']
        S_c = calc_results['critical_slope']

        # Get channel for additional calculations
        if channel_type == 'rectangular':
            channel = RectangularChannel(channel_params['width'])
        elif channel_type == 'trapezoidal':
            channel = TrapezoidalChannel(channel_params['bottom_width'], channel_params['side_slope'])
        elif channel_type == 'circular':
            channel = CircularChannel(channel_params['diameter'])
        elif channel_type == 'triangular':
            channel = TriangularChannel(channel_params['side_slope'])
        elif channel_type == 'wide':
            channel = WideChannel()
        elif channel_type == 'compound':
            channel = CompoundChannel(
                bottom_section_type=channel_params['bottom_section_type'],
                bottom_params=channel_params['bottom_params'],
                break_depth=channel_params['break_depth'],
                top_section_type=channel_params.get('top_section_type'),
                top_params=channel_params.get('top_params')
            )

        results = {
            'Normal Depth (yₙ)': y_n,
            'Critical Depth (yc)': y_c,
            'Froude Number (Fr)': Fr,
            'Flow Regime': regime.capitalize(),
            'Critical Slope (Sc)': S_c,
            'Area at Normal Depth (m²)': channel.area(y_n),
            'Velocity (m/s)': Q / channel.area(y_n),
            'Hydraulic Radius (m)': channel.hydraulic_radius(y_n)
        }

        return render_template('results.html', inputs=inputs, results=results)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/calculate/jump', methods=['POST'])
def calculate_jump():
    """Calculate hydraulic jump properties"""
    try:
        channel_type = request.form['channel_type']
        Q = float(request.form['Q'])
        y1 = float(request.form['y1'])

        # Build channel parameters
        channel_params = {}
        if channel_type == 'rectangular':
            channel_params['width'] = float(request.form['width'])
        elif channel_type == 'trapezoidal':
            channel_params['bottom_width'] = float(request.form['bottom_width'])
            channel_params['side_slope'] = float(request.form['side_slope'])
        elif channel_type == 'triangular':
            channel_params['side_slope'] = float(request.form['side_slope'])
        elif channel_type == 'compound':
            # Bottom section parameters
            bottom_section_type = request.form['bottom_section_type']
            bottom_params = {}
            if bottom_section_type == 'rectangular':
                bottom_params['width'] = float(request.form['bottom_width'])
            elif bottom_section_type == 'trapezoidal':
                bottom_params['bottom_width'] = float(request.form['bottom_bottom_width'])
                bottom_params['side_slope'] = float(request.form['bottom_side_slope'])
            elif bottom_section_type == 'triangular':
                bottom_params['side_slope'] = float(request.form['bottom_side_slope'])

            channel_params['bottom_section_type'] = bottom_section_type
            channel_params['bottom_params'] = bottom_params
            channel_params['break_depth'] = float(request.form['break_depth'])

            # Top section parameters (optional)
            if request.form.get('use_top_section') == 'yes':
                top_section_type = request.form['top_section_type']
                top_params = {}
                if top_section_type == 'rectangular':
                    top_params['width'] = float(request.form['top_width'])
                elif top_section_type == 'trapezoidal':
                    top_params['bottom_width'] = float(request.form['top_bottom_width'])
                    top_params['side_slope'] = float(request.form['top_side_slope'])
                elif top_section_type == 'triangular':
                    top_params['side_slope'] = float(request.form['top_side_slope'])

                channel_params['top_section_type'] = top_section_type
                channel_params['top_params'] = top_params

        # Use existing solver
        calc_results = solver.solve_hydraulic_jump_problem(
            channel_type=channel_type,
            channel_params=channel_params,
            Q=Q,
            y1=y1,
            find_sequent=True,
            find_energy_loss=True
        )

        inputs = {
            'Channel Type': channel_type.capitalize(),
            'Discharge (Q)': f"{Q} m³/s",
            'Upstream Depth (y₁)': f"{y1} m"
        }
        inputs.update({k.replace('_', ' ').title(): f"{v}" for k, v in channel_params.items()})

        # Get channel for velocity calculations
        if channel_type == 'rectangular':
            channel = RectangularChannel(channel_params['width'])
        elif channel_type == 'trapezoidal':
            channel = TrapezoidalChannel(channel_params['bottom_width'], channel_params['side_slope'])
        elif channel_type == 'triangular':
            channel = TriangularChannel(channel_params['side_slope'])
        elif channel_type == 'compound':
            channel = CompoundChannel(
                bottom_section_type=channel_params['bottom_section_type'],
                bottom_params=channel_params['bottom_params'],
                break_depth=channel_params['break_depth'],
                top_section_type=channel_params.get('top_section_type'),
                top_params=channel_params.get('top_params')
            )

        y2 = calc_results['sequent_depth']

        results = {
            'Sequent Depth (y₂)': y2,
            'Froude Number (Fr₁)': calc_results['froude_1'],
            'Froude Number (Fr₂)': froude_number(channel, y2, Q),
            'Energy Loss (ΔE) (m)': calc_results['energy_loss'],
            'Energy Loss Fraction': calc_results['energy_loss_fraction'],
            'Depth Ratio (y₂/y₁)': y2/y1,
            'Upstream Velocity (m/s)': Q / channel.area(y1),
            'Downstream Velocity (m/s)': Q / channel.area(y2)
        }

        return render_template('results.html', inputs=inputs, results=results)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/calculate/weir', methods=['POST'])
def calculate_weir():
    """Calculate weir flow properties"""
    try:
        channel_type = request.form['channel_type']
        Q = float(request.form['Q'])
        S = float(request.form.get('S', 0.0002))
        n = float(request.form.get('n', 0.015))
        weir_height = float(request.form['weir_height'])

        channel_params = {}
        if channel_type == 'rectangular':
            channel_params['width'] = float(request.form['width'])

        # Use existing solver
        calc_results = solver.solve_weir_problem(
            channel_type=channel_type,
            channel_params=channel_params,
            Q=Q,
            S=S,
            n=n,
            weir_height=weir_height,
            problem_type='depths'
        )

        inputs = {
            'Channel Type': channel_type.capitalize(),
            'Discharge (Q)': f"{Q} m³/s",
            'Weir Height (P)': f"{weir_height} m",
            'Slope': f"{S}",
            'Manning\'s n': f"{n}"
        }

        if channel_type == 'rectangular':
            inputs['Width'] = f"{channel_params['width']} m"

        results = {
            'Upstream Depth (m)': calc_results['upstream_depth'],
            'Depth Over Crest (m)': calc_results['depth_over_weir'],
            'Critical Depth (m)': calc_results['critical_depth'],
            'Normal Depth (m)': calc_results['normal_depth'],
            'Head Over Weir (m)': calc_results['upstream_depth'] - weir_height,
            'Slope Classification': calc_results['slope_classification']
        }

        return render_template('results.html', inputs=inputs, results=results)

    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/calculate/gate', methods=['POST'])
def calculate_gate():
    """Calculate sluice gate properties"""
    try:
        width = float(request.form['width'])
        y_upstream = float(request.form['y_upstream'])
        y_downstream = float(request.form['y_downstream'])
        S = float(request.form.get('S', 0.001))
        n = float(request.form.get('n', 0.014))

        channel_params = {'width': width}

        # Use existing solver
        calc_results = solver.solve_sluice_gate_problem(
            channel_type='rectangular',
            channel_params=channel_params,
            y_upstream=y_upstream,
            y_downstream=y_downstream,
            S=S,
            n=n,
            find_force=True
        )

        Q = calc_results['discharge']

        inputs = {
            'Channel Width': f"{width} m",
            'Upstream Depth': f"{y_upstream} m",
            'Downstream Depth': f"{y_downstream} m",
            'Slope': f"{S}",
            'Manning\'s n': f"{n}"
        }

        results = {
            'Discharge (Q) (m³/s)': Q,
            'Force on Gate (kN)': calc_results['force_on_gate'] / 1000,
            'Froude Upstream': calc_results['froude_upstream'],
            'Froude Downstream': calc_results['froude_downstream'],
            'Normal Depth (m)': calc_results['normal_depth'],
            'Critical Depth (m)': calc_results['critical_depth'],
            'Contraction Ratio': y_downstream / y_upstream
        }

        return render_template('results.html', inputs=inputs, results=results)

    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌊 OPEN CHANNEL FLOW WEB CALCULATOR")
    print("="*70)
    print("\nStarting Flask web server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)

function showForm(type) {
    document.getElementById('calcSelection').style.display = 'none';
    document.querySelectorAll('.form-section').forEach(el => el.classList.remove('active'));
    document.getElementById(type + 'Form').classList.add('active');
}

function showSelection() {
    document.getElementById('calcSelection').style.display = 'block';
    document.querySelectorAll('.form-section').forEach(el => el.classList.remove('active'));
}

function updateChannelParams(channelType) {
    const container = document.getElementById('channelParams');
    let html = '';

    if (channelType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="width" value="5.0" required></div>';
    } else if (channelType === 'trapezoidal') {
        html = '<div class="form-group"><label>Bottom Width (m):</label><input type="number" step="any" name="bottom_width" value="3.0" required></div>';
        html += '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="side_slope" value="1.5" required></div>';
    } else if (channelType === 'circular') {
        html = '<div class="form-group"><label>Diameter (m):</label><input type="number" step="any" name="diameter" value="1.5" required></div>';
    } else if (channelType === 'triangular') {
        html = '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="side_slope" value="1.0" required></div>';
    } else if (channelType === 'wide') {
        html = '<div class="info-text">Wide channel uses unit width (1m)</div>';
    } else if (channelType === 'compound') {
        html = '<h4 style="color: #667eea; margin-bottom: 10px;">Bottom Section (Main Channel)</h4>';
        html += '<div class="form-group"><label>Bottom Section Type:</label><select name="bottom_section_type" onchange="updateBottomSectionParams(this.value)" required>';
        html += '<option value="rectangular">Rectangular</option>';
        html += '<option value="trapezoidal">Trapezoidal</option>';
        html += '<option value="triangular">Triangular</option>';
        html += '</select></div>';
        html += '<div id="bottomSectionParams">';
        html += '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="bottom_width" value="10.0" required></div>';
        html += '</div>';
        html += '<div class="form-group"><label>Break Depth (Bankfull) (m):</label><input type="number" step="any" name="break_depth" value="2.0" required></div>';
        html += '<h4 style="color: #667eea; margin: 15px 0 10px 0;">Top Section (Floodplains)</h4>';
        html += '<div class="form-group"><label><input type="checkbox" name="use_top_section" value="yes" onchange="toggleTopSection(this.checked)"> Use Different Top Section Geometry</label></div>';
        html += '<div class="info-text">If unchecked, top section will use same geometry as bottom section</div>';
        html += '<div id="topSectionContainer" style="display:none;">';
        html += '<div class="form-group"><label>Top Section Type:</label><select name="top_section_type" onchange="updateTopSectionParams(this.value)">';
        html += '<option value="rectangular">Rectangular</option>';
        html += '<option value="trapezoidal">Trapezoidal</option>';
        html += '<option value="triangular">Triangular</option>';
        html += '</select></div>';
        html += '<div id="topSectionParams">';
        html += '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="top_width" value="10.0"></div>';
        html += '</div></div>';
    }

    container.innerHTML = html;
}

function updateJumpParams(channelType) {
    const container = document.getElementById('jumpChannelParams');
    let html = '';

    if (channelType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="width" value="3.0" required></div>';
    } else if (channelType === 'trapezoidal') {
        html = '<div class="form-group"><label>Bottom Width (m):</label><input type="number" step="any" name="bottom_width" value="3.0" required></div>';
        html += '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="side_slope" value="1.5" required></div>';
    } else if (channelType === 'triangular') {
        html = '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="side_slope" value="1.0" required></div>';
    } else if (channelType === 'compound') {
        html = '<h4 style="color: #667eea; margin-bottom: 10px;">Bottom Section</h4>';
        html += '<div class="form-group"><label>Bottom Section Type:</label><select name="bottom_section_type" onchange="updateJumpBottomParams(this.value)" required>';
        html += '<option value="rectangular">Rectangular</option>';
        html += '<option value="trapezoidal">Trapezoidal</option>';
        html += '<option value="triangular">Triangular</option>';
        html += '</select></div>';
        html += '<div id="jumpBottomParams">';
        html += '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="bottom_width" value="10.0" required></div>';
        html += '</div>';
        html += '<div class="form-group"><label>Break Depth (m):</label><input type="number" step="any" name="break_depth" value="2.0" required></div>';
        html += '<h4 style="color: #667eea; margin: 15px 0 10px 0;">Top Section (Optional)</h4>';
        html += '<div class="form-group"><label><input type="checkbox" name="use_top_section" value="yes" onchange="toggleJumpTopSection(this.checked)"> Use Different Top Section</label></div>';
        html += '<div id="jumpTopContainer" style="display:none;">';
        html += '<div class="form-group"><label>Top Section Type:</label><select name="top_section_type" onchange="updateJumpTopParams(this.value)">';
        html += '<option value="rectangular">Rectangular</option>';
        html += '<option value="trapezoidal">Trapezoidal</option>';
        html += '<option value="triangular">Triangular</option>';
        html += '</select></div>';
        html += '<div id="jumpTopParams">';
        html += '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="top_width" value="10.0"></div>';
        html += '</div></div>';
    }

    container.innerHTML = html;
}

function updateWeirParams(channelType) {
    const container = document.getElementById('weirChannelParams');
    let html = '';

    if (channelType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="width" value="3.0" required></div>';
    } else if (channelType === 'wide') {
        html = '<div class="info-text">Wide channel uses unit width (1m)</div>';
    }

    container.innerHTML = html;
}

// Compound channel helper functions
function updateBottomSectionParams(sectionType) {
    const container = document.getElementById('bottomSectionParams');
    let html = '';

    if (sectionType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="bottom_width" value="10.0" required></div>';
    } else if (sectionType === 'trapezoidal') {
        html = '<div class="form-group"><label>Bottom Width (m):</label><input type="number" step="any" name="bottom_bottom_width" value="10.0" required></div>';
        html += '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="bottom_side_slope" value="1.5" required></div>';
    } else if (sectionType === 'triangular') {
        html = '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="bottom_side_slope" value="1.0" required></div>';
    } else if (sectionType === 'circular') {
        html = '<div class="form-group"><label>Diameter (m):</label><input type="number" step="any" name="bottom_diameter" value="1.5" required></div>';
    }

    container.innerHTML = html;
}

function toggleTopSection(checked) {
    const container = document.getElementById('topSectionContainer');
    container.style.display = checked ? 'block' : 'none';
}

function updateTopSectionParams(sectionType) {
    const container = document.getElementById('topSectionParams');
    let html = '';

    if (sectionType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="top_width" value="10.0"></div>';
    } else if (sectionType === 'trapezoidal') {
        html = '<div class="form-group"><label>Bottom Width (m):</label><input type="number" step="any" name="top_bottom_width" value="10.0"></div>';
        html += '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="top_side_slope" value="5.0"></div>';
    } else if (sectionType === 'triangular') {
        html = '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="top_side_slope" value="5.0"></div>';
    }

    container.innerHTML = html;
}

// Jump form compound channel helpers
function updateJumpBottomParams(sectionType) {
    const container = document.getElementById('jumpBottomParams');
    let html = '';

    if (sectionType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="bottom_width" value="10.0" required></div>';
    } else if (sectionType === 'trapezoidal') {
        html = '<div class="form-group"><label>Bottom Width (m):</label><input type="number" step="any" name="bottom_bottom_width" value="10.0" required></div>';
        html += '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="bottom_side_slope" value="1.5" required></div>';
    } else if (sectionType === 'triangular') {
        html = '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="bottom_side_slope" value="1.0" required></div>';
    }

    container.innerHTML = html;
}

function toggleJumpTopSection(checked) {
    const container = document.getElementById('jumpTopContainer');
    container.style.display = checked ? 'block' : 'none';
}

function updateJumpTopParams(sectionType) {
    const container = document.getElementById('jumpTopParams');
    let html = '';

    if (sectionType === 'rectangular') {
        html = '<div class="form-group"><label>Width (m):</label><input type="number" step="any" name="top_width" value="10.0"></div>';
    } else if (sectionType === 'trapezoidal') {
        html = '<div class="form-group"><label>Bottom Width (m):</label><input type="number" step="any" name="top_bottom_width" value="10.0"></div>';
        html += '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="top_side_slope" value="5.0"></div>';
    } else if (sectionType === 'triangular') {
        html = '<div class="form-group"><label>Side Slope (H:V):</label><input type="number" step="any" name="top_side_slope" value="5.0"></div>';
    }

    container.innerHTML = html;
}

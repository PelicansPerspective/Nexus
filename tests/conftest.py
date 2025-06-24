"""
Test configuration and shared fixtures for CFH project tests.
"""

import pytest
import numpy as np
import tempfile
import os
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Fixture providing path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def temp_dir():
    """Fixture providing temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_eeg_data():
    """Generate synthetic EEG-like data for testing."""
    np.random.seed(42)
    n_channels = 64
    n_samples = 1000
    sampling_rate = 250.0
    
    # Generate synthetic EEG with some realistic characteristics
    time = np.arange(n_samples) / sampling_rate
    data = np.random.randn(n_channels, n_samples) * 50e-6  # 50 μV noise
    
    # Add some structured signals
    for ch in range(n_channels):
        # Alpha waves around 10 Hz
        data[ch] += 20e-6 * np.sin(2 * np.pi * 10 * time + ch * 0.1)
        # Gamma waves around 40 Hz
        data[ch] += 5e-6 * np.sin(2 * np.pi * 40 * time + ch * 0.05)
    
    return {
        'data': data,
        'time': time,
        'sampling_rate': sampling_rate,
        'channels': [f'Ch{i+1}' for i in range(n_channels)]
    }


@pytest.fixture
def cfh_parameters():
    """Standard CFH parameters for testing."""
    return {
        'mass_psi': 1e-18,  # kg
        'coupling_constant': 1e-10,  # Proper dimensions
        'hbar': 1.055e-34,  # J⋅s
        'c': 3e8,  # m/s
        'hyper_causal_speed': 3.1e8,  # m/s (slightly > c)
    }


@pytest.fixture
def simulation_config():
    """Standard simulation configuration for testing."""
    return {
        'grid_size': 32,
        'time_steps': 100,
        'dt': 1e-6,  # seconds
        'dx': 1e-3,  # meters
        'boundary_conditions': 'periodic'
    }


@pytest.fixture
def mock_experimental_data():
    """Mock experimental data structure."""
    np.random.seed(123)
    n_trials = 50
    
    return {
        'chsh_values': np.random.normal(2.1, 0.1, n_trials),
        'plv_values': np.random.uniform(0.3, 0.8, n_trials),
        'timestamps': np.arange(n_trials) * 60,  # 1 minute intervals
        'trial_ids': [f'trial_{i:03d}' for i in range(n_trials)],
        'metadata': {
            'experiment_date': '2025-06-24',
            'equipment': 'Mock Setup v1.0',
            'conditions': 'controlled'
        }
    }


@pytest.fixture
def numerical_tolerance():
    """Standard numerical tolerances for floating point comparisons."""
    return {
        'rtol': 1e-10,
        'atol': 1e-12,
        'rtol_loose': 1e-6,
        'atol_loose': 1e-8
    }


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_field_data():
    """Generate sample consciousness field data for testing."""
    np.random.seed(456)
    
    # 3D grid
    nx, ny, nz = 10, 10, 10
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, ny)
    z = np.linspace(-1, 1, nz)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Gaussian-like consciousness field
    field = np.exp(-(X**2 + Y**2 + Z**2) / 0.5)
    
    # Add some noise
    field += 0.1 * np.random.randn(*field.shape)
    
    return {
        'field': field,
        'coordinates': (X, Y, Z),
        'grid_spacing': (x[1] - x[0], y[1] - y[0], z[1] - z[0])
    }


# Configure matplotlib for testing
@pytest.fixture(autouse=True)
def configure_matplotlib():
    """Configure matplotlib for testing (non-interactive backend)."""
    import matplotlib
    matplotlib.use('Agg')


# Test markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "simulation: marks tests as simulation tests"
    )
    config.addinivalue_line(
        "markers", "validation: marks tests as validation tests"
    )


# Custom assert helpers
def assert_field_shape(field, expected_shape):
    """Assert that a field has the expected shape."""
    assert field.shape == expected_shape, f"Expected shape {expected_shape}, got {field.shape}"


def assert_physical_units(value, expected_units, tolerance=1e-10):
    """Assert that a value has physically reasonable magnitude for given units."""
    # This is a placeholder for more sophisticated unit checking
    assert np.isfinite(value), "Value must be finite"
    assert not np.isnan(value), "Value cannot be NaN"


def assert_consciousness_field_properties(field):
    """Assert basic properties that consciousness fields should satisfy."""
    # Field should be real-valued
    assert np.isreal(field).all(), "Consciousness field should be real-valued"
    
    # Field should be finite everywhere
    assert np.isfinite(field).all(), "Consciousness field should be finite everywhere"
    
    # Field should have reasonable magnitude (not exactly zero everywhere)
    assert not np.allclose(field, 0), "Consciousness field should not be zero everywhere"

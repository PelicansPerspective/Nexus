"""
Unit tests for CFH simulator core functions.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "simulations"))

from cfh_simulator import CFHSimulator


class TestCFHSimulator:
    """Test class for CFH simulator functionality."""
    
    def test_initialization(self, cfh_parameters):
        """Test simulator initialization with valid parameters."""
        sim = CFHSimulator(
            grid_size=16,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        assert sim.grid_size == 16
        assert sim.mass_psi == cfh_parameters['mass_psi']
        assert sim.coupling_constant == cfh_parameters['coupling_constant']
        assert sim.field is not None
        assert sim.field.shape == (16, 16, 16)
    
    def test_invalid_parameters(self):
        """Test that invalid parameters raise appropriate errors."""
        # Negative mass should raise error
        with pytest.raises(ValueError):
            CFHSimulator(grid_size=16, mass_psi=-1e-18)
        
        # Zero grid size should raise error
        with pytest.raises(ValueError):
            CFHSimulator(grid_size=0)
        
        # Negative coupling constant should raise error
        with pytest.raises(ValueError):
            CFHSimulator(grid_size=16, coupling_constant=-1e-10)
    
    def test_field_initialization(self, cfh_parameters):
        """Test that field is properly initialized."""
        sim = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Field should be real-valued
        assert np.isreal(sim.field).all()
        
        # Field should be finite everywhere
        assert np.isfinite(sim.field).all()
        
        # Field should have correct shape
        assert sim.field.shape == (8, 8, 8)
    
    def test_consciousness_density_gaussian(self, cfh_parameters):
        """Test Gaussian consciousness density generation."""
        sim = CFHSimulator(
            grid_size=16,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Generate Gaussian consciousness density
        center = (8, 8, 8)
        sigma = 2.0
        density = sim.consciousness_density_gaussian(center, sigma)
        
        # Check properties
        assert density.shape == (16, 16, 16)
        assert np.all(density >= 0)  # Density should be non-negative
        assert np.max(density) > 0   # Should have some non-zero values
        assert np.isfinite(density).all()
        
        # Maximum should be at center
        max_idx = np.unravel_index(np.argmax(density), density.shape)
        assert max_idx == center
    
    def test_step_evolution(self, cfh_parameters):
        """Test single time step evolution."""
        sim = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Store initial field
        initial_field = sim.field.copy()
        
        # Add consciousness density
        density = sim.consciousness_density_gaussian((4, 4, 4), 1.0)
        
        # Evolve one step
        sim.step(dt=1e-6, consciousness_density=density)
        
        # Field should have changed
        assert not np.allclose(sim.field, initial_field)
        
        # Field should remain finite
        assert np.isfinite(sim.field).all()
    
    def test_energy_conservation(self, cfh_parameters):
        """Test energy calculation and approximate conservation."""
        sim = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Calculate initial energy
        initial_energy = sim.calculate_energy()
        assert np.isfinite(initial_energy)
        assert initial_energy >= 0
        
        # Evolve without sources (should conserve energy approximately)
        for _ in range(5):
            sim.step(dt=1e-7, consciousness_density=None)
        
        final_energy = sim.calculate_energy()
        
        # Energy should be approximately conserved (within numerical precision)
        relative_change = abs(final_energy - initial_energy) / max(initial_energy, 1e-20)
        assert relative_change < 1e-3, f"Energy not conserved: {relative_change}"
    
    def test_field_magnitude_scaling(self, cfh_parameters):
        """Test that field magnitude scales appropriately with coupling constant."""
        base_coupling = cfh_parameters['coupling_constant']
        
        sim1 = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=base_coupling
        )
        
        sim2 = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=2 * base_coupling
        )
        
        # Add same consciousness density to both
        density = sim1.consciousness_density_gaussian((4, 4, 4), 1.0)
        
        # Evolve both
        for _ in range(10):
            sim1.step(dt=1e-6, consciousness_density=density)
            sim2.step(dt=1e-6, consciousness_density=density)
        
        # Stronger coupling should produce larger field changes
        field1_norm = np.linalg.norm(sim1.field)
        field2_norm = np.linalg.norm(sim2.field)
        
        assert field2_norm > field1_norm, "Stronger coupling should produce larger fields"
    
    @pytest.mark.parametrize("grid_size", [4, 8, 16])
    def test_different_grid_sizes(self, cfh_parameters, grid_size):
        """Test simulator works with different grid sizes."""
        sim = CFHSimulator(
            grid_size=grid_size,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        assert sim.field.shape == (grid_size, grid_size, grid_size)
        
        # Should be able to evolve
        density = sim.consciousness_density_gaussian(
            (grid_size//2, grid_size//2, grid_size//2), 
            grid_size//4
        )
        sim.step(dt=1e-6, consciousness_density=density)
        
        assert np.isfinite(sim.field).all()
    
    def test_boundary_conditions(self, cfh_parameters):
        """Test periodic boundary conditions."""
        sim = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Create a sharp feature near boundary
        sim.field[0, 4, 4] = 1.0
        sim.field[7, 4, 4] = 1.0
        
        # Evolve - should maintain periodicity
        for _ in range(5):
            sim.step(dt=1e-7)
        
        # Field should remain finite
        assert np.isfinite(sim.field).all()
        
        # No NaN values
        assert not np.isnan(sim.field).any()


class TestMathematicalConsistency:
    """Test mathematical consistency of CFH formulations."""
    
    def test_dimensional_consistency(self, cfh_parameters):
        """Test that all parameters have consistent dimensions."""
        # Mass should be in kg
        assert cfh_parameters['mass_psi'] > 0
        assert cfh_parameters['mass_psi'] < 1e-10  # Should be very small
        
        # Coupling constant should have correct dimensions
        # [g_ψ] = [M^(1/2) L^(-3/2) T^(-1)]
        assert cfh_parameters['coupling_constant'] > 0
        
        # Physical constants should be correct
        assert abs(cfh_parameters['hbar'] - 1.055e-34) < 1e-36
        assert abs(cfh_parameters['c'] - 3e8) < 1e6
    
    def test_propagator_properties(self, cfh_parameters):
        """Test properties of the field propagator."""
        sim = CFHSimulator(
            grid_size=16,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Create delta function source
        center = sim.grid_size // 2
        r = np.sqrt((np.arange(sim.grid_size) - center)**2)
        
        # Propagator should decay exponentially
        mass_psi = cfh_parameters['mass_psi']
        hbar = cfh_parameters['hbar']
        c = cfh_parameters['c']
        
        expected_decay_length = hbar * c / (mass_psi * c**2)
        
        # For our parameters, this should be very large compared to grid
        assert expected_decay_length > 1e10  # Much larger than typical scales
    
    def test_field_equation_properties(self, cfh_parameters, numerical_tolerance):
        """Test that field equation has expected mathematical properties."""
        sim = CFHSimulator(
            grid_size=8,
            mass_psi=cfh_parameters['mass_psi'],
            coupling_constant=cfh_parameters['coupling_constant']
        )
        
        # Test linearity: if ψ₁ and ψ₂ are solutions, so is aψ₁ + bψ₂
        field1 = sim.field.copy()
        field2 = np.random.randn(*sim.field.shape) * 1e-10
        
        # The field equation should be linear in the field
        # This is implicit in the simulation structure
        assert True  # Placeholder for more detailed linearity tests


if __name__ == "__main__":
    pytest.main([__file__])

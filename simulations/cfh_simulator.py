"""
Consciousness-Field Hypothesis Simulation Suite

This module provides tools for simulating the predicted effects of the 
Ψ-field on quantum correlations, particularly CHSH inequality violations.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from typing import Tuple, Dict, List, Optional
import warnings

class PsiFieldSimulator:
    """
    Simulate consciousness-modulated quantum correlations via Ψ-field theory.
    
    The core prediction is: a = 1 + κ_eff * ⟨Ψ⟩
    where ⟨Ψ⟩ is proportional to neural coherence ρ_obs (e.g., gamma PLV).
    """
    
    def __init__(self, 
                 kappa_eff: float = 0.1,
                 m_psi: float = 1e-2,  # eV
                 C_speed: float = 1e20):  # in units of c
        """
        Initialize the Ψ-field simulator.
        
        Parameters:
        -----------
        kappa_eff : float
            Effective coupling constant (dimensionless after scaling)
        m_psi : float
            Ψ-field mass in eV
        C_speed : float
            Hyper-causal propagation speed in units of c
        """
        self.kappa_eff = kappa_eff
        self.m_psi = m_psi
        self.C_speed = C_speed
        
    def compute_psi_expectation(self, rho_obs: np.ndarray) -> np.ndarray:
        """
        Compute ⟨Ψ⟩ from neural coherence ρ_obs.
        
        In the linear regime: ⟨Ψ⟩ ≈ J₀ * G_C(0)
        where J₀ = κ * ρ_obs and G_C(0) is the zero-momentum propagator.
        """
        # Simplified model: ⟨Ψ⟩ ∝ ρ_obs
        # The full propagator calculation would involve:
        # G_C(0) = -i/(16π²) * (1/m_ψ²) * [log(C/m_ψ) + O(1)]
        
        normalization = np.log(self.C_speed / self.m_psi) / (16 * np.pi**2)
        psi_expectation = self.kappa_eff * rho_obs * normalization
        
        return psi_expectation
    
    def chsh_amplification_factor(self, rho_obs: np.ndarray) -> np.ndarray:
        """
        Compute the CHSH amplification factor a = 1 + κ_eff * ⟨Ψ⟩.
        """
        psi_exp = self.compute_psi_expectation(rho_obs)
        return 1.0 + psi_exp
    
    def simulate_chsh_experiment(self, 
                                rho_obs: np.ndarray,
                                n_trials: int = 10000,
                                noise_level: float = 0.01) -> Dict:
        """
        Simulate an EEG-gated CHSH experiment.
        
        Parameters:
        -----------
        rho_obs : array
            Neural coherence values (e.g., gamma PLV)
        n_trials : int
            Number of measurement trials
        noise_level : float
            Experimental noise level
            
        Returns:
        --------
        dict : Simulation results including S values and statistics
        """
        # Standard quantum mechanical CHSH maximum
        S_quantum = 2 * np.sqrt(2)
        
        # Compute amplification factors
        a_factors = self.chsh_amplification_factor(rho_obs)
        
        # Amplified CHSH values
        S_amplified = a_factors * S_quantum
        
        # Add experimental noise
        noise = np.random.normal(0, noise_level, len(S_amplified))
        S_measured = S_amplified + noise
        
        # Statistical analysis
        results = {
            'rho_obs': rho_obs,
            'amplification_factors': a_factors,
            'S_theoretical': S_amplified,
            'S_measured': S_measured,
            'S_quantum_bound': S_quantum,
            'tsirelson_violations': S_measured > S_quantum,
            'mean_violation': np.mean(S_measured[S_measured > S_quantum] - S_quantum),
            'violation_probability': np.mean(S_measured > S_quantum),
            'statistical_significance': self._compute_significance(S_measured, S_quantum)
        }
        
        return results
    
    def _compute_significance(self, S_measured: np.ndarray, S_quantum: float) -> float:
        """Compute statistical significance of Tsirelson bound violations."""
        violations = S_measured - S_quantum
        if np.all(violations <= 0):
            return 1.0  # No violations
        
        # One-tailed t-test against null hypothesis of no violation
        t_stat, p_value = stats.ttest_1samp(violations.flatten(), 0, alternative='greater')
        return float(p_value)
    
    def generate_realistic_eeg_data(self, 
                                  n_subjects: int = 50,
                                  n_trials_per_subject: int = 100,
                                  coherence_distribution: str = 'beta') -> np.ndarray:
        """
        Generate realistic EEG coherence data.
        
        Parameters:
        -----------
        n_subjects : int
            Number of experimental subjects
        n_trials_per_subject : int
            Number of trials per subject
        coherence_distribution : str
            Distribution type for PLV values ('beta', 'gamma', 'normal')
        """
        total_trials = n_subjects * n_trials_per_subject
        
        if coherence_distribution == 'beta':
            # Beta distribution bounded [0,1], typical for PLV
            rho_obs = np.random.beta(2, 5, total_trials)  # Skewed toward lower values
        elif coherence_distribution == 'gamma':
            # Gamma distribution, rescaled to [0,1]
            raw_values = np.random.gamma(1.5, 0.3, total_trials)
            rho_obs = np.clip(raw_values, 0, 1)
        else:
            # Normal distribution, clipped to [0,1]
            rho_obs = np.clip(np.random.normal(0.3, 0.2, total_trials), 0, 1)
        
        return rho_obs
    
    def plot_results(self, results: Dict, save_path: Optional[str] = None):
        """Plot simulation results."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot 1: ρ_obs vs S values
        axes[0,0].scatter(results['rho_obs'], results['S_measured'], 
                         alpha=0.6, s=20)
        axes[0,0].axhline(y=results['S_quantum_bound'], color='red', 
                         linestyle='--', label='Tsirelson Bound')
        axes[0,0].set_xlabel('Neural Coherence ρ_obs')
        axes[0,0].set_ylabel('CHSH Parameter S')
        axes[0,0].legend()
        axes[0,0].set_title('Consciousness-Modulated CHSH Violations')
        
        # Plot 2: Amplification factor distribution
        axes[0,1].hist(results['amplification_factors'], bins=30, 
                      alpha=0.7, edgecolor='black')
        axes[0,1].axvline(x=1.0, color='red', linestyle='--', 
                         label='Standard QM (a=1)')
        axes[0,1].set_xlabel('Amplification Factor a')
        axes[0,1].set_ylabel('Frequency')
        axes[0,1].legend()
        axes[0,1].set_title('Distribution of Amplification Factors')
        
        # Plot 3: Violation significance
        violations = results['S_measured'] - results['S_quantum_bound']
        axes[1,0].hist(violations, bins=30, alpha=0.7, edgecolor='black')
        axes[1,0].axvline(x=0, color='red', linestyle='--', 
                         label='No Violation')
        axes[1,0].set_xlabel('S - S_quantum')
        axes[1,0].set_ylabel('Frequency')
        axes[1,0].legend()
        axes[1,0].set_title('Tsirelson Bound Violations')
        
        # Plot 4: Coherence vs violations
        axes[1,1].scatter(results['rho_obs'], violations, alpha=0.6, s=20)
        axes[1,1].axhline(y=0, color='red', linestyle='--')
        axes[1,1].set_xlabel('Neural Coherence ρ_obs')
        axes[1,1].set_ylabel('S - S_quantum')
        axes[1,1].set_title('Coherence vs Quantum Violations')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()

def run_example_simulation():
    """Run an example simulation of the CFH predictions."""
    print("Running Consciousness-Field Hypothesis Simulation...")
    
    # Initialize simulator
    simulator = PsiFieldSimulator(kappa_eff=0.15, m_psi=1e-2, C_speed=1e20)
    
    # Generate realistic EEG data
    rho_obs = simulator.generate_realistic_eeg_data(
        n_subjects=50, 
        n_trials_per_subject=200,
        coherence_distribution='beta'
    )
    
    # Run simulation
    results = simulator.simulate_chsh_experiment(
        rho_obs=rho_obs,
        n_trials=len(rho_obs),
        noise_level=0.02
    )
    
    # Print results
    print(f"\nSimulation Results:")
    print(f"Tsirelson violations: {results['violation_probability']:.1%}")
    print(f"Mean violation magnitude: {results['mean_violation']:.4f}")
    print(f"Statistical significance: p = {results['statistical_significance']:.2e}")
    
    # Plot results
    simulator.plot_results(results)
    
    return results

if __name__ == "__main__":
    results = run_example_simulation()

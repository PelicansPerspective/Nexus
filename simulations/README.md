# CFH Simulation Suite

This directory contains comprehensive simulation tools for modeling and analyzing the predictions of the Consciousness-Field Hypothesis.

## Overview

The simulation suite provides:
- **Theoretical predictions**: Model CFH effects under various conditions
- **Experimental design**: Power analysis and optimization
- **Data analysis**: Tools for processing real experimental data
- **Validation**: Cross-check theoretical predictions

## Core Modules

### 📊 [`cfh_simulator.py`](./cfh_simulator.py)
Primary simulation engine for consciousness-modulated quantum correlations
- CHSH parameter calculations with Ψ-field amplification
- Realistic EEG data generation
- Statistical analysis tools
- Visualization and plotting

### 🧮 Mathematical Models

#### Ψ-Field Propagator
```python
def psi_field_propagator(k, m_psi, C_speed):
    """Modified propagator with hyper-causal boundary conditions"""
    return (1j * np.exp(-np.abs(k[0])/C_speed)) / (k**2 - m_psi**2 + 1j*epsilon)
```

#### CHSH Amplification
```python
def chsh_amplification(rho_obs, kappa_eff=0.1):
    """Compute amplification factor a = 1 + κ_eff⟨Ψ⟩"""
    psi_expectation = compute_psi_expectation(rho_obs)
    return 1.0 + kappa_eff * psi_expectation
```

#### Neural Coherence Modeling
```python
def generate_realistic_plv(n_subjects=50, distribution='beta'):
    """Generate realistic EEG phase-locking values"""
    if distribution == 'beta':
        return np.random.beta(2, 5, n_subjects)  # Skewed toward lower values
    elif distribution == 'gamma':
        raw = np.random.gamma(1.5, 0.3, n_subjects)
        return np.clip(raw, 0, 1)
```

## Simulation Workflows

### 1. Basic CFH Prediction
```python
from cfh_simulator import PsiFieldSimulator

# Initialize simulator
sim = PsiFieldSimulator(kappa_eff=0.15, m_psi=1e-2, C_speed=1e20)

# Generate test data
rho_obs = sim.generate_realistic_eeg_data(n_subjects=100)

# Run simulation
results = sim.simulate_chsh_experiment(rho_obs, n_trials=10000)

# Analyze results
print(f"Tsirelson violations: {results['violation_probability']:.1%}")
print(f"Statistical significance: p = {results['statistical_significance']:.2e}")
```

### 2. Parameter Sensitivity Analysis
```python
def parameter_sweep():
    """Analyze sensitivity to model parameters"""
    kappa_values = np.logspace(-3, 0, 20)  # 0.001 to 1.0
    violation_rates = []
    
    for kappa in kappa_values:
        sim = PsiFieldSimulator(kappa_eff=kappa)
        results = sim.simulate_chsh_experiment(standard_eeg_data)
        violation_rates.append(results['violation_probability'])
    
    plot_parameter_sensitivity(kappa_values, violation_rates)
```

### 3. Power Analysis for Experiments
```python
def experimental_power_analysis(effect_size_range, n_subjects_range):
    """Determine required sample sizes for statistical power"""
    power_matrix = np.zeros((len(effect_size_range), len(n_subjects_range)))
    
    for i, effect_size in enumerate(effect_size_range):
        for j, n_subjects in enumerate(n_subjects_range):
            power = simulate_statistical_power(effect_size, n_subjects)
            power_matrix[i, j] = power
    
    plot_power_analysis(power_matrix, effect_size_range, n_subjects_range)
```

## Advanced Features

### Monte Carlo Validation
```python
class MonteCarloValidator:
    """Validate theoretical predictions with Monte Carlo methods"""
    
    def __init__(self, n_iterations=10000):
        self.n_iterations = n_iterations
    
    def validate_amplification_formula(self):
        """Test a = 1 + κ_eff⟨Ψ⟩ against numerical integration"""
        theoretical_results = []
        numerical_results = []
        
        for _ in range(self.n_iterations):
            # Generate random parameters
            rho_obs = np.random.beta(2, 5)
            kappa_eff = np.random.uniform(0.01, 0.5)
            
            # Theoretical calculation
            theoretical = 1 + kappa_eff * self.compute_psi_analytical(rho_obs)
            
            # Numerical integration
            numerical = self.compute_amplification_numerical(rho_obs, kappa_eff)
            
            theoretical_results.append(theoretical)
            numerical_results.append(numerical)
        
        correlation = np.corrcoef(theoretical_results, numerical_results)[0,1]
        return correlation
```

### Noise Modeling
```python
def add_realistic_noise(clean_signal, noise_model='experimental'):
    """Add realistic noise to simulation data"""
    if noise_model == 'experimental':
        # Based on actual experimental conditions
        detector_noise = np.random.poisson(100, len(clean_signal))  # Dark counts
        timing_jitter = np.random.normal(0, 25e-12, len(clean_signal))  # 25ps RMS
        thermal_drift = generate_thermal_drift(len(clean_signal))
        
        noisy_signal = clean_signal + detector_noise + timing_jitter + thermal_drift
        
    elif noise_model == 'quantum':
        # Fundamental quantum limitations
        shot_noise = np.random.poisson(clean_signal)
        noisy_signal = shot_noise
        
    return noisy_signal
```

### Data Analysis Tools
```python
def analyze_experimental_data(chsh_data, eeg_data, metadata):
    """Comprehensive analysis of experimental results"""
    results = {}
    
    # Basic statistics
    results['mean_S'] = np.mean(chsh_data)
    results['std_S'] = np.std(chsh_data)
    results['tsirelson_violations'] = np.sum(chsh_data > 2.828)
    
    # Correlation analysis
    plv_data = extract_plv(eeg_data)
    results['eeg_correlation'] = pearsonr(chsh_data, plv_data)
    
    # Time-series analysis
    results['temporal_stability'] = analyze_temporal_trends(chsh_data)
    
    # Individual differences
    results['subject_effects'] = analyze_individual_differences(chsh_data, metadata)
    
    # Statistical significance
    baseline_S = 2.828
    results['significance'] = ttest_1samp(chsh_data, baseline_S, alternative='greater')
    
    return results
```

## Visualization Tools

### Standard Plots
```python
def create_standard_plots(results, save_path=None):
    """Generate comprehensive result visualization"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot 1: Neural coherence vs CHSH values
    axes[0,0].scatter(results['rho_obs'], results['S_measured'])
    axes[0,0].axhline(y=2.828, color='red', linestyle='--', label='Tsirelson Bound')
    axes[0,0].set_xlabel('Neural Coherence ρ_obs')
    axes[0,0].set_ylabel('CHSH Parameter S')
    
    # Plot 2: Amplification factor distribution
    axes[0,1].hist(results['amplification_factors'], bins=30, alpha=0.7)
    axes[0,1].axvline(x=1.0, color='red', linestyle='--', label='Standard QM')
    axes[0,1].set_xlabel('Amplification Factor a')
    
    # Plot 3: Statistical significance
    violations = results['S_measured'] - 2.828
    axes[0,2].hist(violations, bins=30, alpha=0.7)
    axes[0,2].axvline(x=0, color='red', linestyle='--')
    axes[0,2].set_xlabel('S - 2.828')
    
    # Add more specialized plots...
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
```

### Interactive Analysis
```python
def create_interactive_dashboard():
    """Create interactive dashboard for parameter exploration"""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import ipywidgets as widgets
    
    # Parameter sliders
    kappa_slider = widgets.FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01)
    n_subjects_slider = widgets.IntSlider(value=50, min=10, max=200, step=10)
    
    # Interactive plotting function
    def update_plot(kappa_eff, n_subjects):
        sim = PsiFieldSimulator(kappa_eff=kappa_eff)
        rho_obs = sim.generate_realistic_eeg_data(n_subjects=n_subjects)
        results = sim.simulate_chsh_experiment(rho_obs)
        
        # Create interactive plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=results['rho_obs'], y=results['S_measured'],
                                mode='markers', name='Data'))
        fig.add_hline(y=2.828, line_dash="dash", line_color="red",
                     annotation_text="Tsirelson Bound")
        
        return fig
    
    # Widget interaction
    interactive_plot = widgets.interact(update_plot, 
                                       kappa_eff=kappa_slider,
                                       n_subjects=n_subjects_slider)
    
    return interactive_plot
```

## Running Simulations

### Quick Start
```bash
# Basic simulation
python cfh_simulator.py

# Parameter sweep
python scripts/parameter_analysis.py

# Power analysis
python scripts/power_calculation.py

# Validation suite
python scripts/validation_tests.py
```

### Custom Analysis
```python
# Example custom analysis
from cfh_simulator import PsiFieldSimulator
import numpy as np

# Set up simulation
sim = PsiFieldSimulator(kappa_eff=0.12, m_psi=1e-2)

# Generate data for specific experimental conditions
high_meditators = sim.generate_realistic_eeg_data(n_subjects=25, 
                                                 coherence_distribution='gamma')
control_subjects = sim.generate_realistic_eeg_data(n_subjects=25,
                                                  coherence_distribution='normal')

# Run comparative simulation
results_meditators = sim.simulate_chsh_experiment(high_meditators)
results_controls = sim.simulate_chsh_experiment(control_subjects)

# Statistical comparison
from scipy.stats import mannwhitneyu
statistic, p_value = mannwhitneyu(results_meditators['S_measured'],
                                 results_controls['S_measured'],
                                 alternative='greater')

print(f"Meditation effect p-value: {p_value:.2e}")
```

## Validation and Testing

### Unit Tests
```python
def test_amplification_formula():
    """Test core amplification calculation"""
    sim = PsiFieldSimulator(kappa_eff=0.1)
    rho_obs = np.array([0.0, 0.5, 1.0])
    
    a_factors = sim.chsh_amplification_factor(rho_obs)
    
    # Test bounds
    assert np.all(a_factors >= 1.0)  # Amplification only
    assert a_factors[0] == 1.0  # No enhancement at zero coherence
    assert a_factors[2] > a_factors[1]  # Monotonic increase

def test_chsh_bounds():
    """Test CHSH parameter bounds"""
    sim = PsiFieldSimulator(kappa_eff=0.0)  # No enhancement
    rho_obs = np.random.random(1000)
    
    results = sim.simulate_chsh_experiment(rho_obs, noise_level=0.0)
    
    # Should respect Tsirelson bound with no enhancement
    assert np.all(results['S_theoretical'] <= 2.828 + 1e-10)
```

### Integration Tests
```python
def test_full_simulation_pipeline():
    """Test complete simulation workflow"""
    # Generate test data
    sim = PsiFieldSimulator()
    eeg_data = sim.generate_realistic_eeg_data(n_subjects=100)
    
    # Run simulation
    results = sim.simulate_chsh_experiment(eeg_data, n_trials=1000)
    
    # Verify output structure
    required_keys = ['S_measured', 'amplification_factors', 'violation_probability']
    for key in required_keys:
        assert key in results
    
    # Verify statistical properties
    assert len(results['S_measured']) == 1000
    assert 0 <= results['violation_probability'] <= 1
```

## Performance Optimization

### Vectorized Calculations
```python
@numba.jit(nopython=True)
def fast_plv_calculation(eeg_data, freq_range):
    """Optimized PLV calculation using Numba"""
    # Vectorized operations for speed
    filtered_data = bandpass_filter_vectorized(eeg_data, freq_range)
    phases = np.angle(hilbert_transform_fast(filtered_data))
    plv_values = compute_plv_vectorized(phases)
    return plv_values
```

### Parallel Processing
```python
from multiprocessing import Pool
import concurrent.futures

def parallel_simulation(parameter_sets):
    """Run multiple simulations in parallel"""
    def run_single_simulation(params):
        sim = PsiFieldSimulator(**params)
        return sim.simulate_chsh_experiment(params['eeg_data'])
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(run_single_simulation, parameter_sets))
    
    return results
```

## Documentation and Help

### Function Documentation
All functions include comprehensive docstrings with:
- Parameter descriptions
- Return value specifications
- Usage examples
- Mathematical formulations
- References to theory documents

### Example Notebooks
See `examples/` directory for Jupyter notebooks demonstrating:
- Basic simulation usage
- Advanced analysis techniques
- Parameter sensitivity studies
- Experimental design optimization
- Data visualization methods

---

*The simulation suite is designed to bridge theory and experiment, providing robust tools for exploring the fascinating predictions of the Consciousness-Field Hypothesis.*

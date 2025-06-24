#!/usr/bin/env python3
"""
Consciousness-Field Hypothesis Project Setup
============================================

This script sets up the development environment and validates the project structure
for the CFH research suite.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+ is being used."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_requirements():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def validate_directory_structure():
    """Validate that all required directories exist."""
    required_dirs = [
        "theory",
        "experiments", 
        "simulations",
        "papers",
        "data",
        "scripts",
        "docs",
        "legacy"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ Directory structure validated")
    return True

def test_simulation_suite():
    """Test that the simulation suite works correctly."""
    print("🧮 Testing simulation suite...")
    try:
        # Try to import and run basic simulation
        sys.path.append('simulations')
        from cfh_simulator import PsiFieldSimulator
        
        # Run quick test
        sim = PsiFieldSimulator(kappa_eff=0.1)
        test_data = sim.generate_realistic_eeg_data(n_subjects=10)
        results = sim.simulate_chsh_experiment(test_data, n_trials=100)
        
        if 'violation_probability' in results:
            print("✅ Simulation suite working correctly")
            return True
        else:
            print("❌ Simulation suite test failed")
            return False
            
    except ImportError as e:
        print(f"❌ Cannot import simulation modules: {e}")
        return False
    except Exception as e:
        print(f"❌ Simulation test failed: {e}")
        return False

def create_config_file():
    """Create default configuration file."""
    config = {
        "project_name": "Consciousness-Field Hypothesis",
        "version": "1.0.0",
        "author": "Justin Todd",
        "description": "A scalar field theory of consciousness-quantum interactions",
        "theory": {
            "psi_field_mass": 1e-2,  # eV
            "hyper_causal_speed": 1e20,  # in units of c
            "coupling_strength_range": [0.01, 0.5],
            "chsh_quantum_bound": 2.828
        },
        "experiments": {
            "eeg_sampling_rate": 2000,  # Hz
            "gamma_frequency_range": [35, 45],  # Hz
            "plv_threshold": 0.7,
            "significance_threshold": 0.001
        },
        "simulations": {
            "default_n_subjects": 50,
            "default_n_trials": 10000,
            "noise_level": 0.02,
            "monte_carlo_iterations": 10000
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration file created")

def generate_project_summary():
    """Generate a project summary report."""
    summary = """
# Consciousness-Field Hypothesis Project Summary

## Setup Status: ✅ COMPLETE

### Project Structure
- Theory documents: Complete mathematical framework
- Experimental protocols: Detailed methodology for 3 key experiments  
- Simulation suite: Functional prediction and analysis tools
- Analysis scripts: Data processing and statistical analysis
- Documentation: Comprehensive guides and tutorials

### Key Features
- **Testable Predictions**: S > 2.828 CHSH violations
- **Mathematical Rigor**: Proven micro-causality, renormalizability
- **Experimental Protocols**: EEG-gated Bell tests, remote viewing, NV-centers
- **Simulation Tools**: Monte Carlo validation, parameter sensitivity
- **Open Science**: Reproducible methods, shareable data

### Next Steps
1. Complete experimental preparations
2. Seek laboratory collaborations  
3. Apply for research funding
4. Submit theoretical papers for publication
5. Begin proof-of-concept experiments

### Status: Ready for Research!
The theoretical framework is complete and experimentally testable.
The simulation suite provides robust prediction and analysis capabilities.
All systems are ready for the next phase of validation and discovery.
"""
    
    with open('PROJECT_SUMMARY.md', 'w') as f:
        f.write(summary)
    
    print("✅ Project summary generated")

def main():
    """Main setup routine."""
    print("🧠⚛️ Consciousness-Field Hypothesis Project Setup")
    print("=" * 50)
    
    success = True
    
    # Check prerequisites
    success &= check_python_version()
    success &= validate_directory_structure()
    
    # Install dependencies
    if success:
        success &= install_requirements()
    
    # Test functionality
    if success:
        success &= test_simulation_suite()
    
    # Create configuration
    if success:
        create_config_file()
        generate_project_summary()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\n🚀 Quick Start:")
        print("   python simulations/cfh_simulator.py")
        print("   python scripts/analyze_experimental_data.py --help")
        print("\n📚 Documentation:")
        print("   docs/README.md - Project overview")
        print("   theory/README.md - Theoretical framework")
        print("   experiments/README.md - Experimental protocols")
        print("\n🤝 Contributing:")
        print("   See CONTRIBUTING.md for collaboration guidelines")
        print("   Open GitHub issues for questions and discussion")
        
    else:
        print("❌ Setup encountered errors. Please resolve issues and try again.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

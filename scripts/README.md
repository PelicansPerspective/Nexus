# Analysis and Utility Scripts

This directory contains utility scripts for data analysis, visualization, and experimental support.

## Core Scripts

### 📊 `analyze_experimental_data.py`
Comprehensive analysis pipeline for experimental results
- Statistical hypothesis testing
- Effect size calculations
- Correlation analysis
- Report generation

### 📈 `visualize_results.py`
Advanced visualization tools
- Publication-quality plots
- Interactive dashboards
- Animation capabilities
- Multi-dimensional analysis

### 🔧 `calibration_tools.py`
Equipment calibration and validation
- EEG system calibration
- Quantum optics alignment
- Noise characterization
- Cross-lab standardization

### 📋 `experimental_control.py`
Real-time experimental control
- EEG-based triggering
- CHSH measurement coordination
- Data acquisition management
- Safety monitoring

## Usage Examples

### Basic Data Analysis
```bash
python analyze_experimental_data.py --data_file results.csv --output report.pdf
```

### Visualization
```bash
python visualize_results.py --input data/ --format publication --save plots/
```

### Calibration
```bash
python calibration_tools.py --system eeg --auto_calibrate --save_config
```

## Dependencies

See `requirements.txt` for complete dependency list:
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.4.0
- pandas >= 1.3.0
- plotly >= 5.0.0
- scikit-learn >= 1.0.0

# Testing Framework

This directory contains unit tests, integration tests, and validation scripts for the CFH project components.

## Test Organization

### Structure
```
/tests/
├── unit/                 # Unit tests for individual functions
├── integration/          # Integration tests for complete workflows
├── validation/           # Validation tests against known results
├── simulation/           # Tests for simulation accuracy and consistency
├── analysis/             # Tests for data analysis scripts
└── conftest.py          # Pytest configuration and fixtures
```

## Running Tests

### Prerequisites
```bash
pip install pytest pytest-cov numpy scipy matplotlib
```

### All Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=simulations --cov=scripts --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/validation/
```

### Individual Test Files
```bash
# Test simulation framework
pytest tests/simulation/test_cfh_simulator.py

# Test analysis scripts
pytest tests/analysis/test_experimental_analysis.py

# Test mathematical consistency
pytest tests/validation/test_dimensional_consistency.py
```

## Test Categories

### Unit Tests (`unit/`)
- Individual function validation
- Parameter boundary testing
- Error handling verification
- Mathematical operation accuracy

### Integration Tests (`integration/`)
- End-to-end workflow testing
- Component interaction validation
- File I/O operations
- Simulation pipeline integrity

### Validation Tests (`validation/`)
- Comparison with analytical solutions
- Benchmark against published results
- Dimensional consistency checks
- Physical constraint verification

### Simulation Tests (`simulation/`)
- Numerical accuracy verification
- Convergence testing
- Parameter sensitivity analysis
- Performance benchmarking

### Analysis Tests (`analysis/`)
- Statistical method validation
- Data processing accuracy
- Visualization correctness
- Error propagation verification

## Test Data

### Synthetic Datasets
- Small test datasets for unit tests
- Known-result scenarios for validation
- Edge cases and boundary conditions
- Error condition examples

### Reference Results
- Analytical solutions where available
- Published benchmark results
- Cross-validation with other tools
- Expected output examples

## Continuous Integration

### GitHub Actions
The repository includes GitHub Actions workflows for:
- Automated testing on push/PR
- Coverage reporting
- Multi-platform testing (Windows, Linux, macOS)
- Python version compatibility (3.8+)

### Quality Gates
- All tests must pass
- Minimum 80% code coverage
- No critical linting errors
- Documentation completeness

## Writing Tests

### Test Function Naming
- Use descriptive names: `test_consciousness_field_propagation()`
- Include edge cases: `test_field_propagation_zero_coupling()`
- Test error conditions: `test_invalid_mass_parameter_raises_error()`

### Test Structure
```python
def test_feature():
    # Arrange - Set up test data
    input_data = create_test_data()
    
    # Act - Execute the function
    result = function_under_test(input_data)
    
    # Assert - Verify the result
    assert result == expected_value
    assert result.shape == expected_shape
    np.testing.assert_allclose(result, expected_array, rtol=1e-10)
```

### Fixtures
Use pytest fixtures for:
- Common test data setup
- Simulation configuration
- Mock objects
- Temporary file handling

### Parameterized Tests
Use `@pytest.mark.parametrize` for:
- Testing multiple parameter values
- Boundary condition testing
- Cross-validation scenarios

## Performance Testing

### Benchmarking
- Execution time measurements
- Memory usage profiling
- Scalability testing
- Comparison with reference implementations

### Regression Testing
- Performance regression detection
- Accuracy regression monitoring
- Feature completeness verification

## Test Requirements

### Dependencies
```python
pytest>=7.0.0
pytest-cov>=4.0.0
numpy>=1.20.0
scipy>=1.7.0
matplotlib>=3.5.0
hypothesis>=6.0.0  # For property-based testing
```

### Additional Tools
- **Black**: Code formatting
- **Flake8**: Linting
- **mypy**: Type checking
- **pytest-xdist**: Parallel testing

## Contributing Tests

### Guidelines
1. Write tests for new features
2. Maintain high coverage (>80%)
3. Include both positive and negative test cases
4. Document complex test scenarios
5. Use meaningful assertions and error messages

### Review Process
1. All tests must pass in CI
2. New tests reviewed for completeness
3. Performance impact assessed
4. Documentation updated as needed

## Test Data Management

### Storage
- Small test data in repository
- Large datasets referenced by URL
- Synthetic data generation scripts
- Version control for test datasets

### Cleanup
- Temporary file cleanup
- Memory management
- Resource deallocation
- Cache clearing

---

For questions about testing or to report test failures, please open an issue with the label "testing".

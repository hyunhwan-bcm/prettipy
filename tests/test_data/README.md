# Test Data for Integration Tests

This directory contains test data used by integration tests.

## mixed_project/

A test project with mixed `.py` and `.ipynb` files that reference each other. Used by `test_integration_mixed.py`.

### Files:

- **utils.py**: Utility functions and Calculator class
  - `calculate_sum(a, b)` - Calculates sum of two numbers
  - `calculate_product(a, b)` - Calculates product of two numbers
  - `Calculator` - A simple calculator class with history

- **main.py**: Main module that imports and uses functions from utils.py
  - `main()` - Demonstrates usage of utility functions
  - `process_data(data)` - Processes list of numbers using utils functions

- **analysis.ipynb**: Jupyter notebook that imports from utils.py
  - Demonstrates using utility functions in a notebook
  - Uses Calculator class
  - Processes sample data

- **experiments.ipynb**: Jupyter notebook that imports from both main.py and utils.py
  - Uses `process_data()` from main.py
  - Uses `Calculator` from utils.py
  - Defines helper function that uses imported functions

### Purpose:

This test project demonstrates:
1. Cross-references between `.py` files (main.py imports utils.py)
2. Jupyter notebooks importing from `.py` files (both notebooks import from utils.py)
3. Jupyter notebooks importing from modules that have dependencies (experiments.ipynb imports from main.py)
4. Mixed project conversion with dependency sorting
5. Auto-linking across file boundaries

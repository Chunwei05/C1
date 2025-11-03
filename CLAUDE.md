# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is BAT (Borrow and Access Tool), a software system for managing library loans and makerspace access, developed as an assignment for FIT2107 Software Quality and Testing at Monash University.

## Architecture

The system follows a layered architecture:

1. **Entry Point**: `run.py` - Simple launcher that imports and calls the main function
2. **Main Controller**: `src/bat.py` - Contains `main()` which initializes all components and starts the UI loop
3. **UI Layer**: `src/bat_ui.py` - Handles all user interface interactions and menu navigation
4. **Business Logic**: `src/business_logic.py` - Implements loan eligibility rules, patron type determination, and makerspace access logic
5. **Data Management**: `src/data_mgmt.py` - Contains both `DataManager` (manages data structures) and `Patron` class (domain model)
6. **Domain Models**: `src/patron.py`, `src/loan.py`, `src/borrowable_item.py` - Entity classes
7. **Supporting Modules**: `src/search.py` (patron/item lookup), `src/user_input.py` (input validation)
8. **Configuration**: `src/config.py` - File paths and system constants

### Application Flow
```
run.py → main() in bat.py → Initializes DataManager, BusinessLogic, BatUi → ui.run() → Main menu loop
```

### Key Business Rules

**Patron Types** (determined by age in `Patron.get_type()`):
- Minor: age < 18 (max 3 loans)
- Regular: 18 ≤ age < 65 (max 5 loans)
- Elderly: age ≥ 65 (max 10 loans)

**Important Constraints**:
- Patrons cannot borrow if they have outstanding fees
- Tools require training flags (`gardening_tool_training`, `carpentry_tool_training`)
- Minors cannot borrow tools (gardening or carpentry)
- Patrons cannot have duplicate item types on loan simultaneously
- Overdue fees calculated at $1.00 per day per item

## Key Commands

### Running the Application
```bash
python run.py
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_ui.py -v

# Run specific test class
python -m pytest tests/test_aal_whitebox.py::TestAALWhiteBox -v
```

### Static Analysis
```bash
# Run pylint (configured in CI to continue on errors)
pylint src/*.py --score=y --exit-zero

# Run pycodestyle for PEP 8 compliance
pycodestyle src/ --statistics
```

## Testing Strategy

The codebase includes comprehensive test coverage with different testing methodologies:

- **White-box testing**: `test_aal_whitebox.py` - Tests business logic with various coverage criteria
- **Path testing**: `test_path_testing.py` - Tests different execution paths through the code
- **MC/DC testing**: `test_mc_dc.py` - Modified Condition/Decision Coverage tests
- **UI testing**: `test_ui.py` - Tests user interface interactions and input validation

All tests use pytest framework and are configured to run in CI/CD pipeline.

## Data Structure

The system uses JSON files for persistence:
- `data/patrons.json` - Stores patron information (ID, name, age, fees, training flags, active loans)
- `data/catalogue.json` - Stores borrowable items (books, gardening tools, carpentry tools)

Configuration is centralized in `src/config.py` with:

- File paths (`CATALOGUE_FILE`, `PATRON_FILE`)
- System constants (`MAX_LOANS`, `OVERDUE_FEE_PER_DAY`)

### Important Implementation Details

**Data Manager and Patron Relationship**:

- `Patron` class is defined in both `src/patron.py` AND `src/data_mgmt.py` (appears to be duplicated)
- `DataManager` stores patrons/items as dictionaries keyed by ID
- Search functions in `src/search.py` work on dictionary `.values()` (converted to lists)

**UI Component Initialization**:

- `BatUi.__init__()` takes parameters in order: `(business_logic, data_manager)` not `(data_manager, business_logic)`
- UI accesses data via `self.data_manager._patron_data` and `self.data_manager._catalogue_data` (direct dict access)

## Development Notes

- **Python Version**: 3.9 (as configured in CI)
- **Dependencies**: pytest, pylint, pycodestyle (installed via pip in CI)
- **CI/CD**: GitHub Actions workflow runs tests and static analysis on push/PR to main/master
- **Code Quality**: Uses pylint and pycodestyle for static analysis with continue-on-error for educational purposes

cd ~/Git/SE_LAB_PES1UG24AM350

cat > LAB5_PES1UG24AM350/issues.md <<'EOF'
# Lab 5 - Static Code Analysis Issues

## Project
Movie Theater Ticket Booking System

## Tools Used
- Pylint
- Bandit
- Flake8

## 1. Pylint Issues

### Issues identified before fixing
- Missing final newline.
- Missing function docstrings.
- Function name did not follow snake_case naming conventions.
- Mutable default argument used in a function.
- Old-style string formatting.
- Bare except statement.
- Incorrect comparison with None.
- Unused local variables.
- Unused import.
- Unsafe use of eval().
- File opened without specifying encoding.
- File handling did not use a context manager.
- Variable name shadowing.

### Fixes applied
- Added function docstrings.
- Renamed reserveSeat() to reserve_seat().
- Replaced the mutable default list with None.
- Used f-strings for formatting.
- Replaced the bare except with explicit error handling.
- Used is None checks where appropriate.
- Removed unused variables and imports.
- Replaced eval() with restricted expression parsing.
- Specified UTF-8 encoding.
- Used a with statement for file handling.
- Improved variable naming and code structure.

### Result
Pylint score after fixes: 10.00/10.

## 2. Bandit Security Issues

### Issues identified before fixing
- B110: try/except/pass could suppress errors.
- B307: use of eval() could execute unsafe expressions.
- B324: MD5 was used for ticket hashing.
- B311: random was used to generate a booking PIN.
- B605: shell command execution through os.system().

### Fixes applied
- Removed the unnecessary exception suppression.
- Replaced eval() with restricted AST-based expression validation.
- Replaced MD5 with SHA-256 for ticket hashing.
- Used the secrets module to generate booking PINs.
- Removed os.system() and used print() instead.

### Result
Bandit after fixes: No issues identified.

## 3. Flake8 Issues

### Issues identified before fixing
- F401: unused import.
- E501: line too long.
- E722: bare except statement.
- F841: unused local variables.
- E711: comparison with None.
- W292: missing final newline.

### Fixes applied
- Removed unused imports and variables.
- Wrapped long lines.
- Replaced the bare except statement.
- Corrected the None comparison.
- Ensured the source file ends with a newline.

### Result
See flake8_report_after.txt for the final Flake8 output.

## Conclusion
Static analysis helped improve code quality, formatting, and security.
Before-and-after reports for Pylint, Bandit, and Flake8 are included
in this submission.
EOF

# LAB 5: Static Code Analysis

## Objective
Analyze and improve the Python ticket booking system using static analysis tools.

## Tools Used
- Pylint
- Bandit
- Flake8

## Improvements
- Fixed code style and naming issues.
- Added function docstrings.
- Removed the mutable default argument.
- Replaced unsafe eval usage with restricted expression parsing.
- Replaced MD5 with SHA-256.
- Used a secure random generator for booking PINs.
- Removed shell command execution.
- Improved file handling.

## Results
- Pylint: 10.00/10
- Bandit: No issues identified
- Flake8: Refer to flake8_report_after.txt.

Before-and-after reports for all three tools are included.

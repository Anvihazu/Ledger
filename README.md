# Ledger CLI

A command-line application written in Python for managing simple bank accounts: creating accounts, depositing and withdrawing funds, transferring money between users, and viewing transaction history. The core application relies strictly on the Python standard library, while the packages listed in `requirements.txt` are used solely for testing, static type checking, and code formatting.

## Requirements

- Python 3.10 or higher (developed and tested on Python 3.14).

## Installation

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone https://github.com/Anvihazu/Ledger.git
   cd ledger
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   *(On Windows: `.venv\Scripts\activate`)*

3. Install development dependencies for testing and code quality checks (the `-r` flag reads the package list from the file):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

By default, all account data is stored in `accounts.json` in the current working directory.

### Create an account (`create`)
```bash
python cli.py create Ann --balance 500
```
Expected output:
```text
Success, account with name: Ann has been created!
```

### Deposit funds (`deposit`)
```bash
python cli.py deposit Ann 200
```
Expected output:
```text
Deposited 200 to Ann. New balance: 700.
```

### Withdraw funds (`withdraw`)
```bash
python cli.py withdraw Ann 100
```
Expected output:
```text
Withdrew 100 from Ann. New balance: 600.
```

### Transfer between accounts (`transfer`)
```bash
python cli.py create Bob --balance 300
python cli.py transfer Ann Bob 150
```
Expected output:
```text
Transferred 150 from Ann to Bob.
```

### Check account balance (`balance`)
```bash
python cli.py balance Ann
```
Expected output:
```text
Ann, your balance is 450.
```

### View transaction history (`history`)
```bash
python cli.py history Ann
```
Expected output:
```text
Deposited 200.
Withdrew 100.
Transferred 150 to Bob.
```

## Exit Codes

- `0` — command executed successfully.
- `1` — business logic or data error (e.g., account not found, insufficient funds, non-positive amount, self-transfer).
- `2` — invalid CLI usage or argument parsing error (standard `argparse` exit code, e.g., missing subcommand or non-integer amount).

## Project Structure

- `account.py` — core domain logic (`Account` class), balance operations, transaction history, and input validation.
- `storage.py` — serialization/deserialization between `Account` objects and dictionaries, JSON file persistence.
- `cli.py` — command-line interface built with `argparse`, error handling, and application entry point.
- `test_account.py` — unit tests for core account logic and validation edge cases.
- `test_storage.py` — tests for JSON serialization and atomic file storage.
- `test_cli.py` — integration tests covering all CLI commands, exit codes, and state persistence.
- `requirements.txt` — dependencies for testing, type checking, and linting.

## Testing and Quality Checks

Run the test suite with coverage report:
```bash
pytest --cov --cov-report=term-missing
```

Run static type checking:
```bash
mypy account.py storage.py cli.py
```

Run linter and formatting checks:
```bash
ruff check .
ruff format --check .
```

## Architecture & Design

- **Separation of concerns:** the domain core (`account.py`) is completely decoupled from storage (`storage.py`) and the CLI layer (`cli.py`), making the business logic easy to test and reuse.
- **Integer-based currency (cents):** all monetary amounts and balances are stored and processed strictly as `int` values to prevent floating-point rounding inaccuracies.
- **Atomic file writes:** data is first written to a temporary file and then atomically swapped into place via `os.replace`, preventing file corruption if an interruption occurs mid-write.

# JSON Processor

A Python 3.12 project for working with JSON files and AWS services using boto3.

## Setup

```bash
pipenv install --python 3.12
pipenv shell
```

## Usage

```bash
python src/main.py
```

## Testing (TDD)

This project follows Test-Driven Development practices.

### Run tests

```bash
pipenv run pytest
```

### Run tests with coverage

```bash
pipenv run pytest --cov=src --cov-report=term-missing
```

### TDD Workflow

1. Write a failing test first (`tests/test_*.py`)
2. Run `pipenv run pytest` to see it fail
3. Write minimal code to make it pass
4. Refactor if needed
5. Repeat

### Mocking AWS Services

Uses [moto](https://github.com/getmoto/moto) to mock AWS services in tests. See `tests/test_example.py` for examples.

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_example.py
├── pytest.ini
├── Pipfile
├── pyproject.toml
└── README.md
```

## Dependencies

- **boto3**: AWS SDK for Python
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **moto**: AWS service mocking for tests

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

### Run all tests

```bash
pipenv run pytest
```

### Run only unit tests (mocked, fast)

```bash
pipenv run pytest -m unit
```

### Run only integration tests (real AWS, requires credentials)

```bash
RUN_INTEGRATION_TESTS=1 pipenv run pytest -m integration
```

### Run tests excluding integration tests

```bash
pipenv run pytest -m "not integration"
```

### Run tests with coverage

```bash
pipenv run pytest --cov=src --cov-report=term-missing
```

### Test Types

- **Unit tests** (`@pytest.mark.unit`): Fast tests using mocked AWS services via [moto](https://github.com/getmoto/moto). See `tests/test_example.py`.
- **Integration tests** (`@pytest.mark.integration`): Tests against real AWS services. Require valid AWS credentials and `RUN_INTEGRATION_TESTS=1`. See `tests/test_integration.py`.

### TDD Workflow

1. Write a failing test first (`tests/test_*.py`)
2. Run `pipenv run pytest` to see it fail
3. Write minimal code to make it pass
4. Refactor if needed
5. Repeat

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_example.py      # Unit tests
│   └── test_integration.py  # Integration tests
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

---
name: testing-python
description: Write and evaluate effective Python tests using pytest. Use when writing tests, reviewing test code, debugging test failures, or improving test coverage. Covers test design, fixtures, parameterization, mocking, and async testing.
---

# Writing Effective Python Tests

## Core Principles

Every test should be **atomic**, **self-contained**, and test **single functionality**. A test that tests multiple things is harder to debug and maintain.

## Test Structure

### Atomic unit tests

Each test should verify a single behavior. The test name should tell you what's broken when it fails. Multiple assertions are fine when they all verify the same behavior.

```python
def test_user_creation_sets_defaults():
    user = User(name="Alice")
    assert user.role == "member"
    assert user.id is not None
    assert user.created_at is not None
```

### Use parameterization for variations of the same concept

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase_conversion(input, expected):
    assert input.upper() == expected
```

### Use separate tests for different functionality

Don't parameterize unrelated behaviors. If the test logic differs, write separate tests.

## Mocking

### Mock at the boundary

```python
from unittest.mock import patch, AsyncMock

async def test_external_api_call():
    with patch("mymodule.external_client.fetch", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "test"}
        result = await my_function()
        assert result == {"data": "test"}
```

### Don't mock what you own

Test your code with real implementations when possible. Mock external services, not internal classes.

## Test Naming

Use descriptive names that explain the scenario:

```python
def test_login_fails_with_invalid_password():
def test_user_can_update_own_profile():
def test_admin_can_delete_any_user():
```

## Error Testing

```python
import pytest

def test_raises_on_invalid_input():
    with pytest.raises(ValueError, match="must be positive"):
        calculate(-1)

async def test_async_raises():
    with pytest.raises(ConnectionError):
        await connect_to_invalid_host()
```

## Running Tests

```bash
pytest -n auto              # Run all tests in parallel
pytest -n auto -x           # Stop on first failure
pytest path/to/test.py      # Run specific file
pytest -k "test_name"       # Run tests matching pattern
pytest -m "not integration" # Exclude integration tests
```

## Checklist

Before submitting tests:
- [ ] Each test tests one thing
- [ ] Descriptive test names
- [ ] Parameterization for variations of same behavior
- [ ] Separate tests for different behaviors

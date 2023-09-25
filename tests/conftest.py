import pytest


@pytest.fixture
def employer_json():
    return r'{"id": 100, "name": "Test Employer", "open_vacancies": 15, "area": {"name": "Test city"}, "alternate_url": "https://test.com", "description": "<b>Test Employer</b><br>This is the test Employer."}'

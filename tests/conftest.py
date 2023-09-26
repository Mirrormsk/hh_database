import pytest


@pytest.fixture
def employer_json():
    return r'{"id": 100, "name": "Test Employer", "open_vacancies": 15, "area": {"name": "Test city"}, "alternate_url": "https://test.com", "description": "<b>Test Employer</b><br>This is the test Employer."}'


@pytest.fixture
def vacancy_json_with_full_salary():
    return r"""{
  "id": 1,
  "name": "Software Engineer",
  "employer": {
    "id": 123
  },
  "area": {
    "name": "New York"
  },
  "salary": {
    "from": 50000,
    "to": 70000,
    "currency": "USD"
  },
  "url": "https://example.com/job/1",
  "snippet": {
    "requirement": "Experience with Python",
    "responsibility": "Develop software"
  }
}
"""


@pytest.fixture
def vacancy_json_without_salary():
    return r"""{
  "id": 1,
  "name": "Software Engineer",
  "employer": {
    "id": 123
  },
  "area": {
    "name": "New York"
  },
  "salary": null,
  "url": "https://example.com/job/1",
  "snippet": {
    "requirement": "Experience with Python",
    "responsibility": "Develop software"
  }
}
"""

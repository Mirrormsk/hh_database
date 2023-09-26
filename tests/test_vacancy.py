from models.models import Vacancy


def test_init_with_salary(vacancy_json_with_full_salary):
    vacancy = Vacancy.model_validate_json(vacancy_json_with_full_salary)

    assert isinstance(vacancy, Vacancy)


def test_init_without_salary(vacancy_json_without_salary):
    vacancy = Vacancy.model_validate_json(vacancy_json_without_salary)

    assert isinstance(vacancy, Vacancy)

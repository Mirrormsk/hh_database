from models.models import Employer


def test_Employer(employer_json):

    emp = Employer.model_validate_json(employer_json)

    assert isinstance(emp, Employer)
    print('Fields:\n')
    print(tuple(emp.model_dump().values()))


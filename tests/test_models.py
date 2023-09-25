from models.models import Employer


def test_Employer(employer_json):

    emp = Employer.model_validate_json(employer_json)

    assert isinstance(emp, Employer)
    print('Fields:\n')
    print(f"({', '.join(key for key in emp.model_dump().keys())})")


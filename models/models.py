from pydantic import BaseModel, Field, AliasPath
from pydantic.functional_validators import field_validator
import re


class Employer(BaseModel):
    id: int
    name: str
    open_vacancies: int
    area: str = Field(validation_alias=AliasPath("area", "name"))
    url: str = Field(validation_alias="alternate_url")
    description: str

    @field_validator("description")
    @staticmethod
    def remove_html_tags(description_text: str):
        """Removes html tags in description"""
        return re.sub(re.compile("<.*?>"), "", description_text)


class Vacancy(BaseModel):
    id: int
    name: str
    employer_id: int = Field(validation_alias=AliasPath("employer", "id"))
    area: str = Field(validation_alias=AliasPath("area", "name"))
    salary_from: int | None = Field(validation_alias=AliasPath("salary", "from"))
    salary_to: int | None = Field(validation_alias=AliasPath("salary", "to"))
    salary_currency: str | None = Field(
        validation_alias=AliasPath("salary", "currency")
    )
    url: str
    requirement: str | None = Field(
        validation_alias=AliasPath("snippet", "requirement")
    )
    responsibility: str | None = Field(
        validation_alias=AliasPath("snippet", "responsibility")
    )

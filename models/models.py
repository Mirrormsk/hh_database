import re
from typing import Optional

import pydantic
from pydantic import BaseModel, Field, AliasPath
from pydantic.functional_validators import field_validator


class Employer(BaseModel):
    """Employer model. Used AliasPath to make flatten model"""

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
        description_text = re.sub(re.compile("<.*?>"), "", description_text)
        description_text = re.sub(re.compile("&nbsp;"), " ", description_text)
        description_text = re.sub(re.compile("&mdash;"), "–", description_text)
        return description_text


class Vacancy(BaseModel):
    """Vacancy model. Used AliasPath to make flatten model"""

    id: int
    name: str
    employer_id: int = Field(validation_alias=AliasPath("employer", "id"))
    area: str = Field(validation_alias=AliasPath("area", "name"))
    salary_from: Optional[int] = Field(validation_alias=AliasPath("salary", "from"))
    salary_to: Optional[int] = Field(validation_alias=AliasPath("salary", "to"))
    salary_currency: Optional[str] = Field(
        validation_alias=AliasPath("salary", "currency")
    )
    url: str
    requirement: str | None = Field(
        validation_alias=AliasPath("snippet", "requirement")
    )
    responsibility: str | None = Field(
        validation_alias=AliasPath("snippet", "responsibility")
    )

    @pydantic.model_validator(mode="before")
    def check_null_salary(self, v):
        """Used if json comes with 'salary': null value"""
        if not self["salary"]:
            self["salary"] = {
                "from": None,
                "to": None,
                "currency": None,
            }
        return self

from decimal import Decimal
import json
from typing import Optional, Union

import pytest
from pydantic import BaseModel, ValidationError
from sqlmodel import Field, SQLModel, Column, String


class A(BaseModel):
    field: str


class Model(SQLModel):
    a: A


class Table(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    a: A = Field(sa_column=Column(type_=String))


def test_model_in_model() -> None:
    Model.model_validate(Model(a=A(field="f")))
    with pytest.raises(ValidationError):
        Model.model_validate(Model(a=A(field=1)))  # type: ignore
    Model.model_validate_json(json.dumps({"a": {"field": "f"}}))
    with pytest.raises(ValidationError):
        Model.model_validate_json(json.dumps({"a": {"field": 1}}))

    Table(a=A(field="f"))
    with pytest.raises(ValidationError):
        Table(a=A(field=1))  # type: ignore

    # double-validate works
    Table.model_validate(Table.model_validate_json(json.dumps({"a": {"field": "f"}})))
    with pytest.raises(ValidationError):
        Table.model_validate(Table.model_validate_json(json.dumps({"a": {"field": 1}})))

    # normal validate doesn't (as of writing this, of course it should work when you read it)
    Table.model_validate_json(json.dumps({"a": {"field": "f"}}))
    with pytest.raises(ValidationError):
        Table.model_validate_json(json.dumps({"a": {"field": 1}}))

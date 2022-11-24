from __future__ import annotations

from pydantic import ConfigDict, Extra, ConstrainedStr


dt_config = ConfigDict(
    extra=Extra.forbid,
    allow_mutation=False,
    frozen=True,
    validate_all=True,
    validate_assignment=True,
)

class NonEmptyStr(ConstrainedStr):
    min_length = 1
from __future__ import annotations

from pydantic import ConfigDict, Extra, ConstrainedStr


def dt_config(title: str | None = None) -> ConfigDict:
    return ConfigDict(
        title=title,
        extra=Extra.forbid,
        allow_mutation=False,
        frozen=True,
        validate_all=True,
        validate_assignment=True,
    )

class NonEmptyStr(ConstrainedStr):
    min_length = 1
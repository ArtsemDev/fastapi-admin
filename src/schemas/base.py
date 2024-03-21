from pydantic import BaseModel, ConfigDict

__all__ = [
    "Schema",
]


class Schema(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        str_strip_whitespace=True,
        ser_json_bytes="utf8",
        ser_json_timedelta="float",
        allow_inf_nan=False
    )

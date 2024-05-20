# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import pydantic_v1
from .media_type import MediaType


class TypedMediaContent(pydantic_v1.BaseModel):
    """
    In conjunction with MediaType this is used to enforce the
    {"type": "image_url", "image_url":"https://..."} spec.

    Invariant: exactly the `type` url is not None
    """

    audio_url: typing.Optional[str] = None
    image_url: typing.Optional[str] = None
    pdf_url: typing.Optional[str] = None
    type: MediaType
    video_url: typing.Optional[str] = None

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
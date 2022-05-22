import typing as t

from ..generic import AdvancedModel


__all__ = ['GenericApiResponse']


class GenericApiResponse(AdvancedModel):
    Response: t.Optional[t.Dict]
    ErrorCode: int
    ThrottleSeconds: int
    ErrorStatus: str
    Message: str
    MessageDate: t.Optional[t.Dict]
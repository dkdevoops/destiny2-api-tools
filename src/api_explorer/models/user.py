import typing as t

from .generic import BaseModel


__all__ = ('DestinyUser', 'UserNames', 'CleanUserNames')


class UserNames(BaseModel):
    steamDisplayName: t.Optional[str]
    xboxDisplayName: t.Optional[str]
    psnDisplayName: t.Optional[str]
    stadiaDisplayName: t.Optional[str]


class CleanUserNames(BaseModel):
    SteamId: t.Optional[str]
    Xuid: t.Optional[str]
    Psnid: t.Optional[str]
    Stadiaid: t.Optional[str]


class DestinyUser(BaseModel):
    userNames: t.Optional[UserNames]
    bungieName: t.Optional[str]
    membershipId: t.Optional[str]
    displayName: t.Optional[str]
    
import typing as t
from datetime import datetime

from ..generic import *


__all__ = ('RefreshTokenResponse', 'UserApiResponse', 'UserProfile',
           'BungieMembership', 'ErrorProfile', 'PlatformMembership', 
           'UserResponse', 'AuthResponse', 'ScopedResponse',
           'ScopedApiRespone')


class RefreshTokenResponse(BaseModel):
    accessToken: str
    tokenType: str
    expiresIn: int
    refreshToken: str
    refreshExpiresIn: int
    membershipId: str


class UserApiResponse(BaseModel):
    about: t.Optional[str]
    membershipId: t.Optional[str]
    uniqueName: t.Optional[str]
    displayName: t.Optional[str]
    profilePicture: t.Optional[str]
    profileTheme: t.Optional[str]
    userTitle: t.Optional[str]
    successMessageFlags: t.Optional[str]
    isDeleted: t.Optional[bool]
    firstAccess: t.Optional[datetime]
    lastUpdate: t.Optional[datetime]
    psnDisplayName: t.Optional[str]
    xboxDisplayName: t.Optional[str]
    showActivity: t.Optional[bool]
    locale: t.Optional[str]
    localeInheritDefault: t.Optional[bool]
    lastBanReportId: t.Optional[str]
    showGroupMessaging: t.Optional[bool]
    profilePicturePath: t.Optional[str]
    profileThemeName: t.Optional[str]
    userTitleDisplay: t.Optional[str]
    statusText: t.Optional[str]
    statusDate: t.Optional[str]
    steamDisplayName: t.Optional[str]
    stadiaDisplayName: t.Optional[str]
    cachedBungieGlobalDisplayName: t.Optional[str]
    cachedBungieGlobalDisplayNameCode: t.Optional[str]


class UserProfile(BaseModel):
    dateLastPlayed: t.Optional[datetime]
    isOverridden: t.Optional[bool]
    isCrossSavePrimary: t.Optional[bool]
    crossSaveOverride: t.Optional[int]
    applicableMembershipTypes: t.Optional[t.List[int]]
    isPublic: t.Optional[bool]
    membershipType: t.Optional[int]
    membershipId: t.Optional[str]
    displayName: t.Optional[str]
    bungieGlobalDisplayName: t.Optional[str]
    bungieGlobalDisplayNameCode: t.Optional[int]


class BungieMembership(BaseModel):
    supplementalDisplayName: t.Optional[str]
    iconPath: t.Optional[str]
    crossSaveOverride: t.Optional[int]
    isPublic: t.Optional[bool]
    membershipType: t.Optional[int]
    membershipId: t.Optional[str]
    displayName: t.Optional[str]
    bungieGlobalDisplayName: t.Optional[str]
    bungieGlobalDisplayNameCode: t.Optional[int]


class ErrorProfile(BaseModel):
    errorCode: int
    infoCard: UserProfile


class PlatformMembership(BaseModel):
    profiles: t.List[UserProfile]
    bnetMembership: t.Optional[BungieMembership]
    profilesWithErrors: t.Optional[t.List[ErrorProfile]]


UserResponse = t.TypeVar('UserResponse', UserApiResponse, UserProfile, BungieMembership, ErrorProfile, PlatformMembership)
AuthResponse = t.TypeVar('AuthResponse', bound=RefreshTokenResponse)
ScopedResponse: t.TypeAlias = t.Union[UserResponse, AuthResponse]


class ScopedApiRespone(AdvancedModel):
    Response: t.Optional[ScopedResponse]
    ErrorCode: int
    ThrottleSeconds: int
    ErrorStatus: str
    Message: str
    MessageDate: t.Optional[t.Dict]
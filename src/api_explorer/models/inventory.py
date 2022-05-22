import typing as t
from enum import Enum
from datetime import datetime
from pydantic import validator, root_validator

from models.generic import *


__all__ = ('D2Profile', 'CharacterType', 'Component', 'ItemPlug', 'ItemSocket', 
           'InventoryItem', 'ComponentItem', 'ItemComponents', 'D2Currency', 
           'CharacterPlugSet', 'CharacterInventory', 'CharacterEquipment', 
           'LevelProgression', 'D2Character')


class CharacterType(Enum):
    titan: 0
    hunter = 1
    warlock = 2
    unknown = 3

class Component(Enum):
    Null = 0
    Profiles = 100
    VendorReceipts = 101
    ProfileInventories = 102
    ProfileCurrencies = 103
    ProfileProgression = 104
    PlatformSilver = 105
    Characters = 200
    CharacterInventories = 201
    CharacterProgressions = 202
    CharacterRenderData = 203
    CharacterActivities = 204
    CharacterEquipment = 205
    ItemInstances = 300
    ItemObjectives = 301
    ItemPerks = 302
    ItemRenderData = 303
    ItemStats = 304
    ItemSockets = 305
    ItemTalentGrids = 306
    ItemCommonData = 307
    ItemPlugStates = 308
    ItemPlugObjectives = 309
    ItemReusablePlugs = 310
    Vendors = 400
    VendorCategories = 401
    VendorSales = 402
    Kiosks = 500
    CurrencyLookups = 600
    PresentationNodes = 700
    Collectibles = 800
    Records = 900
    Transitory = 1000
    Metrics = 1100
    StringVariables = 1200
    Craftables = 1300

class EmblemColor(BaseModel):
    alpha: int
    blue: int
    green: int
    red: int

class ItemPlug(BaseModel):
    plugId: str
    canInsert: bool
    enabled: bool
    plugItemHash: str

class ItemSocket(BaseModel):
    socketId: str
    isEnabled: bool
    isVisible: bool
    plugHash: str

class InventoryItem(BaseModel):
    bindStatus: int
    bucketHash: str
    dismantlePermission: int
    isWrapper: bool
    itemHash: str
    itemInstanceId: str
    location: int
    lockable: bool
    quantity: int
    state: int
    tooltipNotificationIndexes: t.Optional[t.List]
    transferStatus: int
    versionNumber: int

class ComponentItem(BaseModel):
    itemId: str
    quality: t.Optional[int]
    canEquip: t.Optional[bool]
    cannotEquipReason: t.Optional[int]
    damageType: t.Optional[int]
    equipRequiredLevel: t.Optional[int]
    isEquipped: t.Optional[bool]
    itemLevel: t.Optional[int]
    unlockHashesRequiredToEquip: t.Optional[t.Dict]

class ItemComponents(BaseModel):
    instances: t.List[ComponentItem]
    reusablePlugs: t.List[ItemPlug]
    sockets: t.List[ItemSocket]

class D2Currency(BaseModel):
    bindStatus: int
    bucketHash: int
    dismantlePermission: int
    isWrapper: bool
    itemHash: int
    location: int
    lockable: bool
    quantity: int
    state: int
    tooltipNotificationIndexes: t.Optional[t.List]
    transferStatus: int

class CharacterPlugSet(BaseModel):
    characterId: str
    plugSet: t.Optional[t.List[ItemPlug]]

class CharacterInventory(BaseModel):
    characterId: str
    inventory: t.Optional[t.List[InventoryItem]]

class CharacterEquipment(BaseModel):
    characterId: str
    equipment: t.Optional[t.List[InventoryItem]]

class LevelProgression(BaseModel):
    currentProgress: int
    dailyLimit: int
    dailyProgress: int
    level: int
    levelCap: int
    nextLevelAt: int
    progressToNextLevel: int
    progressionHash: int
    stepIndex: int
    weeklyLimit: int
    weeklyProgress: int

class D2Character(AdvancedModel):
    character_id: t.Optional[str]
    character_type: t.Optional[CharacterType]
    characterEquipment: t.Optional[CharacterEquipment]
    characterInventory: t.Optional[CharacterInventory]
    characterPlugSets: t.Optional[CharacterPlugSet]
    baseCharacterLevel: t.Optional[str]
    characterId: t.Optional[str]
    classHash: t.Optional[str]
    classType: t.Optional[str]
    dateLastPlayed: t.Optional[str]
    emblemBackgroundPath: t.Optional[str]
    emblemColor: t.Optional[EmblemColor]
    emblemHash: t.Optional[str]
    emblemPath: t.Optional[str]
    genderHash: t.Optional[str]
    genderType: t.Optional[str]
    levelProgression: t.Optional[LevelProgression]
    light: t.Optional[str]
    membershipId: t.Optional[str]
    membershipType: t.Optional[str]
    minutesPlayedThisSession: t.Optional[str]
    minutesPlayedTotal: t.Optional[str]
    percentToNextLevel: t.Optional[str]
    raceHash: t.Optional[str]
    raceType: t.Optional[str]
    stats: t.Optional[t.Dict]
    titleRecordHash: t.Optional[str]

    @root_validator
    def handle_character_id(cls, values):
        for k in values:
            if k.isnumeric() and len(k) >= 19:
                values['character_id'] = k
                del(values[k])
        return values

    @validator('character_type')
    def handle_character_type(cls, value):
        match value:
            case 0:
                return CharacterType.titan
            case 1:
                return CharacterType.hunter
            case 2:
                return CharacterType.warlock
            case 3:
                return CharacterType.unknown
            case _:
                return None

class D2Characters(AdvancedModel):
    data: t.Dict[str, D2Character]
    privacy: int

class UserInfo(BaseModel):
    applicableMembershipTypes: t.List[int]
    bungieGlobalDisplayName: str
    bungieGlobalDisplayNameCode: int
    crossSaveOverride: int
    displayName: str
    isPublic: bool
    membershipId: str
    membershipType: int

class ProfileData(AdvancedModel):
    characterIds: t.List[str]
    currentSeasonHash: str
    currentSeasonRewardPowerCap: int
    dateLastPlayed: datetime
    seasonHashes: t.List[int]
    userInfo: UserInfo
    versionsOwned: int

class Profile(AdvancedModel):
    data: ProfileData
    privacy: int

class D2Profile(AdvancedModel):
    characters: D2Characters
    profile: Profile
    equipment: t.Optional[t.List[CharacterEquipment]]
    inventory: t.Optional[t.List[CharacterInventory]]
    plugSet: t.Optional[t.List[CharacterPlugSet]]
    itemComponents: t.Optional[ItemComponents]
    profileCurrencies: t.Optional[D2Currency]
    profileInventory: t.Optional[t.List[InventoryItem]]
    profilePlugSets: t.Optional[t.List[ItemPlug]]
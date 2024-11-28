from enum import Enum

class Phase(Enum):
    INVOCATION = "Draw Phase"
    PREPARATION = "Preparation Phase"
    SUMMONING = "Summoning Phase"
    MISSION = "Mission Phase"
    REFLECTION = "Reflection Phase"

class Position(Enum):
    HAND = "Hand"
    SANCTUARY = "Sanctuary"
    PREACHING = "Preaching"
    MISSION = "Mission"

class CardType(Enum):
    BELIEVER = "Believer"
    RELIC = "Relic"
    MIRACLE = "Miracle"
    MISSION = "Mission"

class Faction(Enum):
    GOD = "GOD"
    CHURCH = "CHURCH"
    NEUTRAL = "NEUTRAL"

class Zone(Enum):
    SANCTUARY = "SANCTUARY"
    MISSION = "MISSION"
    HAND = "HAND"
    DECK = "DECK" 
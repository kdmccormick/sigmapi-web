# -*- coding: UTF-8 -*-


class ChoiceEnumeration(object):

    def __init__(self, code, name):
        self.code = code
        self.name = name

    @classmethod
    def get_instances(cls):
        return [
            getattr(cls, attr) for attr in dir(cls)
            if getattr(cls, attr).__class__ is cls
        ]

    @classmethod
    def get_instance(cls, code):
        for inst in cls.get_instances():
            if inst.code == code:
                return inst
        else:
            return None

    @classmethod
    def get_instance_from_name(cls, name):
        for inst in cls.get_instances():
            if inst.name == name:
                return inst
        else:
            return None

    @classmethod
    def get_choice_tuples(cls):
        return [
            (inst.code, inst.name)
            for inst in cls.get_instances()
        ]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.__class__.__name__ + '(\'' + self.code + \
            '\', \'' + self.name + '\')'

    def __unicode__(self):
        return unicode(str(self))


class GameTime(ChoiceEnumeration):
    CODE_LENGTH = 1

GameTime.DAWN = GameTime('A', 'Dawn')
GameTime.DAY = GameTime('D', 'Day')
GameTime.DUSK = GameTime('U', 'Dusk')
GameTime.NIGHT = GameTime('N', 'Night')


class Faction(object):
    VILLAGE = 'Village'
    MAFIA = 'Mafia'
    ROGUE = 'Rogue'


class PlayerNightStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

PlayerNightStatus.SAFE = PlayerNightStatus('S', 'Safe')
PlayerNightStatus.ATTACKED = PlayerNightStatus('A', 'Attacked')
PlayerNightStatus.TERMINATED = PlayerNightStatus('T', 'Terimated')


class ActionType(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, targets_can_be_self,
                 targets_dead=False, is_direct_offense=False,
                 is_lethal=False, is_covert=False):
        super(ActionType, self).__init__(code, name)
        self.targets_can_be_self = targets_can_be_self
        self.targets_dead = targets_dead
        self.is_direct_offense = is_direct_offense
        self.is_lethal = is_lethal
        self.is_covert = True

    @property
    def num_targets(self):
        return len(targets_can_be_self)

ActionType.NO_ACTION = ActionType('NA', 'No Action', [])
ActionType.CONTROL = ActionType('Co', 'Control', [False, True])
ActionType.ON_GUARD = ActionType('OG', 'On Guard', [], is_lethal=True)
ActionType.SEDUCE = ActionType('Se', 'Seduce', [False])
ActionType.SWITCH = ActionType('Sw', 'Switch', [True, True])
ActionType.FRAME = ActionType('Fr', 'Frame', [True])
ActionType.INVESTIGATE = ActionType('In', 'Investigate', [False])
ActionType.INSANE_INVESTIGATE = ActionType('II', 'Investigate', [False])
ActionType.FORGETFUL_INVESTIGATE = ActionType('FI', 'Forgetful Investigate', [True])
ActionType.SCRUTINIZE = ActionType('Sc', 'Scrutinize', [True])
ActionType.PROTECT = ActionType('Pr', 'Protect', [False])
ActionType.DEFEND = ActionType('De', 'Defend', [False], is_lethal=True)
ActionType.BULLETPROOF_VEST = ActionType('BV', 'Bulletproof Vest', [])
ActionType.CORRUPT = ActionType('Co', 'Corrupt', [False], is_direct_offense=True)
ActionType.SLAY = ActionType('Sl', 'Slay', [True], is_direct_offense=True, is_lethal=True)
ActionType.AMBUSH = ActionType('Am', 'Ambush', [True], is_lethal=True)
ActionType.SNIPE = ActionType('Sn', 'Snipe', [True], is_lethal=True, is_covert=True)
ActionType.IGNITE = ActionType('Ig', 'Ignite', [], is_lethal=True)
ActionType.SABOTAGE = ActionType('Sa', 'Sabotage', [True], is_lethal=True)
ActionType.DOUSE = ActionType('Do', 'Douse', [True])
ActionType.UN_DOUSE = ActionType('UD', 'Un-Douse', [True])
ActionType.DISPOSE = ActionType('Di', 'Dispose', [True])
ActionType.REVEAL = ActionType('Re', 'Reveal', [])
ActionType.FOLLOW = ActionType('Fo', 'Follow', [True])
ActionType.WATCH = ActionType('Wa', 'Watch', [True])
ActionType.REMEMBER = ActionType('Re', 'Remember', [False], targets_dead=True)


class ApparentGuilt(ChoiceEnumeration):
    FACTION_BASED = 0
    INNOCENT = 1
    GUILTY = 2


class Role(ChoiceEnumeration):

    CODE_LENGTH = 2

    def __init__(self, code, name, faction, action_types_and_uses, apparent_name=None,
                 night_immune=False, immune_to_seduction=False,
                 hidden_to_mafia=False, apparent_guilt=ApparentGuilt.FACTION_BASED,
                 min_in_game=0, max_in_game=float('inf')):
        super(Role, self).__init__(code, name)

        self.faction = faction
        self.action_types_and_uses = action_types_and_uses
        self.apparent_name = apparent_name or name
        self.night_immune = night_immune
        self.immune_to_seduction = immune_to_seduction

        if self.faction != Faction.MAFIA and hidden_to_mafia:
            raise ValueError('Role: faction!=mafia but hidden_to_mafia==True')
        self.hidden_to_mafia = hidden_to_mafia

        self.apparent_guilt = apparent_guilt

        if min_in_game > max_in_game:
            raise ValueError('Role: min_in_game > max_in_game')
        self.min_in_game = min_in_game
        self.max_in_game = max_in_game

UNLIMITED_USES = -1
EVERY_OTHER_NIGHT = -2

Role.MAYOR = Role(
    'VM', 'Mayor', Faction.VILLAGE,
    [(ActionType.REVEAL, 1)],
    min_in_game=1, max_in_game=1
)
Role.COP = Role(
    'VC', 'Cop', Faction.VILLAGE,
    [(ActionType.INVESTIGATE, UNLIMITED_USES)],
)
Role.INSANE_COP = Role(
    'VI', 'Insane Cop', Faction.VILLAGE,
    [(ActionType.INSANE_INVESTIGATE, UNLIMITED_USES)],
    apparent_name='Cop'
)
Role.FORGETFUL_COP = Role(
    'VF',  'Forgetful Cop',  Faction.VILLAGE,
    [(ActionType.FORGETFUL_INVESTIGATE, UNLIMITED_USES)],
)
Role.DOCTOR = Role(
    'VD', 'Doctor', Faction.VILLAGE,
    [(ActionType.PROTECT, UNLIMITED_USES)],
)
Role.BUS_DRIVER = Role(
    'VB', 'Bus Driver', Faction.VILLAGE,
    [(ActionType.SWITCH, UNLIMITED_USES)],
    max_in_game=1,
)
Role.TRACKER = Role(
    'VT',  'Tracker', Faction.VILLAGE,
    [(ActionType.FOLLOW, UNLIMITED_USES)],
)
Role.WATCHER = Role(
    'VW',  'Watcher', Faction.VILLAGE,
    [(ActionType.WATCH, UNLIMITED_USES)],
)
Role.ESCORT = Role(
    'VE',  'Escort', Faction.VILLAGE,
    [(ActionType.SEDUCE, UNLIMITED_USES)],
    immune_to_seduction=True,
)
Role.VIGILANTE = Role(
    'Vi',  'Vigilante', Faction.VILLAGE,
    [(ActionType.SEDUCE, UNLIMITED_USES)],
)
Role.VETERAN = Role(
    'VV',  'Veteran', Faction.VILLAGE,
    [(ActionType.ON_GUARD, 3)],
)
Role.MILLER = Role(
    'Vl',  'Miller', Faction.VILLAGE,
    [],
    apparent_guilt=ApparentGuilt.GUILTY,
)
Role.BOMB = Role(
    'Vo',  'Bomb', Faction.VILLAGE,
    [],
    immune_to_seduction=True,
    max_in_game=1,
)
Role.BODYGUARD = Role(
    'Vg',  'Bodyguard', Faction.VILLAGE,
    [(ActionType.DEFEND, UNLIMITED_USES)],
)
Role.DETECTIVE = Role(
    'Ve',  'Detective', Faction.VILLAGE,
    [(ActionType.SCRUTINIZE, UNLIMITED_USES)],
)
Role.BASIC_VILLAGER = Role(
    'Va', 'Basic Villager', Faction.VILLAGE,
    []
)
Role.GODFATHER = Role(
    'MG', 'Godfather', Faction.MAFIA,
    [(ActionType.SLAY, UNLIMITED_USES)],
    apparent_guilt=ApparentGuilt.INNOCENT,
    min_in_game=1, max_in_game=1,
)
Role.LIMO_DRIVER = Role(
    'ML', 'Limo Driver', Faction.MAFIA,
    [(ActionType.SWITCH, UNLIMITED_USES)],
    max_in_game=1,
)
Role.STALKER = Role(
    'MS', 'Stalker', Faction.MAFIA,
    [(ActionType.FOLLOW, UNLIMITED_USES)],
)
Role.LOOKOUT = Role(
    'Mk', 'Lookout', Faction.MAFIA,
    [(ActionType.WATCH, UNLIMITED_USES)],
)
Role.HOOKER = Role(
    'MH',  'Hooker', Faction.MAFIA,
    [(ActionType.SEDUCE, UNLIMITED_USES)],
    immune_to_seduction=True,
)
Role.JANITOR = Role(
    'MJ', 'Janitor', Faction.MAFIA,
    [(ActionType.DISPOSE, UNLIMITED_USES)],
)
Role.FRAMER = Role(
    'MF', 'Framer', Faction.MAFIA,
    [(ActionType.FRAME, UNLIMITED_USES)],
)
Role.YAKUZA = Role(
    'MY', 'Yakuza', Faction.MAFIA,
    [(ActionType.CORRUPT, UNLIMITED_USES)],
)
Role.SABOTEUR = Role(
    'Mt', 'Saboteur', Faction.MAFIA,
    [(ActionType.SABOTAGE, UNLIMITED_USES)],
    hidden_to_mafia=True,
)
Role.SNIPER = Role(
    'Mi', 'Sniper', Faction.MAFIA,
    [(ActionType.SNIPE, 1)],
    hidden_to_mafia=True,
)
Role.BASIC_MAFIA = Role(
    'Ma', 'Basic ', Faction.MAFIA,
    [],
    max_in_game=0, # can only be included by corruption
)
Role.JESTER = Role(
    'RJ', 'Jester', Faction.ROGUE,
    [],
)
Role.SERIAL_KILLER = Role(
    'RK', 'Serial Killer', Faction.ROGUE,
    [(ActionType.SLAY, UNLIMITED_USES)],
    night_immune=True,
)
Role.MASS_MURDERER = Role(
    'RM', 'Mass Murderer', Faction.ROGUE,
    [(ActionType.AMBUSH, EVERY_OTHER_NIGHT)],
)
Role.ARSONIST = Role(
    'RA', 'Arsonist', Faction.ROGUE,
    [
        (ActionType.DOUSE, UNLIMITED_USES),
        (ActionType.UN_DOUSE, UNLIMITED_USES),
        (ActionType.IGNITE, UNLIMITED_USES)
    ],
    night_immune=True,
)
Role.WITCH = Role(
    'RW', 'Witch', Faction.ROGUE,
    [(ActionType.CONTROL, UNLIMITED_USES)],
    immune_to_seduction=True,
)
Role.AMNESIAC = Role(
    'RE', 'Amnesiac', Faction.ROGUE,
    [(ActionType.REMEMBER, 1)],
)
Role.SURVIVOR = Role(
    'RS', 'Survivor', Faction.ROGUE,
    [(ActionType.BULLETPROOF_VEST, 3)],
)
Role.EXECUTIONER = Role(
    'RX', 'Executioner', Faction.ROGUE,
    [],
)


class PlayerStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

PlayerStatus.ALIVE = PlayerStatus('A', 'Alive')
PlayerStatus.LYNCHED = PlayerStatus('L', 'Lynched')
PlayerStatus.DIED_AT_NIGHT = PlayerStatus('K', 'Died at Night')


class VoteType(ChoiceEnumeration):
    CODE_LENGTH = 1

VoteType.ABSTAIN = VoteType('A', 'Abstain')
VoteType.NO_LYNCH = VoteType('N', 'No Lynch')
VoteType.LYNCH = VoteType('L', 'Lynch')
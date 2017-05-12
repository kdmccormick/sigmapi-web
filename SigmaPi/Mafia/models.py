
from django.db import models
from django.contrib.auth.models import User
from collections import defaultdict
import json

from enums import *

MAFIA_GAME_NAME_MAX_LENGTH = 50

class MafiaGame(models.Model):
    name = models.CharField(
        max_length=MAFIA_GAME_NAME_MAX_LENGTH,
        default='Unnamed Mafia Game'
    )
    created = models.DateField()
    creator = models.ForeignKey(User)
    day_number = models.PositiveSmallIntegerField(default=0)
    time = models.CharField(
        max_length=MafiaGameTime.CODE_LENGTH,
        choices=MafiaGameTime.get_choice_tuples(),
        default=MafiaGameTime.DUSK.code
    )
    is_finished = models.BooleanField(default=False)

    @property
    def is_accepting(self):
        return self.day_number == 0

    @property
    def status_string(self):
        if self.is_finished:
            return 'Complete'
        elif self.is_accepting:
            return 'Accepting Players'
        else:
            time_name = MafiaGameTime.get_instance(self.time).name
            return time_name + ' ' + `self.day_number`
        
class MafiaPlayer(models.Model):
    game = models.ForeignKey(MafiaGame)
    user = models.ForeignKey(User)
    role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        null=True, blank=True,
    )
    old_role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        null=True, blank=True,
    )
    older_role = models.CharField(
        max_length=MafiaRole.CODE_LENGTH,
        choices=MafiaRole.get_choice_tuples(),
        null=True, blank=True,
    )
    status = models.CharField(
        max_length=MafiaPlayerStatus.CODE_LENGTH,
        choices=MafiaPlayerStatus.get_choice_tuples(),
        default=MafiaPlayerStatus.ALIVE.code
    )
    actions_used_json = models.TextField(default='{}')
    doused = models.BooleanField(default=False)
    executioner_target = models.ForeignKey(User, null=True, related_name='executioner_target')

    def get_actions_used(self):
        return defaultdict(
            (lambda: (0, False)),
            json.loads(self.actions_used_json)
        )

    def mark_action_used(self, action_type_code):
        used = self.get_actions_used()
        used[action_type_code] = (used[action_type_code][0] + 1, True)
        self.actions_used_json = json.dumps(used)

    def mark_night_passed(self):
        used = self.get_actions_used()
        json.dumps({at: (use[0], False) for at, use in used.iteritems()})

    @property
    def revealed_as_mayor(self):
        return self.get_actions_used()[MafiaActionType.REVEAL.code][0] >= 1

class MafiaNightResult(models.Model):
    game = models.ForeignKey(MafiaGame)
    night_number = models.PositiveSmallIntegerField()
    description = models.TextField(default='')

class MafiaAction(models.Model):
    performer = models.ForeignKey(MafiaPlayer)
    night_number = models.PositiveSmallIntegerField()
    action_type = models.CharField(
        max_length=MafiaActionType.CODE_LENGTH,
        choices=MafiaActionType.get_choice_tuples(),
        default=MafiaActionType.NO_ACTION.code
    )
    target0 = models.ForeignKey(User, related_name='target0', null=True)
    target1 = models.ForeignKey(User, related_name='target1', null=True)

class MafiaPlayerNightStatus(ChoiceEnumeration):
    CODE_LENGTH = 1

MafiaPlayerNightStatus.SAFE = MafiaPlayerNightStatus('S', 'Safe')
MafiaPlayerNightStatus.ATTACKED = MafiaPlayerNightStatus('A', 'Attacked')
MafiaPlayerNightStatus.TERMINATED = MafiaPlayerNightStatus('T', 'Terimated')

class MafiaPlayerNightResult(models.Model):
    action = models.OneToOneField(MafiaAction)

    controlled_to_target = models.ForeignKey(User, null=True, related_name='controlled_to_target')
    switched_by_json = models.TextField(default='[]')
    switched_with = models.ForeignKey(User, null=True, related_name='switched_with')
    attempted_seduced = models.BooleanField(default=False)
    framed = models.BooleanField(default=False)
    protected_by_json = models.TextField(default='[]')
    defended_by_json = models.TextField(default='[]')
    attempted_corrupted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=MafiaPlayerNightStatus.CODE_LENGTH,
        choices=MafiaPlayerNightStatus.get_choice_tuples(),
        default=MafiaPlayerNightStatus.SAFE.code
    )
    doused = models.BooleanField(default=False)
    un_doused = models.BooleanField(default=False)
    disposed = models.BooleanField(default=False)
    remembered = models.ForeignKey(User, null=True, related_name='remembered')
    action_effective = models.BooleanField(default=False)
    other_targeted_by_json = models.TextField(default='[]')
    report = models.TextField(default='')

    @property
    def player(self):
        return self.action.performer

    @property
    def action_type(self):
        return self.action.action_type

    @property
    def target0(self):
        return self.action.target0

    @property
    def target1(self):
        return self.action.target1

    @property
    def target0_after_control(self):
        return self.controlled_to_target or self.target0

    @property
    def target1_after_control(self):
        return self.target1

    @property
    def apparent_target0(self):
        return None if self.seduced else self.target0_after_control

    @property
    def apparent_target1(self):
        return None if self.seduced else self.target1_after_control

    @property
    def _resisted(self):
        return self.protected or self.defended or self.bulletproof or self.on_guard or (
            MafiaRole.get_instance(self.player.role).night_immune
        )

    @property
    def died(self):
        return (
            self.status == MafiaPlayerNightStatus.TERMINATED or (
                self.status == MafiaPlayerNightStatus.ATTACKED.code and
                not self._resisted
            )
        )

    @property
    def protected(self):
        return len(json.loads(self.protected_by_json)) >= 1

    @property
    def seduced(self):
        return (
            self.attempted_seduced and
            not MafiaRole.get_instance(self.player.role).immune_to_seduction
        )

    @property
    def seduced_or_died(self):
        return self.seduced or self.died

    @property
    def corrupted(self):
        return self.attempted_corrupted and not self._resisted

    @property
    def on_guard(self):
        return self.action_type == MafiaActionType.ON_GUARD.code

    @property
    def bulletproof(self):
        return self.action_type == MafiaActionType.BULLETPROOF_VEST.code

    @property
    def switched_with_or_self(self):
        return self.switched_with or self.player.user

    def add_switched_by(self):
        self.switched_by_json = json.dumps(list(set(
            json.loads(self.switched_by_json) + [user.username]
        )))

    def clear_switched_by(self):
        self.switched_by_json = '[]'
        self.switched_with = None

    def get_switched_by(self):
        return [
            User.get(username=username)
            for username in json.loads(self.switched_by_json)
        ]

    @property
    def times_switched(self):
        return len(json.loads(self.switched_by_json))

    def add_protected_by(self, user):
        self.protected_by_json = json.dumps(list(set(
            json.loads(self.protected_by_json) + [user.username]
        )))

    def get_protected_by(self):
        return [
            User.get(username=username)
            for username in json.loads(self.protected_by_json)
        ]

    def add_defended_by(self, user):
        self.defended_by_json = json.dumps(list(set(
            json.loads(self.defended_by_json) + [user.username]
        )))

    def get_defended_by(self, user):
        return [
            User.get(username=username)
            for username in json.loads(self.defended_by_json)
        ]

    def add_targeted_by(self, user):
        self.other_targeted_by_json = json.dumps(list(set(
            json.loads(self.other_targeted_by_json) + [user.username]
        )))

    def get_targeted_by(self):
        return [
            User.get(username=username)
            for username in (
                json.loads(self.switched_by_json) +
                json.loads(self.protected_by_json) +
                json.loads(self.defended_by_json) +
                json.loads(self.other_targeted_by_json)
            )
        ]

    def add_report_line(self, line):
        if self.report:
            self.report += '\n'
        self.report += line

    def contains_report_line(self, line):
        return line in self.report.splitlines()

class MafiaVote(models.Model):
    voter = models.ForeignKey(MafiaPlayer)
    day_number = models.PositiveSmallIntegerField()
    vote_type = models.CharField(
        max_length=MafiaVoteType.CODE_LENGTH,
        choices=MafiaVoteType.get_choice_tuples(),
        default=MafiaVoteType.ABSTAIN.code
    )
    vote = models.ForeignKey(User, null=True)
    comment = models.TextField(default='')

class MafiaDayResult(models.Model):
    game = models.ForeignKey(MafiaGame)
    day_number = models.PositiveSmallIntegerField()
    lynched = models.ForeignKey(User, null=True)
    description = models.TextField(default="")

class MafiaError(Exception):
    pass

class MafiaUserError(Exception):
    pass

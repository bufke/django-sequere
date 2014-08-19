from .models import Project

from ..compat import User
from ..base import ModelBase

from sequere.contrib.timeline import Action
from sequere import register


class ProjectSequere(ModelBase):
    identifier = 'projet'


class JoinAction(Action):
    verb = 'join'


class UserSequere(ModelBase):
    identifier = 'user'

    actions = [JoinAction, ]


register(User, UserSequere)
register(Project, ProjectSequere)

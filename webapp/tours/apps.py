from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _



class ToursConfig(AppConfig):
    name = 'tours'

    def ready(self):
        import tours.signals

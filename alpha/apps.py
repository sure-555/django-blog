from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AlphaConfig(AppConfig):
    name = 'alpha'
    def ready(self):
        from alpha.signals import create_groups_permessions
        post_migrate.connect(create_groups_permessions)


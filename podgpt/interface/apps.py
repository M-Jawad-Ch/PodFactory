from django.apps import AppConfig


class InterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interface'

    def ready(self) -> None:
        try:
            from .models import SeriesGenerator
            generators = SeriesGenerator.objects.filter(running=True).all()

            for generator in generators:
                generator.running = False
                generator.used = False
                generator.save()

        except:
            pass
        return super().ready()

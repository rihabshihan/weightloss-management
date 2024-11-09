from django.apps import AppConfig  # Import the AppConfig class to define the app configuration


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Set the default auto field type for this app
    name = 'home'  # The name of the app, which is typically the folder name

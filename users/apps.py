from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'  # sets the name of the app config as 'users'

    def ready(self):
    	import users.signals  # imports the signals module from the users app

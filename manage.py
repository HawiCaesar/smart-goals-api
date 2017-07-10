import os
from flask_script import Manager  # handles a set of commands
from flask_migrate import Migrate, MigrateCommand
from bucketlist import database, create_application
from bucketlist import models

app = create_application(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, database)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

import os

from bucketlist import create_application

config_name = os.getenv('APP_SETTINGS')  # config_name = "development"
app = create_application(config_name)

if __name__ == '__main__':
    app.run()

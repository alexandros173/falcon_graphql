import os

from dotenv import load_dotenv

load_dotenv('config/.env.dev')


class Config:
    def __init__(self):
        try:
            default_env = os.getenv('ENV', '')

            if default_env != '':
                load_dotenv('config/.env.' + default_env)

            self.APP_NAME = 'ms-graphql-test'
            self.ENV = 'dev'
            self.HOST = os.getenv('HOST', '0.0.0.0')
            self.PORT = int(os.getenv('PORT', 8080))

            self.POSTGRES: dict = {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': int(os.getenv('POSTGRES_PORT', 5432)),
                'user': os.getenv('POSTGRES_USER', 'postgres'),
                'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
                'db': os.getenv('POSTGRES_DB', 'postgres'),
            }

        except OSError as e:
            print(f'Unable to load variable environments: {e.strerror}')

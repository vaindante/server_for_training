import environ


@environ.config(prefix='APP')
class Config:
    db_user = environ.var('postgres')
    db_password = environ.var('book12345')
    db_name = environ.var('library')
    db_host = environ.var('localhost')
    db_port = environ.var(5432)
    database_url = environ.var('', name='DATABASE_URL')

    @property
    def db_url(self):
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


config: Config = environ.to_config(Config)

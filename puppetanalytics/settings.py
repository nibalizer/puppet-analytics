class Settings(object):
    DEBUG = False
    sqlite_db = 'sqlite:////tmp/puppetanalytics.sqlite'


class ProductionSettings(Settings):
    DEBUG = False


class DevelopmentSettings(Settings):
    DEBUG = True

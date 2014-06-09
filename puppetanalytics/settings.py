class Settings(object):
    DEBUG = False


class DevelopmentSettings(Settings):
    DEBUG = True


class ProductionSettings(Settings):
    DEBUG = False


class TestingSettings(Settings):
    DEBUG = False

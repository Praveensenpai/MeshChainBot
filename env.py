from pyenvloadermeta import EnvLoaderMeta


class Env(metaclass=EnvLoaderMeta):
    REF_ID: str
    SESSION_NAME: str
    API_ID: int
    API_HASH: str
    PHONE: str
    SLEEP_DELAY_MINUTES: int

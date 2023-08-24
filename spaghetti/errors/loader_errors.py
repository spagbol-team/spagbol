class InvalidSourceError(Exception):
    def __init__(self, cause: str):
        self.cause = cause

    def __str__(self):
        return "Data loader source is invalid. Reason: %s" % self.cause

class UsageError(Exception):
    """The user has used zcloud incorrectly."""
    pass


class ParamError(Exception):
    """The input parameters specified does not work or is invalid for zcloud to run with."""
    pass


class CloudError(Exception):
    """Cloud related errors raised during cloud service calls."""
    pass

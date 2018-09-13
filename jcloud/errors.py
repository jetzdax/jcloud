class UsageError(Exception):
    """ User error when they tried to use jcloud """
    pass


class ParamError(Exception):
    """ Input parameters passed to jcloud is either invalid or not compatible """
    pass


class TemplateError(Exception):
    """ Template used contains error """
    pass


class ClientError(Exception):
    """ Client side error when calling a cloud service """
    pass


class CloudError(Exception):
    """ Error when calling a cloud service """
    pass

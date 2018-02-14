# ------------------------------------------------------------------------
#
# Module: invalid_env_err.py
# Created By: coreym
# Created On: 2018/Feb/10
#
# Description: Thrown when an invalid environment string is passed as
#              argument.
#
# ------------------------------------------------------------------------

class InvalidEnvException(Exception):
    def __init__(self, message, errors=None):
        super(InvalidEnvException, self).__init__(message)
        self.errors = errors
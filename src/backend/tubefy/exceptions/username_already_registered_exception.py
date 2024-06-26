from .app_base_exception import AppBaseException


class UsernameAlreadyRegisteredException(AppBaseException):

    def __init__(self, username: str) -> None:

        super().__init__(status_code=409, message=f'Username \'{username}\' already registered')

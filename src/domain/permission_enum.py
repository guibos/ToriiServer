import enum


@enum.unique
class Permission(enum.Enum):
    USER_GET = 'user_get'
    USER_ADD = 'user_add'
    USER_DEL = 'user_del'
    USER_MOD = 'user_mode'

    LIBRARY_GET = 'library_get'
    LIBRARY_ADD = 'library_add'
    LIBRARY_DEL = 'library_del'
    LIBRARY_MOD = 'library_mod'
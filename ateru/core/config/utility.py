import getpass


def user_name() -> str:
    user = getpass.getuser()
    return user

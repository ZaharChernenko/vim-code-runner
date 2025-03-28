import functools

import vim


def save_file_if(enable: str):
    """Saves the current file before executing the function if enable is '1'"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            vim.command("w")
            return func(*args, **kwargs)

        return wrapper if enable == "1" else func

    return decorator


def save_all_files_if(enable: str):
    """Saves all files before executing the function if enable is '1'"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            vim.command("wall")
            return func(*args, **kwargs)

        return wrapper if enable == "1" else func

    return decorator

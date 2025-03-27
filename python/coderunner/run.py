import vim

from . import runners


def run(filetype: str, filepath: str):
    if filetype == "python":
        vim.command(runners.TPythonRunner.run(filepath))
    elif filetype == "cpp":
        vim.command(runners.TCppRunner.run(filepath))

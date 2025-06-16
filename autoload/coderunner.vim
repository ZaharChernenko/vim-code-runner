" This is basic vim plugin boilerplate
let s:save_cpo = &cpo
set cpo&vim

let s:script_folder_path = escape(expand('<sfile>:p:h'), '\')


function coderunner#Load() abort
python3 << EOF
import os
import sys
import traceback
import typing

import vim


def safe_coderunner_access(func):
    def wrapper(*args, **kwargs):
        if "coderunner" in globals() and coderunner is not None:
            return func(*args, **kwargs)
        vim.command("redraw | echohl WarningMsg")
        vim.command("echom 'CodeRunner unavailable, please look at messages.'")
        vim.command("echohl None")
    return wrapper


@safe_coderunner_access
def coderunner_run():
    coderunner.run()


@safe_coderunner_access
def coderunner_run_by_glob():
    coderunner.run_by_glob()


@safe_coderunner_access
def coderunner_run_by_file_ext():
    coderunner.run_by_file_ext()


@safe_coderunner_access
def coderunner_run_by_file_type():
    coderunner.run_by_file_type()


@safe_coderunner_access
def coderunner_remove_coderunner_tempfiles():
    coderunner.remove_coderunner_tempfiles()


@safe_coderunner_access
def coderunner_on_exit():
    coderunner.on_exit()


root_folder_path: str = os.path.dirname(vim.eval("s:script_folder_path"))
sys.path[0:0] = [os.path.join(root_folder_path, "python_coderunner")]
try:
    from src.coderunner import TCodeRunner
    from src.coderunner_builder import TVimCodeRunnerBuilder
    coderunner: TCodeRunner = TVimCodeRunnerBuilder().build()
except Exception as error:
    vim.command("redraw | echohl ErrorMsg")
    for line in traceback.format_exc().splitlines():
        vim.command("echom '{0}'".format(line.replace("'", "''")))
    vim.command("echom 'CodeRunner unavailable: {0}'".format(str(error).replace("'", "''")))
    vim.command("echohl None")
    vim.command("return 0")
else:
    vim.command("return 1")
EOF
endfunction


function coderunner#Run() abort
python3 << EOF
coderunner_run()
EOF
endfunction


function coderunner#RunByGlob() abort
python3 << EOF
coderunner_run_by_glob()
EOF
endfunction


function coderunner#RunByFileExt() abort
python3 << EOF
coderunner_run_by_file_ext()
EOF
endfunction


function coderunner#RunByFileType() abort
python3 << EOF
coderunner_run_by_file_type()
EOF
endfunction


function coderunner#RemoveCoderunnerTempfiles() abort
python3 << EOF
coderunner_remove_coderunner_tempfiles()
EOF
endfunction


function coderunner#OnExit() abort
python3 << EOF
coderunner_on_exit()
EOF
endfunction


function coderunner#GetSelectedText()
    if mode() !~# '[vV]'
        return v:null
    end

    execute "normal! \<Esc>"

    let [line_start, column_start] = getpos("'<")[1:2]
    let [line_end, column_end] = getpos("'>")[1:2]
    let lines = getline(line_start, line_end)

    if len(lines) == 0
        return ''
    endif

    let lines[-1] = lines[-1][: column_end - (&selection == 'inclusive' ? 1 : 2)]
    let lines[0] = lines[0][column_start - 1:]

    return join(lines, "\n")
endfunction


" This is basic vim plugin boilerplate
let &cpo = s:save_cpo
unlet s:save_cpo

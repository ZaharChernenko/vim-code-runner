" This is basic vim plugin boilerplate
let s:save_cpo = &cpo
set cpo&vim

command! -range CodeRunnerRun call coderunner#Run(visualmode(), <range>, <line1>, <line2>)
command! -range CodeRunnerRunByFileExt call coderunner#RunByFileExt(visualmode(), <range>, <line1>, <line2>)
command! -range CodeRunnerRunByFileType call coderunner#RunByFileType(visualmode(), <range>, <line1>, <line2>)
command! -range CodeRunnerRunByGlob call coderunner#RunByGlob(visualmode(), <range>, <line1>, <line2>)


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
def coderunner_run_by_file_ext():
    coderunner.run_by_file_ext()


@safe_coderunner_access
def coderunner_run_by_file_type():
    coderunner.run_by_file_type()


@safe_coderunner_access
def coderunner_run_by_glob():
    coderunner.run_by_glob()


@safe_coderunner_access
def coderunner_remove_coderunner_tempfiles():
    coderunner.remove_coderunner_tempfiles()


@safe_coderunner_access
def coderunner_on_exit():
    coderunner.on_exit()


sys.path.insert(0, os.path.dirname(vim.eval("s:script_folder_path")))
try:
    import python_coderunner
    coderunner: python_coderunner.coderunner.TCodeRunner = python_coderunner.coderunner_builder.TVimCodeRunnerBuilder().build()
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


function coderunner#Run(visualmode, range, first_line, last_line) range abort
python3 << EOF
coderunner_run()
EOF
endfunction


function coderunner#RunByFileExt(visualmode, range, first_line, last_line) range abort
python3 << EOF
coderunner_run_by_file_ext()
EOF
endfunction


function coderunner#RunByFileType(visualmode, range, first_line, last_line) range abort
python3 << EOF
coderunner_run_by_file_type()
EOF
endfunction


function coderunner#RunByGlob(visualmode, range, first_line, last_line) range abort
python3 << EOF
coderunner_run_by_glob()
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


function! coderunner#GetSelectedText(visualmode, range, first_line, last_line) abort
    " a slightly modified version from https://github.com/voldikss/vim-floaterm
    if a:range == 0
        return v:null
    elseif a:range == 1
        let lines = [getline(a:first_line)]
    else
        let [selected_line_1, selected_col_1] = getpos("'<")[1:2]
        let [selected_line_2, selected_col_2] = getpos("'>")[1:2]
        if selected_line_1 == 0 || selected_col_1 == 0 || selected_line_2 == 0 || selected_col_2 == 0
            \ || a:first_line != selected_line_1 || a:last_line != selected_line_2
            let lines = getline(a:first_line, a:last_line)
        else
            let lines = getline(selected_line_1, selected_line_2)
            if !empty(lines)
                if a:visualmode ==# 'v'
                    let lines[-1] = lines[-1][: selected_col_2 - (&selection == 'inclusive' ? 1 : 2)]
                    let lines[0] = lines[0][selected_col_1 - 1:]
                elseif a:visualmode ==# 'V'
                elseif a:visualmode == "\<c-v>"
                    let i = 0
                    for line in lines
                        let lines[i] = line[selected_col_1 - 1: selected_col_2 - (&selection == 'inclusive' ? 1 : 2)]
                        let i = i + 1
                    endfor
                endif
            endif
        endif
    endif
    return join(lines, "\n")
endfunction


" This is basic vim plugin boilerplate
let &cpo = s:save_cpo
unlet s:save_cpo

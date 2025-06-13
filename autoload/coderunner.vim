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

root_folder_path: str = os.path.dirname(vim.eval("s:script_folder_path"))
sys.path.insert(0, os.path.join(root_folder_path, "python_coderunner"))
try:
    from src.coderunner import TCodeRunner
    from src.coderunner_builder import TVimCodeRunnerBuilder
    coderunner: TCodeRunner = TVimCodeRunnerBuilder().build()
except Exception as error:
    vim.command("redraw | echohl WarningMsg")
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
coderunner.run()
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

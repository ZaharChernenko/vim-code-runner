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
sys.path.insert(0, os.path.join(root_folder_path, "python"))
try:
    from coderunner import decorators, metaclasses, runners

    class TRunnerContext(metaclass=metaclasses.ContextMeta):
        LANG_TO_RUNNER: typing.Final[typing.Dict[str, typing.Type[runners.IRunner]]] = {
            "python": runners.TPythonRunner,
            "cpp": runners.TCppRunner,
        }

        @classmethod
        @decorators.save_file_if(vim.eval("g:coderunner_save_file_before_run"))
        @decorators.save_all_files_if(vim.eval("g:coderunner_save_all_files_before_run"))
        def run(cls, filetype: str, filepath: str):
            runner: typing.Optional[typing.Type[runners.IRunner]] = cls.LANG_TO_RUNNER.get(filetype)
            if runner is None:
                return
            vim.command(cls.LANG_TO_RUNNER[filetype].run(filepath))

        @classmethod
        def clear(cls):
            runners.TPythonRunner.clear()

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
TRunnerContext.run(vim.eval("&filetype"), vim.eval("expand('%:p')"))
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

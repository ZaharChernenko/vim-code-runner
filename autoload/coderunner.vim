" This is basic vim plugin boilerplate
let s:save_cpo = &cpo
set cpo&vim

let s:script_folder_path = escape(expand('<sfile>:p:h'), '\')


function coderunner#Load() abort
python3 << EOF
import os
import sys
import traceback

import vim

root_folder_path: str = os.path.dirname(vim.eval("s:script_folder_path"))
sys.path.insert(0, os.path.join(root_folder_path, "python"))
try:
    from coderunner import decorators, TRunnerContext

    TRunnerContext.clear()

    @decorators.save_file_if(vim.eval("g:coderunner_save_file_before_run"))
    @decorators.save_all_files_if(vim.eval("g:coderunner_save_all_files_before_run"))
    def run(filetype: str, filepath: str):
        TRunnerContext.run(filetype, filepath)

except Exception as error:
    vim.command("redraw | echohl WarningMsg")
    for line in traceback.format_exc().splitlines():
        vim.command(f"echom '{line.replace("'", "''")}'")
    vim.command(f"echo 'Code Runner unavailable: {str(error).replace("'", "''")}'")
    vim.command("echohl None")
    vim.command("return 0")
else:
    vim.command("return 1")
EOF
endfunction


function coderunner#Run() abort
python3 << EOF
run(vim.eval("&filetype"), vim.eval("expand('%:p')"))
EOF
endfunction


" This is basic vim plugin boilerplate
let &cpo = s:save_cpo
unlet s:save_cpo

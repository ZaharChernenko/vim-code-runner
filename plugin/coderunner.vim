" This is basic vim plugin boilerplate
function! s:restore_cpo()
  let &cpo = s:save_cpo
  unlet s:save_cpo
endfunction

let s:save_cpo = &cpo
set cpo&vim

if exists('g:loaded_coderunner')
    call s:restore_cpo()
    finish
elseif !has('python3')
    echohl ErrorMsg
    echo 'Coderunner unavailable: unable to load python3.'
    echohl None
    call s:restore_cpo()
    finish
endif

let g:loaded_coderunner = 1
let g:coderunner_save_file_before_run = get(g:, 'coderunner_save_file_before_run', 0)
let g:coderunner_save_all_files_before_run = get(g:, 'coderunner_save_all_files_before_run', 0)

if has('vim_starting')
    augroup coderunnerStart
        autocmd!
        autocmd VimEnter * call coderunner#Load()
    augroup END
else
    call coderunner#Load()
endif

call s:restore_cpo()

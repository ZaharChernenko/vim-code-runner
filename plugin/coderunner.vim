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
    echom 'Coderunner unavailable: unable to load python3.'
    echohl None
    call s:restore_cpo()
    finish
endif

let g:loaded_coderunner = 1
let g:coderunner_by_file_ext = get(g:, 'coderunner_by_file_ext', {})
let g:coderunner_by_file_type = get(g:, 'coderunner_by_file_type', {})
let g:coderunner_by_glob = get(g:, 'coderunner_by_glob', {})
let g:coderunner_executor = get(g:, 'coderunner_executor', 'ter')
let g:coderunner_ignore_selection = get(g:, 'coderunner_ignore_selection', 0)
let g:coderunner_remove_coderunner_tempfiles_on_exit = get(g:, 'coderunner_remove_coderunner_tempfiles_on_exit', 0)
let g:coderunner_respect_shebang = get(g:, 'coderunner_respect_shebang', 1)
let g:coderunner_runners_order = get(g:, 'coderunner_runners_order', ['by_glob', 'by_file_ext', 'by_file_type'])
let g:coderunner_save_all_files_before_run = get(g:, 'coderunner_save_all_files_before_run', 0)
let g:coderunner_save_file_before_run = get(g:, 'coderunner_save_file_before_run', 0)
let g:coderunner_tempfile_prefix = get(g:, 'coderunner_tempfile_prefix', 'coderunner_tempfile_')

if has('vim_starting')
    augroup coderunnerStart
        autocmd!
        autocmd VimEnter * call coderunner#Load()
    augroup END
else
    call coderunner#Load()
endif

augroup coderunnerEnd
  autocmd!
  autocmd VimLeave * call coderunner#OnExit()
augroup END

call s:restore_cpo()

" This is basic vim plugin boilerplate
function! s:restore_cpo()
  let &cpo = s:save_cpo
  unlet s:save_cpo
endfunction

let s:save_cpo = &cpo
set cpo&vim

if exists("g:loaded_coderunner")
  call s:restore_cpo()
  finish
elseif !has("python3")
  echohl WarningMsg |
        \ echomsg "Code Runner unavailable: unable to load python3." |
        \ echohl None
  call s:restore_cpo()
  finish
elseif &encoding !~? 'utf-\?8'
    echohl WarningMsg |
        \ echomsg "Code Runner unavailable: requires UTF-8 encoding. " .
        \ "Put the line 'set encoding=utf-8' in your vimrc." |
        \ echohl None
  call s:restore_cpo()
  finish
endif

let g:loaded_coderunner = 1

if has("vim_starting")
  augroup coderunnerStart
    autocmd!
    autocmd VimEnter * call coderunner#Enable()
  augroup END
else
  call coderunner#Enable()
endif

call s:restore_cpo()

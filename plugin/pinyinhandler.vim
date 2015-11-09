
if exists('g:loaded_pinyinhandler')
  finish
endif
let g:loaded_pinyinhandler = 1

nnoremap <C-p> :call pinyinhandler#enable()<CR>

" vim: foldmethod=marker

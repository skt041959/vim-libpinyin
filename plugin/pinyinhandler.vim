
if exists('g:loaded_pinyinhandler')
  finish
endif
let g:loaded_pinyinhandler = 1

command! -nargs=0 -bar PinyinEnable call pinyinhandler#enable()

nnoremap <C-.> :PinyinEnable<CR>

" vim: foldmethod=marker

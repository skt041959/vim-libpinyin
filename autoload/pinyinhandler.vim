
if !exists('s:is_enabled')
    let s:is_enabled = 0
endif

function! pinyinhandler#is_enabled() abort "{{{
    return s:is_enabled
endfunction "}}}

function! pinyinhandler#enable() abort "{{{
    if pinyinhandler#is_enabled()
        return
    endif

    augroup pinyinhandler
        autocmd!
    augroup END

    PinyinInitializePython

    let s:is_enabled = 1

    call pinyinhandler#init_variables()
    call pinyinhandler#handlers_init()
    call pinyinhandler#mappings_init()
endfunction "}}}

function! pinyinhandler#init_variables() abort
    let g:pinyinhandler#_context= {}
endfunction

function! pinyinhandler#handlers_init() abort "}}}
    augroup pinyin
        autocmd InsertLeave * call s:on_insert_leave()
        autocmd CompleteDone * call s:complete_done()
    augroup END

    for event in ['TextChangedI', 'InsertEnter']
        execute 'autocmd pinyin' event '*'
                    \ 'call s:completion_begin("' . event . '")'
    endfor
endfunction "}}}

function! pinyinhandler#init_context(event) abort "{{{
    return {
                \ 'changedtick': b:changedtick,
                \ 'event': a:event,
                \ 'input': pinyinhandler#get_input(a:event),
                \ 'complete_str': '',
                \ 'position': getpos('.'),
                \ }
endfunction"}}}

function! pinyinhandler#mappings_init() abort "{{{
  inoremap <silent> <Plug>(pinyinhandler_start_complete)
        \ <C-r>=pinyinhandler#mappings_do_complete(g:pinyinhandler#_context)<CR>
endfunction "}}}

function! pinyinhandler#mappings_do_complete(context) abort "{{{
  call pinyinhandler#mappings_set_completeopt()

  if b:changedtick == get(a:context, 'changedtick', -1)
    call complete(a:context.complete_position + 1, a:context.candidates)
  endif

  return ''
endfunction "}}}

function! pinyinhandler#mappings_set_completeopt() abort "{{{
  set completeopt-=longest
  set completeopt+=menuone
  if &completeopt !~# 'noinsert\|noselect'
    set completeopt+=noselect
  endif
endfunction "}}}

function! s:completion_begin(event) abort "{{{
    let context = pinyinhandler#init_context(a:event)

    if &paste || context.position ==#
                \      get(g:pinyinhandler#_context, 'position', [])
        return
    endif

    let g:pinyinhandler#_context.position = context.position

    call rpcnotify(g:pinyinhandler#_channel_id, 'pinyin_track', context)
endfunction "}}}

function! s:on_insert_leave() abort "{{{
    let g:pinyinhandler#_context = {}
endfunction"}}}

function! s:complete_done() abort "{{{
    let g:pinyinhandler#_context.position = getpos('.')
endfunction"}}}

function! pinyinhandler#get_input(event) abort "{{{
    let input = ((a:event ==# 'InsertEnter' || mode() ==# 'i') ?
                \   (col('.')-1) : col('.')) >= len(getline('.')) ?
                \      getline('.') :
                \      matchstr(getline('.'),
                \         '^.*\%' . (mode() ==# 'i' ? col('.') : col('.') - 1)
                \         . 'c' . (mode() ==# 'i' ? '' : '.'))

    if input =~ '^.\{-}\ze\S\+$'
        let complete_str = matchstr(input, '\S\+$')
        let input = matchstr(input, '^.\{-}\ze\S\+$')
    else
        let complete_str = ''
    endif

    if a:event ==# 'InsertCharPre'
        let complete_str .= v:char
    endif

    return input . complete_str
endfunction "}}}

" vim: fdm=marker

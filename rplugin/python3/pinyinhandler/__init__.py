#!/usr/bin/env python
# encoding: utf-8

import sys
import neovim
import traceback
from enum import Enum

from pinyinhandler.libpinyin_wrapper import Libpinyin_Wrapper


class Pinyin_Status(Enum):
    wait = 0
    get = 1
    parse = 2
    candidate = 3
    input = 4

def error(string):
    sys.stderr.write(string)
    sys.stderr.flush()

@neovim.plugin
class PinyinHandler(object):

    def __init__(self, vim):
        """construct the libpinyin plugin"""

        # sys.stderr.writelines([repr(e)+'\n' for e in traceback.extract_stack()])

        self.vim = vim
        self.status = Pinyin_Status.wait
        self.wrapper = None

    @neovim.command('PinyinInitializePython', nargs=0, sync=True)
    def pinyin_start(self):

        self.wrapper = Libpinyin_Wrapper()
        self.vim.vars['pinyinhandler#_channel_id'] = self.vim.channel_id

        # buffer = self.vim.current.buffer
        # buffer.options['completefunc'] = 'Pinyin_parse'

        # self.vim.command('autocmd InsertCharPre * call Pinyin_track()')
        # self.vim.command('autocmd InsertEnter * call Pinyin_track()')
        # self.vim.command('autocmd TextChangedI * call Pinyin_track()')

        # sys.stderr.writelines([repr(e)+'\n' for e in traceback.extract_stack()])

        error("pinyin_start called")

    @neovim.rpc_export('pinyin_track')
    def pinyin_track(self, context):

        error("pinyin_track called "+repr(context))
        try:
            senquence = context['input'].strip().encode('ascii')
        except:
            for line in traceback.format_exc().splitlines():
                 error(line)
            return

        words = self.wrapper.parse(senquence)
        error(words)

        var_context = {}

        if not words or self.vim.eval('mode()') != 'i':
            self.vim.vars['pinyinhandler#_context'] = var_context
            return

        var_context['complete_position'] = context['postion'][3]
        var_context['changedtick'] = context['changedtick']
        var_context['candidates'] = words
        self.vim.vars['pinyinhandler#_context'] = var_context

        # Note: cannot use vim.feedkeys()
        self.vim.command('call feedkeys("\<Plug>(pinyinhandler_start_complete)")')

    @neovim.function('Cmd1')
    def test_function(self, args):
        self.vim.call("complete", self.vim.current.window.cursor[1]+1, ['图书馆', '图', '4'])
        # self.vim.current.line = "test function line"

if __name__ == '__main__':

    import ipdb; ipdb.set_trace()
    socket_path = sys.argv[1]

    nvim = neovim.attach('socket', path=socket_path)

    l = PinyinHandler(nvim)


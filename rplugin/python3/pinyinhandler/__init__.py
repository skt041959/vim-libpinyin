#!/usr/bin/env python
# encoding: utf-8

import sys
import neovim
# import traceback
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
        self.subs_index = [0, 0]
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

        if self.status == Pinyin_Status.wait:
            self.status = Pinyin_Status.get

        error("pinyin_start called")

    @neovim.rpc_export('pinyin_track')
    def pinyin_track(self, args):

        error(__name__+" called "+repr(args))
        return

        char = self.vim.eval("v:char")

        sys.stderr.write(char)
        sys.stderr.flush()

        if self.status == Pinyin_Status.get:
            if isinstance(char, str):
                char = char.encode('ascii')
            if char == b' ':
                self.status = Pinyin_Status.parse
                words = self.parse(self.senquence)
                self.status = Pinyin_Status.candidate

                sys.stderr.write(repr(words))
                sys.stderr.flush()

            else:
                self.senquence+=(char)
                sys.stderr.write(repr(self.senquence))
                sys.stderr.flush()
        elif self.status == Pinyin_Status.candidate:
            try:
                index = int(char)
                sys.stderr.write(repr(index))
                sys.stderr.flush()
            except ValueError:
                self.vim.err_write("entry a index number to select the candidate word")

    @neovim.function('Cmd1')
    def test_function(self, args):
        self.vim.call("complete", self.vim.current.window.cursor[1]+1, ['图书馆', '图', '4'])
        # self.vim.current.line = "test function line"

if __name__ == '__main__':

    import ipdb; ipdb.set_trace()
    socket_path = sys.argv[1]

    nvim = neovim.attach('socket', path=socket_path)

    l = PinyinHandler(nvim)


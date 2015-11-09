#!/usr/bin/env python
# encoding: utf-8

import ctypes
from ctypes import c_char_p, byref

SYSTEMDIR = c_char_p(b"/usr/lib/libpinyin/data/")
USERDIR = c_char_p(b"~/.config/fcitx/libpinyin/data/")
CHARPTR = ctypes.POINTER(ctypes.c_char)

class Libpinyin_Wrapper(object):

    """Docstring for Libpinyin_Wrapper. """

    def __init__(self):
        """TODO: to be defined1. """

        self.prefixbuf = b''
        self.senquence = b''

        self.libpinyin = ctypes.CDLL("libpinyin.so.6")
        self.context = self.libpinyin.pinyin_init(SYSTEMDIR, USERDIR) # pinyin_context_t
        self.libpinyin.pinyin_set_options(self.context, ctypes.c_int(534774208))

        self.instance = self.libpinyin.pinyin_alloc_instance(self.context) # pinyin_instance_t

    def parse(self, pinyin_serial):

        buf = c_char_p(pinyin_serial)

        self.libpinyin.pinyin_parse_more_full_pinyins(self.instance, buf)
        self.libpinyin.pinyin_guess_sentence_with_prefix(self.instance, c_char_p(self.prefixbuf))
        self.libpinyin.pinyin_guess_full_pinyin_candidates(self.instance, 0)

        candi_len = ctypes.c_uint(0)
        self.libpinyin.pinyin_get_n_candidate(self.instance, byref(candi_len))

        words = []
        for i in range(min(7, candi_len.value)):
            candidate_p = ctypes.c_void_p(0)
            self.libpinyin.pinyin_get_candidate(self.instance, i, byref(candidate_p))
            word_p = CHARPTR()
            self.libpinyin.pinyin_get_candidate_string(self.instance, candidate_p, byref(word_p))

            word = ctypes.cast(word_p, ctypes.c_char_p).value.decode('utf8')
            words.append(word)

        return words


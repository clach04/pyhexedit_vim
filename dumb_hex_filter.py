#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
"""Demo filter for use with vim.

do not use! use xxd that ships with vim instead!

Vaguely useful as a reference for bytes IO in py3 and py2 with stdin/stdout.

Created to demo buffered IO issues under Windows with Python and vim.

    echo hello| python ./dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python ./dumb_hex_filter.py write

    echo hello| python ./dumb_hex_filter.py | python ./dumb_hex_filter.py write
    echo hello| python2 ./dumb_hex_filter.py | python2 ./dumb_hex_filter.py write
    echo hello| python3 ./dumb_hex_filter.py | python3 ./dumb_hex_filter.py write

    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python ./dumb_hex_filter.py write | python ./dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python2 ./dumb_hex_filter.py write | python2 ./dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python3 ./dumb_hex_filter.py write | python3 ./dumb_hex_filter.py


in vim try editing a file, then:

    :%!python dumb_hex_filter.py
    !}python dumb_hex_filter.py

For more information see https://vim.fandom.com/wiki/Use_filter_commands_to_process_text


And try .vimrc with autogroup/mode (see https://vim.fandom.com/wiki/Encryption for more info):

and:
    python -u
    python2 -u
    python3 -u

and PYTHONUNBUFFERED=x

.vimrc (TODO find my old debug one from windows machine)
ideally save to artbitry file and use:

    vim -u contents_below.vim ...
    gvim -u contents_below.vim ...
    nvim -u contents_below.vim ...

TODO effect on shell set on Microsoft Windows?

    augroup python_filter_issue
    autocmd!

    let $PYTHON_TEST_SCRIPT = "python dumb_hex_filter.py"

    function! s:PythonBinReadPre()
        set cmdheight=3
        set viminfo=
        set noswapfile
        set shell=/bin/sh
        set bin
    endfunction

    function! s:PythonBinReadPost()

        " TODO look at using filename <afile> rather than stdin as potential workaround
        " Python unuffeered values 0 and 1 both work so far under Linux

        let l:expr = "1,$!$PYTHON_TEST_SCRIPT"
        silent! execute l:expr
        if v:shell_error
            silent! 0,$y
            silent! undo
            echo "Error with EXPRESSION: " . expr
            echo @"
            echo "--------------------"
            return
        endif

        set nobin
        set cmdheight&
        set shell&
        execute ":doautocmd BufReadPost ".expand("%:r")
        redraw!
    endfunction

    function! s:PythonBinWritePre()
        set cmdheight=3
        set viminfo=
        set noswapfile
        set shell=/bin/sh
        set bin
        set nofixendofline
        " noeol has no effect, BUT vim 7.4+ directive nofixendofline does on vim 8.1.2269
        "set noeol

        " 0 and 1 both work so far under Linux

        let l:expr = "1,$!$PYTHON_TEST_SCRIPT write"

        silent! execute l:expr
        if v:shell_error
            silent! 0,$y
            silent! undo
            echo "Error with EXPRESSION: " . expr
            echo @"
            echo "--------------------"
            return
        endif

        set nobin
        set cmdheight&
        set shell&
        execute ":doautocmd BufReadPost ".expand("%:r")
        redraw!
    endfunction

    function! s:PythonBinWritePost()
        silent! undo
        set nobin
        set shell&
        set cmdheight&
        redraw!
    endfunction


    autocmd BufReadPre,FileReadPre     *.bin call s:PythonBinReadPre()
    autocmd BufReadPost,FileReadPost   *.bin call s:PythonBinReadPost()
    autocmd BufWritePre,FileWritePre   *.bin call s:PythonBinWritePre()
    autocmd BufWritePost,FileWritePost *.bin call s:PythonBinWritePost()

    augroup END

"""

import os
import sys

is_py3 = sys.version_info >= (3,)
is_win = sys.platform.startswith('win')


def unhex(hex_str):
    """dumb reverse of python builtin hex()
    returns integer value of string hex"""
    return int(hex_str, 16)


def main(argv=None):
    debug = False
    #debug = True
    if argv is None:
        argv = sys.argv
    # dumb  argv processing either hex read or hex write
    read_mode = True
    if len(argv) > 1:
        read_mode = False

    # treat everything as bytes
    if is_py3:
        in_file = sys.stdin.buffer
        out_file = sys.stdout.buffer
    else:
        in_file = sys.stdin
        out_file = sys.stdout

    failed = True
    # do stuff
    raw_bytes = in_file.read()  # read it all, doesn't need to be efficient
    if debug:
        sys.stderr.write('Python %s on %s\n' % (sys.version.replace('\n', ' - '), sys.platform))
        sys.stderr.write('raw_bytes length %d\n' % (len(raw_bytes),))
        #sys.stderr.write('raw_bytes %r\n' % (raw_bytes,))
        sys.stderr.flush()

    if read_mode:
        # read in binary and emit hex
        if is_py3:
            result = [b'0x%02x' % x for x in raw_bytes]
        else:
            result = [b'0x%02x' % ord(x) for x in raw_bytes]
        result = b' '.join(result)  # don't even have new lines, the worst hex dump ever ;-)
        # TODO revisit newlines, may need for debugging purposes :-D Line count may be the easiest byte counter
        out_file.write(result)
        out_file.write(b'\n')
        # NOTE no explictly flush
        failed = False
    else:
        # read in hex strings and write out binary
        pass
        # stupid bytes to string conversion, as its faster to write this than do it properly...
        # aim of this test case is buffered IO experiments and interaction with vim under Microsoft Windows
        string_buffer = raw_bytes.decode('us-ascii')
        if is_py3:
            result = [unhex(x) for x in string_buffer.split()]
            result = bytes(result)
        else:
            result = [chr(unhex(x)) for x in string_buffer.split()]
            result = ''.join(result)
            result = result.encode('latin1')
        #sys.stderr.write('DEBUG result %r' % result)
        out_file.write(result)
        # NOTE no explictly flush
        failed = False

    if failed:
        sys.stderr.write('error: something bad happened')
        sys.stderr.flush()
        return 1


    return 0


if __name__ == "__main__":
    sys.exit(main())

# pyhexedit_vim

Demo filter for use with vim - created for Microsoft Windows compat testing

A very bad hex viewer and editor filter for vim,
do not use! use xxd that ships with vim instead!

Vaguely useful as a reference for bytes IO in py3 and py2 with stdin/stdout.

Created to demo buffered IO issues under Windows with Python and vim.

Works fine under Linux with:

  * VIM - Vi IMproved 8.0
      * Python 2.7.17
      * Python 3.6.9

## Demo

    echo hello| python dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python dumb_hex_filter.py write

    echo hello> hello.bin
    python dumb_hex_filter.py < hello.bin


    vim  -u hexedit.vim hello.bin
    gvim -u hexedit.vim hello.bin
    nvim -u hexedit.vim hello.bin


    # or inject contents of hexedit.vim into ~/.vimrc
    env PYTHON_TEST_SCRIPT="python dumb_hex_filter.py" vim  hello.bin
    env PYTHON_TEST_SCRIPT="python2 dumb_hex_filter.py" vim  hello.bin
    env PYTHON_TEST_SCRIPT="python3 dumb_hex_filter.py" vim  hello.bin



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


-------------------------

## Additional Demos

    echo hello| python ./dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python ./dumb_hex_filter.py write

    echo hello| python ./dumb_hex_filter.py | python ./dumb_hex_filter.py write
    echo hello| python2 ./dumb_hex_filter.py | python2 ./dumb_hex_filter.py write
    echo hello| python3 ./dumb_hex_filter.py | python3 ./dumb_hex_filter.py write

    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python ./dumb_hex_filter.py write | python ./dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python2 ./dumb_hex_filter.py write | python2 ./dumb_hex_filter.py
    echo 0x68 0x65 0x6c 0x6c 0x6f 0x0a | python3 ./dumb_hex_filter.py write | python3 ./dumb_hex_filter.py

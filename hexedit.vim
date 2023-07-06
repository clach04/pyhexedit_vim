" ensure we can see status line/bar
set laststatus=2


augroup python_filter_issue
autocmd!


if $PYTHON_TEST_SCRIPT == ""
    let $PYTHON_TEST_SCRIPT = "python dumb_hex_filter.py"
endif



function! s:PythonBinReadPre()
    set cmdheight=3
    set viminfo=
    set noswapfile
    set shell=/bin/sh
    set bin
endfunction

function! s:PythonBinReadPost()

    " TODO look at using filename <afile> rather than stdin as potential workaround
    " PYTHONUNBUFFERED - Python unbuffered values 0 and 1 both work so far under Linux

    " TODO add debug option for silent and non-silent call
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
" end python_filter_issue

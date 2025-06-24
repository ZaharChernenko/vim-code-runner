# Vim Code Runner - run your code the same way as with [vs code runner](https://github.com/formulahendry/vscode-code-runner)
https://github.com/user-attachments/assets/63109233-1e5d-4d54-b890-30eb07dab826
- [Vim Code Runner - run your code the same way as with vs code runner](#vim-code-runner---run-your-code-the-same-way-as-with-vs-code-runner)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [`CodeRunnerRunByFileExt`](#coderunnerrunbyfileext)
    - [`CodeRunnerRunByFileType`](#coderunnerrunbyfiletype)
    - [`CodeRunnerRunByGlob`](#coderunnerrunbyglob)
    - [`CodeRunnerRun`](#coderunnerrun)
    - [`coderunner#Load()`](#coderunnerload)
    - [`coderunner#RemoveCoderunnerTempfiles()`](#coderunnerremovecoderunnertempfiles)
  - [Configuration](#configuration)
    - [`g:coderunner_by_file_ext`](#gcoderunner_by_file_ext)
    - [`g:coderunner_by_file_type`](#gcoderunner_by_file_type)
    - [`g:coderunner_by_glob`](#gcoderunner_by_glob)
    - [`g:coderunner_executor`](#gcoderunner_executor)
    - [`g:coderunner_ignore_selection`](#gcoderunner_ignore_selection)
    - [`g:coderunner_remove_coderunner_tempfiles_on_exit`](#gcoderunner_remove_coderunner_tempfiles_on_exit)
    - [`g:coderunner_respect_shebang`](#gcoderunner_respect_shebang)
    - [`g:coderunner_runners_order`](#gcoderunner_runners_order)
    - [`g:coderunner_save_all_files_before_run`](#gcoderunner_save_all_files_before_run)
    - [`g:coderunner_save_file_before_run`](#gcoderunner_save_file_before_run)
    - [`g:coderunner_tempfile_prefix`](#gcoderunner_tempfile_prefix)

## Requirements
- Vim version 8.0+ with Python3 support. Check with:
    ```vim
    :echo has('python3') " should return 1
    ```
- To use `CodeRunnerRunByGlob` python version must be above 3.13. Check with:
   ```vim
   :py3 import sys;print(sys.version) " should return >= 3.13
   ```

## Installation
Install the Vim plugin with your favorite plugin manager, e.g. vim-plug:
```vim  
Plug 'ZaharChernenko/vim-code-runner'  
```

## Usage
### `CodeRunnerRunByFileExt`
Tries to execute the code if the extension of the current file matches the extension from [`g:coderunner_by_file_ext`](#gcoderunner_by_file_ext), the extension is a dot + the last part of the file name after the last dot.
### `CodeRunnerRunByFileType`
Tries to execute the code if the current file type is defined in the [`g:coderunner_by_file_type`](#gcoderunner_by_file_type), to find out what type of open file run `:echo &filetype`.
### `CodeRunnerRunByGlob`
Tries to execute the code if the full path of the current file corresponds to some glob pattern in [`g:coderunner_by_glob`](#gcoderunner_by_glob), **it is important that this function works only with vim, which has version python3.13+.**
### `CodeRunnerRun`
Tries to execute the code using the fallback strategy defined in [`g:coderunner_runners_order`](#gcoderunner_runners_order).
### `coderunner#Load()`
The function that loads the coderunner module also updates the variables: g:coderunner_by_file_ext, g:coderunner_by_file_type g:coderunner_by_glob.
### `coderunner#RemoveCoderunnerTempfiles()`
The function that cleans up temporary files that were created due to run with selection, it clears only those files that were created in the current vim session.

## Configuration
### `g:coderunner_by_file_ext`
Hash table with mapping of file extensions to commands, default `{}`, example:
```vim
let g:coderunner_by_file_ext = {
    \ '.cpp': 'bash -c "cd \"$dir\" && g++ -o cpp_output -std=c++2a *.cpp && ./cpp_output"',
    \ '.py': 'bash -c "cd \"$dir\" && python3 \"$fullFileName\""',
\ }
```
### `g:coderunner_by_file_type`
Hash table with mapping of file types to commands, default `{}`, example:
```vim
let g:coderunner_by_file_type = {
    \ 'cpp': 'bash -c "cd \"$dir\" && g++ -o cpp_output -std=c++2a *.cpp && ./cpp_output"',
    \ 'python': 'bash -c "cd \"$dir\" && python3 \"$fullFileName\""',
\ }
```
To find out what type of open file run `:echo &filetype`.
### `g:coderunner_by_glob`
Hash table with mapping glob patterns into commands, given that the hash table is unordered, coderunner sorts the patterns in reverse lexicographic order, trying to find the most accurate one first, default `{}`, example:
```vim
let g:coderunner_by_glob = {
    \ '**/*.cpp': 'bash -c "cd \"$dir\" && g++ -o cpp_output -std=c++2a *.cpp && ./cpp_output"',
    \ '**/*.py': 'bash -c "cd \"$dir\" && python3 \"$fullFileName\""',
\ } 
```
### `g:coderunner_executor`
Any vim command that can execute a string is suitable, default `ter`, default behaviour:

https://github.com/user-attachments/assets/bea987a0-7269-4dc4-ae01-590a71d9dd5f

It is important to note that a regular terminal does not execute commands related through logical operators, for example `&`, so you need to use `bash -c` with a string.

But for example, if you have [floaterm](https://github.com/voldikss/vim-floaterm) plugin installed, you can set the following command:
```vim
let g:coderunner_executor = "FloatermNew --autoclose=0"
```

https://github.com/user-attachments/assets/374e11d4-efd8-42ae-bdce-92b5df0cdb39
### `g:coderunner_ignore_selection`
If 1 ranges do not work, the command is executed for the entire file, default `0`.
### `g:coderunner_remove_coderunner_tempfiles_on_exit`
If 1, then when exiting the vim, it calls the [coderunner#RemoveCoderunnerTempfiles()](#coderunnerremovecoderunnertempfiles) command, default `0`.
### `g:coderunner_respect_shebang`
if 1, the shebang command is executed, even if there are matches in the hash tables, default `1`.
### `g:coderunner_runners_order`
Defines the order of searching for matches when executing the [CodeRunnerRun](#coderunnerrun) command, default `['by_glob', 'by_file_ext', 'by_file_type']`.
### `g:coderunner_save_all_files_before_run`
If 1, saves all open files before execution, note files are saved only if a runner is found, default `0`.
### `g:coderunner_save_file_before_run`
If 1, saves the current file before execution, default `0`.
### `g:coderunner_tempfile_prefix`
The prefix with which files will be saved in the directory of the executable file when executing commands with selection.
# Vim Code Runner - run your code the same way as with [vs code runner](https://github.com/formulahendry/vscode-code-runner)
https://github.com/user-attachments/assets/63109233-1e5d-4d54-b890-30eb07dab826
- [Vim Code Runner - run your code the same way as with vs code runner](#vim-code-runner---run-your-code-the-same-way-as-with-vs-code-runner)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)

## Requirements
- Vim version 8.0+ with Python3 support. Check with:
    ```vim
    :echo has('python3') "should return 1
    ```
- To use `CodeRunnerRunByGlob` python version must be above 3.13. Check with:
   ```vim
   :py3 import sys;print(sys.version)
   ```

## Installation
Install the Vim plugin with your favorite plugin manager, e.g. vim-plug:
```vim  
Plug 'ZaharChernenko/vim-code-runner'  
```

## Usage
1. `CodeRunnerRunByFileExt` - tries to execute the code if the extension of the current file matches the extension from g:coderunner_by_file_ext, the extension is a dot + the last part of the file name after the last dot.
2. `CodeRunnerRunByFileType` - tries to execute the code if the current file type is defined in the g:coderunner_by_file_type, to find out what type of open file run `:echo &filetype`.
3. `CodeRunnerRunByGlob` - tries to execute the code if the full path of the current file corresponds to some glob pattern in g:coderunner_by_glob, **it is important that this function works only with vim, which has version python3.13+.**
4. `CodeRunnerRun` - tries to execute the code using the fallback strategy defined in g:coderunner_runners_order.
5. `coderunner#Load()` - the function that loads the coderunner module also updates the variables: g:coderunner_by_file_ext, g:coderunner_by_file_type g:coderunner_by_glob.
6. `coderunner#RemoveCoderunnerTempfiles()` - a function that cleans up temporary files that were created due to run with selection, it clears only those files that were created in the current vim session.

## Configuration
- `g:coderunner_save_all_files_before_run`: If 1, saves all open files before execution, note files are saved only if a runner is found. (default 0)
- `g:coderunner_save_file_before_run`: If 1, saves the current file before execution (default 0)

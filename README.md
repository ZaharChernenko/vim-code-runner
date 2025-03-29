# Vim Code Runner  

- [Vim Code Runner](#vim-code-runner)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Supported Languages](#supported-languages)
  - [Example Usage](#example-usage)
  - [Extension Guide](#extension-guide)

## Overview  

Vim Code Runner is a plugin that provides code execution capabilities within Vim for multiple programming languages. It allows you to run code directly from your editor with customizable behavior.

## Requirements

- Vim version 8.0+ with Python3 support. Check with:
    ```vim
    :echo has('python3') "should return 1
    ```

## Installation

Install the Vim plugin with your favorite plugin manager, e.g. vim-plug:
```vim  
Plug 'ZaharChernenko/vim-code-runner'  
```

## Usage

1. **`coderunner#Load()`**  
   Initializes the plugin and checks for dependencies, it can also be used to update the configuration.

2. **`coderunner#Run()`**  
   Executes the current file based on its filetype.  

3. **`coderunner#Clear()`**  
   Cleans up any execution artifacts. 

## Configuration  

- `g:coderunner_save_file_before_run`: If 1, saves the current file before execution (default 0)
- `g:coderunner_save_all_files_before_run`: If 1, saves all open files before execution (default 0)

## Supported Languages  

The plugin currently supports:

- Python3
- C++

The language runners are defined in the `TRunnerContext.LANG_TO_RUNNER` dictionary.  

## Example Usage  

```vim  
" Map F5 to run current file  
nnoremap <F5> :call coderunner#Run()<CR>  

" Map F6 to clear execution artifacts  
nnoremap <F6> :call coderunner#Clear()<CR>  
```  

## Extension Guide  

To add support for new languages:  

1. Create a new runner class implementing `runners.IRunner` or `runner.ICompilingRunner`  
2. Add it to `TRunnerContext.LANG_TO_RUNNER` dictionary  
3. Implement any necessary cleanup in the `clear` method 
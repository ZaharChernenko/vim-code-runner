from typing import Any

import vim

from .exceptions import UndefinedValueError


class TBaseVimConfigValueGetter:
    """Base class for getting Vim config values"""

    def _get_vim_var(self, var_name: str) -> Any:
        try:
            return vim.eval(var_name)
        except vim.error:
            raise UndefinedValueError(f"Vim variable {var_name} is not defined. Please set it in your vimrc.")


class TVimByFileExtConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_by_file_ext")


class TVimByFileTypeConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_by_file_type")


class TVimByGlobConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_by_glob")


class TVimCoderunnerTempfilePrefixConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_tempfile_prefix")


class TVimDispatchersOrderConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_runners_order")


class TVimExecutorConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_executor")


class TVimIgnoreSelectionConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_ignore_selection")


class TVimRespectShebangConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_respect_shebang")


class TVimRemoveCoderunnerTempfilesOnExitConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_remove_coderunner_tempfiles_on_exit")


class TVimSaveAllFilesBeforeRunConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_save_all_files_before_run")


class TVimSaveFileBeforeRunConfigValueGetter(TBaseVimConfigValueGetter):
    def __call__(self) -> Any:
        return self._get_vim_var("g:coderunner_save_file_before_run")

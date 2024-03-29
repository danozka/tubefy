import logging

from logging import Logger
from pathlib import Path


class DirectoryHandler:

    _log: Logger = logging.getLogger(__name__)
    _root_path: Path

    def __init__(self, root_path: Path):

        self._root_path = root_path

    def create_directory(self, directory_path: Path) -> Path:

        self._log.debug(f'Start [funcName](directory_path=\'{directory_path}\')')
        directory_absolute_path: Path = self._get_directory_absolute_path(directory_path)
        directory_absolute_path.mkdir(parents=True, exist_ok=True)
        self._log.debug(f'End [funcName](directory_path=\'{directory_path}\')')

        return directory_absolute_path

    def delete_directory(self, directory_path: Path) -> None:

        self._log.debug(f'Start [funcName](directory_path=\'{directory_path}\')')

        directory_absolute_path: Path = self._get_directory_absolute_path(directory_path)

        if self._is_directory(directory_absolute_path):

            try:

                self._delete_directory_recursively(directory_absolute_path)

            except Exception as exception:

                self._log.warning(
                    msg=f'Exception found while deleting directory \'{directory_path}\'',
                    extra={'exception': exception}
                )

        self._log.debug(f'End [funcName](directory_path=\'{directory_path}\')')

    def _get_directory_absolute_path(self, directory_path: Path) -> Path:

        if directory_path.is_absolute():

            return directory_path.resolve()

        else:

            return self._root_path.joinpath(directory_path).resolve()

    def _is_directory(self, directory_path: Path) -> bool:

        if directory_path.exists() and directory_path.is_dir():

            return True

        else:

            self._log.warning(f'Path \'{directory_path}\' does not exist or it is not a directory')

            return False

    def _delete_directory_recursively(self, directory_path: Path) -> None:

        item: Path
        for item in directory_path.iterdir():

            if item.is_file():

                item.unlink()

            elif item.is_dir():

                self._delete_directory_recursively(item)

        directory_path.rmdir()

import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path

from ..configuration.app_settings import AppSettings
from .database_context import DatabaseContext
from .domain.database_audio_sample import DatabaseAudioSample
from ..services.directory_handler import DirectoryHandler


class AudioSamplesPersistence:

    _log: Logger = logging.getLogger(__name__)
    _sample_files_directory: str = 'samples'
    _database_context: DatabaseContext
    _sample_files_directory_path: Path

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        directory_handler: DirectoryHandler = Provide['directory_handler']
    ):

        self._database_context = DatabaseContext(
            directory_handler.create_directory(app_settings.persistence_settings.data_path)
        )
        self._sample_files_directory_path = directory_handler.create_directory(
            app_settings.persistence_settings.data_path.joinpath(self._sample_files_directory)
        )

    def close(self) -> None:

        self._database_context.close()

    def get_audio_sample(self, video_id: str) -> DatabaseAudioSample | None:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        result: DatabaseAudioSample | None = self._database_context.get_audio_sample(video_id)
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result

    def add_audio_sample(self, database_audio_sample: DatabaseAudioSample) -> None:

        self._log.debug(f'Start [funcName](database_audio_sample={database_audio_sample})')
        self._database_context.add_audio_sample(database_audio_sample)
        self._log.debug(f'End [funcName](database_audio_sample={database_audio_sample})')

    def delete_all_audio_samples(self) -> None:

        self._log.debug('Start [funcName]()')
        database_audio_samples: list[DatabaseAudioSample] = self._database_context.get_all_audio_samples()

        database_audio_sample: DatabaseAudioSample
        for database_audio_sample in database_audio_samples:

            database_audio_sample_file_path: Path = Path(database_audio_sample.file_path)

            if database_audio_sample_file_path.is_file():

                database_audio_sample_file_path.unlink()

            self._database_context.delete_audio_sample(database_audio_sample)

        self._log.debug('End [funcName]()')

    def get_audio_samples_directory(self) -> Path:

        return self._sample_files_directory_path

    @staticmethod
    def get_audio_sample_filename(video_id: str) -> str:

        return video_id

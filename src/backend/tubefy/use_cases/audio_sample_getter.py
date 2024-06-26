import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from ..adapters.audio_sample_adapter import AudioSampleAdapter
from ..communications.youtube_audio_sample_getter import YoutubeAudioSampleGetter
from ..domain.audio_sample import AudioSample
from ..dtos.audio_output import AudioOutput
from ..exceptions.audio_file_not_found_exception import AudioFileNotFoundException
from ..persistence.audio_samples_persistence import AudioSamplesPersistence
from ..persistence.domain.audio_sample_persistence_domain import AudioSamplePersistenceDomain


class AudioSampleGetter:

    _log: Logger = logging.getLogger(__name__)
    _audio_sample_adapter: AudioSampleAdapter
    _youtube_audio_sample_getter: YoutubeAudioSampleGetter
    _audio_samples_persistence: AudioSamplesPersistence

    @inject
    def __init__(
        self,
        audio_sample_adapter: AudioSampleAdapter = Provide['audio_sample_adapter'],
        youtube_audio_sample_getter: YoutubeAudioSampleGetter = Provide['youtube_audio_sample_getter'],
        audio_samples_persistence: AudioSamplesPersistence = Provide['audio_samples_persistence']
    ) -> None:

        self._audio_sample_adapter = audio_sample_adapter
        self._youtube_audio_sample_getter = youtube_audio_sample_getter
        self._audio_samples_persistence = audio_samples_persistence

    async def get(self, video_id: str) -> AudioOutput:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        audio_sample_persistence_domain: AudioSamplePersistenceDomain | None = (
            await self._audio_samples_persistence.get_audio_sample(video_id)
        )

        if audio_sample_persistence_domain is None:

            audio_sample: AudioSample = self._youtube_audio_sample_getter.get(
                video_id=video_id,
                output_directory=self._audio_samples_persistence.get_audio_samples_directory(),
                output_filename=self._audio_samples_persistence.get_audio_sample_filename(video_id)
            )
            audio_sample_persistence_domain: AudioSamplePersistenceDomain = (
                self._audio_sample_adapter.adapt_to_persistence(audio_sample)
            )
            await self._audio_samples_persistence.add_audio_sample(audio_sample_persistence_domain)

        else:

            audio_sample: AudioSample = self._audio_sample_adapter.adapt_from_persistence(
                audio_sample_persistence_domain
            )

            if not audio_sample.file_path.is_file():

                raise AudioFileNotFoundException(audio_sample.file_path)

        result: AudioOutput = self._audio_sample_adapter.adapt_to_output_file(audio_sample)
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result

import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from uuid import UUID
from ..domain.audio_recording import AudioRecording
from ..domain.user import User
from ..exceptions.audio_recording_not_found_exception import AudioRecordingNotFoundException
from ..persistence.audio_recordings_persistence import AudioRecordingsPersistence
from ..persistence.domain.audio_recording_persistence_domain import AudioRecordingPersistenceDomain


class AudioRecordingDeleter:

    _log: Logger = logging.getLogger(__name__)
    _audio_recordings_persistence: AudioRecordingsPersistence

    @inject
    def __init__(
        self,
        audio_recordings_persistence: AudioRecordingsPersistence = Provide['audio_recordings_persistence']
    ) -> None:

        self._audio_recordings_persistence = audio_recordings_persistence

    async def delete(self, audio_recording_id: UUID, user: User) -> None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\', user={user})')
        audio_recording: AudioRecording | None = next(
            (x for x in user.audio_recordings if x.id == audio_recording_id),
            None
        )

        if audio_recording is None:

            raise AudioRecordingNotFoundException(audio_recording_id)

        else:

            audio_recording_persistence_domain: AudioRecordingPersistenceDomain = (
                await self._audio_recordings_persistence.get_audio_recording(audio_recording_id)
            )
            await self._audio_recordings_persistence.delete_audio_recording(audio_recording_persistence_domain)
            self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\', user={user})')

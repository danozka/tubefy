import logging

from logging import Logger
from pathlib import Path
from uuid import UUID

from ..domain import AudioRecording, User
from ..dtos import AudioRecordingOutput, AudioOutput
from ..persistence.domain import DatabaseAudioRecording


class AudioRecordingAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_to_domain(self, database_audio_recording: DatabaseAudioRecording) -> AudioRecording:

        self._log.debug(f'Start [funcName](database_audio_recording={database_audio_recording})')
        result: AudioRecording = AudioRecording(
            id_=UUID(database_audio_recording.id),
            video_id=database_audio_recording.video_id,
            file_path=Path(database_audio_recording.file_path),
            title=database_audio_recording.title,
            artist=database_audio_recording.artist,
            codec=database_audio_recording.codec,
            bit_rate=database_audio_recording.bit_rate,
            user_id=UUID(database_audio_recording.user_id)
        )
        self._log.debug(f'End [funcName](database_audio_recording={database_audio_recording})')

        return result

    def adapt_to_output(self, audio_recording: AudioRecording) -> AudioRecordingOutput:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        result: AudioRecordingOutput = AudioRecordingOutput(
            id=audio_recording.id,
            video_id=audio_recording.video_id,
            title=audio_recording.title,
            artist=audio_recording.artist,
            codec=audio_recording.codec,
            bit_rate=audio_recording.bit_rate
        )
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

        return result

    def adapt_to_output_file(self, audio_recording: AudioRecording) -> AudioOutput:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        result: AudioOutput = AudioOutput(audio_recording.file_path)
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

        return result

    def adapt_to_persistence(self, audio_recording: AudioRecording, user: User) -> DatabaseAudioRecording:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording}, user={user})')
        result: DatabaseAudioRecording = DatabaseAudioRecording(
            id=str(audio_recording.id),
            video_id=audio_recording.video_id,
            file_path=str(audio_recording.file_path),
            title=audio_recording.title,
            artist=audio_recording.artist,
            codec=audio_recording.codec,
            bit_rate=audio_recording.bit_rate,
            user_id=str(user.id)
        )
        self._log.debug(f'End [funcName](audio_recording={audio_recording}, user={user})')

        return result

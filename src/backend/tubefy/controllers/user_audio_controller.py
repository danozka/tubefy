import logging
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from logging import Logger
from uuid import UUID
from .app_base_controller import AppBaseController
from ..domain.user import User
from ..dtos.audio_download_options_input import AudioDownloadOptionsInput
from ..dtos.audio_output import AudioOutput
from ..dtos.audio_recording_output import AudioRecordingOutput
from ..middleware.request_authentication_middleware import RequestAuthenticationMiddleware
from ..use_cases.audio_recording_adder import AudioRecordingAdder
from ..use_cases.audio_recording_deleter import AudioRecordingDeleter
from ..use_cases.audio_recording_getter import AudioRecordingGetter
from ..use_cases.user_getter import UserGetter


class UserAudioController(AppBaseController):

    api_router: APIRouter = APIRouter(prefix='/api', tags=['user_audio'])
    _log: Logger = logging.getLogger(__name__)
    _audio_recording_adder: AudioRecordingAdder
    _audio_recording_deleter: AudioRecordingDeleter
    _audio_recording_getter: AudioRecordingGetter
    _user_getter: UserGetter

    @inject
    def __init__(
        self,
        audio_recording_adder: AudioRecordingAdder = Provide['audio_recording_adder'],
        audio_recording_deleter: AudioRecordingDeleter = Provide['audio_recording_deleter'],
        audio_recording_getter: AudioRecordingGetter = Provide['audio_recording_getter'],
        user_getter: UserGetter = Provide['user_getter']
    ) -> None:

        self.api_router.add_api_route(
            path='/videos/{video_id}/audio',
            endpoint=self.add_user_audio_recording,
            methods=['POST']
        )
        self.api_router.add_api_route(
            path='/audio',
            endpoint=self.get_all_user_audio_recordings,
            methods=['GET']
        )
        self.api_router.add_api_route(
            path='/audio/{audio_recording_id}',
            endpoint=self.get_user_audio_recording,
            methods=['GET']
        )
        self.api_router.add_api_route(
            path='/audio/{audio_recording_id}',
            endpoint=self.delete_user_audio_recording,
            methods=['DELETE']
        )
        self._audio_recording_adder = audio_recording_adder
        self._audio_recording_deleter = audio_recording_deleter
        self._audio_recording_getter = audio_recording_getter
        self._user_getter = user_getter

    async def add_user_audio_recording(
        self,
        video_id: str,
        audio_download_options_input: AudioDownloadOptionsInput,
        token: str = Depends(RequestAuthenticationMiddleware.authenticate_request)
    ) -> None:

        self._log.info(
            f'Start [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input})'
        )

        try:

            user: User = await self._user_getter.get(token)
            await self._audio_recording_adder.add(
                video_id=video_id,
                audio_download_options_input=audio_download_options_input,
                user=user
            )
            self._log.info(
                f'End [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input})'
            )

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input}) '
                f'with exceptions',
                extra={'exception': exception}
            )

            raise exception

    async def get_all_user_audio_recordings(
        self,
        token: str = Depends(RequestAuthenticationMiddleware.authenticate_request)
    ) -> list[AudioRecordingOutput]:

        self._log.info('Start [funcName]()')

        try:

            user: User = await self._user_getter.get(token)
            result: list[AudioRecordingOutput] = self._audio_recording_getter.get_all(user)
            self._log.info('End [funcName]()')

            return result

        except Exception as exception:

            self._log.error(msg='End [funcName]() with exceptions', extra={'exception': exception})

            raise exception

    async def get_user_audio_recording(
        self,
        audio_recording_id: UUID,
        token: str = Depends(RequestAuthenticationMiddleware.authenticate_request)
    ) -> AudioOutput:

        self._log.info(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')

        try:

            user: User = await self._user_getter.get(token)
            result: AudioOutput = self._audio_recording_getter.get(audio_recording_id=audio_recording_id, user=user)
            self._log.info(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

            return result

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](audio_recording_id=\'{audio_recording_id}\') with exceptions',
                extra={'exception': exception}
            )

            raise exception

    async def delete_user_audio_recording(
        self,
        audio_recording_id: UUID,
        token: str = Depends(RequestAuthenticationMiddleware.authenticate_request)
    ) -> None:

        self._log.info(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')

        try:

            user: User = await self._user_getter.get(token)
            await self._audio_recording_deleter.delete(audio_recording_id=audio_recording_id, user=user)
            self._log.info(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](audio_recording_id=\'{audio_recording_id}\') with exceptions',
                extra={'exception': exception}
            )

            raise exception

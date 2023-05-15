import os
import pytest

from datetime import datetime
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.domain.song import Song


@pytest.fixture(scope='package')
@inject
def integration_tests_song(app_settings: AppSettings = Provide['app_settings']) -> Song:

    song_id = 'Ucmo6hDZRSY'
    song_title = 'Self control'
    song_artist = 'Laura Branigan'
    song_creation_date = datetime.now()
    music_files_absolute_directory = os.path.abspath(app_settings.persistence_settings.music_files_directory)
    song_file = os.path.join(music_files_absolute_directory,
                             f'{song_artist} - {song_title}.{app_settings.music_downloader_settings.audio_codec}')

    song = Song(id_=song_id,
                title=song_title,
                artist=song_artist,
                creation_date=song_creation_date,
                file=song_file)

    return song

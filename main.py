import asyncio
import io
import zipfile
from pathlib import Path
from typing import Dict
from urllib.parse import urljoin

import aiohttp
import imdb
from bullet import Bullet
from requests import codes

wizdom_title_info = 'https://wizdom.xyz/api/releases/'
wizdom_sub_download_url = 'https://wizdom.xyz/api/files/sub/'


class NoMatchingSubtitle(Exception):
    pass


def find_subtitle_match(subtitle_matches, file_name):
    match_options = [match['version'] for match in subtitle_matches]
    if not match_options:
        raise NoMatchingSubtitle()

    skip_option = 'Skip'
    print("\033c", end="")
    chosen_match = Bullet(
        prompt=f'\nMatching [{file_name}]...',
        choices=match_options + [skip_option],
        return_index=False
    ).launch()

    if chosen_match == skip_option:
        raise NoMatchingSubtitle()

    for match in subtitle_matches:
        if match['version'] == chosen_match:
            return match

    raise NoMatchingSubtitle()


async def list_subtitle_for_title(title_id: str) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(urljoin(wizdom_title_info, title_id)) as response:
            if response.status == codes.ok:
                result = await response.json()
                return result['subs']

    raise ConnectionError()


async def download_subtitle(subtitle_id: str, output_file: Path) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(urljoin(wizdom_sub_download_url, subtitle_id)) as response:
            if response.status == codes.ok:
                content = await response.read()
            else:
                raise ConnectionError()

    with zipfile.ZipFile(io.BytesIO(content), 'r') as zip_archive:
        with zip_archive.open(zip_archive.namelist()[0]) as file_in_zip:
            with output_file.open('wb') as output_file:
                output_file.write(file_in_zip.read())


async def main():
    ia = imdb.IMDb()
    result = await loop.run_in_executor(None, ia.search_movie, title)
    imdb_id = result[0].getID()

    title_subs = await list_subtitle_for_title(title_id=f'tt{imdb_id}')
    available_subs = list()
    for _, value in title_subs[season].items():
        available_subs += value
    available_subs.sort(key=lambda x: x['version'])

    for video_file in output_dir.iterdir():
        if not video_file.is_file() or video_file.with_suffix('.srt').is_file():  # ignore already downloaded subtitles
            continue

        try:
            subtitle_match = find_subtitle_match(available_subs, video_file.stem)
            await download_subtitle(str(subtitle_match['id']), video_file.with_suffix('.srt'))
            available_subs.remove(subtitle_match)
        except NoMatchingSubtitle:
            continue


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir')
    parser.add_argument('title')
    parser.add_argument('season', type=str)
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    assert output_dir.is_dir()

    title = args.title
    season = args.season

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

import requests
from requests_toolbelt.multipart import encoder
import os
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import shutil
import pathlib

def get_files(path: str):
    paths = []
    pathlist_ts = pathlib.Path(path).glob('*.ts')
    pathlist_m3u8 = pathlib.Path(path).glob('*.m3u8')
    pathlist_thumb = pathlib.Path(path).glob('*.webp')
    for file in pathlist_ts:
        paths.append(file)
    for file in pathlist_m3u8:
        paths.append(file)
    for file in pathlist_thumb:
        paths.append(file)
    return paths

def get_total_size(paths: list[str]):
    total_size = 0
    for file in paths:
        total_size += os.stat(file).st_size
    return total_size

def uploads(paths: list[str], api:str, original_name:str, username:str):
    total_size = get_total_size(paths)
    with tqdm(
        total=total_size, unit='B', unit_scale=True, unit_divisor=1024,
        colour='green', position=0, desc='total', leave=False
    ) as t:
        for file in paths:
            _upload(file, api, username, original_name)
            t.update(os.stat(file).st_size)
    return True

def _upload(path:str, api:str, username:str, original_name:str):
    file_size = os.stat(path).st_size
    file_name = os.path.basename(path)
    dir_name = os.path.basename(os.path.dirname(path))
    original_name = os.path.splitext(os.path.basename(original_name))[0]
    with open(path, 'rb') as file:
        with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024,
            position=1, leave=False, colour='blue', desc=file_name
        ) as t:
            monitor = encoder.MultipartEncoder({
                'file': (file_name, CallbackIOWrapper(t.update, file, 'read')),
                'username': username,
                'dirname': dir_name,
                'original_name': original_name
                }
            )
            response = requests.post(
                api,
                data=monitor,
                verify=False, # 証明書チェック無視
                headers={'Content-Type': monitor.content_type}
            )
    return True

def register(json:dict, api:str):
    response = requests.post(
        api,
        json=json
    )
    return response.text


def depricated_to_zip(path: str, archive_name: str):
    # archive_name = os.path.splitext(os.path.basename(input))[0]
    shutil.make_archive(archive_name, 'zip', path)
    shutil.rmtree(path)

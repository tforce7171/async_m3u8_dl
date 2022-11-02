import m3u8
from urllib.parse import urlparse
from glob import glob
import os
import subprocess
import shutil
import async_requests
from pprint import pprint

temp_path = os.path.join(os.path.dirname(__file__), "temp")

def download(m3u8_file, output):
	_clear_temp()
	playlist = m3u8.load(m3u8_file)
	chunks = _get_chunks(playlist)
	_save_chunks(chunks, playlist)
	_concat_chunks(playlist, output)
	_clear_temp()

def _get_chunks(playlist):
	urls = []
	for uri in playlist.files:
		if urlparse(uri).scheme == '':
			uri = playlist._base_uri + uri
		urls.append(uri)
	results = async_requests.get(urls)
	return results

def _save_chunks(chunks, playlist):
	for i, uri in enumerate(playlist.files):
		for chunk in chunks:
			if uri in chunk._url:
				with open(f'{temp_path}/{i}.ts', 'wb') as f:
					f.write(chunk._body)

def _concat_chunks(playlist, output):
	with open(f'{temp_path}/filelist.txt', 'w') as f:
		for file in playlist.files:
			path_to_file = os.path.join(temp_path, urlparse(file).path.split('/')[-1]).replace('\\', '/')
			f.write(f'file {path_to_file}\n')
	if not os.path.exists(os.path.dirname(output)):
		os.mkdir(os.path.dirname(output))
	cmd = f'ffmpeg -y -f concat -safe 0 -i {temp_path}/filelist.txt -c copy "{output}"'
	subprocess.run(cmd, shell=True)

def _clear_temp():
	shutil.rmtree(temp_path, ignore_errors=True)
	os.mkdir(temp_path)
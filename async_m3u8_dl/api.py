import m3u8
from urllib.parse import urlparse
from glob import glob
import os
import subprocess
import shutil
import async_requests
from pprint import pprint

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
	for chunk in chunks:
		for uri in playlist.files:
			file = uri.split('/')[-1]
			if file in str(chunk._url):
				break
		with open(f'async_m3u8_dl/temp/{file}', 'wb') as f:
			f.write(chunk._body)

def _concat_chunks(playlist, output):
	with open('async_m3u8_dl/temp/filelist.txt', 'w') as f:
		for file in playlist.files:
			path_to_file = os.path.join(os.getcwd(), 'async_m3u8_dl/temp\\'+file.split('/')[-1]).replace('\\', '/')
			f.write(f'file {path_to_file}\n')
	cmd = f'ffmpeg -y -f concat -safe 0 -i async_m3u8_dl/temp/filelist.txt -c copy "{output}"'
	subprocess.run(cmd, shell=True)

def _clear_temp():
	shutil.rmtree('async_m3u8_dl/temp')
	os.mkdir('async_m3u8_dl/temp')
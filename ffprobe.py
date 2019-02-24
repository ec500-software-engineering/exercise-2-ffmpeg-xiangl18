import subprocess
import json
from pathlib import Path


def ffprobe_sync(filein: Path) -> dict:
	""" get media metadata """
	meta_json = subprocess.check_output(['ffprobe', '-v', 'warning', '-print_format',
'json', '-show_streams', '-show_format', filein], universal_newlines=True)
	# file = open('test.json{}', 'w', encoding='utf-8')
	# json.dump(meta_json, file, ensure_ascii=False)
	return json.loads(meta_json)



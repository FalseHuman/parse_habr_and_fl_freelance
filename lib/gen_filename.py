import re


def gen_filename_by_url(url: str, filetype: str) -> str:
    filename = url.replace('http://', '').replace('https://', '').replace('/', '_') + f'.{filetype}'
    return filename
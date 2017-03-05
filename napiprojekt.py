"""
Simple script for taget download of subtitles from napiprojekt.pl

It's based on script i found somewhere over the net,
but can't find it rigt now to provide link. If you are the
author of original script, let me know.

It's modified to use python3

Usage
python napiprojekt.py subs_id_from_the_webpage > subs_name.txt

ex.
$ python napiprojekt.py e79975aa41dfecf52b81ac8231f4abde > napisy.txt

Reqs:
* Python 3.x
* pylzma (py7zlib)
* rquests
"""

from io import BytesIO
import base64
import sys
import xml.etree.ElementTree as ET

from py7zlib import Archive7z
import requests


response = requests.post(
    url='http://www.napiprojekt.pl/api/api-napiprojekt3.php',
    data=dict(
        downloaded_subtitles_id=sys.argv[1],
        downloaded_subtitles_lang='PL',
        client='NapiProjekt',
        mode=17,
    )
)
parser = ET.XML(response.content)
content = parser.find('subtitles').find('content').text

decoded = base64.b64decode(content)
file_like = BytesIO(decoded)

archive = Archive7z(file_like, password='iBlm8NTigvru0Jr0')
member = archive.getmember(0)

text_file = open("subs.txt", "wb")
text_file.write(member.read().decode('cp1250').encode('utf-8'))
text_file.close()

print(member.read().decode('unicode_escape'))

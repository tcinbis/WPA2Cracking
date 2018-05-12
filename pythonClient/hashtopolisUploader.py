import requests
import base64

ENCODING = 'utf-8'

class HashToPolisUploader:

    def __init__(self):
        self.hashtopolisUrl = 'http://ec2-18-191-5-181.us-east-2.compute.amazonaws.com/hashtopolis/src/api/client.php'

    def upload(self, captureFileName):
        with open(captureFileName, "rb") as capture_file:
            byte_content = base64.b64encode(capture_file.read())

        test_string = byte_content.decode(ENCODING)

        payload = {'action': 'createTask', 'cmdline': '#HL# -a 3 ?u?u?u?u?u?u?u?u','hashlistname':'test','capdata':test_string}

        r = requests.post(self.hashtopolisUrl,json=payload)

        print(r.url)
        print(r.status_code)
        print(r.headers)
        print(r.content)
        print(r.text)
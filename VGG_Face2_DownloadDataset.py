import requests
import os
import sys

LOGIN_URL = "http://zeus.robots.ox.ac.uk/vgg_face2/login/"
FILE_URL = "http://zeus.robots.ox.ac.uk/vgg_face2/get_file?fname=vggface2_test.tar.gz"
# print('Please enter your VGG Face 2 credentials:')
# user_string = input('    User: ')
# password_string = getpass.getpass(prompt='    Password: ')

payload = {
    'username': 'mgheisar',
    'password': '2508mgh2508'
}

session = requests.session()
r = session.get(LOGIN_URL)

if 'csrftoken' in session.cookies:
    csrftoken = session.cookies['csrftoken']
elif 'csrf' in session.cookies:
    csrftoken = session.cookies['csrf']
else:
    raise ValueError("Unable to locate CSRF token.")

payload['csrfmiddlewaretoken'] = csrftoken

r = session.post(LOGIN_URL, data=payload)

filename = FILE_URL.split('=')[-1]

with open(os.path.join('/nfs/nas4/marzieh/marzieh/VGG_Face2/', filename), 'wb') as f:
    print(f"Downloading file: `{filename}`")
    r = session.get(FILE_URL, data=payload, stream=True)
    bytes_written = 0
    for data in r.iter_content(chunk_size=4096):
        f.write(data)
        bytes_written += len(data)
        MiB = bytes_written / (1024 * 1024)
        sys.stdout.write(f"\r{MiB:0.2f} MiB downloaded...")
        sys.stdout.flush()

print("\nDone.")

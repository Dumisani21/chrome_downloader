import argparse
import requests
import os
from tqdm import tqdm

OWENER_OF_THE_GITHUB_REPOSITORY = 'webnicer'
NAME_OF_THE_GITHUB_REPOSITORY = 'chrome-downloads'
PATH_TO_THE_FILE_WITHIN_THE_REPOSITORY = 'x64.deb'


def list_files(owner, repo, path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url)
    if response.status_code == 200:
        contents = response.json()
        for item in contents:
            if item['type'] == 'file':
                print(f'File: {item["name"]}')
            elif item['type'] == 'dir':
                print(f'Directory: {item["name"]}')

def download_file(owner, repo, path, filename):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}/{filename}'
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        if 'download_url' in content:
            download_url = content['download_url']
            # Extract the filename from the path
            filename = os.path.basename(f"{path}/{filename}")
            print(f'Downloading {filename}')
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                with open(filename, 'wb') as f, tqdm(
                    desc=f'Downloading {filename}', total=total_size, unit='B', unit_scale=True, unit_divisor=1024
                ) as progress_bar:
                    for data in response.iter_content(block_size):
                        f.write(data)
                        progress_bar.update(len(data))
                print(f'Downloaded {filename}')
            else:
                print(f'Failed to download {filename}. Status code: {response.status_code}')
        else:
            print(f'Download URL not found for {path}')
    else:
        print(f'File not found: {filename}')

def main():
    parser = argparse.ArgumentParser(description='GitHub Repository File Downloader')
    parser.add_argument('--list', action='store_true', help='List files and directories in the specified folder')
    parser.add_argument('--file', required=False, help='Name of the file to download')
    parser.add_argument('--download', action='store_true', help='Download the specified file')

    args = parser.parse_args()

    if args.list:
        list_files(OWENER_OF_THE_GITHUB_REPOSITORY, NAME_OF_THE_GITHUB_REPOSITORY, PATH_TO_THE_FILE_WITHIN_THE_REPOSITORY)
    elif args.download:
        if not args.file:
            parser.error("--file is required when using --download.")
        download_file(OWENER_OF_THE_GITHUB_REPOSITORY, NAME_OF_THE_GITHUB_REPOSITORY, PATH_TO_THE_FILE_WITHIN_THE_REPOSITORY, args.file)

if __name__ == "__main__":
    main()
# Chrome version downloader

This Python script allows you to list files and download specific chrome versions from webnicer's github repo which holds all chrome versions. It only works with debian based linux

## Usage

### List Files

To list all chrome versions

```shell
python chrome_version.py --list
```

### Download a File

To download a specific file from the GitHub repository, use the following command, replacing `file_name` with the name of the file you want to download:

```shell
python chrome_version.py --download --file file_name
```

## Requirements

- Python 3
- Install the required libraries using the following command:

```shell
pip install requests tqdm #if not installed
```

import os


def get_latest_filetag(dir_path):
    """get the number of latest configuration file"""

    dir_size = (len(os.listdir(dir_path)))
    file_tag = int(dir_size)
    if file_tag < 10:
        file_tag = str("0" + str(file_tag))
    return file_tag

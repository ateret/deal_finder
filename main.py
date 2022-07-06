import csv
import json
import os
import pathlib
import time

import feedparser


def create_directory(name: str) -> bytes | str:
    """
    Creates a directory.
    Returns path to this directory
    """
    # Location of py.file this method is in
    # @TODO maybe change it to dynamic/user defined location
    py_file_location = os.path.join(pathlib.Path(__file__).parent.resolve())

    # Checks if directory exists, creates it if not
    if not os.path.isdir(os.path.join(py_file_location, name)):
        try:
            print(f'{name} directory created')
            os.mkdir(os.path.join(py_file_location, name))
        except OSError as err:
            print(f'Error creating {name} directory: \n{err}')

    return os.path.join(py_file_location, name)


def get_undesired_keys() -> list:
    """
    This method either gets a list of undesired RSS keys,
    from config/undesired_keywords.csv or creates that file
    with default undesired keys
    """
    # Sets path to be used later. py_file_location is a location of this py.file
    # @TODO maybe change it to dynamic/user defined location
    py_file_location = os.path.join(pathlib.Path(__file__).parent.resolve())
    default_undesired_keys = ['published', 'guidislink', 'base', 'media_content', 'scheme', 'width', 'height']
    undesired_keys_csv = os.path.join(py_file_location, 'config', 'undesired_keywords.csv')

    # If this file and its directory doesn't exists, creates it
    if not os.path.isdir(os.path.join(py_file_location, 'config')):
        create_directory('config')

    if not os.path.isfile(undesired_keys_csv):
        with open(undesired_keys_csv, 'wt', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(default_undesired_keys)

    # Opens undesired_keywords.csv
    with open(undesired_keys_csv, 'r', newline='') as f:
        csv_reader = csv.reader(f)
        tmp_list = list(csv_reader)
        undesired_keys = tmp_list[0]

    return undesired_keys


def list_of_dicts_to_dict(l: list) -> dict:
    """
    Simple method that creates dictionaries from lists.
    This makes raw RSS data easier to read and modify later
    """
    d = {}
    tmp = []

    # Checks if list is a list of dictionaries, and list itself
    if isinstance(l, list):
        for x in range(len(l)):
            if not isinstance(l[x], list) and isinstance(l[x], dict):
                tmp.append(l[x])

            elif isinstance(l[x], list):
                d.list_of_dicts_to_dict(l[x])
            elif not isinstance(l[x], dict):
                print(f'{l[x]} is not a list of dictionaries')
    else:
        raise TypeError(f'{l} is not a list')

    d = dict.fromkeys(range(len(l)), tmp)
    return d


def dict_clean_bad_keys(important_data: dict, undesired_keys: list) -> dict:
    important_data = dict(important_data)
    copied_data = important_data.copy()

    for key, val in important_data.items():

        # Deletes the key if it's on a list of undesired keys
        if key in undesired_keys:
            # print(f'Deleting {key}')
            copied_data.pop(key)

        # If value is a list of dictionaries,  converts it into a dict, recursively
        if isinstance(val, list):
            list_of_dicts_to_dict(val)

        # If value is a dict, run this method again, recursively
        if isinstance(val, dict):
            copied_data[key] = dict_clean_bad_keys(val, undesired_keys)

    return copied_data


def save_rss_data(rss_data: feedparser.util.FeedParserDict, name: str):
    """
    Saves feedparser dictionary in json file with given name and "_data" suffix,
    or appends new entries into existing dictionary, omitting duplicates
    """

    # Creates paths to be used later. py_file_location is a location of this py.file
    data_json_filename = os.path.join(create_directory('data'), name + '_data.json')
    post_counter = len(rss_data.entries)
    undesired_keys = get_undesired_keys()


    print(f'Deleting undesired keys from RSS data \nUndesired keys: {undesired_keys} ')
    # Checks if file exists, to see if it needs to append or create
    if os.path.isfile(data_json_filename):
        try:
            with open(data_json_filename, 'r', encoding="utf-8") as f:
                # Loads new data to append new entries to
                data = json.load(f)

                # Saving id of existing entries, to exclude duplicates later
                id_list = []
                for x in range(len(data)):
                    id_list.append(data[x].get('id'))

                # Appending new post to data dictionary, if they are not a duplicate
                for post in range(post_counter):

                    post_content = dict_clean_bad_keys(dict(rss_data.entries[post]), get_undesired_keys())
                    if post_content['id'] not in id_list:
                        data.append(post_content)
                        print(f'Appended new post: "{post_content["title"]}" to .json file!')
                        id_list.append(post_content['id'])

        except OSError as err:
            print(f'Error occurred while reading a file: {err}')

        # Dumps new dictionary into json file
        try:
            with open(data_json_filename, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as err:
            print(f'Error occurred while saving a file: {err}')
    else:

        # Creates json file in 'data' directory
        try:
            with open(data_json_filename, 'at', encoding="utf-8") as f:
                json.dump(rss_data.entries, f, ensure_ascii=False, indent=4)
        except OSError as err:
            print(err)
    print(rss_data.feed.title + ' RSS data saved in ' + data_json_filename)
    return


def print_rss_data(rss_data: feedparser.util.FeedParserDict) -> dict:
    # @ TODO Redo this entire method
    post_counter = len(rss_data.entries)
    print('Number of Posts: ', post_counter)
    date_format = '%x (%a)'
    time_format = '%X'
    for post in range(post_counter, 0, -1):
        post_content = rss_data.entries[post - 1]

        print('NR:' + str(post))
        print('Title :', post_content.title)
        print('Link: ', post_content.link)
        print('Updated: ', time.strftime(date_format, post_content.updated_parsed))
        print('Time: ', time.strftime(time_format, post_content.updated_parsed))
        print("-" * 100)

    return





if __name__ == "__main__":
    pepper_rss_data_all = feedparser.parse('HTTPS://pepper.pl/rss/wszystkie')
    save_rss_data(pepper_rss_data_all, 'pepper_all')

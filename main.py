import json
import os
import pathlib
import time
import csv

import feedparser

def get_undesired_keys() -> list:

    # Sets path to be used later. py_file_location is a location of this py.file
    # @TODO maybe change it to dynamic/user defined location
    py_file_location = os.path.join(pathlib.Path(__file__).parent.resolve())

    undesired_keys_csv = os.path.join(py_file_location, 'config', 'undesired_keywords.csv')
    undesired_keys = ['published', 'guidislink', 'base', 'media_content', 'scheme']

    if not os.path.isdir(os.path.join(py_file_location, 'config')):
        create_directory('config')

    if not os.path.isfile(undesired_keys_csv):
        with open(undesired_keys_csv, 'wt', newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(undesired_keys)
    else:
        with open(undesired_keys_csv, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            tmp_list = list(csv_reader)
            undesired_keys = tmp_list[0]

    print(undesired_keys)
    return undesired_keys

def list_to_dict(l: list) -> dict:
    d = {}
    if isinstance(l, list):
        for x in range(len(l)):
            if not isinstance(val[x], list):
                # @TODO make it work with lists with more then one entry
                print(val)
                copied_data[key] = get_important_data(val[0], undesired_keys)
    else:
        raise TypeError(f'{l} is not a list')
    return d


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


def save_rss_data(rss_data: feedparser.util.FeedParserDict, name: str):
    """
    Saves feedparser dictionary in json file with given name and "_data" suffix,
    or appends new entries into existing dictionary, omitting duplicates
    """

    # Creates paths to be used later. py_file_location is a location of this py.file
    data_json_filename = os.path.join(create_directory('data'), name + '_data.json')
    post_counter = len(rss_data.entries)

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

                    post_content = get_important_data(dict(rss_data.entries[post]), get_undesired_keys())
                    if post_content['id'] not in id_list:
                        data.append(post_content)
                        print('Appended new post to .json file!')
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


def get_important_data(important_data: dict, undesired_keys: list) -> dict:
    important_data = dict(important_data)
    copied_data = important_data.copy()

    for key, val in important_data.items():

        # Deletes the key if it's on a list of undesired keys
        if key in undesired_keys:
            print(f'Deleting {key}')
            copied_data.pop(key)

        # If value is a list, converts it into a dict
        if isinstance(val, list):
            # @TODO make it work with lists with more then one entry
            print(val)
            copied_data[key] = get_important_data(val[0], undesired_keys)

        # If value is a dict, run this method recursively
        if isinstance(val, dict):
            copied_data[key] = get_important_data(val, undesired_keys)

    return copied_data


if __name__ == "__main__":
    pepper_rss_data_all = feedparser.parse('HTTPS://pepper.pl/rss/wszystkie')
    save_rss_data(pepper_rss_data_all, 'pepper_all')

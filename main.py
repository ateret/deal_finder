import json
import os
import pathlib
import time

import feedparser
import requests


def create_data_directory() -> os.PathLike:
    py_file_location = os.path.join(pathlib.Path(__file__).parent.resolve())
    # Creates 'data' directory, as a location to store all json data files
    if os.path.isdir(os.path.join(py_file_location, 'data')):
        pass
    else:
        try:
            print('"data" directory created')
            os.mkdir(os.path.join(py_file_location, 'data'))
            return py_file_location
        except OSError as err:
            print(f'Error creating "data" directory: \n{err}')
    return py_file_location


# Saves feedparser dictionary in json file with given name and "_data" suffix
def save_rss_data(rss_data: feedparser.util.FeedParserDict, name: str):
    # Creates paths used to be used later. py_file_location is a location of this py.file

    data_json_filename = os.path.join(create_data_directory(), 'data', name + '_data.json')
    post_counter = len(rss_data.entries)

    # Checks if file exists, to see if it needs to append or create
    if os.path.isfile(data_json_filename):
        try:
            with open(data_json_filename, 'r', encoding="utf-8") as f:
                # Loads new data to append new entries to
                data = json.load(f)
                for post in range(post_counter):
                    post_content = dict(rss_data.entries[post])
                    print(type(data[0]))
                    data.append(post_content)
                    print('Appended!')

        except Exception as err:
            print(f'Error occured while reading a file: {err}')

        try:
            with open(data_json_filename, 'w', encoding="utf-8") as f:
                # Dumps new data
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as err:
            print(f'Error occured while saving a file: {err}')
    else:
        # Saves json data file in 'data' directory
        try:
            with open(data_json_filename, 'at', encoding="utf-8") as f:
                json.dump(rss_data.entries, f, ensure_ascii=False, indent=4)
        except Exception as err:
            print(err)
        print(rss_data.feed.title + ' RSS data saved in ' + data_json_filename)
        return


def print_rss_data(rss_data: feedparser.util.FeedParserDict) -> dict:
    post_counter = len(rss_data.entries)
    print('Number of Posts: ', post_counter)
    date_format = '%x (%a)'
    time_format = '%X'
    for post in range(post_counter, 0, -1):
        post_content = rss_data.entries[post - 1]

        print('NR:' + str(post))
        print('Title :', post_content.title)
        print('Link: ', post_content.link)
        print('Updated: ', time.strftime(date_format, (post_content.updated_parsed)))
        print('Time: ', time.strftime(time_format, (post_content.updated_parsed)))
        print("-" * 100)

    return


def get_data(url: str) -> dict:
    server_response = requests.get(url)
    print(server_response)

    return server_response


# pepper_rss_data_new = feedparser.parse('HTTPS://pepper.pl/rss/nowe')
# pepper_rss_data_hot = feedparser.parse('HTTPS://pepper.pl/rss/hot')
pepper_rss_data_all = feedparser.parse('HTTPS://pepper.pl/rss/wszystkie')
# print_rss_data(pepper_rss_data_all)
# save_rss_data(pepper_rss_data_new, 'pepper_new')
# save_rss_data(pepper_rss_data_hot, 'pepper_hot')
save_rss_data(pepper_rss_data_all, 'pepper_all')

# pepper_rss_hot = feedparser.parse('HTTPS://pepper.pl/rss/hot')


# print(pepper_rss_hot.feed)
# print(type(pepper_rss_hot.entries[0]))

# data_json_filename = (os.path.join(pathlib.Path(__file__).parent.resolve(), 'data.json'))
# with open(data_json_filename, 'w') as f:
#     json.dump(pepper_rss_hot.entries[0], f, indent=4)

# baseurl = 'https://rickandmortyapi.com/api/'
# endpoint = 'character'
#
# pepperURL = 'https://www.pepper.pl'
# p_endpoint = '/thread/hottest'
#
# data = get_data(pepperURL)
# print(data.text)


# nr_of_pages = data['info']['pages']
#
# print(nr_of_pages)
# print(data['results'][0]['name'])

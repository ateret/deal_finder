import requests
import feedparser
import time


def get_rss_data (rss_source: feedparser.util.FeedParserDict) -> dict :
    post_counter = len(rss_source.entries)
    date_format = '%x (%a)'
    time_format = '%X'
    for post in range(post_counter, 0, -1):
        post_content = rss_source.entries[post - 1]

        print("-" * 100)
        print('NR:' + str(post))
        print('Title :', post_content.title)
        print('Link: ', post_content.link)
        print('Updated: ', time.strftime(date_format , (post_content.updated_parsed)))
        print('Time: ', time.strftime(time_format , (post_content.updated_parsed)))


    return

def get_data(url: str) -> dict:
    server_response = requests.get(url)
    print(server_response)

    return server_response

#
# pepper_rss_new = feedparser.parse('HTTPS://pepper.pl/rss/nowe')
pepper_rss_hot = feedparser.parse('HTTPS://pepper.pl/rss/hot')


# get_rss_data(pepper_rss_new)
get_rss_data(pepper_rss_hot)


print(type(pepper_rss_hot))



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



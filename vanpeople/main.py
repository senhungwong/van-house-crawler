# -*- coding: utf-8 -*-
from url_builder import main_page
from requester import request
from list_parser import parse_list
from post_parser import parse_post
from json import dumps
from time import time


def get_vanpeople_posts(page_numbers):
    """
    get vanpeople's posts

    :param page_numbers: List[int]
    :return: Dict
    """

    # init posts list
    posts = []

    # loop through each page
    for page_number in page_numbers:
        # get all posts' link in the page
        post_links = parse_list(request(main_page(page_number)))

        # parse content in each post
        for post_link in post_links:
            # assign post link
            post = {'link': post_link}

            # assign other fields to post
            post.update(parse_post(request(post_link)))

            # push post into posts list
            posts.append(post)

    return posts


def store_locally(posts):
    with open('data/vanpeople/' + str(time()) + '.json', 'w') as f:
        f.write(dumps(posts, ensure_ascii=False, sort_keys=True, indent=4))


def transform(post):
    return {
        'title': post['title'],
        'published_date': post['date'],
        'contact_info': {
            'name': post['details']['contact'],
            'telephone': post['details']['telephone'],
            'wechat': post['details']['wechat'],
            'qq': post['details']['qq']
        },
        'location_info': {
            'area': post['details']['area'],
            'address': post['details']['address']
        },
        'description': post['description'],
        'images': post['images'],
        'link': post['link']
    }

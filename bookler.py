#!/usr/bin/python

""" """
import logging

from os import makedirs
from os.path import exists, join

from BeautifulSoup import BeautifulSoup as soup
from requests import get
from shutil import copyfileobj

_logger = logging.getLogger('bookler')
_logger.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)
_stream_handler.setLevel(logging.DEBUG)
_logger.addHandler(_stream_handler)

def _download(url, path):
    """
    :param url:
    :param path:
    :returns:
    """
    response = get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as output:
            response.raw.decode_content = True
            copyfileobj(response.raw, output)
            return True
    return False

class Bookler(object):
    """ """

    def __init__(self, url_builder, image_extractor):
        """ Default constructor.

        :param url_builder: Function to use for building page URL from parameter.
        :param image_extractor: Function to use for extracting image URL from a given page.
        """
        self._url_builder = url_builder
        self._image_extractor = image_extractor
    
    def run(
        self,
        target_directory,
        start_chapter=1,
        start_page=1,
        failure_threshold=2):
        """
        :param target_directory:
        """
        if not exists(target_directory):
            makedirs(target_directory)
        current_chapter = start_chapter
        current_page = start_page
        current_directory = join(target_directory, str(current_chapter))
        if not exists(current_directory):
            makedirs(current_directory)
        failure = 0
        visited = []
        _logger.info('Downloading chapter %s' % current_chapter)
        next_page_url = self._url_builder(current_chapter, current_page)
        while next_page_url is not None:
            response = get(next_page_url)
            if response.status_code == 200:
                html = soup(response.text)
                image_url = self._image_extractor(html)
                if image_url is None or image_url in visited:
                    failure += 1
                else:
                    path = join(current_directory, str(current_page)) + '.jpg'
                    success = _download(image_url, path)
                    if success:
                        failure = 0
                        visited.append(image_url)
                    else:
                        _logger.warn('Failed downloading page %s' % current_page)
                        failure += 1
            else:
                failure += 1
                _logger.warn('Failed downloading page %s' % current_page)
            if failure == 0:
                current_page += 1
            if failure > failure_threshold:
                current_chapter += 1
                current_page = start_page
                visited = []
                current_directory = join(target_directory, str(current_chapter))
                if not exists(current_directory):
                    makedirs(current_directory)
                _logger.info('Downloading chapter %s' % current_chapter)
            next_page_url = self._url_builder(current_chapter, current_page)

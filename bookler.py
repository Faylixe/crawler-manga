#!/usr/bin/python

""" """
import logging

from os import makedirs
from os.path import exists, join

from BeautifulSoup import BeautifulSoup as soup
from requests import get
from shutil import copyfileobj

# TODO : Consider use specific logger configuration.
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S')

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


class Mode:
    """ """

    """ """
    VOLUME = 1

    """ """
    CHAPTER = 2

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
        target_directory,
        mode=Mode.VOLUME,
        start_parameter=(1, 1, 1),
        failure_threshold=2):
        """
        :param target_directory:
        """
        if not exists(target_directory):
            makedirs(target_directory)
        current_volume = start_parameter[0]
        current_chapter = start_parameter[1]
        current_page = start_parameter[2]
        failure = 0
        next_page_url = self._url_builder(current_volume, current_chapter, current_page)
        while next_page_url is not None:
            response = get(next_page_url)
	        if response.status_code == 200:
                html = soup(response.text)
                image_url = self._image_extractor(html)
                # TODO : Build path.
                success = _download(image_url, None)
                if success:
                    failure = 0
                else:
                    failure += 1
            else:
                failure += 1
            if failure > failure_threshold:
                if mode == Mode.VOLUME:
                    current_volume += 1
                else:
                    current_chapter += 1
            next_page_url = self._url_builder(current_volume, current_chapter, current_page)

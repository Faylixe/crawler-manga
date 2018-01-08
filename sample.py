#!/usr/bin/python

from bookler import Bookler

def build_url(chapter, page):
    """ """
    return 'http://www.japscan.com/lecture-en-ligne/love-hina/volume-%s/%s.html' % (chapter, page)

def get_image_url(soup):
    """ """
    img = soup.find('img', {'id': 'image'})
    if img is not None:
        for attribute in img.attrs:
            if attribute[0] == 'src':
                return attribute[1]
    return None

if __name__ == '__main__':
    bookler = Bookler(build_url, get_image_url)
    bookler.run('/Users/fv/Books/Love Hina')

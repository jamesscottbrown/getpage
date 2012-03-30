#!/usr/bin/env python
""" getpage - A Program to fetch a webpage and save it in a single file in MIME-HTML (RFC 2557) format.

    MIME-HTML makes it possible to save a webpage complete with all needed ressources
    to render, including stylesheets, images or scripts right into a single file.

"""
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import urllib2
import sys
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import quopri
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser


class PageGetter():
    """ Get a webpage, and save it in a single file  the URL of a HTML Page. Returns a MIME-HTML representation of that page in a single File.

            There are a number of document formats
            consisting of a root resource and a number of distinct
            subsidiary resources referenced by URIs within that root resource.

            There is an obvious need to be able to save such multi-resource
            documents in a single file.

    """

    _title = ''
    _msg = None
    _urls = {}

    def __init__(self):

        self._read_parameters()

        self._msg = MIMEMultipart('related')
        self._msg.preamble = 'This is a multi-part message in MIME format.\n'


    def add_html(self, url):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """
        self._base_url=url
        response = urllib2.urlopen(url)
        html = response.read()
        print html
        htmltxt = MIMEText(quopri.encodestring(html), 'html')
        htmltxt.add_header('Content-Transfer-Encoding', 'quoted-printable')
        htmltxt.add_header('Content-Location', url)

        self._msg.attach(htmltxt)

        soup = BeautifulSoup(html)
        self._title = quopri.encodestring(soup.head.title.string)

        images = soup.findAll('img')
        for img in images:
            url = self._base_url + img['src']
            if not url in self._urls:
                self._urls[url] = url
                self._add_image(url)

        links = soup.findAll('link', type='text/css')
        for link in links:
            #self.add_css(link['href'])
            pass

        scripts = soup.findAll('script')
        for script in scripts:
            #self.add_script(script)
            pass

        iframes = soup.findAll('iframe')
        for iframe in iframes:
            #self.add_iframe(iframe)
            pass

    def _add_css(self, url):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """

        response = urllib2.urlopen(url)
        html = response.read()

        htmltxt =MIMEText(quopri.encodestring(html), 'html')
        htmltxt.add_header('Content-Transfer-Encoding', 'quoted-printable')
        htmltxt.add_header('Content-Location', url)

    def _add_image(self, url):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """

        response = urllib2.urlopen(url)
        img = response.read()

        # TODO: Expand to more MIME subtypes
        if url.lower().endswith('jpg'):
            mime_type='jpeg'
        elif url.lower().endswith('png'):
            mime_type='png'
        elif url.lower().endswith('gif'):
            mime_type='gif'
        else:
            image_type = 'test'


        html_image =MIMEImage(img, mime_type)
        html_image.add_header('Content-Location', url)


        self._msg.attach(html_image)


    def _add_script(self, url):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """

        response = urllib2.urlopen(url)
        html = response.read()

        htmltxt =MIMEText(quopri.encodestring(html), 'html')
        htmltxt.add_header('Content-Transfer-Encoding', 'quoted-printable')
        htmltxt.add_header('Content-Location', url)

    def _add_iframe(self, url):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """

        response = urllib2.urlopen(url)
        html = response.read()

        htmltxt =MIMEText(quopri.encodestring(html), 'html')

        htmltxt.add_header('Content-Transfer-Encoding', 'quoted-printable')
        htmltxt.add_header('Content-Location', url)

    def _read_parameters(self):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """

        parser = OptionParser()

        parser.add_option("-f", "--file", dest="filename",
                          help="write report to FILE", metavar="FILE")
        parser.add_option("-d", "--debug",
                          action="store_false", dest="verbose", default=True,
                          help="print debug and verbose status messages to stdout")
        parser.add_option("-v", "--verbose",
                          action="store_false", dest="verbose", default=True,
                          help="print verbose status messages to stdout")
        parser.add_option("-q", "--quiet",
                          action="store_false", dest="verbose", default=True,
                          help="don't print status messages to stdout")

        (options, args) = parser.parse_args()


    def retrieve(self):
        """ Takes the URL of a HTML Page. Returns a MIME encapsulated form of the HTML Code.

            If the HTML page itself links to images, scripts or stylesheet it calls the matching
            encapsulation Methods for them recursivly

        """

        self.add_html('http://www.python.org',)

        f=open(self._title +'.mht', 'w')
        f.write('From: <Saved by getpage 0.1>\r\n')
        f.write('Subject: ' + self._title + '\r\n')
        f.write('Date: Fri, 16 Mar 2012 11:13:53 +0100\r\n')
        f.write(self._msg.as_string())
        f.close


if __name__ == '__main__':
    page = PageGetter()
    page.retrieve()

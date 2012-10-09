#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from urlparse import urlparse
from urllib import urlencode
from unittestzero import Assert

from base import Base


@pytest.mark.skip_selenium
@pytest.mark.nondestructive
class TestRedirects(Base):

    @pytest.mark.parametrize('url', ["http://download.allizom.org/", "https://download.allizom.org/"])
    def test_that_checks_redirect_using_incorrect_query_values(self, url):
        param = {
            'product': 'firefox-16.0b6',
            'lang': 'kitty_language',
            'os': 'stella'
        }

        response = self._head_request(url, params=param)

        Assert.equal(response.status_code, requests.codes.not_found)

        parsed_url = urlparse(response.url)
        Assert.equal(parsed_url.scheme, 'https')
        Assert.equal(parsed_url.netloc, urlparse(url).netloc)
        Assert.equal(parsed_url.query, urlencode(param))

    def test_stub_installer_redirect_for_en_us_and_win(self, mozwebqa):
        url = mozwebqa.base_url
        param = {
            'product': 'firefox-16.0b6',
            'lang': 'en-US',
            'os': 'win'
        }

        response = self._head_request(url, params=param)

        parsed_url = urlparse(response.url)

        Assert.equal(response.status_code, requests.codes.ok, 'Failed on %s \nUsing %s' %(url, param))
        Assert.equal(parsed_url.scheme, 'https', 'Failed on %s \nUsing %s' %(url, param))
        Assert.equal(parsed_url.netloc, 'download-installer.cdn.mozilla.net','Failed on %s \nUsing %s' %(url, param))

#!/usr/bin/env python

agent_name = "password_test.py"
agent_version = "0.1"
# this script doesn't submit anything (empty dict)
# so testing this on live server (with live passwords) is okay.
musicbrainz_server = "test.musicbrainz.org"
#musicbrainz_server = "musicbrainz.org"

import sys
import getpass

import musicbrainzngs
from musicbrainzngs import AuthenticationError, ResponseError, WebServiceError

try:
    user_input = raw_input
except NameError:
    user_input = input


class WebService2():
    """A web service wrapper that asks for a password when first needed.

    This uses musicbrainzngs as a wrapper itself.
    """

    def __init__(self, username=None, password=None):
        self.auth = False
        self.username = username
        self.password = password
        musicbrainzngs.set_hostname(musicbrainz_server)
        musicbrainzngs.set_useragent(agent_name, agent_version,
                "http://github.com/JonnyJD/musicbrainz-isrcsubmit")

    def authenticate(self):
        """Sets the password if not set already
        """
        if not self.auth:
            if self.username is None:
                print("")
                sys.stdout.write("Please input your MusicBrainz username: ")
                self.username = user_input()
            if self.password is None:
                self.password = getpass.getpass(
                                    "Please input your MusicBrainz password: ")
                print("")
            musicbrainzngs.auth(self.username, self.password)
            self.auth = True

    def submit_isrcs(self):
        try:
            self.authenticate()
            musicbrainzngs.submit_isrcs(dict())
        except AuthenticationError as err:
            sys.exit("Invalid credentials: %s" % err)
        except WebServiceError as err:
            sys.exit("Couldn't send: %s" % err)
        else:
            print("Successfully submitted.")


if __name__ == "__main__":
    # use test user with standard test server password
    ws2 = WebService2("test", "mb")
    ws2.submit_isrcs()

# vim:set shiftwidth=4 smarttab expandtab:

# vim: set ts=4 sw=4 et fileencoding=utf-8:

from urllib.parse import quote
import json
import main
import unittest


POSTMATES_HQ = '425 Market St #8, San Francisco, CA 94105'


class AppTestCase(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_geocode_for_known(self):
        '''Validates that geocoding with the mock requester works through the
        HTTP stack'''

        url = f'/location/geocode?address={quote(POSTMATES_HQ)}'
        data = json.loads(self.app.get(url).data)

        self.assertAlmostEqual(37.7913035, data['lat'])
        self.assertAlmostEqual(-122.3988535, data['lon'])

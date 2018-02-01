# vim: set ts=4 sw=4 et fileencoding=utf-8:

from location import *
from os import path
import json
import unittest


RUN_LIVE_TESTS = False

POSTMATES_HQ = '425 Market St #8, San Francisco, CA 94105'
POSTMATES_HQ_LAT = 37.7913035
POSTMATES_HQ_LON = -122.3988535


class GeocoderTestCase(unittest.TestCase):

    def setUp(self):
        self.geocoder = Geocoder()

    def test_resolver_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            self.geocoder.resolve('foo')

    def test_validate_address_with_None(self):
        with self.assertRaises(Geocoder.Error):
            self.geocoder.validate_address(None)

    def test_validate_address_with_empty_string(self):
        with self.assertRaises(Geocoder.Error):
            self.geocoder.validate_address('  ')

    def test_validate_address_with_content(self):
        self.assertEqual('foo', self.geocoder.validate_address('foo'))


class MockGeocoderTestCase(unittest.TestCase):

    def setUp(self):
        self.geocoder = MockGeocoder()

    def test_resolve_throws_on_empty_address(self):
        with self.assertRaises(Geocoder.Error):
            self.geocoder.resolve('')

    def test_resolve(self):
        result = self.geocoder.resolve(POSTMATES_HQ)
        self.assertEqual(POSTMATES_HQ_LAT, result.lat)
        self.assertEqual(POSTMATES_HQ_LON, result.lon)


class GoogleGeocoderTestCase(unittest.TestCase):

    TEST_API_KEY = '{GOOGLE_API_KEY}'

    def setUp(self):
        self.geocoder = GoogleGeocoder(self.TEST_API_KEY)

    def test_parse_offline_success(self):
        with open(path.join(path.dirname(__file__),
                            'assets', 'google_geocoder.json'), 'r') as f:
            payload = f.read()

        result = self.geocoder._GoogleGeocoder__parse(payload)
        self.assertAlmostEqual(37.7913035, result.lat)
        self.assertAlmostEqual(-122.3988535, result.lon)

    def test_parse_offline_no_results(self):
        with open(path.join(path.dirname(__file__),
                            'assets',
                            'google_geocoder_no_results.json'), 'r') as f:
            payload = f.read()

        result = self.geocoder._GoogleGeocoder__parse(payload)
        self.assertIsNone(result)

    @unittest.skipUnless(RUN_LIVE_TESTS, 'Performs a live call')
    def test_resolve_live(self):
        result = self.geocoder.resolve(POSTMATES_HQ)
        self.assertAlmostEqual(37.7913035, result.lat)
        self.assertAlmostEqual(-122.3988535, result.lon)


class HereGeocoderTestCase(unittest.TestCase):

    TEST_APP_ID = '{HERE_APP_ID}'
    TEST_APP_CODE = '{HERE_APP_CODE}'

    def setUp(self):
        self.geocoder = HereGeocoder(self.TEST_APP_ID, self.TEST_APP_CODE)

    def test_parse_offline_success(self):
        with open(path.join(path.dirname(__file__),
                            'assets', 'here_geocoder.json'), 'r') as f:
            payload = f.read()

        result = self.geocoder._HereGeocoder__parse(payload)
        self.assertAlmostEqual(37.7915599, result.lat)
        self.assertAlmostEqual(-122.3985, result.lon)

    def test_parse_offline_no_results(self):
        with open(path.join(path.dirname(__file__),
                            'assets',
                            'here_geocoder_no_results.json'), 'r') as f:
            payload = f.read()

        result = self.geocoder._HereGeocoder__parse(payload)
        self.assertIsNone(result)

    @unittest.skipUnless(RUN_LIVE_TESTS, 'Performs a live call')
    def test_resolve_live(self):
        result = self.geocoder.resolve(POSTMATES_HQ)
        self.assertAlmostEqual(37.7915599, result.lat)
        self.assertAlmostEqual(-122.3985, result.lon)


class GeocoderDispatcherTestCase(unittest.TestCase):

    def test_mock(self):
        g = GeocoderDispatcher(['Mock'])

        self.assertEqual(1, len(g.geocoders))
        self.assertIsInstance(g.geocoders[0], MockGeocoder)

        result = g.resolve(POSTMATES_HQ)
        self.assertEqual(POSTMATES_HQ_LAT, result.lat)
        self.assertEqual(POSTMATES_HQ_LON, result.lon)

    def test_google_and_here_construction(self):
        g = GeocoderDispatcher(['Google', 'Here'],
                               {'GOOGLE_API_KEY': None,
                                'HERE_APP_ID': None,
                                'HERE_APP_CODE': None})

        self.assertEqual(2, len(g.geocoders))
        self.assertIsInstance(g.geocoders[0], GoogleGeocoder)
        self.assertIsInstance(g.geocoders[1], HereGeocoder)

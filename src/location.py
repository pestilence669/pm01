# vim: set ts=4 sw=4 et fileencoding=utf-8:
'''Geocoder service implementations'''

from urllib.parse import quote
import json
import os
import random
import urllib


class Geocoder:
    '''Geocodes addresses'''

    class Error(Exception):
        def __init__(self, message, code):
            super().__init__(message)
            self.code = code

    class Response:
        '''Geolocation in latitude and longitude'''
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon

        def __str__(self):
            return f'Geocoder.Response({repr(self.lat)}, {repr(self.lon)})'

    def resolve(self, address):
        '''Resolve the geolocation for the given address'''
        raise NotImplementedError

    @staticmethod
    def validate_address(address):
        '''Validate the address

        Given the flexibility of address formatting, the validation here is
        very light. It consists solely on the definition and non-emptiness.

        TODO: Maybe separate this out into an Address type, if needed
        '''
        if address is None or address.strip() == '':
            raise Geocoder.Error('An address is required to geocode', 400)
        else:
            return address


class MockGeocoder(Geocoder):
    '''Mock implementation

    Assumes all addresses are Postmates HQ.
    '''
    def resolve(self, address):
        self.validate_address(address)  # still validate input, even as mock
        return self.Response(37.7913035, -122.3988535)


class GoogleGeocoder(Geocoder):
    '''Leverages the Google Maps API'''

    SERVICE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    def __init__(self, api_key):
        '''Initialize the service with an API key'''
        self.api_key = api_key

    def resolve(self, address):
        self.validate_address(address)

        url = f'{self.SERVICE_URL}?address={quote(address)}&key={self.api_key}'

        with urllib.request.urlopen(url) as response:
            payload = response.read()

        return self.__parse(payload)

    def __parse(self, payload):
        '''Parses the JSON payload of the service response'''
        data = json.loads(payload)

        results = data['results']
        if results:
            location = results[0]['geometry']['location']
            return Geocoder.Response(location['lat'], location['lng'])
        else:
            return None


class HereGeocoder(Geocoder):
    '''Leverages the Here Maps API'''

    SERVICE_URL = 'https://geocoder.cit.api.here.com/6.2/geocode.json'

    def __init__(self, app_id, app_code):
        '''Initialize the service with an app ID & app code'''
        self.app_id = app_id
        self.app_code = app_code

    def resolve(self, address):
        self.validate_address(address)

        url = (f'{self.SERVICE_URL}'
               f'?app_id={self.app_id}'
               f'&app_code={self.app_code}'
               f'&searchtext={quote(address)}')

        with urllib.request.urlopen(url) as response:
            payload = response.read()

        return self.__parse(payload)

    def __parse(self, payload):
        '''Parses the JSON payload of the service response'''
        data = json.loads(payload)

        views = data['Response']['View']

        if not views:
            return None

        resultsView = next(view for view in views
                           if view.get('_type') == 'SearchResultsViewType' or
                           view['ViewId'] == 0)

        results = resultsView['Result']

        if results:
            location = results[0]['Location']['NavigationPosition'][0]
            # TODO: determine what to do with multiple locations & positions
            return Geocoder.Response(location['Latitude'],
                                     location['Longitude'])
        else:
            return None


class GeocoderDispatcher:
    '''Container of Geocoder instances for dispatch'''

    def __init__(self, geocoders, env=os.environ):
        '''Creates a dispatcher and instantiates geocoders by name

        Optionally, you can pass the parameter environment variables as a dict
        for testing and other purposes.

        g = GeocoderDispatcher(['Google', 'Here'], {'GOOGLE_API_KEY': 'FOO'})
        '''
        self.geocoders = []
        self.primary = None

        # dynamically instantiate by name and pass any matching env vars to the
        # constructor. "magic."
        for geocoder in geocoders:
            geocoder_class = globals()[f'{geocoder}Geocoder']
            potential_envs = {k.lower()[len(geocoder) + 1:]: v
                              for k, v in env.items()
                              if k.startswith(f'{geocoder}_'.upper())}
            self.add(geocoder_class(**potential_envs))

    def add(self, geocoder: Geocoder):
        self.geocoders.append(geocoder)
        if self.primary is None:
            self.primary = geocoder

    def resolve(self, address):
        '''Resolve the geolocation for the given address

        Checks against the primary first, then chooses a backup (at random) in
        the event of a failure.

        This can easily be modified to query against all options.
        '''
        plan = [self.primary]

        backups = self.geocoders[1:]
        if backups:
            plan.append(random.choice(backups))

        for resolver in plan:
            result = resolver.resolve(address)
            if result:
                return result

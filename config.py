# vim: set ts=4 sw=4 et fileencoding=utf-8:
'''Contains configuration settings

Secrets & API keys are contained in environment variables / not checked into
source control.
'''


class Default:
    JSONIFY_PRETTYPRINT_REGULAR = False
    GEOCODING_RESOLVERS = ['Google', 'Here']
    TESTING = False


class Production(Default):
    '''Clone of the default settings'''
    pass


class Dev(Default):
    '''Clone of the default settings'''
    GEOCODING_RESOLVERS = ['Mock']


class Test(Default):
    '''Settings for unit testing'''
    GEOCODING_RESOLVERS = ['Mock']
    # TODO: configure integration endpoints / sandbox servers

#!/usr/bin/env python3
from apis.efa import EFA

supported = ('VRR', )

class VRR(EFA):
    name = 'vrr'
    base_url = 'http://app.vrr.de/standard/'
    country = 'de'

    def __init__(self):
        self.ids = {}
        self.raws = {}

def network(name):
    global supported
    if name not in supported:
        raise NameError('Unsupported network: %s' % name)
    return globals()[name]
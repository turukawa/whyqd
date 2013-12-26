import os
from django.contrib.gis.utils import LayerMapping
from whyqd.wiqi.models import Wiqi, Geomap
from django.contrib.auth.models import User

uip = "192.168.0.9"
u = User.objects.all()[0]

world_mapping = {
    'fips' : 'FIPS',
    'iso2' : 'ISO2',
    'iso3' : 'ISO3',
    'un' : 'UN',
    'name' : 'NAME',
    'area' : 'AREA',
    'region' : 'REGION',
    'subregion' : 'SUBREGION',
    'lon' : 'LON',
    'lat' : 'LAT',
    'map_shape' : 'MULTIPOLYGON',
}

world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/TM_WORLD_BORDERS-0.3.shp'))

def run(verbose=True):
    lm = LayerMapping(Geomap, world_shp, world_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)

def connect():
    geomaps = Geomap.objects.all()
    kwargs = {'a': None}
    for g in geomaps:
        wiqi = Wiqi()
        wiqi.set(**kwargs)
        wiqi.stack = g
        wiqi.save()
        g.wiqi = wiqi
        g.creator = u
        g.creator_ip = uip
        g.save()
#encoding: utf-8
from lxml import etree
from urlparse import urljoin

from django.core.management.base import NoArgsCommand

from iphonefood_core.management.commands.sync_evrasia import BASE_URL
from iphonefood_core.models import Address


ADDRESSES_URL = BASE_URL + 'address/spb.html'
ADDRESSES_CITY = u'Санкт-Петербург'

XADDRESSES = r'//*[contains(@class, "address")]//dd//a/@href'
ADDRESS = {
    'address': r'//h1/text()',
    'description': r'//*[contains(@class, "content")]//p[position()=1]/text()',
    'district': r'//*[contains(@class, "address")]//*[@class="current"]/a/text()'
}


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        Address.objects.all().delete()
        
        tree = self.get_tree(ADDRESSES_URL)
        for url in tree.xpath(XADDRESSES):
            self.create_address(self.parse_address(url))

    def get_tree(self, url):
        parser = etree.HTMLParser()
        tree = etree.parse(urljoin(BASE_URL, url), parser=parser)
        return tree

    def parse_address(self, url):
        print 'Parse address %s' % url
        try:
            tree = self.get_tree(url)
            data = dict([(name, tree.xpath(path)) for name, path in ADDRESS.items()])
            data['description'] = ['\n'.join([d.strip() for d in data['description']])]
            return dict([(k, v[0]) for k,v in data.items()])
        except Exception, e:
            print e
            return None

    def create_address(self, data):
        data['city'] = ADDRESSES_CITY
        address = Address.objects.create(**data)
        address.save()



        


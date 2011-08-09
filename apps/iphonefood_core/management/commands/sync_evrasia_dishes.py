#encoding: utf-8
from pprint import pprint
from urlparse import urljoin
from lxml import etree
import re

from django.core.management.base import NoArgsCommand

from iphonefood_core.models import Dish, Menu, Category


BASE_URL = u'http://evrasia.spb.ru/'
MENU_URL = BASE_URL + u'menu/japaneese.html'
MENU = u'Японское меню'

XCATS = r'//*[@class="leftside-block list"]/*/dt/a/@href'

DISH = {
    'name': r'//h1/text()',
    'description': r'//h1/../text()[position()=2]',
    'photo_url': r'//*[contains(@class, "content")]/table[position()=1]//img/@src',
    'price': r'//h1/..//p/strong/text()'
}

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        self.menu = Menu.objects.get_or_create(name=MENU)[0]

        self.create_cat(self.parse_cat(MENU_URL))

        tree = self.get_tree(MENU_URL)
        cats = tree.xpath(XCATS)

        for cat in cats[1:]:
            self.create_cat(self.parse_cat(cat))

    def get_tree(self, url):
        parser = etree.HTMLParser()
        tree = etree.parse(urljoin(BASE_URL, url), parser=parser)
        return tree

    def parse_cat(self, url):
        tree = self.get_tree(url)
        data = {}
        data['name'] = tree.xpath(r'//h2/text()')[0]
        data['items'] = ([self.parse_dish(url)]
                         + [self.parse_dish(u) for u in tree.xpath('//*[@class="menu-list"]//a/@href')])
        return data


    def parse_dish(self, url):
        print 'Parse dish %s' % url
        try:
            tree = self.get_tree(url)
            return dict([(name, tree.xpath(path)[0]) for name, path in DISH.items()])
        except Exception, e:
            print e
            return None

    def create_cat(self, catdata):
        cat = Category.objects.get_or_create(menu=self.menu, name=catdata['name'])[0]
        for item in catdata['items']:
            if item:
                dish = Dish.objects.get_or_create(name=item['name'].capitalize(), category=cat)[0]
                dish.description = item['description'].strip()
                dish.photo_url = urljoin(BASE_URL, item['photo_url'])
                dish.price = re.sub(r'\D', '', item['price'])
                dish.save()
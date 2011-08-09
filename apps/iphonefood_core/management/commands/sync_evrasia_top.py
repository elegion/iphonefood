from lxml import etree
from urlparse import urljoin

from django.core.management.base import NoArgsCommand

from iphonefood_core.management.commands.sync_evrasia import BASE_URL
from iphonefood_core.models import Dish


XTOP = r'//*[contains(@class, "top-10")]//li/a/text()'


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        tree = self.get_tree(BASE_URL)
        max_rating = 100
        Dish.objects.all().update(rating=0)

        for top in tree.xpath(XTOP):
            dish = Dish.objects.filter(name=top.capitalize())
            if len(dish):
                dish = dish[0]
                dish.rating = max_rating
                dish.save()
                max_rating -= 1
            else:
                print top


    def get_tree(self, url):
        parser = etree.HTMLParser()
        tree = etree.parse(urljoin(BASE_URL, url), parser=parser)
        return tree


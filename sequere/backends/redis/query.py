try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

from sequere.query import QuerySetTransformer
from sequere import utils


class RedisQuerySetTransformer(QuerySetTransformer):
    def __init__(self, client, count, key, prefix, manager):
        super(RedisQuerySetTransformer, self).__init__(client, count)

        self.keys = [key, ]
        self.order_by(False)
        self.prefix = prefix
        self.manager = manager

    def order_by(self, desc):
        self.desc = desc

        if desc:
            self.method = getattr(self.qs, 'zrevrangebyscore')

            self.pieces = self.keys + ['+inf', '-inf']
        else:
            self.method = getattr(self.qs, 'zrangebyscore')

            self.pieces = self.keys + ['-inf', '+inf']

        return self

    def transform(self, qs):
        scores = self.method(*self.pieces,
                             start=self.start,
                             num=self.stop - self.start,
                             withscores=True)

        scores = OrderedDict(scores)

        objects = self.manager.get_from_uid_list(scores.keys())

        return [(objects[i], utils.from_timestamp(value[1]))
                for i, value in enumerate(scores.items())]

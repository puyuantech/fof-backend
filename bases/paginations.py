from sqlalchemy import text
from flask import request


class BasePagination:
    def __init__(self, page=1, page_size=10, ordering=None):
        self.page = int(page)
        self.page_size = int(page_size)
        self.ordering = ordering if ordering else []
        self.convert_ordering()

    def paginate(self, query):
        raise NotImplementedError

    def convert_ordering(self):
        raise NotImplementedError


class SQLPagination(BasePagination):

    def paginate(self, query, call_back=None, equal_filter=None, range_filter=None, contains_filter=None,
                 multi_filter=None):

        if range_filter:
            for i in range_filter:
                j = str(i).split('.')[1]
                if request.args.get('min_{}'.format(j)) is not None and request.args.get('min_{}'.format(j)) != '':
                    query = query.filter(i >= request.args.get('min_{}'.format(j)))

                if request.args.get('max_{}'.format(j)) is not None and request.args.get('max_{}'.format(j)) != '':
                    query = query.filter(i <= request.args.get('max_{}'.format(j)))

        if equal_filter:
            for i in equal_filter:
                j = str(i).split('.')[1]
                if request.args.get(j) is not None and request.args.get(j) != '':
                    query = query.filter_by(**{j: request.args.get(j)})

        if contains_filter:
            for i in contains_filter:
                j = str(i).split('.')[1]
                if request.args.get(j) is not None and request.args.get(j) != '':
                    query = query.filter(i.contains(request.args.get(j)))

        if multi_filter:
            for i in multi_filter:
                j = str(i).split('.')[1]
                if request.args.get(j) is not None and request.args.get(j) != '':
                    c = request.args.get(j).split(',')
                    query = query.filter(i.in_(c))

        if self.ordering:
            query = query.order_by(*[text(i) for i in self.ordering])
        instances = query.limit(self.page_size).offset((self.page - 1) * self.page_size).all()
        if call_back:
            results = call_back(instances)
        else:
            results = [i.to_dict() for i in instances]
        return {
            'page': self.page,
            'page_size': self.page_size,
            'count': query.count(),
            'results': results,
        }

    def convert_ordering(self):
        for i in range(len(self.ordering)):
            if self.ordering[i].startswith('-'):
                self.ordering[i] = '{} {}'.format(self.ordering[i][1:], 'DESC')
            else:
                self.ordering[i] = '{} {}'.format(self.ordering[i], 'ASC')



class PaginationHelper():

    def __init__(self, url, start, limit):
        self.url = url
        self.start = start
        self.limit = limit

    def paginate_results(self, results):

        # check if page exists
        count = len(results)

        # make response
        obj = {}
        obj['start'] = self.start
        obj['limit'] = self.limit
        obj['count'] = count
        # make URLs
        # make previous url
        if self.start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, self.start - self.limit)
            limit_copy = self.start - 1
            obj['previous'] = self.url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        # make next url
        if self.start + self.limit > count:
            obj['next'] = ''
        else:

            start_copy = self.start + self.limit
            obj['next'] = self.url + '?start=%d&limit=%d' % (start_copy, self.limit)
        # finally extract result according to bounds
        obj['results'] = results[(self.start - 1):(self.start - 1 + self.limit)]
        return obj

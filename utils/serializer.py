from flask import request


def convert(df):

    header = list(df.columns)
    body = []
    for i in df.index:
        body.append(list(df.loc[i, :]))

    return {
        'header': header,
        'body': body,
    }


def convert_to_dict(df):

    results = []
    for i in df.index:
        current = {}
        for j in df.columns:
            current[j] = df.loc[i, j]
        results.append(current)

    return results


class DataFrameSerializer:
    page = 1
    page_size = 25
    paginated = False

    def __init__(self):
        page = request.args.get('page')
        if page:
            self.page = int(page)
        page_size = request.args.get('page_size')
        if page_size:
            self.page_size = int(page_size)
        self.paginated = True

    def set_pagination(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self.paginated = True

    def to_representation(self, df):

        if not self.paginated:
            return convert(df)

        begin = (self.page - 1) * self.page_size
        end = self.page * self.page_size

        dff = df[begin:end]

        return {
            'page': self.page,
            'page_size': self.page_size,
            'count': len(df.index),
            'results': convert(dff),
        }


class DataFrameTSerializer:
    """
    将dff反转再转化为dict
    """
    page = 1
    page_size = 25
    paginated = False

    def __init__(self):
        page = request.args.get('page')
        if page:
            self.page = int(page)
        page_size = request.args.get('page_size')
        if page_size:
            self.page_size = int(page_size)
        self.paginated = True

    def set_pagination(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self.paginated = True

    def to_representation(self, df):

        if not self.paginated:
            return convert(df)

        begin = (self.page - 1) * self.page_size
        end = self.page * self.page_size

        dff = df[begin:end]
        dff = dff.T
        dff = dff.reset_index()
        return {
            'page': self.page,
            'page_size': self.page_size,
            'count': len(df.index),
            'results': convert(dff),
        }


class DataFrameDictSerializer:
    """为了精确的控制前端的格式，DataFrame的序列号需要更精确的控制，字典的输出会更好"""

    page = 1
    page_size = 25
    paginated = False

    def __init__(self):
        page = request.args.get('page')
        if page:
            self.page = int(page)
        page_size = request.args.get('page_size')
        if page_size:
            self.page_size = int(page_size)
        self.paginated = True

    def set_pagination(self, page, page_size):
        self.page = page
        self.page_size = page_size
        self.paginated = True

    def to_representation(self, df):

        if not self.paginated:
            return {
                'page': 0,
                'results': convert_to_dict(df),
            }

        begin = (self.page - 1) * self.page_size
        end = self.page * self.page_size

        dff = df[begin:end]

        return {
            'page': self.page,
            'page_size': self.page_size,
            'count': len(df.index),
            'results': convert_to_dict(dff),
        }


from flask.ext.appbuilder import IndexView


class MyIndexView(IndexView):
    index_template = 'index.html'
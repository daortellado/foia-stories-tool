
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import csv
import pickle
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///argfoia.db'
db = SQLAlchemy(app)



summary_tags = db.Table('summary_tags', db.Model.metadata, 
    db.Column('summary_id', db.Integer, db.ForeignKey('summary.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Summary(db.Model):
    __tablename__ = 'summary'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    summary_text = db.Column(db.String(8000))
    tags = db.relationship('Tag', secondary=summary_tags)

    def __init__(self, summary_text):
        self.summary_text = summary_text

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    summary_id = db.Column(db.Integer, db.ForeignKey('summary.id'))
    title = db.Column(db.String(80))
    url = db.Column(db.String(80))
    author = db.Column(db.String(80))
    date = db.Column(db.String(120))
    organization = db.Column(db.String(120))

    def __init__(self, summary_id, title, url, author, organization, date=None):
        self.title = title
        self.url = url
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.author = author
        self.organization = organization
        
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    subject = db.Column(db.String(120))

    def __init__(self, subject):
        self.subject = subject

    def __repr__(self):
        return self.subject

db.create_all()

CSV_FILE = '/Users/dortellado/Desktop/summariesenc.csv'

with open(CSV_FILE, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        attrs = ['org', 'title', 'author', 'date', 'url', 'summary', 'tag']
        for attr in attrs: locals()[attr] = []

        for key in row:
            for attr in attrs:
                if attr in key.lower():
                    locals()[attr].append(row.get(key))

        new_summary = Summary(summary_text=unicode(summary[0], 'utf-8'))
        db.session.add(new_summary)
        db.session.flush()
        new_tag = Tag(subject=unicode(tag[0], 'utf-8'))
        db.session.add(new_tag)
        new_summary.tags.append(new_tag)

        for i, v in enumerate(locals()['title']):
            logging.warning(i)
        # add new_article code here.....

            new_article = Article(summary_id=new_summary.id, title=unicode(locals()['title'][i], 'utf-8'),
                organization=unicode(locals()['org'][i], 'utf-8'), author=unicode(locals()['author'][i], 'utf-8'),
                url=unicode(locals()['url'][i], 'utf-8'), date=unicode(locals()['date'][i], 'utf-8'))
            db.session.add(new_article)

        db.session.commit()

if __name__ == '__main__':
    

    admin = Admin(app, name='FOIA Stories: Argentina', template_mode='bootstrap3')
# Add administrative views here

class ArticleModelView( ModelView ):

        column_auto_select_related = True
        # column_select_related_list = (Summary.summary_text, Tag.subject)
        #column_searchable_list = ( Summary.summary_text, Tag.subject )
        column_filters = (Summary.summary_text, Tag.subject)


        # column_auto_select_related()

        # def init_search( self ):
        #     r = super( ArticleModelView, self ).init_search()
        #     #add the association table to search join list
        #     self._search_joins['tag'] = Tag.subject
        #     #reverse the lsit so that the association table appears before the two main tables
             
        #     return r

        def scaffold_filters(self, subject):
            filters = super( ArticleModelView, self).scaffold_filters(subject)
            #Check if "tag" table has been processed and the join table added
            if "tags" in self._filter_joins:
              #add the association table to the filter join tables
              self._filter_joins['tags'].append(summary_tags)
              #reverse the list so that the association table appears before the two main tables
              self._filter_joins['tags'].reverse()

            return filters

admin.add_view(ArticleModelView(Summary, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Tag, db.session))


app.run(debug=True)

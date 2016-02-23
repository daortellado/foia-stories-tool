import csv
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Table
from sqlalchemy.orm import relationship, backref
from flask.ext.appbuilder import Model
from flask.ext.appbuilder import SQLA
from sqlalchemy.orm.collections import attribute_mapped_collection

summary_tags = Table('summary_tags', Model.metadata, 
    Column('summary_id', Integer, ForeignKey('summary.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Summary(Model):
    __tablename__ = 'summary'
    id = Column(Integer, autoincrement=True, primary_key=True)
    summary_text_en = Column(String(8000))
    summary_text_es = Column(String(8000))
    title_en = Column(String(80))
    title_es = Column(String(80))
    url = Column(String(80))
    language_en = Column(String(80))
    language_es = Column(String(80))
    tags = relationship('Tag', secondary=summary_tags)

    #collection_class=attribute_mapped_collection('subject')
    #collection_class=attribute_mapped_collection('subject'),cascade="all, delete-orphan", backref='summary', single_parent=True
        
 
        
class Tag(Model):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    subject_en = Column(String(120))
    subject_es = Column(String(120))

    def __repr__(self):
        return u"{0},{1}".format(self.subject_en, self.subject_es)

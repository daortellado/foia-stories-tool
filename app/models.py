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
    summary_text = Column(String(8000))
    title = Column(String(80))
    url = Column(String(80))
    language = Column(String(80))
    tags = relationship('Tag', secondary=summary_tags)

    def __init__(self, summary_text, title, url, language):
        self.summary_text = summary_text
        self.title = title
        self.url = url
        self.language = language
        
class Tag(Model):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    subject = Column(String(120))


    def __init__(self, subject):
        self.subject = subject

    def __repr__(self):
        return self.subject



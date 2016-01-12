from flask.ext.appbuilder import ModelView, MasterDetailView, SQLA
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from .models import Summary, Tag
from app import db, appbuilder
from flask import render_template, redirect, Flask
from flask.ext.appbuilder.widgets import ListItem

import sqlite3

class SummaryView(ModelView):
        datamodel = SQLAInterface(Summary)
        list_columns = ['title', 'summary_text']
        list_widget = ListItem

class TagView(ModelView):
        datamodel = SQLAInterface(Tag)
        related_views = [SummaryView]
        list_columns = ['subject']   

class ArticleMasterView(MasterDetailView):
        datamodel = SQLAInterface(Tag)
        related_views = [SummaryView]

db.create_all()

appbuilder.add_view(ArticleMasterView, "By subject", icon = "fa-tags", category = "View stories",
                category_icon = "fa-book")
appbuilder.add_separator("View stories")
appbuilder.add_view(SummaryView, "Detailed search", icon = "fa-search-plus", category = "View stories",
                category_icon = "fa-book")

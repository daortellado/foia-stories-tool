from flask.ext.appbuilder import ModelView, MasterDetailView, SQLA
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from .models import Summary, Tag
from app import db, appbuilder
from flask import render_template, redirect, Flask
from flask.ext.appbuilder.widgets import ListItem
from config import LANGUAGES

import sqlite3

class SummaryViewEN(ModelView):
        datamodel = SQLAInterface(Summary)
        list_columns = ['title_en', 'summary_text_en']
        list_widget = ListItem

        show_fieldsets = [
        ('Summary',{'fields':['title_en','url','language_en','summary_text_en']})
        ]

class SummaryViewES(ModelView):
        datamodel = SQLAInterface(Summary)
        list_columns = ['title_es', 'summary_text_es']
        list_widget = ListItem

        show_fieldsets = [
        ('Summary',{'fields':['title_es','url','language_es','summary_text_es']})
        ]

class TagViewEN(ModelView):
        datamodel = SQLAInterface(Tag)
        related_views = [SummaryViewEN]
        list_columns = ['subject_en']   

class TagViewES(ModelView):
        datamodel = SQLAInterface(Tag)
        related_views = [SummaryViewES]
        list_columns = ['subject_es']  

class ArticleMasterViewEN(MasterDetailView):
        datamodel = SQLAInterface(Tag)
        related_views = [TagViewEN, SummaryViewEN]
        list_columns = ['subject_en'] 

class ArticleMasterViewES(MasterDetailView):
        datamodel = SQLAInterface(Tag)
        related_views = [TagViewES, SummaryViewES]
        list_columns = ['subject_es'] 


db.create_all()

appbuilder.add_view(ArticleMasterViewEN, "By subject", icon = "fa-tags", category = "View stories",
                category_icon = "fa-book")
appbuilder.add_separator("View stories")
appbuilder.add_view(SummaryViewEN, "Detailed search", icon = "fa-search-plus", category = "View stories",
                category_icon = "fa-book")

appbuilder.add_view(ArticleMasterViewES, "Por tema", icon = "fa-tags", category = "Ver historias",
        category_icon = "fa-book")
appbuilder.add_separator("Ver historias")
appbuilder.add_view(SummaryViewES, "Buscar en detalle", icon = "fa-search-plus", category = "Ver historias",
        category_icon = "fa-book")

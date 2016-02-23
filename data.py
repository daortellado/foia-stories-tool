import csv

import logging
from app import db
from app.models import Summary, Tag

CSV_FILE = 'summariesencspa.csv'

with open(CSV_FILE, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        attrs = ['title', 'url', 'summary', 'tags', 'language', 'titulo', 'resumen', 'temas', 'idioma']
        for attr in attrs: locals()[attr] = []

        for key in row:
            for attr in attrs:
                if attr in key.lower():
                    locals()[attr].append(row.get(key))

        new_summary = Summary(url=unicode(url[0], 'utf-8'),
                              summary_text_en=unicode(summary[0], 'utf-8'),
                              title_en=unicode(title[0], 'utf-8'),
                              language_en=unicode(language[0], 'utf-8'),
                              summary_text_es=unicode(resumen[0], 'utf-8'),
                              title_es=unicode(titulo[0], 'utf-8'),
                              language_es=unicode(idioma[0], 'utf-8')
        )

        if not db.session.query(Summary).filter(Summary.url == unicode(url[0], 'utf-8')).first():
       	    db.session.add(new_summary)

            tagArray = tags[0].split(',') # crime, drugs, jails
            temaArray = temas[0].split(',') # drugas, jailies, crimas
            for i in range(0, len(tagArray)):
                tag_en = tagArray[i].strip()
                tag_es = temaArray[i].strip()
                new_tag = Tag(subject_en=unicode(tag_en, 'utf-8'), subject_es=unicode(tag_es, 'utf-8'))
                result = db.session.query(Tag).filter(Tag.subject_en == unicode(tag_en, 'utf-8'), Tag.subject_es == unicode(tag_es, 'utf-8')).first()
                logging.debug(result)
                if not result:
                    logging.debug(u'Creating new tag {}.'.format(new_tag))
                    db.session.add(new_tag)
                else:
                    logging.debug(u'Tag {} already exists.'.format(new_tag))
                    new_tag = result
                new_summary.tags.append(new_tag)

        db.session.commit()

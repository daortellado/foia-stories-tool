import csv

import logging
from app import db
from app.models import Summary, Tag

CSV_FILE = 'summariesurlsenc.csv'

with open(CSV_FILE, 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        attrs = ['title', 'url', 'summary', 'tags', 'language']
        for attr in attrs: locals()[attr] = []

        for key in row:
            for attr in attrs:
                if attr in key.lower():
                    locals()[attr].append(row.get(key))

        new_summary = Summary(summary_text=unicode(summary[0], 'utf-8'), title=unicode(locals()['title'][0], 'utf-8'),
                url=unicode(locals()['url'][0], 'utf-8'), language=unicode(locals()['language'][0], 'utf-8'))
        db.session.add(new_summary)
        tagArray = tags[0].split(',')
       	for tag in tagArray:
       		tag = tag.strip()
        	new_tag = Tag(subject=unicode(tag, 'utf-8'))
        	result = db.session.query(Tag).filter(Tag.subject == tag).first()
        	logging.debug(result)
        	if not result:
        		logging.debug('Creating new tag {}.'.format(new_tag))
        		db.session.add(new_tag)
        	else:
        		logging.debug('Tag {} already exists.'.format(new_tag))
        		new_tag = result
        	new_summary.tags.append(new_tag)

        db.session.commit()

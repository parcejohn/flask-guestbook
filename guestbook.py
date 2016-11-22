#!/usr/bin/env python

"""
    @uthor: John Gallo
    Flask Guestbook application with persistence via pickle'd objects
"""

from flask import Flask
import flask
import pickle
import time

datastore = 'data/guestbook.pickle'

class Guestbook(object):

    def __init__(self, guestbook_id):
        ''' Initialize a Guestbook object or retrieve from datastore'''
        try:
            with open(datastore) as fh:
                guestbooks = pickle.load(fh)
                if guestbook_id in guestbooks:
                    guestbook = guestbooks[guestbook_id]

                self.guestbook_id = guestbook.guestbook_id
                self.entries = guestbook.entries
                self.index = guestbook.index
        except Exception as e:
            self.guestbook_id = guestbook_id
            self.entries = []
            self.index = -1


    def add_entry(self, entry):
        ''' Add Entry objects '''
        self.entries.append(entry)


    def store(self):
        ''' Store to file using pickle '''     
        try:
            fhr = open(datastore, 'rb')
            guestbooks = pickle.load(fhr)
            guestbooks[self.guestbook_id] = self
        except Exception as e:
            guestbooks = { self.guestbook_id : self }
        
        fhw = open(datastore, 'wb')
        pickle.dump(guestbooks, fhw)


    def __iter__(self):
        return self


    def next(self):
        self.index += 1
        if self.index > len(self.entries) - 1:
            self.index = -1
            raise StopIteration
        return self.entries[self.index]


class Entry(object):
    ''' Guestbook Entry object'''
    def __init__(self, name, comment):
        self.name = name
        self.comment = comment
        self.date = time.ctime()


app = Flask(__name__)      

@app.route('/')
def root():
    return flask.render_template('guestbook.html')


@app.route('/display_entries')
def display_entries():
    guestbook_id = flask.request.args.get('guestbook_id')
    return flask.render_template('guestbook.html',guestbook=Guestbook(guestbook_id))


@app.route('/add_entry')
def add_entry():
    guestbook_id = flask.request.args.get('guestbook_id')
    name = flask.request.args.get('name')
    comment = flask.request.args.get('comment')

    guestbook = Guestbook(guestbook_id)
    entry = Entry(name, comment)

    guestbook.add_entry(entry)

    guestbook.store()

    return flask.redirect(flask.url_for('display_entries', guestbook_id=guestbook_id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)    



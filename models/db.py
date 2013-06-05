# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

my_set_type = ['Full-time employement', 'Short-term contract', 'Volunteer contributer', 'Freelance/Consulting', 'Partner for a venture', 'Internship']
my_set_category = ['Physician/Surgeon', 'Paedriattrics', 'OBG', 'Psychiatry', 'Opthamology', 'ENT', 'Neurology', 'Dermatology', 'Dentistry', 'Nursing', 'Physio occupational therapy', 'Audiology/Speech Therapy', 'Alternative Medicine', 'Cardiology', 'Urology', 'Clinical Psychologist']
my_set_location =['Mumbai', 'Delhi', 'Chennai', 'Kolkatta', 'Bangalore']
my_set_experience =['1 year', '2 year', '3 year', '4 year', '5 year']
my_set_days = ['1 month', '2 month', '3 month', '4 month']

db.define_table('page',
    Field('title', requires=IS_NOT_EMPTY()),
    Field('days',requires=IS_IN_SET(my_set_days, multiple=False),widget=SQLFORM.widgets.options.widget, label=T('How many days do you want this job to be available for?')),
    Field('type', requires=IS_IN_SET(my_set_type,multiple=False),widget=SQLFORM.widgets.radio.widget, label=T('Type of Job')),
    Field('category', requires=IS_IN_SET(my_set_category,multiple=False),widget=SQLFORM.widgets.radio.widget, label=T('Category of Job')),
    Field('location', requires=IS_IN_SET(my_set_location, multiple=True), widget=SQLFORM.widgets.multiple.widget, label=T('Location of Job')),
    Field('relocation', requires=IS_IN_SET(['yes', 'no']), widget = SQLFORM.widgets.radio.widget, label=T('Relocation assistance available')),
    Field('description', widget = SQLFORM.widgets.text.widget, label=T('Description of Job')),
    Field('perks', requires=IS_IN_SET(['yes', 'no']), widget = SQLFORM.widgets.radio.widget, label=T('Job perks available')),
    Field('how_apply','text', label=T('How do people apply for this job?'), default='Mail to abc@xyz.com'),
    Field('experience',requires=IS_IN_SET(my_set_experience, multiple=False), widget = SQLFORM.widgets.options.widget, label=T('Work experience needed')),
    Field('name', widget=SQLFORM.widgets.string.widget, label=T('Name of the Organization'), requires=IS_NOT_EMPTY()),
    Field('logo', 'upload', label=T('Logo')),
    Field('URL','string', default='http://'),
    Field('email', 'string', IS_EMAIL(), label=T('Company Email for confirmation'), requires=IS_NOT_EMPTY()),
    Field('contact_listing', requires=IS_IN_SET(['Yes', 'No']),widget=SQLFORM.widgets.radio.widget,label=T('Can recruiters contact you about this listing?')),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by','reference auth_user', default=auth.user_id),
    format='%(title)s')

db.define_table('apply',
    Field('page_id', 'reference page'),
    Field('name','string'),
    Field('resume', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', default=auth.user_id))
    

db.page.title.requires = IS_NOT_IN_DB(db, 'page.title')       #i.e. page.title should be unique
db.page.created_by.readable = db.page.created_by.writable = False
db.page.created_on.readable = db.page.created_on.writable = False 

db.apply.resume.requires = IS_NOT_EMPTY()
db.apply.name.requires = IS_NOT_EMPTY()
db.apply.page_id.readable = db.apply.page_id.writable = False  
db.apply.created_by.readable = db.apply.created_by.writable = False  
db.apply.created_on.readable = db.apply.created_on.writable = False

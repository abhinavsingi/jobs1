# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
#    pages = db().select(db.page.id, db.page.title,db.page.body,db.page.created_by, orderby=db.page.id)
    pages = db().select(db.page.ALL, orderby=db.page.id)
    return dict(pages = pages)
    
def trending():
    pages = db().select(db.page.ALL, orderby=db.page.created_on)   
    """
    change order_by
    """
    return dict(pages = pages)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
    
@auth.requires_login()
def create():
    form = SQLFORM(db.page).process(next=URL('index'))
    return dict(form=form)
        
    
@auth.requires_login()    
def show():
    this_page=db(db.page.id==int(request.args(0))).select(db.page.ALL)
    form = SQLFORM(db.apply).process() if auth.user else None 

    return dict(pages=this_page, form=form)
   
#    titles = db().select(db.page.id ==int(request.args(0)))
#    bodyy = db().select(db.page.body)
#    appliednames = db(db.apply.page_id == int(request.args(0))
#    return dict(titles = titles, body=bodyy, form = form)

        
def show1():
    this_page=db(db.page.id==int(request.args(0))).select(db.page.ALL)
    return (this_page)
       
@auth.requires_login()
def edit():

    this_page=db(db.page.id==int(request.args(0))).select(db.page.ALL)
    form = SQLFORM(db.page, this_page).process()

    return dict(form=form)

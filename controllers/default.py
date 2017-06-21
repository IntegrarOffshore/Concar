# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

# VIEWS

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

@auth.requires_login()
def level():
    # contador = db(db.funcionario.status != "Concluido").count()
    # if contador == 0:
    #     response.flash = 'Nenhum atendimento pendente'
    # elif contador == 1:
    #     response.flash = 'Existe %s atendimento pendente' % contador
    # else:
    #     response.flash = 'Existem %s atendimentos pendentes' % contador
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

# CREATE

#@auth.requires_login()
def carro():
    form = SQLFORM(Carro)
    if form.process().accepted:
        session.flash = 'Carro %s cadastrado' % form.vars.modelo
        redirect(URL('carro'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

def manutencao():
    form = SQLFORM(Manutencao)
    if form.process().accepted:
        session.flash = 'Manutenção cadastrada'
        redirect(URL('manutencao'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)


# READ

#@auth.requires_login()
def ver_usuarios():
    grid = SQLFORM.grid(db.auth_user,
    create=False,
    deletable=False,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False,
                       xml=False,
                       json=False))
    return dict(grid=grid)

#auth.requires_login()
def ver_carro():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        param = edit[2]
        url = 'editar_carro/' + param
        redirect(URL(url))
    # if 'view' in request.args:
    #     db.carro.id.readable = False # or writable
    #     view = request.args
    #     response.flash = view
    #     param = view[2]
    #     url = 'ver_carro_atual/' + param
    #     redirect(URL(url))
    grid = SQLFORM.grid(Carro,
    fields=[db.carro.marca,
            db.carro.modelo,
            db.carro.placa,
            db.carro.ano],
            maxtextlength=16,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

def ver_carro_atual():
    db.carro.id.readable = False
    db.carro.marca.writable = False
    db.carro.modelo.writable = False
    db.carro.placa.writable = False
    db.carro.ano.writable = False
    form = SQLFORM(Carro, request.args(0, cast=int))
    if form.process().accepted:
        session.flash = 'Carro atualizado: %s' % form.vars.nome
        redirect(URL('ver_carro'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


def ver_manutencao():
    # if 'edit' in request.args:
    #     edit = request.args
    #     response.flash = edit
    #     param = edit[2]
    #     url = 'editar_revisao/' + param
    #     redirect(URL(url))
    grid = SQLFORM.grid(Manutencao, fields=[db.manutencao.carro,
                                            db.manutencao.km,
                                            db.manutencao.data_nf,
                                            db.manutencao.valor],
                                            create=False,
    exportclasses=dict(tsv_with_hidden_cols=False, csv=False, xml=False, json=False))
    return dict(grid=grid)

# EDITAR


def editar_carro():
    db.carro.id.readable = False
    form = SQLFORM(Carro, request.args(0, cast=int))
    if form.process().accepted:
        session.flash = 'Carro atualizado: %s' % form.vars.nome
        redirect(URL('ver_carro'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

def editar_revisao():
    db.manutencao.id.readable = False
    form = SQLFORM(Manutencao,request.args(0, cast=int))
    db.manutencao.id.readable = False 
    if form.process().accepted:
        session.flash = 'Revisão atualizada'
        redirect(URL('ver_manutencao'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

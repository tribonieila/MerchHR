# ------------------------------------------------------------------------------------------
# -----------------------  C O M M U N I C A T I O N   S Y S T E M  ------------------------
# ------------------------------------------------------------------------------------------

import string, random, locale
from datetime import date
@auth.requires_login()
def communication_tranx_prefix():
    form = SQLFORM(db.Communication_Tranx_Prefix)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('#'),TH('Prefix'),TH('Prefix Name'),TH('Serial Key'),TH('Prefix Key'),TH('Action')))
    _query = db(db.Communication_Tranx_Prefix).select()
    for n in _query:
        view_lnk = A(I(_class='fas fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication_tranx_prefix_edit', args = n.id))
        dele_lnk = A(I(_class='fas fa-trash-alt'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.serial_key),TD(n.prefix_key),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires_login()
def communication_tranx_prefix_edit():
    form = SQLFORM(db.Communication_Tranx_Prefix, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('communication_tranx_prefix'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    return dict(form = form)

@auth.requires_login()
def validate_incoming_mail(form):
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.incoming_mail_no = _ckey
    form.vars.mail_prefix_no_id = _pre.id

@auth.requires_login()
def get_incoming_mail_grid():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form = SQLFORM(db.Incoming_Mail)
    if form.process(onvalidation = validate_incoming_mail).accepted:
        _pre.update_record(serial_key = _skey)
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    thead = THEAD(TR(TH('Date'),TH('Mail No.'),TH('Sender'),TH('Subject'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db().select(orderby = ~db.Incoming_Mail.mail_date)
    else:
        _query = db(((db.Incoming_Mail.confidential==True) & (db.Incoming_Mail.created_by == auth.user_id)) | (db.Incoming_Mail.confidential==False)).select(orderby = ~db.Incoming_Mail.mail_date)
    for n in _query:
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_incoming_mail_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.mail_date),TD(n.incoming_mail_no),TD(n.mail_sender),TD(n.mail_subject),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table, _ckey = _ckey)

@auth.requires_login()
def put_incoming_mail_id():
    _id = db(db.Incoming_Mail.id == request.args(0)).select().first()
    form = SQLFORM(db.Incoming_Mail, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)

@auth.requires_login()
def validate_outgoing_mail(form):
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.outgoing_mail_no = _ckey
    form.vars.mail_prefix_no_id = _pre.id

@auth.requires_login()
def get_outgoing_mail_form():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]    
    form = SQLFORM(db.Outgoing_Mail)
    if form.process(onvalidation = validate_outgoing_mail).accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
        redirect(URL('communication','get_outgoing_mail_form'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Mail No.'),TH('Sender'),TH('Subject'),TH('Address'),TH('Postage'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db(db.Outgoing_Mail.mail_date == request.now).select(orderby = ~db.Outgoing_Mail.id)
    else:
        _query = db(((db.Outgoing_Mail.confidential==True) & (db.Outgoing_Mail.mail_date == request.now) & (db.Outgoing_Mail.created_by == auth.user_id)) | ((db.Outgoing_Mail.confidential==False) & (db.Outgoing_Mail.mail_date == request.now))).select(orderby = ~db.Outgoing_Mail.id)    
    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_outgoing_mail_id', args = n.id))
        prin_lnk = A(I(_class='fa fa-print'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('procurement','insurance_proposal_reports', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, prin_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mail_date),TD(n.outgoing_mail_no),TD(n.mail_sender),TD(n.mail_subject),TD(n.mail_addressee),TD(n.postage),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)

@auth.requires_login()
def get_outgoing_mail_grid():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'LTR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]    
    form = SQLFORM(db.Outgoing_Mail)
    if form.process(onvalidation = validate_outgoing_mail).accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Mail No.'),TH('Sender'),TH('Subject'),TH('Address'),TH('Postage'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db().select(orderby = ~db.Outgoing_Mail.id)
    else:
        _query = db(((db.Outgoing_Mail.confidential==True) & (db.Outgoing_Mail.created_by == auth.user_id)) | (db.Outgoing_Mail.confidential==False)).select(orderby = ~db.Outgoing_Mail.id)    
    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_outgoing_mail_id', args = n.id))
        prin_lnk = A(I(_class='fa fa-print'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('procurement','insurance_proposal_reports', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, prin_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mail_date),TD(n.outgoing_mail_no),TD(n.mail_sender),TD(n.mail_subject),TD(n.mail_addressee),TD(n.postage),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)

@auth.requires_login()
def put_outgoing_mail_id():
    _id = db(db.Outgoing_Mail.id == request.args(0)).select().first()
    form = SQLFORM(db.Outgoing_Mail, request.args(0))
    if form.process().accepted:
        redirect(URL('get_outgoing_mail_form'))
        session.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)


@auth.requires_login()
def validate_circular(form):
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'CIR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.circular_no = _ckey
    form.vars.circular_prefix_no_id = _pre.id

@auth.requires_login()
def get_circular_form():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'CIR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]    
    form = SQLFORM(db.Circular)
    if form.process(onvalidation = validate_circular).accepted:
        _pre.update_record(serial_key = _skey)        
        redirect(URL('communication','get_circular_form'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Circular No.'),TH('Subject'),TH('Address'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db(db.Circular.circular_date == request.now).select(orderby = ~db.Circular.id)
    else:
        _query = db(((db.Circular.confidential==True) & (db.Circular.circular_date == request.now) & (db.Circular.created_by == auth.user_id)) | ((db.Circular.confidential==False) & (db.Circular.circular_date == request.now))).select(orderby = ~db.Circular.id)
    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_circular_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.circular_date),TD(n.circular_no),TD(n.circular_subject),TD(n.circular_addressee),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)    

@auth.requires_login()
def get_circular_grid():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'CIR').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]    
    form = SQLFORM(db.Circular)
    if form.process(onvalidation = validate_circular).accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Circular No.'),TH('Subject'),TH('Address'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db().select(orderby = ~db.Circular.id)
    else:
        _query = db(((db.Circular.confidential==True) & (db.Circular.created_by == auth.user_id)) | (db.Circular.confidential==False)).select(orderby = ~db.Circular.id)
    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_circular_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.circular_date),TD(n.circular_no),TD(n.circular_subject),TD(n.circular_addressee),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)    

@auth.requires_login()
def put_circular_id():
    _id = db(db.Circular.id == request.args(0)).select().first()
    form = SQLFORM(db.Circular, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('communication','get_circular_form'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)

@auth.requires_login()
def validate_memorandum(form):
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.memorandum_no = _ckey
    form.vars.memorandum_prefix_no_id = _pre.id

@auth.requires_login()
def get_memorandum_form():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]   
    form = SQLFORM(db.Memorandum)
    if form.process(onvalidation = validate_memorandum).accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
        redirect(URL('communication','get_memorandum_form'))
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Memorandum No.'),TH('Subject'),TH('Memo From'),TH('Memo To'),TH('Attached'),TH('Action'),_class='bg-gray disabled color-palette'))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db(db.Memorandum.memorandum_date==request.now).select(orderby = ~db.Memorandum.id)
    else:        
        _query = db(((db.Memorandum.memorandum_date==request.now) & (db.Memorandum.confidential==True) & (db.Memorandum.created_by == auth.user_id)) | ((db.Memorandum.confidential==False) & (db.Memorandum.memorandum_date==request.now))).select(orderby = ~db.Memorandum.id)
    for n in _query:        
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_memorandum_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.memorandum_date),TD(n.memorandum_no),TD(n.memorandum_subject),TD(n.memorandum_from),TD(n.memorandum_to),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _target=' _blank',_href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)    

@auth.requires_login()
def get_memorandum_grid():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]    
    form = SQLFORM(db.Memorandum)
    if form.process(onvalidation = validate_memorandum).accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Memorandum No.'),TH('Subject'),TH('Memo From'),TH('Memo To'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):        
        _query = db().select(orderby = ~db.Memorandum.id)
    else:        
        _query = db(((db.Memorandum.confidential==True) & (db.Memorandum.created_by == auth.user_id)) | (db.Memorandum.confidential==False)).select(orderby = ~db.Memorandum.id)
    for n in _query:        
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_memorandum_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.memorandum_date),TD(n.memorandum_no),TD(n.memorandum_subject),TD(n.memorandum_from),TD(n.memorandum_to),TD(A(SPAN(_class='fa fa-paperclip'), _title='Attached', _target=' _blank',_href = URL('default', 'download', args= n.attached)) if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)    

@auth.requires_login()
def put_memorandum_id():
    _id = db(db.Memorandum.id == request.args(0)).select().first()
    form = SQLFORM(db.Memorandum, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD SAVE'
        redirect(URL('communication','get_memorandum_form'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)

@auth.requires_login()
def validate_fax(form):
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'FAX').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]
    form.vars.fax_no = _ckey
    form.vars.fax_prefix_no_id = _pre.id

@auth.requires_login()
def get_fax_grid():
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'FAX').select().first() 
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]    
    form = SQLFORM(db.Fax)
    if form.process(onvalidation = validate_fax).accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Fax No.'),TH('Subject'),TH('Fax From'),TH('Fax To'),TH('Attached'),TH('Action')))
    if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'ROOT'):
        _query = db().select(orderby = ~db.Fax.fax_date)
    else:
        _query = db(((db.Fax.confidential==True) & (db.Fax.created_by == auth.user_id)) | (db.Fax.confidential==False)).select(orderby = ~db.Fax.fax_date)
    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_fax_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.fax_date),TD(n.fax_no),TD(n.fax_subject),TD(n.fax_from),TD(n.fax_to),TD(A(I(_class='fa fa-paperclip'),_type='button',_role=' button',  _class='btn btn-icon-toggle',  _title='Attached',_href = URL('default','download', args = n.attached), _target=' _blank') if n.attached else ""),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, _ckey = _ckey, table = table)    

@auth.requires_login()
def put_fax_id():
    _id = db(db.Fax.id == request.args(0)).select().first()
    form = SQLFORM(db.Fax, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('get_fax_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)    

@auth.requires_login()
def get_comm_tranx_prefix_grid():
    form = SQLFORM(db.Communication_Tranx_Prefix)
    if form.process().accepted:
        _pre.update_record(serial_key = _skey)        
        response.flash = 'RECORD SAVE'        
    elif form.errors:
        response.flash = 'ENTRY HAS ERRORS'

    row = []
    thead = THEAD(TR(TH('#'),TH('Prefix'),TH('Prefix Name'),TH('Serial Key'),TH('Action')))
    _query = db().select(orderby = db.Communication_Tranx_Prefix.id)
    for n in _query:
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('communication','put_comm_tranx_prefix_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.serial_key),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)    

@auth.requires_login()
def put_comm_tranx_prefix_id():
    _id = db(db.Communication_Tranx_Prefix.id == request.args(0)).select().first()
    form = SQLFORM(db.Communication_Tranx_Prefix, request.args(0))
    if form.process().accepted:
        session.flash = 'RECORD UPDATED'
        redirect(URL('get_comm_tranx_prefix_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)    

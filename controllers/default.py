# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import string
import random
from datetime import date, datetime, timedelta
import locale
from fractions import Fraction
# ---- example index page ----
@auth.requires_login()
def index():
    response.flash = T("Hello World")
    # for n in db(db.Employee_Employment_Details.sub_department_code_id == 5).select():
    #     n.update_record(sub_department_code_id = 3)
    # # grid = SQLFORM.grid(db.Employee_Employment_Details)
    
    return dict(message=T('Welcome to web2py!'))


def get_bank_account_grid():
    row = []
    ctr = 0
    form = SQLFORM(db.Bank_Account)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Bank Account Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Bank_Account.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.bank_account_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def get_sponsor_grid():
    row = []
    ctr = 0
    db.Sponsor.status_id.default = 1 
    form = SQLFORM(db.Sponsor)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Sponsors Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Sponsor.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.sponsor),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def get_help(): 
    return dict()

def get_department_head_grid():
    grid = SQLFORM.grid(db.auth_membership)
    return dict(grid = grid)

def get_department_head_assignment():
    grid = SQLFORM.grid(db.Department_Head_Assignment)
    return dict(grid = grid)

def get_managers_assignment():
    grid = SQLFORM.grid(db.Department_Head_Assignment)
    form = SQLFORM.factory(db.Department_Head_Assignment)
    if form.process().accepted:
        print 'RECORD SAVE'
    elif form.errors:
        print 'FORM HAS ERROR'        
    row = []
    thead = THEAD(TR(TH('Name'),TH('Department'),TH('Control Action')))
    for n in db().select(db.Department_Head_Assignment.ALL):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)        
        row.append(TR(TD(n.users_id.first_name.upper(),' ', n.users_id.last_name.upper() ),TD(n.sub_department_id.sub_department_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody],_class='table')
    return dict(form =form, table = table, grid = grid)

def get_users_group():
    grid = SQLFORM.grid(db.auth_group)
    return dict(grid = grid)
 
def get_users_group_member():
    grid = SQLFORM.grid(db.auth_membership)
    return dict(grid = grid)

def get_users_grid():
    # grid = SQLFORM.grid(db.auth_user)
    grid = db(db.auth_user).select(db.auth_user.ALL, db.auth_membership.ALL,orderby = db.auth_user.id, left = db.auth_user.on(db.auth_user.id == db.auth_membership.user_id))
    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Name'),TH('Group')))
    for n in grid:
        ctr+=1
        _name = n.auth_user.first_name, ' ', n.auth_user.last_name
        row.append(TR(TD(ctr),TD(_name),TD(n.auth_membership.group_id.role)))
    body = TBODY(*row)
    table = TABLE(*[head,body], _class='table')
    return dict(grid = table)

def get_employee_master_leave():
    grid = SQLFORM.grid(db.Employee_Master_Leave, orderby = ~db.Employee_Master_Leave.id)
    return dict(grid = grid)

def get_department_users_assignment_grid():
    grid = SQLFORM.grid(db.Department_Users_Assignment)
    return dict(grid = grid)

def get_back_office_assignment_grid():
    grid = SQLFORM.grid(db.Back_Office_Assignment)
    return dict(grid = grid)

def get_comm_tranx():
    grid = SQLFORM.grid(db.Employee_Master)
    return dict(grid = grid)

def get_sub_department_grid():
    grid = SQLFORM.grid(db.Sub_Department)
    return dict(grid = grid)

def get_employee_employment_details_grid():
    grid = SQLFORM.grid(db.Employee_Employment_Details)
    return dict(grid = grid)

def get_employee_master_account_info_grid():
    grid = SQLFORM.grid(db.Employee_Master_Account_Info)
    return dict(grid = grid)

def get_group_member():
    # 1 - MANAGEMENT
    # 3 - HR MANAGER
    _id = db(db.auth_membership.group_id == 1).select().first()    
    return dict()

def get_generate():
    print '--=--'
    for n in db(db.Employee_Master_Leave.status_id <= 10).select(orderby = db.Employee_Master_Leave.id):
        _mngr = db(db.Department_Head_Assignment.sub_department_id == n.manager_assigned).select().first()
        _to  = db(db.auth_user.id == _mngr.users_id).select().first()
        # if not _to:
        #     print 'not: ', n.id
        # else:
        if n.status_id == 1: # notify to department head
            print 'pending', n.id, n.type_of_leave_id, n.status_id.status, n.manager_assigned, _mngr.users_id
    return dict()

# def queue_task():
#     mysched.queue_task('demo1', prevent_drift = True, repeats = 0, period = 5)
# python web2py.py -K Merch_HR

def send_email_():
    # from gluon.tools import Mail
    # mail = Mail()
    # mail.settings.server = 'smtp.gmail.com:587'    
    # mail.settings.sender = 'merch.noreply@gmail.com'    
    # mail.settings.login = 'merch.noreply@gmail.com:45Password123' 
    # mail.settings.tls = 'smtp.tls'        
    mail.send(
        to='h.villar@merch.com.qa',           
        subject='HR WORKFLOW REMINDER',
        message = 'Welcome to the jungle!')


def send_email():
    from gluon.tools import Mail
    # from gluon.tools import Recaptcha2
    mail = Mail()
    _id = db(db.Email_Notification).select().first()    
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    # print _sender, _login
    # mail.settings.server = 'smtp.office365.com:587' or 'logging'
    mail.settings.server = 'smtp.gmail.com:587'    
    mail.settings.sender = _sender
    mail.settings.login = _login   

    # _id = db(db.auth_membership.group_id == 1).select().first()
    _id = db(db.auth_user.id == 3).select().first()
    _msg2 = "You have pending leave application required for your approval.\n\nPlease click this link http://128.1.2.2:3010/Merch_HR to access your HR workflow.\n\nNOTE: This is an auto-generated email. Please do not reply."
    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending leave application required for your approval.</p>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">Please click this link <a href="http://128.1.2.2:3010/Merch_HR">http://128.1.2.2:3010/Merch_HR</a> to access your HR workflow.</p>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """
    mail.send(
        # to=[_id.user_id.email],   
        to=['j.kumar@merch.com.qa'],        
        subject='HR WORKFLOW REMINDER',
        message = _msg)
    # mail.settings.tls = 'smtp.tls'
    return dict()
    
def put_salary_adjustment_send_mngr_email():
    from gluon.tools import Mail
    from gluon.tools import Recaptcha2
    mail = Mail()    
    _id = db(db.Email_Notification).select().first()    
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    
    mail.settings.server = 'smtp.gmail.com:587'    
    mail.settings.sender = _sender
    mail.settings.login = _login   
    _to = db(db.auth_membership.group_id == 1).select().first()   # testing 1 / change to 2 for management
    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending salary adjustment required for your approval.</p>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">Please click this link <a href="http://128.1.2.2:3010/Merch_HR/leave_mngt/get_salary_adjustment_grid/1">http://128.1.2.2:3010/Merch_HR</a> to access your HR workflow.</p>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """
    mail.send(
        to=[_id.user_id.email],   
        # to='j.massoud@merch.com.qa',   
        subject='HR WORKFLOW REMINDER',
        message = _msg)
    # mail.settings.tls = 'smtp.tls'
    return dict()

def get_email_notification_form():
    grid = SQLFORM.grid(db.Email_Notification)
    return dict(grid = grid)


from datetime import date, timedelta
import datetime
import locale

def overlap():
    _start = datetime.date(2020, 4, 1)
    _end = datetime.date(2020, 6, 30)    
    print '*', _start, _end, '<-- test'
    for n in db((db.Employee_Master_Leave.employee_id == 185) & (db.Employee_Master_Leave.id != 7481) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.from_effective_date):     
        if n.from_effective_date != None:
            if not(_end <= n.from_effective_date or _start >= n.to_effective_date):
                print n.id, n.from_effective_date, n.to_effective_date, 'overlap'                
            else:
                print n.id, n.from_effective_date, n.to_effective_date, 'not overlap'
        
def test():            
    _april = datetime.date(2020, 4, 1)
    # for n in db(db.Employee_Master_Leave.from_effective_date == _april).select():
    #     n.update_record(status_id = 1)        
    return dict(grid = SQLFORM.grid(db(db.Leave_Salary_Slip)))    

def queue_task():
    mysched.queue_task('demo1', prevent_drift = True, repeats = 0, period = 5)

def recompute():

    _april = datetime.date(2020, 5, 1)
    query = db(db.Employee_Master_Leave.status_id != 16).select()
    
    _emergency = 0 # 7707
    for n in db((db.Employee_Master_Leave.id == 7668) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select():
    # for n in db((db.Employee_Master_Leave.from_effective_date == _april) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select():
        _joi = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
        _no = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
        if n.type_of_leave_id == 5:
            if not _no.date_last_return > n.from_effective_date:
                _emergency += n.duration_leave or 0
        _working_days = n.from_effective_date - _no.date_last_return
        
        _working_days = _working_days - timedelta(int(_emergency or 0))    
        # print 'working days: ', n.id, _working_days.days, _emergency, _no.date_last_return, n.from_effective_date
        # _paid_leave_per_year = (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days / 365
        _paid_leave_per_year, _days = divmod((n.from_effective_date - _no.date_joined).days, 365)
        
        if _paid_leave_per_year >= 5:
            if _no.leave_days_per_year < 28:
                _paid_leave_per_year = 28                
                
            else:
                _paid_leave_per_year = _no.leave_days_per_year    
        else:
            _paid_leave_per_year = _no.leave_days_per_year
        _var2 = 0
        _var2 = (n.from_effective_date - _no.date_joined).days
        
        # print '_var2', _var2
        if _var2 < 366: 
            _var = 365 # one year
        else:
            _var = (365 - _paid_leave_per_year) # more than one year

        # print ': ', _no.date_joined.strftime('%Y-%m-%d'), datetime.strptime(request.vars.from_effective_date, '%d %b. %Y').date()
        # if _paid_leave_per_year < 2 :
        # print 'date joined: ', _no.date_joined, datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()
        if _no.date_joined == n.from_effective_date:
            # _paid_leave = ((_working_days / 365) * _paid_leave_per_year).days                    
            _var1 = (float(_working_days.days) / 365) * _paid_leave_per_year
            _paid_leave = int(round(_var1))      
            # print 'paid leave: ', _paid_leave
        else:                        
            # _paid_leave = ((_working_days / _var) * _paid_leave_per_year).days
            _var1 = (float(_working_days.days) / _var) * _paid_leave_per_year            
            _paid_leave = int(round(_var1))  

        n.update_record(working_days = _working_days.days, leave_days_per_year = _paid_leave_per_year, entitled_days = _paid_leave, last_joining_date = _joi.last_joining_date)
    return dict(query = SQLFORM.grid(db.Employee_Master_Leave.status_id != 16))

def leave_canceled():
    print '-- leave canceled --'
    for n in db(db.Employee_Master_Leave.deleted == True).select():
        print n.id
    return locals()

def test_export():
    import json
    import gluon.contrib.simplejson
    from datetime import date, datetime, timedelta
    row = []
    ctr = 0
    head = THEAD(TR(TH('employee_id')))
    table = TABLE(*[head], _class= 'table', _id='table')
    db.Employee_Master_Leave.employee_id.represent = lambda id,row: row.employee_id
    _salary = json.dumps(
        db(db.Employee_Master_Leave).select(
        db.Employee_Master_Leave.id,
        # _employee_id,
        db.Employee_Master_Leave.employee_id,
        db.Employee_Master_Leave.from_effective_date).as_list(), default = default)
    
    _query = db(db.Employee_Master_Leave.status_id == 16).select(db.Employee_Master_Leave.ALL, orderby = db.Employee_Master_Leave.id)
    _salary  =  response.json([(n.employee_id.first_name)for n in _query])         
    return dict(table = table, salary = XML(_salary))

def myconverter(o):
    if isinstance(o, datetime.date):
        return "{}-{}-{}".format(o.year, o.month, o.day)

def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def weekdays():
    names=['Sunday', 'Monday', 'Tuesday', 'Wednesday',
           'Thursday', 'Friday', 'Saturday']
    import gluon.contrib.simplejson

    return gluon.contrib.simplejson.dumps(names)

def test2():
    d1 = datetime.datetime(2005,9,11)
    d2 = datetime.datetime(2019,12,31)
    _avgyear  = 365.2425
    _avgmonth = 365.2425/12.0
    _years, _remainder = divmod((d2-d1).days, _avgyear)
    _years, _months = int(_years), int(_remainder // _avgmonth)
    print _years, _months, _remainder
    func(1)
    return dict()

def func(z):
    def func1(x):
        x = 10
        return x
    def func2(y):
        y = 20        
        return y

    if z == 1:
        num2 = func1(z)
    else:
        num2 = func2(z)
    print 'func(z)', num2
    
    



# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    # redirect(URL('default','test'))
    # auth.login(next=redirect('http://10.128.4.21:3010/Merch_HR/'))
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """

    return dict(form=auth())
    # return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

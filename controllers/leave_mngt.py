# ------------------------------------------------------------------------------------------
# -------  L E A V E & A P P L I C A T I O N  M A N A G E M E N T   S Y S T E M  -----------
# ------------------------------------------------------------------------------------------
from gluon.tools import Mail
from gluon.tools import Recaptcha2
mail = Mail()
import string
import random
from datetime import date, datetime, timedelta
import locale
from fractions import Fraction
# from dateutil import relativedelta

locale.setlocale(locale.LC_ALL, '')
def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def get_leave_status_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Status'),TH('Action Required'),TH('Description'),TH('Action')))
    for n in db().select(db.Leave_Status.ALL, orderby=db.Leave_Status.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('leave_mngt','put_leave_status_id', args = n.id))) #callback = URL(args = n.status), **{'_data-id':(n.id),'_data-sta':(n.status), '_data-des':(n.description)})
        # edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle edit', callback = URL(args = n.status), **{'_data-id':(n.id),'_data-sta':(n.status), '_data-des':(n.description)})
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.action_required),TD(n.description),TD(btn_lnk), _class='stat'))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblls', _class='table')
    
    form = SQLFORM(db.Leave_Status)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form=form, table=table)

def post_leave_status():
    form = SQLFORM(db.Leave_Status)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        redirect(URL('leave_mngt','get_leave_status_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form=form)

def put_leave_status_id():
    form = SQLFORM(db.Leave_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        redirect(URL('leave_mngt','get_leave_status_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form=form)

def put_leave_status_updated():
    _id = db(db.Leave_Status.status == request.vars.status).select().first()
    if _id:
        _id.update(status = request.vars.status, description = request.vars.description)
        print 'updated', request.vars.status, request.vars.description
    else:
        print 'save'

def get_salary_adjustment_status_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Status'),TH('Action Required'),TH('Description'),TH('Action')))
    for n in db().select(db.Salary_Adjustment_Status.ALL, orderby=db.Salary_Adjustment_Status.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('leave_mngt','put_salary_adjustment_status_id', args = n.id))) #callback = URL(args = n.status), **{'_data-id':(n.id),'_data-sta':(n.status), '_data-des':(n.description)})        
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.action_required),TD(n.description),TD(btn_lnk), _class='stat'))
    body = TBODY(*row)
    table = TABLE(*[head, body], _id='tblsas', _class='table')
    
    form = SQLFORM(db.Salary_Adjustment_Status)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        response.js = "jQuery(console.log('success'))"
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form=form, table=table)

def put_salary_adjustment_status_id():
    form = SQLFORM(db.Salary_Adjustment_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'      
        redirect(URL('leave_mngt','get_salary_adjustment_status_grid'))  
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def get_type_leave_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Type'),TH('Description'),TH('Action')))
    for n in db(db.Type_Leave).select(orderby = db.Type_Leave.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_type_leave_id', args = n.id))            
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))                    
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.type_of_leave),TD(n.description),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table=table)

def post_type_leave():
    form = SQLFORM(db.Type_Leave)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        redirect(URL('leave_mngt','get_type_leave_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def put_type_leave_id():
    form = SQLFORM(db.Type_Leave, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        redirect(URL('leave_mngt','get_type_leave_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def put_check_overlap_id(form):    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if _id:
        for n in db((db.Employee_Master_Leave.id != request.args(0)) & (db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.id): 
            if n.from_effective_date == None:
                y = 0
            else:
                if (datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date() < n.from_effective_date) or (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() > n.to_effective_date):              
                    x = 0  
                    # print n.id, n.from_effective_date, n.to_effective_date, 'not overlap'
                else:
                    form.errors.from_effective_date = 'Overlapping date not allowed.' 
                    # print n.id, n.from_effective_date, n.to_effective_date, 'overlap'


def put_validate_application(form):
    _today = date.today()
    # print 'pass', request.vars.employee_id, request.vars.type_of_leave_id, request.vars.from_effective_date, request.vars.to_effective_date
    # _app = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & ((db.Employee_Master_Leave.from_effective_date == request.vars.from_effective_date) | (db.Employee_Master_Leave.to_effective_date == request.vars.to_effective_date))).select().first()
    _app = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.from_effective_date).first()
    _query = (db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False) &(db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id)
    # _usr = db(db.Employee_Managers_Assignment.users_id == auth.user_id).select().first()
    _joi = db(db.Employee_Employment_Details.employee_id == request.vars.employee_id).select().first()
    _sum = db.Employee_Master_Leave.duration_leave.sum()
    _number_of_days_worked = datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _joi.date_joined
    _pending = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id <= 9) & (db.Employee_Master_Leave.canceled == False)).select(_sum).first()[_sum]    
        
    if int(request.vars.type_of_leave_id) == 1: # annual leave
        put_check_overlap_id(form)

    elif int(request.vars.type_of_leave_id) == 2: # compassionate leave
        put_check_overlap_id(form)
        # if int(_number_of_days_worked.days) <= int(365):
        _count = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == 2) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.canceled == False)).select(_sum).first()[_sum]
        
        _current_days = int(_count or 0) + float(request.vars.duration_leave)
        # if (request.now.date() < datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()) or (request.now.date() < datetime.strptime(request.vars.to_effective_date, '%Y-%m-%d').date()):
        #     form.errors.from_effective_date = 'Compassionate leave should on days forward.'

        if float(request.vars.duration_leave) > 3:
            form.errors.duration_leave = 'Duration leave must not more than 3 days.'                
        elif int(_current_days) > 3:
            _balanced = 3 - int(_count)
            form.errors.duration_leave = 'Balanced remaining is ' + str(_balanced)
        # elif _pending >= 1:
        #     form.errors.type_of_leave_id = 'Pending application exist.'
        # elif datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()


    elif int(request.vars.type_of_leave_id) == 3: # sick leave
        put_check_overlap_id(form)
        # for n in db(_query).select(orderby = ~db.Employee_Master_Leave.from_effective_date):
            
        #     if (n.from_effective_date == datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()) and (n.to_effective_date == datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date()):
        #         form.errors.from_effective_date = 'already exist'
        #         # print n.id, ' alread exist'
        #     # elif not (n.to_effective_date < datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()) or (n.from_effective_date > datetime.strptime(request.vars.to_effective_date, '%Y-%m-%d').date()):
        #     #     form.errors.from_effective_date = 'overlap not allowed'

    elif int(request.vars.type_of_leave_id) == 4: # business leave
        put_check_overlap_id(form)
        

    elif int(request.vars.type_of_leave_id) == 5: # emergency leave
        put_check_overlap_id(form)

    elif int(request.vars.type_of_leave_id) == 6: # maternity leave
        put_check_overlap_id(form)
        # print 'maternity leave' ,(datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _joi.date_joined).days, 365

        if int((datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _joi.date_joined).days) <= int(365):
            # print 'Not entitled for maternity leave.'
            form.errors.from_effective_date = 'Not entitled for maternity leave.'
        # else:
        #     print 'entitled'
        #     form.vars.duration_leave = 50

    
    elif int(request.vars.type_of_leave_id) == 7: # day of excess
        put_check_overlap_id(form)
    
    form.vars.manager_assigned = int(_joi.sub_department_code_id)
    form.vars.leave_days_per_year = session.paid_leave_per_year
    form.vars.working_days = session.working_days
    form.vars.entitled_days = session.paid_leave
    form.vars.last_joining_date = _joi.last_joining_date

def check_overlap(form):
    _app = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.from_effective_date).first()    
    if _app:
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.from_effective_date):    
            if n.from_effective_date == None: # print n.id, n.from_effective_date, n.to_effective_date
                y = 0
            else:
                if (datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date() < n.from_effective_date) or (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() > n.to_effective_date):              
                    x = 0  # print n.id, n.from_effective_date, n.to_effective_date, 'not overlap'
                else:
                    form.errors.from_effective_date = 'Overlapping date not allowed.' # print n.id, n.from_effective_date, n.to_effective_date, 'overlap'

def validate_application(form):
    _today = date.today()
    _app = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.from_effective_date).first()
    _query = (db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False) &(db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id)
    _joi = db(db.Employee_Employment_Details.employee_id == request.vars.employee_id).select().first()
    _sum = db.Employee_Master_Leave.duration_leave.sum()
    _number_of_days_worked = datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _joi.date_joined
    _pending = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id <= 9) & (db.Employee_Master_Leave.canceled == False)).select(_sum).first()[_sum]    
       
    # if _app:
    #     for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.canceled == False)).select(orderby = db.Employee_Master_Leave.from_effective_date):    
    #         if n.from_effective_date == None: # print n.id, n.from_effective_date, n.to_effective_date
    #             y = 0
    #         else:
    #             if (datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date() < n.from_effective_date) or (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() > n.to_effective_date):              
    #                 x = 0  # print n.id, n.from_effective_date, n.to_effective_date, 'not overlap'
    #             else:
    #                 form.errors.from_effective_date = 'Overlapping date not allowed.' # print n.id, n.from_effective_date, n.to_effective_date, 'overlap'
    if _pending >= 1:
        form.errors.type_of_leave_id = 'Pending application exists.'

    if int(request.vars.type_of_leave_id) == 1: # annual leave        
        check_overlap(form)
        # if (request.now.date() < datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()) or (request.now.date() < datetime.strptime(request.vars.to_effective_date, '%Y-%m-%d').date()):
        #     form.errors.from_effective_date = 'Annual leave should on days forward.'

    elif int(request.vars.type_of_leave_id) == 2: # compassionate leave
        check_overlap(form)
        # if int(_number_of_days_worked.days) <= int(365):
        _count = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == 2) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.canceled == False)).select(_sum).first()[_sum]
        
        _current_days = int(_count or 0) + float(request.vars.duration_leave)
        # if (request.now.date() < datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()) or (request.now.date() < datetime.strptime(request.vars.to_effective_date, '%Y-%m-%d').date()):
        #     form.errors.from_effective_date = 'Compassionate leave should on days forward.'

        if float(request.vars.duration_leave) > 3:
            form.errors.duration_leave = 'Duration leave must not more than 3 days.'                
        elif int(_current_days) > 3:
            _balanced = 3 - int(_count)
            form.errors.duration_leave = 'Balanced remaining is ' + str(_balanced)
        elif _pending >= 1:
            form.errors.type_of_leave_id = 'Pending application exist.'
        # elif datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()


    elif int(request.vars.type_of_leave_id) == 3: # sick leave
        check_overlap(form)
        for n in db(_query).select(orderby = ~db.Employee_Master_Leave.from_effective_date):            
            if (n.from_effective_date == datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()) and (n.to_effective_date == datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date()):
                form.errors.from_effective_date = 'already exist'

    elif int(request.vars.type_of_leave_id) == 4: # business leave
        check_overlap(form)
        # if (request.now.date() < datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date()) or (request.now.date() < datetime.strptime(request.vars.to_effective_date, '%Y-%m-%d').date()):
        #     form.errors.from_effective_date = 'Business leave should on days forward.'

        for n in db(_query).select(orderby = ~db.Employee_Master_Leave.from_effective_date):
            if (n.from_effective_date == datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()) and (n.to_effective_date == datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date()):
                form.errors.from_effective_date = 'already exist'
                # print n.id, ' alread exist'
            elif not (n.to_effective_date < datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()) or (n.from_effective_date > datetime.strptime(request.vars.to_effective_date, '%m-%d-%Y').date()):
                form.errors.from_effective_date = 'overlap not allowed'

    elif int(request.vars.type_of_leave_id) == 5: # emergency leave
        check_overlap(form)

    elif int(request.vars.type_of_leave_id) == 6: # maternity leave
        check_overlap(form)

        if int((datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _joi.date_joined).days) <= int(365):
            form.errors.from_effective_date = 'Not entitled for maternity leave.'

    
    elif int(request.vars.type_of_leave_id) == 7: # day of excess
        check_overlap(form)
    
    form.vars.manager_assigned = int(_joi.sub_department_code_id)
    form.vars.leave_days_per_year = session.paid_leave_per_year
    form.vars.working_days = session.working_days
    form.vars.entitled_days = session.paid_leave
    form.vars.last_joining_date = _joi.last_joining_date 

@auth.requires_login()
def post_application_leave():      

    ctr = db(db.Employee_Master_Leave.id).count()    
    ctr = str(datetime.now().year) +'-' + str(ctr+1)
    _usr = db(db.Department_Users_Assignment.users_id == auth.user_id).select().first()
    
    if not _usr:
        _user = 0
        _assi = 0
    else: 
        _user = _usr.employee_id
        _assi = _usr.sub_department_id
    
    if auth.has_membership(role = 'BACK OFFICE DEPARTMENT'):               
        _default_status = 1
        _status = db.Leave_Status.id == 1
        _leave =  (db.Type_Leave.id != 8) & (db.Type_Leave.id != 9) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _bof = db(db.Back_Office_Assignment.users_id == auth.user_id).select().first()
        _employee_id = (db.Employee_Employment_Details.back_office_code_id == _bof.back_office_code_id) & (db.Employee_Master.id == db.Employee_Employment_Details.employee_id) & (db.Employee_Master.employee_status_id == 1)
        _replacement = (db.Employee_Employment_Details.back_office_code_id == _bof.back_office_code_id) & (db.Employee_Master.id == db.Employee_Employment_Details.employee_id) & (db.Employee_Master.employee_status_id == 1)
        _default_employee = int(_bof.employee_id)               
        db.Employee_Master_Leave.replacement.requires = IS_EMPTY_OR(IS_IN_DB(db(_replacement), db.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Name'))  
    elif auth.has_membership(role = 'DEPARTMENT MANAGERS'):        
        _default_status = 4
        _status = db.Leave_Status.id == 4   
        _leave =  (db.Type_Leave.id != 8) & (db.Type_Leave.id != 9) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _employee_id = db.Employee_Master.id == _usr.employee_id
        _default_employee = int(_usr.employee_id)   
        # _replacement = (db.Employee_Employment_Details.back_office_code_id == _bof.back_office_code_id) & (db.Employee_Master.id == db.Employee_Employment_Details.employee_id) & (db.Employee_Master.employee_status_id == 1)
        # get_leave_history_id(int(_usr.employe_id))
    elif auth.has_membership(role = 'ACCOUNTS'):
        _default_status = 1
        _status = db.Leave_Status.id == 1
        _leave =  (db.Type_Leave.id != 8) & (db.Type_Leave.id != 9) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _employee_id = db.Employee_Master.id == _usr.employee_id
        _default_employee = int(_usr.employee_id)   
    elif auth.has_membership(role = 'ADMINISTRATION MANAGER'):        
        _status = db.Leave_Status.id == 1  
        # _leave =  (db.Type_Leave.id != 8) &  (db.Type_Leave.id != 9)        
        _leave =  (db.Type_Leave.id >= 1) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _employee_id = db.Employee_Master.employee_status_id == 1
        _default_employee = int(_usr.employee_id)             
        _default_status = 1
    elif auth.has_membership(role = 'HR MANAGER'):
        _status = db.Leave_Status.id == 7  
        _default_status = 7             
        _status = db.Leave_Status.id == 7   
        _leave =  (db.Type_Leave.id >= 1) & (db.Type_Leave.id != 11) 
        _employee_id = db.Employee_Master.employee_status_id == 1
        _default_employee = int(_usr.employee_id)   
    elif auth.has_membership(role='MANAGEMENT'):
        _default_status = 4
        _status = db.Leave_Status.id == 4
        _leave =  (db.Type_Leave.id <= 9) & (db.Type_Leave.id != 11) 
        _employee_id = db.Employee_Master.id == _usr.employee_id
        _default_employee = int(_usr.employee_id)
    else: # auth.has_membership(role='DEPARTMENT USERS'):
        _status = db.Leave_Status.id == 1             #(db.Leave_Status.id != 8) & (db.Leave_Status.id != 9)
        _default_status = 1
        _leave =  (db.Type_Leave.id != 8) & (db.Type_Leave.id != 9) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _employee_id = db.Employee_Master.id == _usr.employee_id
        _default_employee = int(_usr.employee_id) 
    db.Employee_Master_Leave.employee_id.requires = IS_IN_DB(db(_employee_id), db.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Name') 
    db.Employee_Master_Leave.employee_id.default = _default_employee
    # db.Employee_Master_Leave.replacement.requires = IS_EMPTY_OR(IS_IN_DB(db(_replacement), db.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Name')) 
    db.Employee_Master_Leave.type_of_leave_id.requires = IS_IN_DB(db(_leave), db.Type_Leave.id, '%(type_of_leave)s', zero = 'Choose Type')
    db.Employee_Master_Leave.status_id.requires = IS_IN_DB(db(_status), db.Leave_Status.id, '%(status)s', zero = 'Choose Status')
    db.Employee_Master_Leave.from_effective_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Employee_Master_Leave.to_effective_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Employee_Master_Leave.duration_leave.default = 1
    db.Employee_Master_Leave.status_id.default = _default_status
    db.Employee_Master_Leave.date_returned.writable = False
    form = SQLFORM(db.Employee_Master_Leave)
    if form.process(onvalidation = validate_application).accepted:                
        if auth.has_membership(role = 'DEPARTMENT MANAGERS'):
            redirect(URL('leave_mngt','get_application_dept_leave_grid'))
        elif auth.has_membership(role = 'HR MANAGER'):
            redirect(URL('leave_mngt','get_application_hr_leave_grid'))
        elif auth.has_membership(role = 'MANAGEMENT'):
            redirect(URL('leave_mngt','get_application_mngt_leave_grid'))
        elif auth.has_membership(role = 'BACK OFFICE DEPARTMENT'):            
            _usr = db(db.Back_Office_Assignment.users_id == auth.user_id).select().first()            
            _dha = db((db.Department_Head_Assignment.back_office_code_id == _usr.back_office_code_id) & (db.Department_Head_Assignment.status_id == 1)).select().first()
            _to  = db(db.auth_user.id == _dha.users_id).select().first()
            _eml = db(db.Email_Notification).select().first()
            _sender = _eml.email_notification
            _login = str(_eml.email_notification) + str(':') + str(_eml.email_password)
            mail.settings.server = 'smtp.gmail.com:587'            
            mail.settings.sender = _sender
            mail.settings.login = _login
            _msg = """\
                    <html>
                    <head></head>
                    <body>
                        <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending leave application required for your approval.</p>                        
                        <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
                    </body>
                    </html>
                    """
            mail.send(
                to=[_to.email],
                subject='HR WORKFLOW REMINDER',
                message = _msg)                   
            redirect(URL('leave_mngt','get_application_leave_grid'))     
            # else:
            #     redirect(URL('leave_mngt','get_application_leave_grid'))                
        # db.User_Log.insert(
        #     activities = 'applied for % ' % (form.vars.type_of_leave_id)
        # )            
        else:            
            _dha = db((db.Department_Head_Assignment.sub_department_id == form.vars.manager_assigned) & (db.Department_Head_Assignment.status_id == 1)).select().first()
            _to  = db(db.auth_user.id == _dha.users_id).select().first()
            _eml = db(db.Email_Notification).select().first()
            _sender = _eml.email_notification
            _login = str(_eml.email_notification) + str(':') + str(_eml.email_password)

            # mail.settings.server = 'smtp.office365.com:587' or 'logging'
            mail.settings.server = 'smtp.gmail.com:587'
            mail.settings.sender = _sender
            mail.settings.login = _login
            # mail.settings.server = 'smtp.gmail.com:587'
            # mail.settings.sender = 'merch.noreply@gmail.com'
            # mail.settings.login = 'merch.noreply@gmail.com:45Password123' # 45Password123
            # mail.settings.tls = 'smtp.tls'                
            _msg = """\
                    <html>
                    <head></head>
                    <body>
                        <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending leave application required for your approval.</p>                        
                        <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
                    </body>
                    </html>
                    """
            mail.send(
                to=[_to.email],
                subject='HR WORKFLOW REMINDER',
                message = _msg)                   
            redirect(URL('leave_mngt','get_application_leave_grid'))
            response.js = 'jQuery(toastr.success("Application submitted"))' 
    elif form.errors:        
        response.js = 'jQuery(toastr.warning("%s"))' % TABLE(*[TR(v) for k, v in form.errors.items()])
        # print form.errors
    return dict(form = form, ctr = ctr)    

def get_application_his_id_():
    if not request.vars.employee_id:
        print 'None'
        _table_id = 'None'
    else:
        print 'leave: ', request.vars.employee_id
        _table_id = request.vars.employee_id
    return XML(DIV(_table_id))

def get_application_history_id(): #form entry       
     
    _tl = db(db.Type_Leave.id == request.vars.type_of_leave_id).select().first()
    
    _id = db(db.Employee_Master.id == request.vars.employee_id).select().first()
    _no = db(db.Employee_Employment_Details.employee_id == request.vars.employee_id).select().first()
    
    _sum = db.Employee_Master_Leave.duration_leave.sum()
    _count = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id)).select(_sum).first()[_sum]
    _appli = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id < 16)).select(_sum).first()[_sum]
    _ctr = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id <= 9)).count()
    _pending = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id <= 9)).count()
    
    if not ((_count) or (_appli)):
        _count = _appli = 0 
    _balanced = _paid_leave = 0
    
    _title = str(_tl.type_of_leave) + ' Information'         
    # print _title
    _table_id = DIV(TABLE(TBODY(TR(TH('Card Name'),TH('Card #'),TH('Date Issued'),TH('Date Expiration')),
    TR(TD('Residence Permit'),TD(_id.residence_permit_no),TD(_id.residence_no_date),TD(_id.residence_permit_no_expiration_date)),
    TR(TD('Passport'),TD(_id.passport_no),TD(_id.passport_date_issued),TD(_id.passport_date_expiration)),
    TR(TD('Health Card'),TD(_id.health_card_no),TD(),TD(_id.health_card_no_expiration_date)),
    TR(TD('Driver License'),TD(_id.driver_license_no),TD(),TD(_id.driver_license_no_expiration_date))),_class='table'),_class='info-box bg-green')    
    _emergency = 0
    if int(request.vars.type_of_leave_id) == 1 or int(request.vars.type_of_leave_id) == 8 or int(request.vars.type_of_leave_id) == 9:# annual leave, resignation, end of services
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.type_of_leave_id == 5)).select():            
            # print ':', n.id, _no.date_last_return, n.from_effective_date, n.duration_leave
            if n.from_effective_date > _no.last_joining_date:
                _emergency += n.duration_leave or 0
            # if not _no.date_last_return > n.from_effective_date:
            #     _emergency += n.duration_leave or 0
            # else:
            #     _emergency += n.duration_leave or 0
        
        _working_days = datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.last_joining_date
        
        _working_days = _working_days - timedelta(int(_emergency or 0))    
        
        # _paid_leave_per_year = (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days / 365
        _paid_leave_per_year, _days = divmod((datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days, 365)
        
        x = _no.date_joined + timedelta(int(365 * 5))
        _year5 = 0
        # print 'paid leave: ', _paid_leave_per_year, x, _no.date_joined
        if _paid_leave_per_year >= 5:            
            if _paid_leave_per_year == 5:
                _working_days_1 =  x - _no.date_last_return
                _working_days_1 = _working_days_1 - timedelta(int(_emergency or 0))                   

                _working_days_2 =  datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - x
                # _working_days_2 = _working_days_2 - timedelta(int(_emergency or 0))
                # _var1 = (float(_working_days.days) / _var) * _paid_leave_per_year
                _paid_leave_21 = (float(_working_days_1.days) / (365 - 21)) * 21
                _paid_leave_28 = (float(_working_days_2.days) / (365 - 28)) * 28
                # print  ':', round(_paid_leave_21 + _paid_leave_28)
                _year5 = 1
                

            if _no.leave_days_per_year < 28:
                _paid_leave_per_year = 28                
                
            else:
                _paid_leave_per_year = _no.leave_days_per_year    
            
        else:
            _paid_leave_per_year = _no.leave_days_per_year
            
        _var2 = 0
        _var2 = (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days
        # print '_var2', _var2
        if _var2 < 366: 
            _var = 365 # one year
        else:
            _var = (365 - _paid_leave_per_year) # more than one year
        
        # print ': ', _no.date_joined.strftime('%Y-%m-%d'), datetime.strptime(request.vars.from_effective_date, '%d %b. %Y').date()
        # if _paid_leave_per_year < 2 :
        # print 'date joined: ', _no.date_joined, datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()
        if _year5 == 1:
            _paid_leave = int(round(_paid_leave_21 + _paid_leave_28))
        else:

            if _no.date_joined.strftime('%Y-%m-%d') == datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date():
                # _paid_leave = ((_working_days / 365) * _paid_leave_per_year).days                    
                _var1 = (float(_working_days.days) / 365) * _paid_leave_per_year
                _paid_leave = int(round(_var1))      
            else:                        
                # _paid_leave = ((_working_days / _var) * _paid_leave_per_year).days
                _var1 = (float(_working_days.days) / _var) * _paid_leave_per_year            
                _paid_leave = int(round(_var1))  
                # print 'paid: --> ', float(_working_days.days), _var, int(round(_var1)), _paid_leave_per_year
        
        if (_no.date_last_return == _no.date_joined) and (_working_days.days < 365):
            _proportionate = T('Proportional Air ticket covering %s %%{day} of service.', _working_days.days)            
        elif _no.date_last_return != _no.date_joined:
            if _paid_leave_per_year == 21:                
                _x = 365 - 21                
                _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _working_days.days)
            elif _paid_leave_per_year == 28:
                _x = 365 - 28                
                if int(_working_days.days) < int(_x):                    
                    _proportionate = T('Proportional Air ticket covering %s %%{day} of service.', _working_days.days)
                else:                    
                    _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _working_days.days)
            elif _paid_leave_per_year == 30:
                _x = 365 - 30                
                _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _working_days.days)
            else:
                _proportionate = T('')
        else:
            _proportionate = T('')        
        _row2 = TABLE(TBODY(TR(TD('Paid Leave:'),TD(T('%s %%{day}',_paid_leave)),TD('Total Working Days:'),TD(T('%s %%{day}',_working_days.days))),
        TR(TD('Paid Leave/Year:'),TD(T('%s %%{day}',_paid_leave_per_year)),TD('Total Emergency Leave:'),TD(T('%s %%{day}',locale.format('%d', _emergency or 0, grouping = True)))),
        TR(TD('Last Joining Date:'),TD(_no.last_joining_date.strftime('%d %b. %Y')),TD('Engagement Date:'),TD(_no.date_joined.strftime('%d %b. %Y'))),
        TR(TD('Air Ticket:'),TD(_no.air_fare,_colspan='3')),
        TR(TD('Remarks:'),TD('To deduct absent days if any from the monthly salary',_colspan='3')),
        TR(TD(),TD('Economy Class Air ticket: ' + str(_no.sector),_colspan='3')), 
        TR(TD(),TD(_proportionate,_colspan='3')),         
        TR(TD('Note: This leave will be paid leave.',_colspan='4'))), _class='table')        
        _table_id = _table_id

        session.working_days = _working_days.days 
        session.paid_leave_per_year = _paid_leave_per_year
        session.paid_leave = _paid_leave
        # print _working_days.days, _paid_leave
    elif int(request.vars.type_of_leave_id) == 2: # Compassionate Leave
        _applied = 0
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.from_effective_date > _no.last_joining_date) & (db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.type_of_leave_id == 2)).select(orderby = ~db.Employee_Master_Leave.id):
            _applied += n.duration_leave or 0
            _balanced = float(3.0) - float(_applied or 0)        
            # print ': ', n.id, n.duration_leave, n.status_id, _applied, _balanced
        _row2 = TABLE(TBODY(TR(TH('Total paid compassionate leave/year'),TH('Availed (including this leave)'),TH('Balance entitlement for the year'),TH('Pending Application')),
        TR(TD('3 days'),TD(_applied, ' days'),TD(_balanced,' days'),TD(_pending or 0)),
        # TR(TD('3 days'),TD(T('%s %%{day}',locale.format('%d', _appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d', _balanced or 0, grouping = True))),TD(_pending or 0)),
        TR(TD('Note: This leave will be paid leave.'),TD(),TD(),TD())), _class='table')
        _table_id = ''        

    elif int(request.vars.type_of_leave_id) == 3: # Sick Leave
        # print 'sick leave: '
        # print request.vars.employee_id, _no.last_joining_date, request.vars.type_of_leave_id
        _applied = 0
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.from_effective_date > _no.last_joining_date) & (db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.type_of_leave_id == 3)).select(orderby = ~db.Employee_Master_Leave.id):        
            _applied += n.duration_leave or 0
            # print ': ', n.id, n.from_effective_date, _no.last_joining_date, n.from_effective_date > _no.last_joining_date
        _applied =  float(_applied or 0) + float(request.vars.duration_leave or 0)
        _balanced = 14 - int(_applied or 0)
        if _applied > 14:
            _half_paid = int(_applied or 0) - 14
        else:
            _half_paid = 0
        _row2 = TABLE(TBODY(TR(TH('Total Paid Sick Leave/Year'),TH('Availed (including this leave)'),TH('Balanced Remaining'),TH('Paid Leave'),TH('Half Paid Leave')),
        TR(TD('14 days'),TD(T('%s %%{day}',locale.format('%d',_applied or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_balanced or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_count or 0, grouping = True))), TD(T('%s %%{day}',locale.format('%d',_half_paid or 0, grouping = True)))),
        TR(TD('Note: This leave will be paid leave.',_colspan='5'))),_class='table')
        
        _table_id = _table_id
        
    elif int(request.vars.type_of_leave_id) == 4: # Business Leave
        
        _row2 = TABLE(TBODY(TR(TH('Leave Applied For'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(_pending))),_class='table')
        _table_id = _table_id

    elif int(request.vars.type_of_leave_id) == 5: # Emergency Leave
        
        _row2 = TABLE(TBODY(TR(TH('Leave Applied For'),TH('Availed (including this leave)'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(_pending))),_class='table')
        _table_id = _table_id

    elif int(request.vars.type_of_leave_id) == 6: # Maternity Leave
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.type_of_leave_id == 5)).select():            
            if not _no.date_last_return > n.from_effective_date:
                _emergency += n.duration_leave or 0
        _working_days = datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_last_return

        _working_days = _working_days - timedelta(int(_emergency or 0))    
        session.working_days = _working_days.days         
        session.paid_leave = 50
        
        
        _row2 = TABLE(TBODY(TR(TH('Total Paid Maternity Leave/Year'),TH('Pending')),
        TR(TD('50 days'),TD(locale.format('%d',_pending or 0, grouping = True)))),_class='table')
        _table_id = _table_id

    elif int(request.vars.type_of_leave_id) == 7: # Day Off(Excess Hours)
        
        _row2 = TABLE(TBODY(TR(TH('Total Excess Hours applied (including this leave)'),TH('Availed (including this leave)'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d', _count or 0, grouping = True))),TD(_pending)),
        TR(TD('Note: This leave will be paid leave.'),TD(),TD())),_class='table')
        _table_id = ''
    if _id.middle_name == None:
        _middle_name = 'None'
    else:
        _middle_name = _id.middle_name.upper()
    return XML(DIV(
        DIV(
            DIV(SPAN(I(_class='fa fa-user-o'),_class='info-box-icon'),
            DIV(SPAN(_title,_class='info-box-text'),SPAN(_id.first_name.upper(),' ', _middle_name, ' ', _id.last_name.upper(), ', ' ,_no.account_code,_class='info-box-number'),
            DIV(B(str(_no.designation_code_id.designation_name)) + str(', ') + str(_no.department_code_id.department_name)),
            _class='info-box-content'),_class='info-box bg-yellow'),
            DIV(_table_id),
            _class="col-md-6 col-sm-6 col-sx-6"),
        DIV(
            DIV(SPAN(I(_class='fa fa-calendar'),_class='info-box-icon'),DIV(_row2,
            _class='info-box-content'),_class='info-box bg-light-blue-active'),_class="col-md-6 col-sm-6 col-sx-6")        
    ))

def put_application_history_id_():    
    print 'put_application_history_id::', request.args(0), request.vars.employee_id, request.vars.type_of_leave_id,request.vars.from_effective_date
    return XML(DIV(request.vars.type_of_leave_id))

def put_application_history_id(): #form update      
    _tl = db(db.Type_Leave.id == request.vars.type_of_leave_id).select().first()
    _id = db(db.Employee_Master.id == request.vars.employee_id).select().first()
    _no = db(db.Employee_Employment_Details.employee_id == request.vars.employee_id).select().first()
    
    _sum = db.Employee_Master_Leave.duration_leave.sum()
    _count = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id)).select(_sum).first()[_sum]
    _appli = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id < 11)).select(_sum).first()[_sum]
    _ctr = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id <= 9)).count()
    _pending = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id <= 9)).count()
    
    if not ((_count) or (_appli)):
        _count = _appli = 0 
    _balanced = _paid_leave = 0
    _title = _tl.type_of_leave, ' Information'         
    _table_id = DIV(TABLE(TBODY(TR(TH('Card Name'),TH('Card #'),TH('Date Issued'),TH('Date Expiration')),
    TR(TD('Residence Permit'),TD(_id.residence_permit_no),TD(_id.residence_no_date),TD(_id.residence_permit_no_expiration_date)),
    TR(TD('Passport'),TD(_id.passport_no),TD(_id.passport_date_issued),TD(_id.passport_date_expiration)),
    TR(TD('Health Card'),TD(_id.health_card_no),TD(),TD(_id.health_card_no_expiration_date)),
    TR(TD('Driver License'),TD(_id.driver_license_no),TD(),TD(_id.driver_license_no_expiration_date))),_class='table'),_class='info-box bg-green')    
    _emergency = 0
    if int(request.vars.type_of_leave_id) == 1 or int(request.vars.type_of_leave_id) == 8 or int(request.vars.type_of_leave_id) == 9:# annual leave   
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.type_of_leave_id == 5)).select():            
            if not _no.date_last_return > n.from_effective_date:
                _emergency += n.duration_leave or 0
        _working_days = datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_last_return
        
        _working_days = _working_days - timedelta(int(_emergency or 0))    
        
        # _paid_leave_per_year = (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days / 365
        _paid_leave_per_year, _days = divmod((datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days, 365)
        
        if _paid_leave_per_year >= 5:
            if _no.leave_days_per_year < 28:
                _paid_leave_per_year = 28                
                
            else:
                _paid_leave_per_year = _no.leave_days_per_year    
        else:
            _paid_leave_per_year = _no.leave_days_per_year
        _var2 = 0
        _var2 = (datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_joined).days
        # print '_var2', _var2
        if _var2 < 366: 
            _var = 365 # one year
        else:
            _var = (365 - _paid_leave_per_year) # more than one year
        
        # print ': ', _no.date_joined.strftime('%Y-%m-%d'), datetime.strptime(request.vars.from_effective_date, '%d %b. %Y').date()
        # if _paid_leave_per_year < 2 :
        # print 'date joined: ', _no.date_joined, datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date()
        if _no.date_joined.strftime('%Y-%m-%d') == datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date():
            # _paid_leave = ((_working_days / 365) * _paid_leave_per_year).days                    
            _var1 = (float(_working_days.days) / 365) * _paid_leave_per_year
            _paid_leave = int(round(_var1))      
            # print 'paid leave: ', _paid_leave
        else:                        
            # _paid_leave = ((_working_days / _var) * _paid_leave_per_year).days
            _var1 = (float(_working_days.days) / _var) * _paid_leave_per_year            
            _paid_leave = int(round(_var1))  
            # print 'paid leave: else: ', _paid_leave          
            # print 'paid: --> ', float(_working_days.days), _var, int(round(_var1)), _paid_leave_per_year
        
        if (_no.date_last_return == _no.date_joined) and (_working_days.days < 365):
            _proportionate = T('Proportional Air ticket covering %s %%{day} of service.', _working_days.days)            
        elif _no.date_last_return != _no.date_joined:
            if _paid_leave_per_year == 21:                
                _x = 365 - 21
                _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _working_days.days)
            elif _paid_leave_per_year == 28:
                _x = 365 - 28
                if int(_working_days.days) < int(_x):
                    _proportionate = T('Proportional Air ticket covering %s %%{day} of service.', _working_days.days)
                else:
                    _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _working_days.days)
            elif _paid_leave_per_year == 30:
                _x = 365 - 30
                _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _working_days.days)
        _row2 = TABLE(TBODY(TR(TD('Paid Leave:'),TD(T('%s %%{day}',_paid_leave)),TD('Total Working Days:'),TD(T('%s %%{day}',_working_days.days))),
        TR(TD('Paid Leave/Year:'),TD(T('%s %%{day}',_paid_leave_per_year)),TD('Total Emergency Leave:'),TD(T('%s %%{day}',locale.format('%d', _emergency or 0, grouping = True)))),
        TR(TD('Last Joining Date:'),TD(_no.date_last_return.strftime('%d %b. %Y')),TD('Engagement Date:'),TD(_no.date_joined.strftime('%d %b. %Y'))),
        TR(TD('Air Ticket:'),TD(_no.air_fare,_colspan='3')),
        TR(TD('Remarks:'),TD('To deduct absent days if any from the monthly salary',_colspan='3')),
        TR(TD(),TD('Economy Class Air ticket: ' + str(_no.sector),_colspan='3')), 
        TR(TD(),TD(_proportionate,_colspan='3')),         
        TR(TD('Note: This leave will be paid leave.',_colspan='4'))), _class='table')        
        _table_id = _table_id

        session.working_days = _working_days.days 
        session.paid_leave_per_year = _paid_leave_per_year
        session.paid_leave = _paid_leave

    elif int(request.vars.type_of_leave_id) == 2: # Compassionate Leave
                
        _balanced = int(3) - int(_appli or 0)
        _row2 = TABLE(TBODY(TR(TH('Total paid compassionate leave/year'),TH('Availed (including this leave)'),TH('Balance entitlement for the year'),TH('Pending Application')),
        TR(TD('3 days'),TD(T('%s %%{day}',locale.format('%d', _appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d', _balanced or 0, grouping = True))),TD(_pending or 0)),
        TR(TD('Note: This leave will be paid leave.'),TD(),TD(),TD())), _class='table')
        _table_id = ''

    elif int(request.vars.type_of_leave_id) == 3: # Sick Leave
        
        _balanced = 14 - int(_appli or 0)
        if _appli > 14:
            _half_paid = int(_appli or 0) - 14
        else:
            _half_paid = 0
        _row2 = TABLE(TBODY(TR(TH('Total Paid Sick Leave/Year'),TH('Availed (including this leave)'),TH('Balanced Remaining'),TH('Paid Leave'),TH('Half Paid Leave')),
        TR(TD('14 days'),TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_count or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_count or 0, grouping = True))), TD(T('%s %%{day}',locale.format('%d',_half_paid or 0, grouping = True)))),
        TR(TD('Note: This leave will be paid leave.',_colspan='5'))),_class='table')
        
        _table_id = _table_id
    
    elif int(request.vars.type_of_leave_id) == 4: # Business Leave
        
        _row2 = TABLE(TBODY(TR(TH('Leave Applied For'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(_pending))),_class='table')
        _table_id = _table_id

    elif int(request.vars.type_of_leave_id) == 5: # Emergency Leave
        
        _row2 = TABLE(TBODY(TR(TH('Leave Applied For'),TH('Availed (including this leave)'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(_pending))),_class='table')
        _table_id = _table_id

    elif int(request.vars.type_of_leave_id) == 6: # Maternity Leave
        for n in db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & (db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.type_of_leave_id == 5)).select():            
            if not _no.date_last_return > n.from_effective_date:
                _emergency += n.duration_leave or 0
        _working_days = datetime.strptime(request.vars.from_effective_date, '%m-%d-%Y').date() - _no.date_last_return

        _working_days = _working_days - timedelta(int(_emergency or 0))    
        session.working_days = _working_days.days         
        session.paid_leave = 50
        
        
        _row2 = TABLE(TBODY(TR(TH('Total Paid Maternity Leave/Year'),TH('Pending')),
        TR(TD('50 days'),TD(locale.format('%d',_pending or 0, grouping = True)))),_class='table')
        _table_id = _table_id

    elif int(request.vars.type_of_leave_id) == 7: # Day Off(Excess Hours)
        
        _row2 = TABLE(TBODY(TR(TH('Total Excess Hours applied (including this leave)'),TH('Availed (including this leave)'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d', _count or 0, grouping = True))),TD(_pending)),
        TR(TD('Note: This leave will be paid leave.'),TD(),TD())),_class='table')
        _table_id = ''

    return XML(DIV(
        DIV(
            DIV(SPAN(I(_class='fa fa-user-o'),_class='info-box-icon'),
            DIV(SPAN(_title,_class='info-box-text'),SPAN(_id.first_name.upper(),' ', _id.middle_name.upper(), ' ', _id.last_name.upper(), ', ' ,_no.account_code,_class='info-box-number'),
            DIV(B(str(_no.designation_code_id.designation_name)) + str(', ') + str(_no.department_code_id.department_name)),
            _class='info-box-content'),_class='info-box bg-yellow'),
            DIV(_table_id),
            _class="col-md-6 col-sm-6 col-sx-6"),
        DIV(
            DIV(SPAN(I(_class='fa fa-calendar'),_class='info-box-icon'),DIV(_row2,
            _class='info-box-content'),_class='info-box bg-light-blue-active'),_class="col-md-6 col-sm-6 col-sx-6")        
    ))

def get_leave_history_id():        
    row = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    form = SQLFORM(db.Employee_Master_Leave, request.args(0))    

    return dict(form = form, _row= row)

def show_leave_history_id():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if not _id:
        print 'not'
    else:
        print 'id: ', _id.id
    return XML(DIV(request.args(0)))

def get_leave_history_id_():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if not _id:
        print 'not'
        table = 'wa'
    else:
        if int(_id.type_of_leave_id) == 1: #Annual Leave
            table = 'Annual Leave'        
            print '1'
        elif int(_id.type_of_leave_id) == 2:#Compassionate Leave
            table = 'Compassionate Leave'
        elif int(_id.type_of_leave_id) == 3:#Sick Leave
            table = '3'
        elif int(_id.type_of_leave_id) == 4:#Business Leave
            table = '4'
        elif int(_id.type_of_leave_id) == 5:#Emergency Leave 
            table = '5'
        elif int(_id.type_of_leave_id) == 6:#Maternity Leave
            table = '6'
        elif int(_id.type_of_leave_id) == 7:#Day Off(Excess Hours)
            table = '7'
        elif int(_id.type_of_leave_id) == 8:#Resignation
            table = '8'
        elif int(_id.type_of_leave_id) == 9:#EOS/Termination
            table = '9'
        else:
            table = 'None'
            print 'else'

        # print request.args(0), _id.type_of_leave_id
        # table = TR(TD(request.args(0)),TD('Ref.No.'),TD(_id.type_of_leave_id))
        print request.args(0)
        table = request.args(0)
    return XML(DIV(table))

def get_view_leave_history_id(): # form view 
    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _employee_id = _id.employee_id        

    row = []
    ctr = 0 
    head = THEAD(TR(TH('Transaction No',**{'_data-field':'transaction_no','_data-sortable':'true'}),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave', **{'_data-field':'type_of_leave', '_data-sortable':'true'}),TH('Date From',**{'_data-field':'from_effective_date','_data-sortable':'true'}),TH('Date To',**{'_data-field':'to_effective_date','_data-sortable':'true'}),TH('Duration'),TH('Date Returned'),TH('Status')))
    _que = db((db.Employee_Master_Leave.employee_id == _employee_id) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == True))).select(orderby = ~db.Employee_Master_Leave.id)
    for n in _que:
        
        if n.application_date == None:
            _app_dat = 'None'
        else:            
            _app_dat = n.application_date#.strftime('%d%b%Y')
        if n.from_effective_date == None:
            _fro_dat = 'None'
        else:
            _fro_dat = n.from_effective_date#.strftime('%d')
        if n.to_effective_date == None:
            _to_dat = 'None'
        else:
            _to_dat = n.to_effective_date#.strftime('%d%b%Y')
        if n.date_returned == None:
            _dat_re = 'None'
        else:
            _dat_re = n.date_returned#.strftime('%d%b%Y')

        _status = n.status_id.status
        if n.type_of_leave_id == _id.type_of_leave_id:
            
            if n.canceled == True:
                # print 'cancelled'
                row.append(TR(TD(n.transaction_no),TD(_app_dat),TD(n.type_of_leave_id.type_of_leave),TD(_fro_dat), TD(_to_dat),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_dat_re),TD('Cancelled'),_class='bg-red'))
            else:
                # print 'not cancelled'
                row.append(TR(TD(n.transaction_no),TD(_app_dat),TD(n.type_of_leave_id.type_of_leave),TD(_fro_dat), TD(_to_dat),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_dat_re),TD(_status),_class='bg-green'))
        else:
            # print n.id
            row.append(TR(TD(n.transaction_no),TD(_app_dat),TD(n.type_of_leave_id.type_of_leave),TD(_fro_dat), TD(_to_dat),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_dat_re),TD(_status)))

    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toggle':'table','_data-search':'true','_data-pagination':'true','_data-classes':'table table-striped'})
    return XML(table)

def get_leave_chart_id():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _ed = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()
    for n in db(db.Employee_Employment_Details.department_code_id == int(_ed.department_code_id)).select():
        print 'department: ',n.employee_id, n.department_code_id
    # print 'leave chart', request.args(0), _id.employee_id, _ed.department_code_id
    return XML(dict(message = 'message'))
    # return dict(message = XML('HELLO'))

def get_employee_master_leave_history_id():
    
    row = []
    head = THEAD(TR(TH('Transaction No'),TH('Transaction Date'),TH('Type of Leave'),TH('Date From'),TH('Date To'),TH('Duration'),TH('Status'),TH('Action')))
    for n in db((db.Employee_Master_Leave.employee_id == request.args(0)) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == False) | (db.Employee_Master_Leave.status_id != 16) | (db.Employee_Master_Leave.canceled == False)) & ((db.Employee_Master_Leave.deleted == False) | (db.Employee_Master_Leave.deleted == None))).select(orderby = ~db.Employee_Master_Leave.id):        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href=URL('leave_mngt','get_leave_history_id',args = n.id, extension = False))#, **{'_data-id':(n.id)})
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'ADMINISTRATION MANAGER'):
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle',callback=URL('leave_mngt','put_employee_master_leave_history_delete_id',args = n.id,extension=False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        if n.canceled == True:
            _status = P('Cancelled',_class='text-red')
        else:
            _status = n.status_id.status
        row.append(TR(TD(n.transaction_no),TD(n.application_date),TD(n.type_of_leave_id.type_of_leave),TD(n.from_effective_date),TD(n.to_effective_date),TD(n.duration_leave),
        TD(_status),
        TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',_id='tblLH')
    return dict(table = table, x = 'x')
    # return XML(DIV(table))

def put_employee_master_leave_history_delete_id():
    db(db.Employee_Master_Leave.id == request.args(0)).update(canceled = True)
    response.js = "jQuery(alertify.success('Record Canceled'),window.setTimeout(function(){window.location.reload()}, 1000))"

def get_employee_salary_adjustment_id():    
    ctr = 0
    row = []    
    head = THEAD(TR(TH('#'),TH('Transaction No'),TH('Transaction Date'),TH('Effectivity Date')))
    for n in db(db.Salary_Adjustment.employee_id == request.args(0)).select(orderby = ~db.Salary_Adjustment.id):
        ctr+=1        
        row.append(TR(TD(ctr),TD(n.transaction_no),TD(n.transaction_date),TD(n.effectivity_date)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return XML(DIV(table))

def get_year_end_leave_chart_id():
    _id = db(db.Employee_Employment_Details.employee_id == request.args(0)).select().first() 
    # print '-- #',_id.last_joining_date, '# --'
    _row = db(db.Employee_Master_Leave.employee_id == request.args(0)).select().first()
    _sum = db.Employee_Master_Leave.duration_leave.sum().coalesce_zero()
    _durationm = db((db.Employee_Master_Leave.employee_id == request.args(0)) & (db.Employee_Master_Leave.from_effective_date > _id.last_joining_date) & (db.Employee_Master_Leave.canceled == False)& (db.Employee_Master_Leave.status_id == 16)& (db.Employee_Master_Leave.type_of_leave_id < 8)).select(_sum).first()[_sum]
    _query = db((db.Employee_Master_Leave.employee_id == int(request.args(0))) & (db.Employee_Master_Leave.from_effective_date > _id.last_joining_date) & (db.Employee_Master_Leave.canceled == False)& (db.Employee_Master_Leave.status_id == 16)& (db.Employee_Master_Leave.type_of_leave_id < 8)).select(db.Employee_Master_Leave.duration_leave.sum().coalesce_zero(), db.Employee_Master_Leave.type_of_leave_id, groupby = db.Employee_Master_Leave.type_of_leave_id)
    # for n in _query:
    #     print n[db.Employee_Master_Leave.duration_leave.sum().coalesce_zero()], n.Employee_Master_Leave.type_of_leave_id.type_of_leave
    return dict(_query = _query, _sum = _sum)

def get_employee_salary_adjustment_view_id():
    print 'get_employee_salary_adjustment_view_id:', request.args(0)
    return XML(DIV(request.args(0), sanitize = False))

def get_form_leave_history_id(): # form entry
    # print 'get_form_leave_history_id: ', request.vars.employee_id
    row = []
    ctr = 0 
    head = THEAD(TR(TH('Transaction No',**{'_data-field':'transaction_no','_data-sortable':'true'}),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave', **{'_data-field':'type_of_leave', '_data-sortable':'true'}),TH('Date From',**{'_data-field':'from_effective_date','_data-sortable':'true'}),TH('Date To',**{'_data-field':'to_effective_date','_data-sortable':'true'}),TH('Duration'),TH('Date Returned'),TH('Status')))
    _que = db((db.Employee_Master_Leave.employee_id == request.vars.employee_id) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == True))).select(orderby = ~db.Employee_Master_Leave.id)
    for n in _que:        
        if n.application_date == None:
            _app_dat = 'None'
        else:            
            _app_dat = n.application_date#.strftime('%d%b%Y')
        if n.from_effective_date == None:
            _fro_dat = 'None'
        else:
            _fro_dat = n.from_effective_date#.strftime('%d')
        if n.to_effective_date == None:
            _to_dat = 'None'
        else:
            _to_dat = n.to_effective_date#.strftime('%d%b%Y')
        if n.date_returned == None:
            _dat_re = 'None'
        else:
            _dat_re = n.date_returned#.strftime('%d%b%Y')
        if n.canceled == True:
            _status = P('Canceled', _class='text-red')
        else:
            _status = n.status_id.status
        row.append(TR(TD(n.transaction_no),TD(_app_dat),TD(n.type_of_leave_id.type_of_leave),TD(_fro_dat), TD(_to_dat),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_dat_re),TD(_status)))        
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return HTML(DIV(table))

@auth.requires_login()    
def get_application_leave_grid():    
    row = []
    ctr = 0
    _usr = db(db.Department_Users_Assignment.users_id == auth.user_id).select().first()
    _dep = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    # print 'assigned: ', _dep.users_id, _dep.sub_department_id
    if auth.has_membership('MANAGEMENT'):
        _query = db((db.Employee_Master_Leave.status_id == 13) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id)
    # elif auth.has_membership('ACCOUNTS'):
    #     _query = db((db.Employee_Master_Leave.status_id == 13) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('HR MANAGER') | auth.has_membership('ADMINISTRATION MANAGER'):
        # print 'HR MANAGER'
        _query = db((db.Employee_Master_Leave.status_id != 16) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id)
    # elif auth.has_membership('ADMINISTRATION MANAGER'):        
    #     print 'ADMINISTRATION MANAGER'
    #     # _query = db(((db.Employee_Master_Leave.manager_assigned == _dep.sub_department_id) | (db.Employee_Master_Leave.created_by == auth.user_id) & (db.Employee_Master_Leave.status_id != 16)) & (db.Employee_Master_Leave.status_id != 16) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id)
    #     _query = db((db.Employee_Master_Leave.status_id != 16) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('DEPARTMENT MANAGERS'):        
        for x in db(db.Department_Head_Assignment.users_id == auth.user_id).select():        
            _query = db(db.Employee_Master_Leave.manager_assigned == x.sub_department_id).select()             
            # _query = db(((db.Employee_Master_Leave.manager_assigned == x.sub_department_id) | (db.Employee_Master_Leave.created_by == auth.user_id))& (db.Employee_Master_Leave.canceled == False) & ((db.Employee_Master_Leave.status_id == 1) | (db.Employee_Master_Leave.status_id == 12))).select(orderby = ~db.Employee_Master_Leave.id)            
    elif auth.has_membership('BACK OFFICE DEPARTMENT'):        
        _query = db(((db.Employee_Master_Leave.employee_id == _usr.employee_id) | (db.Employee_Master_Leave.created_by == auth.user_id)) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('ROOT'):
        _query = db((db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select(orderby = ~db.Employee_Master_Leave.id)        
    else:        
        _query = db(((db.Employee_Master_Leave.employee_id == _usr.employee_id) | (db.Employee_Master_Leave.created_by == auth.user_id)) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select(orderby = ~db.Employee_Master_Leave.id)    
    head = THEAD(TR(TH('#'),TH('Transaction Date'),TH('Type of Leave'),TH('Date From'),TH('Date To'),TH('Duration'),TH('Name'),TH('Status'),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))        
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        retu_lnk = A(I(_class='fa fa-mail-reply-all'), _title='Joining', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        _ei = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()        
        _emp_na = n.employee_id.first_name, ' ',n.employee_id.middle_name, ' ' ,n.employee_id.last_name, ', ', SPAN(_ei.account_code,_class='text-muted')
        if (n.type_of_leave_id == 1) or (n.type_of_leave_id == 4) or (n.type_of_leave_id == 5) or (n.type_of_leave_id == 6):
            
            if n.status_id == 11:
                retu_lnk = A(I(_class='fa fa-mail-reply-all'), _title='Joining', _type='button ', _role='button', _class='btn btn-icon-toggle btnReturn', callback = URL('leave_mngt','put_application_leave_returned_id', args = n.id))
            elif n.status_id == 12:          
                # print 'materninty'  ,n.id
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                
                retu_lnk = A(I(_class='fa fa-mail-reply-all'), _title='Joining', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('leave_mngt','put_application_leave_returned_id', args = n.id))            
        else:
            retu_lnk = A(I(_class='fa fa-mail-reply-all'), _title='Joining', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')            
        if auth.has_membership('HR MANAGER'):
            if n.status_id == 7 or n.status_id == 1:
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
            else:
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                    
        elif auth.has_membership('DEPARTMENT MANAGERS'):            
            # view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))
            appr_lnk = A(I(_class='fa fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('leave_mngt','put_application_dept_leave_id_approved', args = n.id))        
            reje_lnk = A(I(_class='fa fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('leave_mngt', 'put_application_dept_leave_id_rejected',args = n.id))        
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                
            if n.status_id == 1:
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                    
            if n.status_id > 2:                    
                appr_lnk = A(I(_class='fa fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('leave_mngt','put_application_dept_leave_id_approved', args = n.id))        
                reje_lnk = A(I(_class='fa fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('leave_mngt', 'put_application_dept_leave_id_rejected',args = n.id))        
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                
            if n.status_id == 4 or n.status_id == 5:                    
                appr_lnk = A(I(_class='fa fa-user-plus'), _title='Approved Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('leave_mngt','put_application_dept_leave_id_approved', args = n.id))        
                reje_lnk = A(I(_class='fa fa-user-times'), _title='Reject Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', callback=URL('leave_mngt', 'put_application_dept_leave_id_rejected',args = n.id))        
            if n.status_id == 7:
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
            if n.status_id == 12:            
                view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_returned_id', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, appr_lnk, reje_lnk, retu_lnk)
        else:            
            if n.status_id >= 3:
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                    
            elif n.status_id == 12:            
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_returned_id', args = n.id))                    
            else:
                edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, retu_lnk)
        
        
        # if n.duration_leave < 1:
        #     _duration_day = str(Fraction(n.duration_leave)) + str(' day')
        #     print 'duration: ', _duration_day
        # else:
        #     _duration_day = T('%s %%{day}',locale.format('%d',round(n.duration_leave) or 0, grouping = True))
        if n.status_id >= 12:
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_returned_id', args = n.id))            
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, retu_lnk)
            if n.type_of_leave_id.id == 1 or n.type_of_leave_id.id == 4 or n.type_of_leave_id.id == 5 or n.type_of_leave_id.id == 6:                
                if n.joining_application_date == None:
                    _joining_date = 'None'
                else:
                    _joining_date = n.joining_application_date.strftime('%d%b%Y')
                row.append(TR(TD(ctr),TD(_joining_date),TD(str('Joining Request - ') + n.type_of_leave_id.type_of_leave),TD(n.from_effective_date.strftime('%d%b%Y')),TD(n.to_effective_date.strftime('%d%b%Y')),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_emp_na),TD(n.status_id.status),TD(n.status_id.action_required),TD(btn_lnk)))
        else:
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))        
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, retu_lnk)
            if n.application_date == None:
                _application_date = 'None'
            else:
                _application_date = n.application_date.strftime('%d%b%Y')
            if n.from_effective_date == None:
                _from_effective_date = 'None'
            else:
                _from_effective_date = n.from_effective_date.strftime('%d%b%Y')
            if n.to_effective_date == None:
                _to_effective_date = 'None'
            else:
                _to_effective_date = n.to_effective_date.strftime('%d%b%Y')
            
            if (len(str(n.mngt_remarks)) > 0) and (str(n.mngt_remarks) != 'None'):
                _action_req = n.status_id.action_required,' ', A(I(_class='fa fa-comment'), _title='Mngt Comment', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')#, **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus','_data-html':'true','_data-original-title':'Mngt Remarks','_data-content':mngt_remarks(n.id)})
            else:
                _action_req = n.status_id.action_required
            row.append(TR(
                TD(ctr),
                TD(_application_date),
                TD(n.type_of_leave_id.type_of_leave),
                TD(_from_effective_date),
                TD(_to_effective_date),
                TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),
                TD(_emp_na),
                TD(n.status_id.status ),
                TD(_action_req),
                TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table display nowrap', _style="width:100%")
    return dict(table = table)

def mngt_remarks(x = request.args(0)):
    print x

def get_application_returned_id():
    _row = db(db.Employee_Master_Leave.id == request.args(0)).select().first()    
    _returned = (_row.date_returned - _row.to_effective_date).days - 1
    if _returned > 0:         
        _msg = T('Returned %s %%{day} late.') % (abs(_returned))
    else:        
        _msg = T('Returned %s %%{day} early.') % (abs(_returned))
    return dict(_row = _row, _returned_days = _msg)

def put_application_leave_returned_id():
    # print 'put_application_leave_returned_id'
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    session._id = _id.id
    if request.now.date() != _id.to_effective_date:
        response.js = "jQuery(late_returned());"
    else:
        response.js = "jQuery(late_returned());"

def put_application_returned_id():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _returned = (_id.date_returned - _id.to_effective_date).days - 1
    if _returned > 0:        
        _msg = T('Returned %s %%{day} late.') % (abs(_returned))
    else:        
        _msg = T('Returned %s %%{day} early.') % (abs(_returned))
    db.Employee_Master_Leave.employee_id.writable = False
    db.Employee_Master_Leave.from_effective_date.writable = False
    db.Employee_Master_Leave.to_effective_date.writable = False
    db.Employee_Master_Leave.replacement.writable = False
    db.Employee_Master_Leave.type_of_leave_id.writable = False
    db.Employee_Master_Leave.duration_leave.writable = False
    db.Employee_Master_Leave.joining_doc_ref_no.writable = False
    db.Employee_Master_Leave.joining_application_date.writable = False
    db.Employee_Master_Leave.remarks.writable = False
    db.Employee_Master_Leave.leave_days_per_year.writable = False
    db.Employee_Master_Leave.working_days.writable = False
    db.Employee_Master_Leave.entitled_days.writable = False
    db.Employee_Master_Leave.status_id.writable = False
    form = SQLFORM(db.Employee_Master_Leave, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('leave_mngt','get_application_leave_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
        # print form.errors
    return dict(form = form, _id = _id, _returned_days = _msg)

def put_return_application_id():    
    _id = db(db.Employee_Master_Leave.id == int(session._id)).select().first()
    _usr = db(db.auth_user.id == _id.created_by).select().first()
    _mem = db(db.auth_membership.user_id == _usr.id).select().first()

    # print 'returned'
    if int(_mem.group_id) == 1: # as management
        _id.update_record(status_id = 14, date_returned=request.args(1), return_justification = request.args(0), joining_application_date = request.now )
        if _id.type_of_leave_id == 1: # for annual leave
            # print 'annual'
            db(db.Employee_Employment_Details.employee_id == _id.employee_id).update(last_joining_date = request.args(1))
        else: # for bussiness, maternity, emergency leave only
            # print 'not annual'
            db(db.Employee_Employment_Details.employee_id == _id.employee_id).update(date_last_return = request.args(1))

    else:
        _id.update_record(status_id = 12, date_returned=request.args(1), return_justification = request.args(0), joining_application_date = request.now )
        if _id.type_of_leave_id == 1: # for annual leave
            db(db.Employee_Employment_Details.employee_id == _id.employee_id).update(last_joining_date = request.args(1))
        else: # for bussiness, maternity, emergency leave only
            db(db.Employee_Employment_Details.employee_id == _id.employee_id).update(date_last_return = request.args(1))
    joining_request_notification(int(_id.id))

def joining_request_notification(x):
    # print 'generate send email to management => ', x
    _usr = db(db.Employee_Master_Leave.id == int(x)).select().first()
    if _usr.employee_id.gender == 'Male':
        _gender = 'his'
    else:
        _gender = 'her'
    _id = db(db.Email_Notification).select().first()
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    mail.settings.server = 'smtp.gmail.com:587'
    mail.settings.sender = _sender
    mail.settings.login = _login 
    _to = db(db.auth_membership.group_id == 2).select().first()    

    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">%s %s applied joining request from %s %s.</p>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """ % (_usr.employee_id.first_name, _usr.employee_id.last_name, _gender, _usr.type_of_leave_id.type_of_leave)
    mail.send(
        to=[_to.user_id.email],
        subject='JOINING REQUEST WORKFLOW',
        message = _msg)    

def get_application_dept_leave_grid():        
    row = []
    ctr = 0 
    _usr = db(db.Department_Users_Assignment.users_id == auth.user_id).select().first()
    _dep = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()    
    if auth.has_membership('DEPARTMENT MANAGERS'):              
        # if _dep.sub_department_id == 3: # check if fmcg sales manager log in
        _query = db((((db.Employee_Master_Leave.manager_assigned == _dep.sub_department_id) & (db.Employee_Master_Leave.manager_assigned <= 6) & ((db.Employee_Master_Leave.status_id == 1) | (db.Employee_Master_Leave.status_id == 12)) ) | (db.Employee_Master_Leave.created_by == auth.user_id)) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select(orderby = ~db.Employee_Master_Leave.id)
        # else:            
            # _query = db(((db.Employee_Master_Leave.manager_assigned == _dep.sub_department_id) | (db.Employee_Master_Leave.created_by == auth.user_id)) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('BACK OFFICE DEPARTMENT'):          
        _query = db(((db.Employee_Master_Leave.employee_id == _usr.employee_id) | (db.Employee_Master_Leave.created_by == auth.user_id)) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 16)).select(orderby = ~db.Employee_Master_Leave.id)    
    else:
        response.js = "jQuery(console.log('not authorized to approved or reject'))"        
    head = THEAD(TR(TH('#'),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave',**{'_data-field':'type_of_leave_id','_data-sortable':'true'}),TH('Date From'),TH('Date To'),TH('Duration'),TH('Name'),TH('Status',**{'_data-field':'status_id','_data-sortable':'true'}),TH('Action Required'),TH('Action')),_class='bg-primary')    
    for n in _query:            
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))        
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        retu_lnk = A(I(_class='fa fa-mail-reply-all'), _title='Joining', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')                        
        if n.created_by != auth.user_id:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                                                    
        else:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                
        if n.status_id >= 3 :                    
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                
        if n.status_id == 7:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
        if n.status_id == 11:            
            retu_lnk = A(I(_class='fa fa-mail-reply-all'), _title='Joining', _type='button ', _role='button', _class='btn btn-icon-toggle btnReturn', callback = URL('leave_mngt','put_application_leave_returned_id', args = n.id))
        if n.status_id == 12:            
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_returned_id', args = n.id))
        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, retu_lnk)
        _ei = db(db.Employee_Employment_Details.id == int(n.employee_id)).select().first()            
        _emp_na = n.employee_id.first_name, ' ',n.employee_id.middle_name, ' ' ,n.employee_id.last_name#, SPAN(_ei.account_code,_class='text-muted')
        
        if n.status_id >= 12:
            if n.type_of_leave_id.id == 1 or n.type_of_leave_id.id == 4 or n.type_of_leave_id.id == 5 or n.type_of_leave_id.id == 6 :                
                if n.joining_application_date == None:
                    _joining_date = 'None'
                else:
                    _joining_date = n.joining_application_date.strftime('%d%b%Y')
                row.append(TR(TD(ctr),TD(_joining_date),TD(str('Joining Request - ') + n.type_of_leave_id.type_of_leave),TD(n.from_effective_date.strftime('%d%b%Y')),TD(n.to_effective_date.strftime('%d%b%Y')),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_emp_na),TD(n.status_id.status),TD(n.status_id.action_required),TD(btn_lnk)))
        else:
            btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, retu_lnk)
            if n.application_date == None:
                _application_date = 'None'
            else:
                _application_date = n.application_date.strftime('%d%b%Y')
            if n.from_effective_date == None:
                _from_effective_date = 'None'
            else:
                _from_effective_date = n.from_effective_date.strftime('%d%b%Y')
            if n.to_effective_date == None:
                _to_effective_date = 'None'
            else:
                _to_effective_date = n.to_effective_date.strftime('%d%b%Y')
            if n.status_id == 2 or n.status_id == 5:
                _status = SPAN(n.status_id.status, _class="badge bg-red")
            else:
                _status = n.status_id.status
            row.append(TR(
                TD(ctr),
                TD(_application_date),
                TD(n.type_of_leave_id.type_of_leave),
                TD(_from_effective_date),
                TD(_to_effective_date),
                TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),
                TD(_emp_na),
                TD(_status),
                TD(n.status_id.action_required),
                TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',_id='aplTbl', **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

def get_department_application_leave_id():
    return dict()

def validate_application_department(form):
    
    _usr = db(db.Employee_Managers_Assignment.users_id == auth.user_id).select().first()
    _app = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _sum = db.Employee_Master_Leave.duration_leave.sum()
    _pen = db((db.Employee_Master_Leave.id == request.args(0)) & (db.Employee_Master_Leave.type_of_leave_id == request.vars.type_of_leave_id) & (db.Employee_Master_Leave.status_id <= 9)).select(_sum).first()[_sum]
    if _app:
        for n in db(db.Employee_Master_Leave.employee_id == _usr.id).select(orderby = db.Employee_Master_Leave.from_effective_date):
            if (datetime.strptime(request.vars.to_effective_date,'%Y-%m-%d').date() < n.from_effective_date) or (datetime.strptime(request.vars.from_effective_date, '%Y-%m-%d').date() > n.to_effective_date):
                x = 0
            else:
                form.errors.from_effective_date = 'Overlapping date not allowed.'
    # if _pen >= 1:
    #     form.errors.type_of_leave_id = 'Pending application exists.'
    
    if int(request.vars.type_of_leave_id) == 1: # annual leave
        print 'update annual leave'
    elif int(request.vars.type_of_leave_id) == 2: # compassionate leave
        print 'update compassionate leave'
    elif int(request.vars.type_of_leave_id) == 3: # sick leave
        print 'update sick leave'
    elif int(request.vars.type_of_leave_id) == 4: # business leave
        print 'business leave'
    elif int(request.vars.type_of_leave_id) == 5: # emergency leave
        print 'update emergency leave'
    elif int(request.vars.type_of_leave_id) == 6: # maternity leave
        print 'update maternity leave'
    elif int(request.vars.type_of_leave_id) == 7: # excess hours
        print 'update excess hours'


def put_department_application_leave_id():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
        #    db.Purchase_Order.status_id.requires = IS_IN_DB(db((db.Stock_Status.id == 1) | (db.Stock_Status.id == 3) | (db.Stock_Status.id == 19)), db.Stock_Status.id, '%(description)s', zero = 'Choose Status')
    db.Employee_Master_Leave.status_id.requires = IS_IN_DB(db((db.Leave_Status.id == 4) | (db.Leave_Status.id == 5)), db.Leave_Status.id, '%(status)s', zero = 'Choose Status')
    form = SQLFORM(db.Employee_Master_Leave, request.args(0))
    if form.process(onvalidation = validate_application_department).accepted:
        response.flash = 'UPDATED FILES'
        redirect(URL('leave_mngt','get_application_dept_leave_grid'))
    elif form.errors:
        response.flash = 'FORM ERROR'
    return dict(form = form, _id = _id)

def put_application_leave_id_cancelled():  
    _usr = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _usr.update_record(canceled = True)
    if _usr.employee_id.gender == 'Male':
        _gender = 'his'
    else:
        _gender = 'her'
    _id = db(db.Email_Notification).select().first()    
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    mail.settings.server = 'smtp.gmail.com:587'
    mail.settings.sender = _sender
    mail.settings.login = _login      
    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">%s%s %s cancelled %s %s workflow application.</p>                
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """ % (_usr.employee_id.title ,_usr.employee_id.first_name.capitalize(), _usr.employee_id.last_name.capitalize(), _gender, _usr.type_of_leave_id.type_of_leave)

    for n in db((db.auth_membership.group_id == 2) | (db.auth_membership.group_id == 3)).select():        
        mail.send(
            to=[n.user_id.email],   
            subject='CANCELLED WORKFLOW APPLICATION',
            message = _msg)        

def put_application_dept_leave_remarks_id():
    db(db.Employee_Master_Leave.id == request.args(0)).update(dept_remarks = request.vars.dept_remarks)

def put_application_dept_leave_id_approved():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if _id.status_id == 1:                
        db(db.Employee_Master_Leave.id == int(request.args(0))).update(status_id = 3, dept_approved_by = auth.user_id, dept_remarks = request.args(1))
        put_email_hr_notification()
    elif _id.status_id == 12:                
        db(db.Employee_Master_Leave.id == int(request.args(0))).update(status_id = 14, dept_approved_by = auth.user_id, dept_remarks = request.args(1))
    
def put_application_dept_leave_id_rejected():        
    # print 'put_application_dept_leave_id_rejected', request.args(0)
    db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 11, remarks = request.args(1), rejected_by = auth.user_id)

def xget_application_dept_leave_chart_grid():
    print '---'
    for n in db().select(db.Employee_Employment_Details.ALL):
        for x in db(db.Department_Head_Assignment.users_id == auth.user_id).select(db.Department_Head_Assignment.sub_department_id, groupby = db.Department_Head_Assignment.sub_department_id):
            if n.sub_department_code_id == x.sub_department_id:
                print '-==-'
    
def yget_application_dept_leave_chart_grid():    
    print '-----'
    for n in db(db.Department_Head_Assignment.users_id == auth.user_id).select(db.Department_Head_Assignment.ALL, db.Employee_Employment_Details.ALL, left = db.Department_Head_Assignment.on(db.Employee_Employment_Details.sub_department_code_id == db.Department_Head_Assignment.sub_department_id)):
        print n.Employee_Employment_Details.sub_department_code_id

def get_application_dept_leave_chart_grid():    
    _id = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    head = THEAD(TR(TH('#'),TH('Name'),TH('Department'),TH('From Date'),TH('To Date')))
    ctr = 0
    row = []
    for x in db(db.Department_Head_Assignment.users_id == auth.user_id).select():
        for n in db(db.Employee_Leave_Chart_Temporary.sub_department_id == x.sub_department_id).select():
            ctr += 1
            row.append(TR(
                TD(ctr,INPUT(_name="ctr", _value=n.id, _hidden = True)),
                TD(n.employee_id.first_name, ' ', n.employee_id.last_name),
                TD(n.sub_department_id.sub_department_name),
                TD(INPUT(_class='form-control date',_type='text',_name='from_effective_date',_value=n.from_effective_date.strftime('%m-%d-%Y'))),
                TD(INPUT(_class='form-control date',_type='text',_name='to_effective_date',_value=n.to_effective_date.strftime('%m-%d-%Y')))))            
    body = TBODY(*row)
    form = FORM(TABLE(*[head, body], _class='table',_id='table', **{'_data-toolbar':'#toolbar','_data-search':'true', '_data-show-refresh':'true','_data-show-pagination-switch':'true','_data-pagination':'true'}))
    if form.accepts(request, session):
        if request.vars.btnUpdate:
            print 'Update '
        elif request.vars.btnSubmit:
            print 'submit'
        elif request.vars.btnProcess:
            print 'process'

    return dict(table = form)

def post_application_dept_leave_chart():    
    _id = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()    
    for x in db(db.Department_Head_Assignment.users_id == auth.user_id).select():        
        db(db.Employee_Leave_Chart_Temporary.sub_department_id ==  x.sub_department_id).delete()
        for n in db(db.Employee_Employment_Details.sub_department_code_id == x.sub_department_id).select():            
            db.Employee_Leave_Chart_Temporary.insert(transaction_date = request.now,employee_id = n.employee_id,sub_department_id = n.sub_department_code_id)
        
def put_application_dept_leave_chart():    
    row = 0
    for n in request.vars.ctr:
        db(db.Employee_Leave_Chart_Temporary.id == n).update(from_effective_date = request.vars.from_effective_date[row], to_effective_date = request.vars.to_effective_date[row])
        row += 1

def get_application_dept_leave_chart_id():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()        
    _chk = db(db.Employee_Leave_Chart_Temporary.sub_department_id == _id.manager_assigned).select().first()
    return dict(_row = _id, _chk = _chk)

def xget_application_dept_leave_chart():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()        
    _chk = db(db.Employee_Leave_Chart_Temporary.sub_department_id == _id.manager_assigned).select().first()
    if not _chk:
        return XML(DIV('Empty chart'))
    else:    
        ctr = 0
        row = []
        head = THEAD(TR(TH('#'),TH('Name'),TH('From Date'),TH('To Date')))
        for n in db(db.Employee_Leave_Chart_Temporary.sub_department_id == _id.manager_assigned).select():
            ctr+=1
            _eed = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
            if n.employee_id == _id.employee_id:
                row.append(TR(TD(ctr),TD(n.employee_id.title, ' ', n.employee_id.first_name,' ',n.employee_id.last_name, ', ', SPAN(_eed.account_code, _class='text-muted')),TD(n.from_effective_date.strftime('%m-%d-%Y')),TD(n.to_effective_date.strftime('%m-%d-%Y')),_class='bg-green'))
            else:
                row.append(TR(TD(ctr),TD(n.employee_id.title, ' ', n.employee_id.first_name,' ',n.employee_id.last_name, ', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.from_effective_date.strftime('%m-%d-%Y')),TD(n.to_effective_date.strftime('%m-%d-%Y'))))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table')
        return XML(DIV(table))

@auth.requires_login()
def get_application_hr_leave_grid():
    row = []
    ctr = 0
    # head = THEAD(TR(TH('#'),TH('Date'),TH('Type of Leave'),TH('Name'),TH('Department'),TH('Designation'),TH('Status'),TH('Required Action'),TH('Remarks'),TH('Action')))
    head = THEAD(TR(TH('#'),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave',**{'_data-field':'type_of_leave_id','_data-sortable':'true'}),TH('Date From'),TH('Date To'),TH('Duration'),TH('Name'),TH('Approved by'),TH('Status',**{'_data-field':'status_id','_data-sortable':'true'}),TH('Action Required'),TH('Action')),_class='bg-primary')    
    for n in db(((db.Employee_Master_Leave.created_by == auth.user_id) & (db.Employee_Master_Leave.canceled == False)  & (db.Employee_Master_Leave.status_id != 16)) | (db.Employee_Master_Leave.status_id >= 3) & (db.Employee_Master_Leave.status_id <= 14) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id):
        ctr += 1               
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                    
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        prin_lnk = A(I(_class='fa fa-check'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
        cale_lnk = A(I(_class='fa fa-calendar-check-o'), _title='Leave Chart', _type='button ', _role='button', _target='_blank', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_dept_leave_chart_id', args = n.id))
        if n.status_id >= 5 and n.status_id <= 6:
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                    
            prin_lnk = A(I(_class='fa fa-check'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
        elif n.status_id == 7 or n.status_id == 8:
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))            
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                    
            prin_lnk = A(I(_class='fa fa-check'), _title='Confirm & Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        elif n.status_id == 9:            
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                    
            prin_lnk = A(I(_class='fa fa-check'), _title='Confirm', _type='button ', _role='button', _class='btn btn-icon-toggle', _onclick="jQuery(Confirm(%s))" % (n.id)) #callback=URL('leave_mngt_reports','put_confirm_and_print_applicaton_id', args = n.id))            
        elif n.status_id == 10: 
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                    
            prin_lnk = A(I(_class='fa fa-check'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href = URL('leave_mngt_reports','get_application_leave_report_id',args = n.id))            
        elif n.status_id == 11: 
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                    
            prin_lnk = A(I(_class='fa fa-check'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href = URL('leave_mngt_reports','get_application_leave_report_id',args = n.id))            
        elif n.status_id == 14:
            view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_returned_id', args = n.id))            
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                    
            dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
            prin_lnk = A(I(_class='fa fa-check'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
        # else:
        #     print 'else'
        #     view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_hr_view_id', args = n.id))        
        #     edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))                                    
        #     dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        #     prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk,dele_lnk, prin_lnk, cale_lnk)
        _ei = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
        if not _ei:
            _emp_no = 'None'
            _emp_de = 'None'
            _emp_ds = 'None'
        else:
            _emp_no = _ei.employee_no
            if not _ei.department_code_id: 
                _emp_de = _emp_ds = 'None'
            else:
                _emp_de = _ei.department_code_id.department_name
            if not _ei.designation_code_id:
                _emp_de = _emp_ds = 'None'
            else: 
                _emp_ds = _ei.designation_code_id.designation_name
        if not n.employee_id:
            _emp_na = 'None'
        else:
            _emp_na = n.employee_id.first_name, ' ',n.employee_id.middle_name, ' ' ,n.employee_id.last_name, ', ', SPAN(_ei.account_code,_class='text-muted')
        
        if n.status_id >= 11:
            if n.type_of_leave_id.id == 1 or n.type_of_leave_id.id == 4 or n.type_of_leave_id.id == 5 or n.type_of_leave_id.id == 6:                
                if n.joining_application_date == None:
                    _joining_date = 'None'
                else:
                    _joining_date = n.joining_application_date.strftime('%d%b%Y')
                if n.dept_approved_by == None:
                    _dept_approved = 'None'
                else:
                    _dept_approved = n.dept_approved_by.first_name.upper()
                row.append(TR(TD(ctr),TD(_joining_date),TD(str('Joining Request - ') + n.type_of_leave_id.type_of_leave),TD(n.from_effective_date.strftime('%d%b%Y')),TD(n.to_effective_date.strftime('%d%b%Y')),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_emp_na),TD(_dept_approved),TD(n.status_id.status),TD(n.status_id.action_required),TD(btn_lnk)))
        else:
            if n.dept_approved_by == None:
                _app_by = 'None'
            else:
                _app_by = n.dept_approved_by.first_name.upper()
            if n.mngt_remarks != "":
                _action_req = n.status_id.action_required,' ', A(I(_class='fa fa-comment'), _title='Mngt Comment', _type='button  ', _role='button', _class='btn btn-icon-toggle', **{'_data-rel':'popover','_data-placement':'left','_data-trigger':'focus','_data-html':'true','_data-original-title':'Mngt Remarks','_data-content':mngt_remarks(n.id)})
            else:
                _action_req = n.status_id.action_required
            row.append(TR(TD(ctr),TD(n.application_date.strftime('%d%b%Y')),TD(n.type_of_leave_id.type_of_leave),TD(n.from_effective_date.strftime('%d%b%Y')),TD(n.to_effective_date.strftime('%d%b%Y')),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_emp_na),TD(_app_by),TD(n.status_id.status ),TD(_action_req),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toggle':'table','_data-search':'true','_data-classes':'table table-striped','_data-pagination':'true'})
    return dict(table = table)

def get_application_hr_view_id():    
    return dict()

def put_application_hr_leave_id():
    db.Employee_Master_Leave.status_id.requires = IS_IN_DB(db((db.Leave_Status.id == 7) | (db.Leave_Status.id == 8)), db.Leave_Status.id, '%(status)s', zero = 'Choose Status')
    form = SQLFORM(db.Employee_Master_Leave, request.args(0))
    if form.process(onvalidation = validate_application_department).accepted:
        response.flash = 'FORM UPDATED'
        redirect(URL('leave_mngt','get_application_hr_leave_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form, _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first())

def get_application_mgnr_view_id(): 
    return dict()

def put_application_hr_leave_id_approved(): #from department head to be approved by hr    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]        
    _memo_to = str(_id.employee_id.first_name) + ' ' + str(_id.employee_id.middle_name) + ' ' + str(_id.employee_id.last_name)
    _leave_type = _id.type_of_leave_id.type_of_leave
    _subject = str(_leave_type) + ' - ' + str(_memo_to)    
    if (_id.type_of_leave_id == 6):        
        _pre.update_record(serial_key = _skey)              
        db.Memorandum.insert(memorandum_prefix_no_id = 4,memorandum_no=_ckey, memorandum_date=request.now, memorandum_from = 'PERSONNEL DEPT',memorandum_to = _memo_to, memorandum_subject = _subject )
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 10, hr_approved_by = auth.user_id)# proceeds to accounts department for processing
        db(db.Employee_Employment_Details.employee_id == int(_id.employee_id)).update(date_last_return = _id.date_returned)
    else:
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey,status_id = 6, hr_remarks = request.vars.hr_remarks, hr_approved_by = auth.user_id)
        put_email_management_notification()

    # if (_id.type_of_leave_id == 1) or (_id.type_of_leave_id == 4) or (_id.type_of_leave_id == 5) or (_id.type_of_leave_id == 8) or (_id.type_of_leave_id == 9):        
    # elif (_id.type_of_leave_id == 2) or (_id.type_of_leave_id == 7):
    #     # _pre.update_record(serial_key = _skey)              
    #     db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 6, hr_remarks = request.vars.hr_remarks, hr_approved_by = auth.user_id) # proceeds to management for final approval
    #     # db.Memorandum.insert(memorandum_prefix_no_id = 4,memorandum_no=_ckey, memorandum_date=request.now, memorandum_from = 'PERSONNEL DEPT',memorandum_to = _memo_to, memorandum_subject = _subject )
    #     # db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 16, hr_remarks = request.vars.hr_remarks, hr_approved_by = auth.user_id)
    #     put_email_management_notification()
    # elif (_id.type_of_leave_id == 3):        
    #     # _pre.update_record(serial_key = _skey)              
    #     db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 6, hr_remarks = request.vars.hr_remarks, hr_approved_by = auth.user_id)# proceeds to management for final approval
    #     # db.Memorandum.insert(memorandum_prefix_no_id = 4,memorandum_no=_ckey, memorandum_date=request.now, memorandum_from = 'PERSONNEL DEPT',memorandum_to = _memo_to, memorandum_subject = _subject )
    #     # db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 16, hr_remarks = request.vars.hr_remarks, hr_approved_by = auth.user_id)# proceeds to accounts department for processing
    #     put_email_management_notification()
    # elif (_id.type_of_leave_id == 6):        
    #     _pre.update_record(serial_key = _skey)              
    #     db.Memorandum.insert(memorandum_prefix_no_id = 4,memorandum_no=_ckey, memorandum_date=request.now, memorandum_from = 'PERSONNEL DEPT',memorandum_to = _memo_to, memorandum_subject = _subject )
    #     db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 10, hr_remarks = request.vars.hr_remarks, hr_approved_by = auth.user_id)# proceeds to accounts department for processing
    #     db(db.Employee_Employment_Details.employee_id == _id.employee_id).update_record(date_last_return = _id.date_returned)

def put_application_hr_leave_id_rejected():    
    db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 2, rejected_by = auth.user_id, hr_remarks = request.vars.hr_remarks)

def put_application_hr_confirmed_id():          
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]        
    _memo_to = str(_id.employee_id.first_name) + ' ' + str(_id.employee_id.middle_name) + ' ' + str(_id.employee_id.last_name)
    _leave_type = _id.type_of_leave_id.type_of_leave
    _subject = str(_leave_type) + ' - ' + str(_memo_to)
    _pre.update_record(serial_key = _skey)                  
    db.Memorandum.insert(memorandum_prefix_no_id = 4,memorandum_no=_ckey, memorandum_date=request.now, memorandum_from = 'PERSONNEL DEPT',memorandum_to = _memo_to, memorandum_subject = _subject )    
    if int(_id.type_of_leave_id) == 4 or int(_id.type_of_leave_id) == 5:
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 11,hr_approved_by = auth.user_id)
    else:
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 10,hr_approved_by = auth.user_id)
        _id = db(db.Email_Notification).select().first()    
        _sender = _id.email_notification
        _login = str(_id.email_notification) + str(':') + str(_id.email_password)
        mail.settings.server = 'smtp.gmail.com:587'
        # mail.settings.server = 'smtp.office365.com:587' or 'logging'
        mail.settings.sender = _sender
        mail.settings.login = _login 

        # mail.settings.server = 'smtp.gmail.com:587'
        # mail.settings.sender = 'merch.noreply@gmail.com'
        # mail.settings.login = 'merch.noreply@gmail.com:45Password123' # 45Password123
        # mail.settings.tls = 'smtp.tls'
        _msg = """\
                <html>
                <head></head>
                <body>
                    <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending leave application required for your approval.</p>                    
                    <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
                </body>
                </html>
                """
        for n in db(db.auth_membership.group_id == 6).select():
            mail.send(
                to=[n.user_id.email],
                subject='HR WORKFLOW REMINDER',
                message = _msg)    

def put_application_hr_remark_id():           
    db(db.Employee_Master_Leave.id == request.args(0)).update(hr_remarks = request.vars.hr_remarks)
    response.js = "jQuery(alertify.success('Remarks sent...'));"

def put_email_management_notification(): # go to management
    _id = db(db.Email_Notification).select().first()    
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    mail.settings.server = 'smtp.gmail.com:587'
    # mail.settings.server = 'smtp.office365.com:587' or 'logging'
    mail.settings.sender = _sender
    mail.settings.login = _login 
    # mail.settings.server = 'smtp.gmail.com:587'
    # mail.settings.sender = 'merch.noreply@gmail.com'
    # mail.settings.login = 'merch.noreply@gmail.com:45Password123' # 45Password123
    # mail.settings.tls = 'smtp.tls'        
    _to = db(db.auth_membership.group_id == 2).select().first()    

    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending leave application required for your approval.</p>                
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """
    mail.send(
        to=[_to.user_id.email],
        subject='HR WORKFLOW REMINDER',
        message = _msg)        
    return dict()

def put_email_hr_notification(): # go to hr management
    _id = db(db.Email_Notification).select().first()    
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    mail.settings.server = 'smtp.gmail.com:587'
    # mail.settings.server = 'smtp.office365.com:587' or 'logging'
    mail.settings.sender = _sender
    mail.settings.login = _login 
    # mail = Mail()
    # mail.settings.server = 'smtp.gmail.com:587'
    # mail.settings.sender = 'merch.noreply@gmail.com'
    # mail.settings.login = 'merch.noreply@gmail.com:45Password123' # 45Password123
    # mail.settings.tls = 'smtp.tls'    

    _to = db(db.auth_membership.group_id == 3).select().first()    
    # _msg = "You have pending leave application required for your approval.\n\nPlease click this link http://10.128.4.21:3010/Merch_HR to access your HR workflow.\n\nNOTE: This is an auto-generated email. Please do not reply."
    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending leave application required for your approval.</p>                
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """
    mail.send(
        to=[_to.user_id.email],
        subject='HR WORKFLOW REMINDER',
        message = _msg)    
    
    return dict()

def get_application_mngt_leave_grid():
    row = []
    ctr = 0
    
    _query = db(((db.Employee_Master_Leave.created_by == auth.user_id) & (db.Employee_Master_Leave.canceled == False)& (db.Employee_Master_Leave.status_id != 16)) | ((db.Employee_Master_Leave.status_id == 6) | (db.Employee_Master_Leave.status_id == 7) & (db.Employee_Master_Leave.canceled == False)) &  (db.Employee_Master_Leave.canceled == False) & ((db.Employee_Master_Leave.type_of_leave_id == 1) | (db.Employee_Master_Leave.type_of_leave_id == 2) |(db.Employee_Master_Leave.type_of_leave_id == 3) |(db.Employee_Master_Leave.type_of_leave_id == 4) | (db.Employee_Master_Leave.type_of_leave_id == 5)| (db.Employee_Master_Leave.type_of_leave_id == 6)| (db.Employee_Master_Leave.type_of_leave_id == 8)| (db.Employee_Master_Leave.type_of_leave_id == 7) |(db.Employee_Master_Leave.type_of_leave_id == 9))).select(orderby = ~db.Employee_Master_Leave.id)    
    # _query = db((db.Employee_Master_Leave.created_by == auth.user_id) | ((db.Employee_Master_Leave.status_id == 6) | (db.Employee_Master_Leave.status_id == 7)) &  (db.Employee_Master_Leave.canceled == False) & ((db.Employee_Master_Leave.type_of_leave_id == 1) | (db.Employee_Master_Leave.type_of_leave_id == 4) | (db.Employee_Master_Leave.type_of_leave_id == 5)| (db.Employee_Master_Leave.type_of_leave_id == 6)| (db.Employee_Master_Leave.type_of_leave_id == 8)| (db.Employee_Master_Leave.type_of_leave_id == 9))).select(orderby = ~db.Employee_Master_Leave.id)    
    # print '------',
    head = THEAD(TR(TH('#'),TH('Transaction Date'),TH('Type of Leave'),TH('Date From'),TH('Date To'),TH('Duration'),TH('Name'),TH('Dept.Approved'),TH('HR Approved'),TH('Status',**{'_data-field':'status_id','_data-sortable':'true'}),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in _query:
        # print 'mangt: ', n.employee_id
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_mgnr_view_id', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
        cale_lnk = A(I(_class='fa fa-calendar-check-o'), _title='Leave Chart', _type='button ', _role='button', _target='blank', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_application_dept_leave_chart_id', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk, cale_lnk)
        _ei = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
        if n.employe_id.middle_name == None:
            _middle_name = ''
        else:
            _middle_name = n.employe_id.middle_name
        _emp_na = n.employee_id.first_name, ' ',_middle_name, ' ' ,n.employee_id.last_name, ', ', SPAN(_ei.account_code,_class='text-muted')
        # row.append(TR(TD(ctr),TD(n.application_date),TD(n.type_of_leave_id.type_of_leave),TD(_emp_na),TD(843),TD(_emp_ds),TD(n.status_id.status),TD(n.status_id.action_required),TD(n.remarks),TD(btn_lnk)))
        if int(n.status_id) == 2:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
        else:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
        if n.dept_approved_by == None:
            _app_by = 'None'
        else:
            _app_by = n.dept_approved_by.first_name.upper()
        if n.hr_approved_by == None:
            _hr_by = 'None'
        else:
            _hr_by = n.hr_approved_by.first_name.upper()
        if n.application_date == None:
            _app_d = 'None'
        else:
            _app_d = n.application_date.strftime('%d%b%Y')
        if n.from_effective_date == None:
            _fro_d = 'None'
        else:
            _fro_d = n.from_effective_date.strftime('%a,%d%b%Y')
        row.append(TR(
            TD(ctr),
            TD(_app_d),
            TD(n.type_of_leave_id.type_of_leave),
            TD(_fro_d),
            TD(n.to_effective_date.strftime('%a,%d%b%Y')),
            TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),
            TD(_emp_na),TD(_app_by),T(_hr_by),TD(n.status_id.status ),TD(B(n.status_id.action_required)),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table display nowrap' , _style="width:100%")
    return dict(table = table)

def get_application_mngt_leave_id_approved():   
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]        
    _memo_to = str(_id.employee_id.first_name) + ' ' + str(_id.employee_id.middle_name) + ' ' + str(_id.employee_id.last_name)
    _leave_type = _id.type_of_leave_id.type_of_leave
    _subject = str(_leave_type) + ' - ' + str(_memo_to)    
    if (int(_id.type_of_leave_id) == 2) or (int(_id.type_of_leave_id) == 3) or (int(_id.type_of_leave_id) == 7):        
        _pre.update_record(serial_key = _skey)   
        db.Memorandum.insert(memorandum_prefix_no_id = 4,memorandum_no=_ckey, memorandum_date=request.now, memorandum_from = 'PERSONNEL DEPT',memorandum_to = _memo_to, memorandum_subject = _subject )
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 16, mngt_approved_by = auth.user_id)
        response.js = "jQuery(GenerateMemo())"        
    else:        
        db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 9, mngt_approved_by = auth.user_id, mngt_remarks = request.vars.mngt_remarks)
        response.js = "jQuery(GenerateMemo())"
def get_application_mngt_leave_id_rejected():    
    db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 2, rejected_by = auth.user_id, mngt_remarks = request.vars.mngt_remarks)

def put_application_mngt_leave_id_remarks():    
    # print 'put_application_mngt_leave_id_remarks: ', request.vars.mngt_remarks
    db(db.Employee_Master_Leave.id == request.args(0)).update(mngt_remarks = request.vars.mngt_remarks)
    response.js = "jQuery(alertify.success('Remarks sent...'));"

def validate_updated_application(form):
    form.vars.remarks = ''

@auth.requires_login()
def put_application_leave_id():
    db.Employee_Master_Leave.date_returned.writable = False
    db.Employee_Master_Leave.manager_assigned.writable = False 
    _rec = db.Employee_Master_Leave(request.args(0)) or redirect(URL('get_application_leave_grid'))
    rec = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    db.Employee_Master_Leave.from_effective_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Employee_Master_Leave.to_effective_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Employee_Master_Leave.leave_days_per_year.writable = False
    db.Employee_Master_Leave.working_days.writable = False
    db.Employee_Master_Leave.entitled_days.writable = False
    db.Employee_Master_Leave.last_joining_date.writable = False
    # db.Employee_Master_Leave.type_of_leave_id.writable = False
    
    # db.Employee_Master_Leave.type_of_leave_id.writable = False
    if auth.has_membership(role='MANAGEMENT'):
        _status = 9        
        _query = (db.Leave_Status.id == 2) | (db.Leave_Status.id == 7)
        _leave =  (db.Type_Leave.id >= 1) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
    elif auth.has_membership(role='HR MANAGER'):
        _query = (db.Leave_Status.id == 7) | (db.Leave_Status.id == 8) | (db.Leave_Status.id == 1)
        _leave =  (db.Type_Leave.id >= 1) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _status = 7
    elif auth.has_membership(role='ADMINISTRATION MANAGER'):
        _query = db.Leave_Status.id <= 2
        _leave =  (db.Type_Leave.id >= 1) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _status = 1
    elif auth.has_membership(role='BACK OFFICE DEPARTMENT'):
        _status = 4
        _query = db.Leave_Status.id <= 2
        _leave =  (db.Type_Leave.id != 8) & (db.Type_Leave.id != 9) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
    elif auth.has_membership(role='DEPARTMENT MANAGERS'):
        _status = 4
        _query = db.Leave_Status.id <= 2
    else:        
        _leave =  (db.Type_Leave.id != 8) & (db.Type_Leave.id != 9) & (db.Type_Leave.id != 10) & (db.Type_Leave.id != 11) 
        _query = db.Leave_Status.id <= 2
        _status = 1        
    db.Employee_Master_Leave.status_id.requires = IS_IN_DB(db(_query), db.Leave_Status.id, '%(status)s', zero = 'Choose Status')
    db.Employee_Master_Leave.status_id.default = _status    

    _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()    
    _default_employee = int(_id.employee_id)        
    _employee_id = db.Employee_Master.id == _id.employee_id

    db.Employee_Master_Leave.type_of_leave_id.requires = IS_IN_DB(db(_leave), db.Type_Leave.id, '%(type_of_leave)s', zero = 'Choose Type')
    db.Employee_Master_Leave.employee_id.requires = IS_IN_DB(db(_employee_id), db.Employee_Master, '%(first_name)s %(middle_name)s %(last_name)s', zero = 'Choose Employee')
    db.Employee_Master_Leave.employee_id.default = _id.employee_id
    form = SQLFORM(db.Employee_Master_Leave, request.args(0), upload=URL('default','download'))
    if form.process(onvalidation = put_validate_application).accepted:
        if auth.has_membership(role='DEPARTMENT MANAGERS'):
            redirect(URL('leave_mngt','get_application_dept_leave_grid'))        
        else:
            redirect(URL('leave_mngt','get_application_leave_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'           
    _row = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if _row.dept_approved_by == None:
        _dept = ''
    else:
        _dept = str(_row.dept_approved_by.first_name.upper()[:1]) + str(_row.dept_approved_by.last_name.upper()[:1]) + ': ' + str(_row.dept_remarks)
    if _row.hr_approved_by == None:
        _hum = ''
    else:
        _hum = str(_row.hr_approved_by.first_name.upper()[:1]) + str(_row.hr_approved_by.last_name.upper()[:1]) + ': ' + str(_row.hr_remarks)
    if _row.mngt_approved_by == None:
        _mngt = ''
    else:
        _mngt = str(_row.mngt_approved_by.first_name.upper()[:1]) + str(_row.mngt_approved_by.last_name.upper()[:1]) + ': ' + str(_row.mngt_remarks)
    _remarks = _dept + str('\n') + _hum + str('\n') + _mngt
             
    return dict(form = form, rec = rec, _remarks = _remarks)

def get_application_leave_id():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if _id.dept_approved_by == None:
        _dept = ''
    else:
        _dept = str(_id.dept_approved_by.first_name.upper()[:1]) + str(_id.dept_approved_by.last_name.upper()[:1]) + ': ' + str(_id.dept_remarks)
    if _id.hr_approved_by == None:
        _hum = ''
    else:
        _hum = str(_id.hr_approved_by.first_name.upper()[:1]) + str(_id.hr_approved_by.last_name.upper()[:1]) + ': ' + str(_id.hr_remarks)
    if _id.mngt_approved_by == None:
        _mngt = ''
    else:
        _mngt = str(_id.mngt_approved_by.first_name.upper()[:1]) + str(_id.mngt_approved_by.last_name.upper()[:1]) + ': ' + str(_id.mngt_remarks)
    _remarks = _dept + str('\n') + _hum + str('\n') + _mngt    
    return dict(_id = _id, _remarks = _remarks )

@auth.requires_login()
def get_application_leave_user_id():
    _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    _row = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    form = SQLFORM(db.Employee_Master_Leave, request.args(0), upload=URL('default','download'))
    if form.process().accepted:
        response.flash = 'updated'
    elif form.errors:        
        response.flash = 'form has error'
    if _row.dept_approved_by == None:
        _dept = ''
    else:
        _dept = str(_row.dept_approved_by.first_name.upper()[:1]) + str(_row.dept_approved_by.last_name.upper()[:1]) + ': ' + str(_row.dept_remarks)
    if _row.hr_approved_by == None:
        _hum = ''
    else:
        _hum = str(_row.hr_approved_by.first_name.upper()[:1]) + str(_row.hr_approved_by.last_name.upper()[:1]) + ': ' + str(_row.hr_remarks)
    if _row.mngt_approved_by == None:
        _mngt = ''
    else:
        _mngt = str(_row.mngt_approved_by.first_name.upper()[:1]) + str(_row.mngt_approved_by.last_name.upper()[:1]) + ': ' + str(_row.mngt_remarks)
    _remarks = _dept + str('\n') + _hum + str('\n') + _mngt

    return dict(form = form,_row = _row, _remarks = _remarks,_usr=_usr)

def get_applicaton_leave_history_id(): # view 
    
    _query = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _tl = db(db.Type_Leave.id == _query.type_of_leave_id).select().first()
    _id = db(db.Employee_Master.id == _query.employee_id).select().first()
    _no = db(db.Employee_Employment_Details.employee_id == _id.id).select().first()
    _sum = db.Employee_Master_Leave.duration_leave.sum()
    _appli = db((db.Employee_Master_Leave.employee_id == _query.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == _query.type_of_leave_id) & (db.Employee_Master_Leave.status_id != 16)).select(_sum).first()[_sum]
    _pending = db((db.Employee_Master_Leave.employee_id == _query.employee_id) & (db.Employee_Master_Leave.type_of_leave_id == _query.type_of_leave_id) & (db.Employee_Master_Leave.status_id <= 9) & (db.Employee_Master_Leave.canceled == False)).count()
    
    _count = db((db.Employee_Master_Leave.id == request.args(0)) & (db.Employee_Master_Leave.status_id == 10) & (db.Employee_Master_Leave.type_of_leave_id == _query.type_of_leave_id)).select(_sum).first()[_sum]
    _balanced = 0
    if _id.residence_no_date == None:
        _res_dat = 'None'
    else:
        _res_dat = _id.residence_no_date#.strftime('%d %b. %Y')
    if _id.health_card_no == None:
        _health = 'None'
    else:
        _health = _id.health_card_no_expiration_date#.strftime('%d %b. %Y')
    if _id.driver_license_no_expiration_date == None:
        _driver = 'None'
    else:
        _driver = _id.driver_license_no_expiration_date#.strftime('%d %b. %Y')
    _title = _tl.type_of_leave, ' Information'
    _table_id = DIV(TABLE(TBODY(TR(TH('Card Name'),TH('Card #'),TH('Date Issued'),TH('Date Expiration')),
    TR(TD('Residence Permit'),TD(_id.residence_permit_no),
    TD(_res_dat),
    TD(_id.residence_permit_no_expiration_date)),
    TR(TD('Passport'),TD(_id.passport_no),TD(_id.passport_date_issued),TD(_id.passport_date_expiration)),
    TR(TD('Health Card'),TD(_id.health_card_no),TD(),TD(_health)),
    TR(TD('Driver License'),TD(_id.driver_license_no),TD(),TD(_driver))),_class='table'),_class='info-box bg-green')    
    _emergency = 0
    _proportionate = _row2 =''
    if (int(_query.type_of_leave_id) == 1) or (int(_query.type_of_leave_id) == 8) or (int(_query.type_of_leave_id) == 9): # Annual Leave        
        for n in db((db.Employee_Master_Leave.employee_id == _query.employee_id) & (db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.type_of_leave_id == 5)).select():
            if n.from_effective_date > _no.last_joining_date:                
                _emergency += n.duration_leave or 0
            # if not _no.date_last_return > n.from_effective_date:
            #     _emergency += n.duration_leave or 0
        if (_no.date_last_return == _no.date_joined) and (_query.working_days < 365):
            _proportionate = T('Proportional Air ticket covering %s %%{day} of service. ', _query.working_days or 0)
        elif _no.date_last_return != _no.date_joined:
            if _query.leave_days_per_year == 28:
                _x = 365 - 28
                if int(_query.working_days) < int(_x):
                    _proportionate = T('Proportional Air ticket covering %s %%{day} of service.', _query.working_days or 0)
                else:
                    _proportionate = T('Entitled for full ticket covering %s %%{day} of service.', _query.working_days or 0)
            elif _query.leave_days_per_year == 30:
                _x = 365 - 30
                _proportionate = T('Entitled for full ticket covering %s %%{day} of service.',  _query.working_days or 0)
            
        _row2 = TABLE(TBODY(TR(TD('Paid Leave:'),TD(T('%s %%{day}',_query.entitled_days or 0)),TD('Total Working Days:'),TD(T('%s %%{day}',_query.working_days or 0))),
        TR(TD('Paid Leave/Year:'),TD(T('%s %%{day}',_query.leave_days_per_year or 0)),TD('Total Emergency Leave:'),TD(T('%s %%{day}', locale.format('%d', _emergency or 0, grouping = True)))),
        TR(TD('Last Joining Date:'),TD(_query.last_joining_date.strftime('%d %b. %Y')),TD('Engagement Date:'),TD(_no.date_joined.strftime('%d %b. %Y'))),
        TR(TD('Air Ticket: '),TD(_no.air_fare, _colspan='3')),
        TR(TD('Remarks:'),TD('To deduct absent days if any from the monthly salary',_colspan='3')),
        TR(TD(),TD('Economy Class Air ticket: ' + str(_no.sector),_colspan='3')), 
        TR(TD(),TD(_proportionate,_colspan='3')),         
        TR(TD('Note: This leave will be paid leave.',_colspan='4'))), _class='table')
        # print 'working days: ', _query.working_days or 0
        _table_id = _table_id
    elif int(_query.type_of_leave_id) == 2: # Compassionate Leave
        _balanced = int(3) - int(_appli or 0)
        _row2 = TABLE(TBODY(TR(TH('Total paid compassionate leave/year'),TH('Availed (including this leave)'),TH('Balance entitlement for the year'),TH('Pending Application')),
        TR(TD('3 days'),TD(T('%s %%{day}',locale.format('%d', _appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d', _balanced or 0, grouping = True))),TD(_pending or 0)),
        TR(TD('Note: This leave will be paid leave.'),TD(),TD(),TD())), _class='table')
        _table_id = ''

    elif int(_query.type_of_leave_id) == 3: # Sick Leave
        # _balanced = 14 - _appli
        _half_paid = 0
        _row2 = TABLE(TBODY(TR(TH('Total Paid Sick Leave/Year'),TH('Availed (including this leave)'),TH('Balanced Remaining'),TH('Paid Leave'),TH('Half Paid Leave')),
        TR(TD('14 days'),TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_count or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_count or 0, grouping = True))), TD(T('%s %%{day}',locale.format('%d',_half_paid or 0, grouping = True)))),
        TR(TD('Note: This leave will be paid leave.',_colspan='5'))),_class='table')
        _table_id = _table_id
    elif int(_query.type_of_leave_id) == 4: # Business Leave
        _row2 = TABLE(TBODY(TR(TH('Leave Applied For'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(_pending))),_class='table')
        _table_id = _table_id
    elif int(_query.type_of_leave_id) == 5: # Emergency Leave
        _row2 = TABLE(TBODY(TR(TH('Leave Applied For'),TH('Availed (including this leave)'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d',_count or 0, grouping = True))),TD(_pending))),_class='table')
        _table_id = _table_id
    elif int(_query.type_of_leave_id) == 6: # Maternity Leave
        _balanced = 50 - _appli
        _row2 = TABLE(TBODY(TR(TH('Total Paid Maternity Leave/Year'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(locale.format('%d',_pending or 0, grouping = True)))),_class='table')
        _table_id = _table_id
    elif int(_query.type_of_leave_id) == 7: # Day Off(Excess Hours)
        _row2 = TABLE(TBODY(TR(TH('Total Excess Hours applied (including this leave)'),TH('Availed (including this leave)'),TH('Pending')),
        TR(TD(T('%s %%{day}',locale.format('%d',_appli or 0, grouping = True))),TD(T('%s %%{day}',locale.format('%d', _count or 0, grouping = True))),TD(_pending)),
        TR(TD('Note: This leave will be paid leave.'),TD(),TD())),_class='table')
        _table_id = ''
    if _no.designation_code_id == None:
        _desig = 'None'
    else:
        _desig = _no.designation_code_id
    if _no.department_code_id == None:
        _dept = 'None'
    else:
        _dept = _no.department_code_id
    if _id.middle_name == None:
        _middle_name = ''
    else:
        _middle_name = _id.middle_name.upper()
    return XML(DIV(
        DIV(
            DIV(SPAN(I(_class='fa fa-user-o'),_class='info-box-icon'),
            DIV(SPAN(_title,_class='info-box-text'),SPAN(_id.first_name.upper(),' ',_middle_name, ' ', _id.last_name.upper(), ', ' ,_no.account_code,_class='info-box-number'),
            DIV(B(str(_no.designation_code_id.designation_name)) + str(', ') + str(_no.department_code_id.department_name)),
            _class='info-box-content'),_class='info-box bg-yellow'),
            DIV(_table_id),
            _class="col-md-6 col-sm-6 col-sx-6"),
        DIV(
            DIV(SPAN(I(_class='fa fa-calendar'),_class='info-box-icon'),DIV(_row2,
            _class='info-box-content'),_class='info-box bg-light-blue-active'),_class="col-md-6 col-sm-6 col-sx-6")        
    ))

def put_application_leave_cancel_id():
    print 'put_application_leave_cancel_id: ', request.args(0)
    db(db.Employee_Master_Leave.id == request.args(0)).update(canceled = True)
    
def get_application_leave_account_grid():
    row = []
    ctr = 0
    # _query = db((db.Employee_Master_Leave.status_id == 10 ) | ((db.Employee_Master_Leave.created_by == auth.user_id) & (db.Employee_Master_Leave.status_id != 16) & (db.Employee_Master_Leave.canceled == False))).select(orderby = ~db.Employee_Master_Leave.id)
    # head = THEAD(TR(TH('#'),TH('Date'),TH('Type of Leave'),TH('Name'),TH('Department'),TH('Designation'),TH('Status'),TH('Required Action'),TH('Remarks'),TH('Action')))    
    head = THEAD(TR(TH('#'),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave',**{'_data-field':'type_of_leave_id','_data-sortable':'true'}),TH('Date From'),TH('Date To'),TH('Duration'),TH('Name'),TH('Status',**{'_data-field':'status_id','_data-sortable':'true'}),TH('Action Required'),TH('Action')),_class='bg-primary')
    for n in db((db.Employee_Master_Leave.status_id == 10) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','post_application_leave_account_id', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('leave_mngt','put_application_leave_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', callback = URL('procurement','generate_purchase_order_no',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk,prin_lnk)
        _ei = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
        if not _ei:
            _emp_no = 'None'
            _emp_de = 'None'
            _emp_ds = 'None'
        else:
            _emp_no = _ei.employee_no
            if not _ei.department_code_id: 
                _emp_de = _emp_ds = 'None'
            else:
                _emp_de = _ei.department_code_id.department_name
            if not _ei.designation_code_id:
                _emp_de = _emp_ds = 'None'
            else: 
                _emp_ds = _ei.designation_code_id.designation_name
        if not n.employee_id:
            _emp_na = 'None'
        else:
            _emp_na = n.employee_id.first_name, ' ',n.employee_id.middle_name, ' ' ,n.employee_id.last_name, ', ', _ei.account_code
        row.append(TR(TD(ctr),TD(n.application_date.strftime('%d%b%Y')),TD(n.type_of_leave_id.type_of_leave),TD(n.from_effective_date.strftime('%d%b%Y')),TD(n.to_effective_date.strftime('%d%b%Y')),TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),TD(_emp_na),TD(n.status_id.status ),TD(n.status_id.action_required),TD(btn_lnk)))    
    body = TBODY(*row)    
    table = TABLE(*[head, body], _class='table')#, _id='table', **{'_data-toggle':'table','_data-detail-view':'true','_data-detail-view-by-click':'true','_data-detail-formatter':'detailFormatter'})
    return dict(table = table)

def validate_settlement_account(form):
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    form.vars.employee_master_leave_id = request.args(0)
    form.vars.employee_id = _id.employee_id    

def post_application_leave_account_id():        
    # _args = db(db.Leave_Salary_Slip.employee_master_leave_id == request.args(0)).select().first()
    # if db(db.Leave_Salary_Slip.employee_master_leave_id == request.args(0)).select().first():        
    #     redirect(URL('leave_mngt','put_application_leave_account_id', args = _args.id))            
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _ei = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()
    _ai = db(db.Employee_Master_Account_Info.employee_id == _id.employee_id).select().first()
    _cm = db(db.Current_Month_Leave_Salary_Slip.employee_master_leave_id == request.args(0)).select().first()
    if int(_id.type_of_leave_id) == 6: # maternity
        _paid_salary = ((_ai.total_gross_pay * 12) / 365) * int(_id.entitled_days or 0)        
    else:            
        _paid_salary = (((_ai.basic_income + _ai.housing_allowances) * 12) / 365) * int(_id.entitled_days or 0)
    _days = _id.from_effective_date.day - 1
    if _id.leave_encashment == True:
        _month_salary = 0
    else:
        _month_salary = ((float(_ai.net_pay) * 12) / 365) * _days
    
    if not _cm:
        _month_salary = ((float(_ai.net_pay) * 12) / 365) * _days
    else:
        _month_salary = _cm.total_gross
    _net_total = float(round(_paid_salary)) + float(round(_month_salary))    
    # db.Leave_Salary_Slip.leave_salary.default = locale.format('%.2f',round(_paid_salary) or 0, grouping = True)    
    # db.Leave_Salary_Slip.month_salary.default = locale.format('%.2f',round(_month_salary) or 0, grouping = True)
    # db.Leave_Salary_Slip.total_gross.default = locale.format('%.2f',round(_net_total) or 0, grouping = True)
    # db.Leave_Salary_Slip.net_total.default = locale.format('%.2f',round(_net_total) or 0, grouping = True)

    db.Leave_Salary_Slip.leave_salary.default = round(_paid_salary)
    db.Leave_Salary_Slip.month_salary.default = round(_month_salary) 
    db.Leave_Salary_Slip.total_gross.default = round(_net_total) 
    db.Leave_Salary_Slip.net_total.default = round(_net_total) 

    db.Leave_Salary_Slip.remarks.default = _id.remarks
    _rec = db(db.Leave_Salary_Slip.employee_master_leave_id == request.args(0)).select().first()
    form = SQLFORM(db.Leave_Salary_Slip, _rec)
    if form.process(onvalidation = validate_settlement_account).accepted:
        response.flash = 'SAVE'      
    elif form.errors:
        response.flash = 'ERROR'                
    return dict(form = form, _row = _id, _ei = _ei, _ai = _ai, _month_salary = _month_salary)

def put_application_save_and_print_id():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()        
    _ai = db(db.Employee_Master_Account_Info.employee_id == _id.employee_id).select().first()        
    _lss = db(db.Leave_Salary_Slip.employee_master_leave_id == int(request.args(0))).select().first()
    if not _lss:           
        db.Leave_Salary_Slip.insert(
            employee_master_leave_id = request.args(0),
            employee_id = _id.employee_id,
            leave_salary = float(request.vars.leave_salary.replace(',','')),
            air_ticket = request.vars.air_ticket,
            commission_or_bonus = request.vars.commission_or_bonus,
            salary_due = request.vars.salary_due,
            gratuity = request.vars.gratuity,
            other_payments = request.vars.other_payments,
            month_salary = float(request.vars.month_salary.replace(',','')),
            total_gross = float(request.vars.total_gross.replace(',','')),
            deductions = request.vars.deductions,
            net_total = float(request.vars.net_total.replace(',','')),
            remarks = request.vars.remarks)    
        _days = _id.from_effective_date.day - 1
        _basic_salary = float(((_ai.basic_income * 12) / 365) * _days)
        _house_alw = float(((_ai.housing_allowances * 12) / 365) * _days)
        _car_alw = float(((_ai.car_allowances * 12) / 365) * _days)
        _food_alw = float(((_ai.food_allowances * 12) / 365) * _days)
        _petrol_alw = float(((_ai.petrol_allowances * 12) / 365) * _days)
        _incentive = float(((_ai.incentive * 12) / 365) * _days)
        _others = float(((_ai.others * 12) / 365) * _days)
        _total_gross = float(_basic_salary + _house_alw + _car_alw + _food_alw +_petrol_alw + _incentive + _others)
        
        if _id.leave_encashment == True:
            db.Current_Month_Leave_Salary_Slip.insert(employee_master_leave_id = request.args(0),employee_id = _id.employee_id,
                basic_salary = 0,housing_allowances = 0,car_allowances = 0,food_allowances = 0,petrol_allowances = 0,
                incentive_bonus = 0,others = 0,total_gross = 0,remarks = request.vars.remarks)
        else:
            db.Current_Month_Leave_Salary_Slip.insert(employee_master_leave_id = request.args(0),employee_id = _id.employee_id,
                basic_salary = _basic_salary,housing_allowances = _house_alw,car_allowances = _car_alw,food_allowances = _food_alw,
                petrol_allowances = _petrol_alw,incentive_bonus = _incentive,others = _others,total_gross = _total_gross,remarks = request.vars.remarks)
    else:             
        
        _lss.update_record(
            leave_salary = float(request.vars.leave_salary.replace(',','')),
            air_ticket = request.vars.air_ticket,
            commission_or_bonus = request.vars.commission_or_bonus,
            salary_due = request.vars.salary_due,
            gratuity = request.vars.gratuity,
            other_payments = request.vars.other_payments,
            month_salary = float(request.vars.month_salary.replace(',','')),
            total_gross = float(request.vars.total_gross.replace(',','')),
            deductions = request.vars.deductions,
            net_total = float(request.vars.net_total.replace(',','')),
            remarks = request.vars.remarks)           
        if float(request.vars.month_salary.replace(',','')) == 0.0:
            db(db.Current_Month_Leave_Salary_Slip.employee_master_leave_id == request.args(0)).update(
                basic_salary = 0,housing_allowances = 0,car_allowances = 0,food_allowances = 0,petrol_allowances = 0,
                incentive_bonus = 0,others = 0,total_gross = 0,remarks = request.vars.remarks)        

def put_monthly_slip_id():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()        
    _ai = db(db.Employee_Master_Account_Info.employee_id == _id.employee_id).select().first()
    _days = _id.from_effective_date.day - 1
    _basic_salary = float(((_ai.basic_income * 12) / 365) * _days)
    _house_alw = float(((_ai.housing_allowances * 12) / 365) * _days)
    _car_alw = float(((_ai.car_allowances * 12) / 365) * _days)
    _food_alw = float(((_ai.food_allowances * 12) / 365) * _days)
    _petrol_alw = float(((_ai.petrol_allowances * 12) / 365) * _days)
    _incentive = float(((_ai.incentive * 12) / 365) * _days)
    _others = float(((_ai.others * 12) / 365) * _days)
    _total_gross = float(_basic_salary + _house_alw + _car_alw + _food_alw +_petrol_alw + _incentive + _others)
    head = THEAD(TR(TH('Basic Salary'),TH('Housing Allw.'),TH('Petrol Allw.'),TH('Car Allw.'),TH('Food Allw.'),TH('Others'),TH('Incd/Bonus'),TH('Total Gross'),TH('Action')))
    body = TBODY(TR(
        TD(INPUT(_class='form-control',_type='text',_name='basic_income',_value=locale.format('%.2F',round(_basic_salary) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='housing_allowances',_value=locale.format('%.2F',round(_house_alw) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='car_allowances',_value=locale.format('%.2F',round(_car_alw) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='food_allowances',_value=locale.format('%.2F',round(_food_alw) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='petrol_allowances',_value=locale.format('%.2F',round(_petrol_alw) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='incentive',_value=locale.format('%.2F',round(_incentive) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='others',_value=locale.format('%.2F',round(_others) or 0, grouping = True))),
        TD(INPUT(_class='form-control',_type='text',_name='_total_gross',_value=locale.format('%.2F',round(_total_gross) or 0, grouping = True))),
        TD(INPUT(_id='btnSubmit', _name= 'btnSubmit', _type='submit', _value='Submit', _class='btn btn-success'))))    
    form = FORM(TABLE(*[head, body]), _class='table')
    if form.accepts(request, session):
        if request.vars.btnSubmit:
            print 'submitted'
        print 'ok'
        response.js = "jQuery(console.log('ok'))"
    elif form.errors:
        print form.errors
    return dict(form = form)
  
def put_application_settled_id():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if (int(_id.type_of_leave_id) == 8) or (int(_id.type_of_leave_id) == 9):        
        _id.update_record(status_id = 16)        
        db(db.Employee_Master.id == int(_id.employee_id)).update(employee_status_id = _id.type_of_leave_id)
        # insert here to copy to EOS table for HR Reminders Process
        db.EOS.insert(employee_id = _id.employee_id,status_id = 2)
    else:        
        _id.update_record(status_id = 11)

def put_application_leave_account_id_approved():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    # db.Employee_Master_Leave.insert(employee_id = _id.employee_id)
    db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 11)
    # print 'approved: ', request.args(0), _id.employee_id
     
def put_application_leave_account_id_rejected():    
    # db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 10)
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    # print 'rejected: ', request.args(0), _id.employee_id

def get_joining_report_grid():
    ctr = 0
    row = []
    form = SQLFORM.factory(
        Field('from_date','date', default = request.now),
        Field('to_date','date', default = request.now))
    if form.accepts(request):                
        head = THEAD(TR(TD('#'),TD('Ref.No.'),TD('Joining Date'),TD('Name'),TD('From Date'),TD('To Date'),TD('Status')))
        for n in db((db.Employee_Master_Leave.type_of_leave_id == 1) & (db.Employee_Master_Leave.type_of_leave_id == 16) & (db.Employee_Master_Leave.joining_application_date >= request.vars.from_date) & (db.Employee_Master_Leave.joining_application_date <= request.vars.to_date)).select():
            ctr += 1
            row.append(TR(
                TD(ctr),
                TD(n.joining_doc_ref_no),
                TD(n.joining_application_date.strftime('%d %b. %Y')),
                TD(n.employee_id.first_name,' ', n.employee_id.middle_name,' ', n.employee_id.last_name),
                TD(n.from_effective_date.strftime('%d %b. %Y')),
                TD(n.to_effective_date.strftime('%d %b. %Y')),
                TD(n.status_id.status)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table')
        return dict(form = form, table = table)

    elif form.errors:
        print 'form error'
    return dict(form = form, table = '')

def get_leave_report_grid():
    ctr = 0
    row = []

    form = SQLFORM.factory(
        Field('from_date','date', default = request.now),
        Field('to_date','date', default = request.now))
    if form.accepts(request):                
        head = THEAD(TR(TD('#'),TD('Ref.No.'),TD('Leave Type'),TD('Name'),TD('From Date'),TD('To Date'),TD('Status')))
        for n in db(((db.Employee_Master_Leave.type_of_leave_id == 1) | (db.Employee_Master_Leave.type_of_leave_id == 4) | (db.Employee_Master_Leave.type_of_leave_id == 5)) &(db.Employee_Master_Leave.status_id == 16) &  (db.Employee_Master_Leave.from_effective_date >= request.vars.from_date) & (db.Employee_Master_Leave.to_effective_date <= request.vars.to_date)).select(orderby = ~db.Employee_Master_Leave.from_effective_date):
            ctr += 1
            row.append(TR(
                TD(ctr),
                TD(n.doc_ref_no),              
                TD(n.type_of_leave_id.type_of_leave),           
                TD(n.employee_id.first_name,' ', n.employee_id.middle_name,' ', n.employee_id.last_name),       
                TD(n.from_effective_date.strftime('%d %b. %Y')),
                TD(n.to_effective_date.strftime('%d %b. %Y')),                
                TD(n.status_id.status)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table')
        return dict(form = form, table = table)

    elif form.errors:
        print 'form error'
    return dict(form = form, table = '')

def get_years_of_services_report_grid():
    row = []
    ctr = 0
    _today = date.today()
    head = THEAD(TR(TH('#'),TH('Name'),TH('Department'),TH('Engagement Date'),TH('Year of Services'),TH('Age'),TH('Action')))
    _query = db(db.Employee_Master.employee_status_id == 1).select(db.Employee_Master.ALL, db.Employee_Employment_Details.ALL,orderby= db.Employee_Employment_Details.date_joined, left = db.Employee_Employment_Details.on(db.Employee_Master.id == db.Employee_Employment_Details.employee_id))
    for n in _query:
        ctr += 1
        _name = str(n.Employee_Master.title)+str(n.Employee_Master.first_name) +' '+ str(n.Employee_Master.middle_name) + ' ' + str(n.Employee_Master.last_name)
        if n.Employee_Employment_Details.department_code_id == None:
            _dept = 'None'
        else:            
            _dept = n.Employee_Employment_Details.department_code_id.department_name
        if n.Employee_Employment_Details.date_joined == None:
            _join = 'None'
        else:
            _join = n.Employee_Employment_Details.date_joined
        if n.Employee_Employment_Details.date_joined == None:
            _serv = 'None'            
        else:
            _serv = _today.year - n.Employee_Employment_Details.date_joined.year
        if n.Employee_Master.birth_date == None:
            _bday = 'None'
        else:
            _bday = _today.year - n.Employee_Master.birth_date.year
        row.append(TR(
            TD(ctr),
            TD(_name),
            TD(_dept),
            TD(_join),
            TD(_serv),
            TD(_bday),
            TD(),
        ))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def get_rejected_leave_report_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Name'),TH('Type of leave'),TH('Date From'),TH('Date To'),TH('Duration'),TH('Rejected By'),TH('HR Status'),TH('Action')))
    # print '---=---'
    for n in db((db.Employee_Master_Leave.canceled == True) | ((db.Employee_Master_Leave.status_id == 2) | (db.Employee_Master_Leave.status_id == 5) | (db.Employee_Master_Leave.status_id == 8))).select(db.Employee_Master_Leave.ALL):
        ctr+=1

        if n.canceled == True:                        
            action = DIV(DIV(A(I(_class='fa fa-calendar-times-o'),_title = 'Canceled', _class='btn btn-icon-toggle disabled',_type='button'),_class='input-group_append'),_class='input-group')            
        elif n.status_id == 2 and n.rejected_status == False or n.rejected_status == None:            
            action = DIV(DIV(A(I(_class='fa fa-bell-slash'),_title = 'Pending', _class='btn btn-outline-secondary dropdown-toggle',_type='button',**{'_data-toggle':'dropdown','_aria-haspopup':'true','aria-expanded':'false'}),
                DIV(LI(A(I(_class='fa fa-bell-slash-o'),'Pending',_class='dropdown-item',callback=URL('leave_mngt','put_rejected_pending_id',args=n.id))),
                    LI(A(I(_class='fa fa-bell-o'),'Settled',_class='dropdown-item',_id='not',callback=URL('leave_mngt','put_rejected_settled_id',args=n.id))),
                    _class='dropdown-menu'),_class='input-group_append'),_class='input-group')
        else:
            action = DIV(DIV(A(I(_class='fa fa-bell'),_title = 'Settled',_class='btn btn-outline-secondary dropdown-toggle',_type='button',**{'_data-toggle':'dropdown','_aria-haspopup':'true','aria-expanded':'false'}),
                DIV(LI(A(I(_class='fa fa-bell-slash-o'),'Pending',_class='dropdown-item',callback=URL('leave_mngt','put_rejected_pending_id',args=n.id))),
                    LI(A(I(_class='fa fa-bell-o'),'Settled',_class='dropdown-item',_id='not',callback=URL('leave_mngt','put_rejected_settled_id',args=n.id))),
                    _class='dropdown-menu'),_class='input-group_append'),_class='input-group')
        btn_lnk = DIV(action)
        if n.rejected_by == None:
            _rej_by = 'None'
        else:
            _rej_by = n.rejected_by.first_name,' ', n.rejected_by.last_name
        if n.rejected_status == True:
            _hr_stat = 'Settled'
        elif n.canceled == True:            
            _hr_stat = SPAN('Canceled',_class='badge bg-red')
        else:
            _hr_stat = 'Pending'
        row.append(TR(
            TD(ctr),
            TD(n.application_date),
            TD(n.employee_id.title,n.employee_id.first_name,' ',n.employee_id.middle_name,' ', n.employee_id.last_name),
            TD(n.type_of_leave_id.type_of_leave),
            TD(n.from_effective_date),            
            TD(n.to_effective_date),
            TD(n.duration_leave),            
            TD(_rej_by),
            TD(n.status_id.status,' - ',_hr_stat),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',_id='tblGrid')
    return dict(table = table)

def put_rejected_pending_id():    
    db(db.Employee_Master_Leave.id == request.args(0)).update(rejected_status = False)
    response.js = "jQuery(alertify.error('Pended'), window.setTimeout(function(){window.location.reload()}, 1000));"

def put_rejected_settled_id():        
    db(db.Employee_Master_Leave.id == request.args(0)).update(rejected_status = True)
    response.js = "jQuery(alertify.success('Settled'), window.setTimeout(function(){window.location.reload()}, 1000));"
    # response.js = "jQuery(alertify.success('Settled'), tbl = $('#tblGrid').DataTable(), tbl.ajax.reload(null,false));"
            #     var table = document.getElementById ("myTable");
            # table.refresh (); $('#example').data.reload() $('#example').DataTable().ajax.reload();
    
def get_pending_leave_application_report_grid():
    row = []
    ctr = 0 
    head = THEAD(TR(TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Department'),TH('Type of Leave', **{'_data-field':'type_of_leave', '_data-sortable':'true'}),TH('Date From',**{'_data-field':'from_effective_date','_data-sortable':'true'}),TH('Date To',**{'_data-field':'to_effective_date','_data-sortable':'true'}),TH('Name'),TH('Duration'),TH('Status'),TH('Action Required')))
    for n in db((db.Employee_Master_Leave.status_id < 11) & (db.Employee_Master_Leave.canceled == False) & (db.Employee_Master_Leave.status_id != 2)).select(db.Employee_Master_Leave.ALL, db.Employee_Employment_Details.ALL, orderby=db.Employee_Employment_Details.department_code_id | ~db.Employee_Master_Leave.id, left = db.Employee_Employment_Details.on(db.Employee_Employment_Details.employee_id == db.Employee_Master_Leave.employee_id)):
        if int(n.Employee_Master_Leave.status_id) == 2:
            _status = str(n.Employee_Master_Leave.status_id.action_required) #+ ", " + str(n.Employee_Master_Leave.updated_by.first_name[:1])+str(n.Employee_Master_Leave.updated_by.last_name[:1])
        else:
            _status = n.Employee_Master_Leave.status_id.action_required
        row.append(TR(
            TD(n.Employee_Master_Leave.application_date),
            TD(n.Employee_Employment_Details.department_code_id.department_name),
            TD(n.Employee_Master_Leave.type_of_leave_id.type_of_leave),
            TD(n.Employee_Master_Leave.from_effective_date),
            TD(n.Employee_Master_Leave.to_effective_date),
            TD(n.Employee_Master_Leave.employee_id.first_name.upper(), ' ',n.Employee_Master_Leave.employee_id.last_name.upper()),
            TD(n.Employee_Master_Leave.duration_leave),
            TD(n.Employee_Master_Leave.status_id.status),
            TD(_status)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    # table = TABLE(*[head, body], _class='table', _id='htmltable', **{'_data-show-export':'true','_data-show-columns':'true','_data-toolbar':'#toolbar','_data-toolbar-align':'left','_data-toggle':'table','_data-search':'true','_data-pagination':'true','_data-classes':'table table-striped'})
    return dict(table = table)
    
def get_on_leave_report_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('Transaction Date'),TH('Department'),TH('Type of Leave'),TH('Date From'),TH('Date To'),TH('Name'),TH('Duration'),TH('Status'),TH('Action Required')))
    for n in db((db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.canceled == False)).select(db.Employee_Master_Leave.ALL, db.Employee_Employment_Details.ALL, orderby=db.Employee_Employment_Details.department_code_id | ~db.Employee_Master_Leave.id, left = db.Employee_Employment_Details.on(db.Employee_Employment_Details.employee_id == db.Employee_Master_Leave.employee_id)):
        row.append(TR(
            TD(n.Employee_Master_Leave.application_date),
            TD(n.Employee_Employment_Details.department_code_id.department_name),
            TD(n.Employee_Master_Leave.type_of_leave_id.type_of_leave),
            TD(n.Employee_Master_Leave.from_effective_date),
            TD(n.Employee_Master_Leave.to_effective_date),
            TD(n.Employee_Master_Leave.employee_id.first_name.upper(), ' ',n.Employee_Master_Leave.employee_id.last_name.upper()),
            TD(n.Employee_Master_Leave.duration_leave),
            TD(n.Employee_Master_Leave.status_id.status),
            TD(n.Employee_Master_Leave.status_id.action_required)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table') #, _id='tblRprt', **{'_data-toolbar':'.toolbar','_data-toolbar-align':'left','_data-toggle':'table','_data-search':'true','_data-pagination':'true','_data-classes':'table table-striped'})
    return dict(table = table)

def load_leave_file_report():
    _usr = db(db.Department_Users_Assignment.users_id == auth.user_id).select().first()
    row = []
    ctr = 0 
    head = THEAD(TR(TH('Transaction No',**{'_data-field':'transaction_no','_data-sortable':'true'}),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave', **{'_data-field':'type_of_leave', '_data-sortable':'true'}),TH('Date From',**{'_data-field':'from_effective_date','_data-sortable':'true'}),TH('Date To',**{'_data-field':'to_effective_date','_data-sortable':'true'}),TH('Name'),TH('Duration'),TH('Date Returned'),TH('Status'),TH('Action Control')))
    if auth.has_membership('ROOT'):
        _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('MANAGEMENT'):
        _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('HR MANAGER'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
        _que = db(db.Employee_Master_Leave.hr_approved_by == auth.user_id).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('ADMINISTRATION MANAGER'): # show all employee leave         
        _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('DEPARTMENT MANAGERS'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
        _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.manager_assigned == _usr.sub_department_id)).select(orderby = ~db.Employee_Master_Leave.id)    
    else:
        _que = db((db.Employee_Master_Leave.employee_id == _usr.employee_id) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == True))).select(orderby = ~db.Employee_Master_Leave.id)
    for n in _que:
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'HR MANAGER'):
            prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle', _href = URL('leave_mngt_reports','get_application_leave_report_id',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
    
        if n.application_date == None:
            _app_dat = 'None'
        else:            
            _app_dat = n.application_date#.strftime('%d%b%Y')
        if n.from_effective_date == None:
            _fro_dat = 'None'
        else:
            _fro_dat = n.from_effective_date#.strftime('%d')
        if n.to_effective_date == None:
            _to_dat = 'None'
        else:
            _to_dat = n.to_effective_date#.strftime('%d%b%Y')
        if n.date_returned == None:
            _dat_re = 'None'
        else:
            _dat_re = n.date_returned#.strftime('%d%b%Y')
        if n.canceled == True:
            _status = P('Canceled', _class='text-red')
        else:
            _status = n.status_id.status
        row.append(TR(
            TD(n.transaction_no),
            TD(_app_dat),
            TD(n.type_of_leave_id.type_of_leave),
            TD(_fro_dat), 
            TD(_to_dat),
            TD(n.employee_id.first_name.upper(),' ', n.employee_id.last_name.upper()),
            TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),
            TD(_dat_re),
            TD(_status),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblRprt', **{'_data-toggle':'table','_data-search':'true','_data-pagination':'true','_data-classes':'table table-striped'})
    return dict(table = table)

def get_leave_file_past_two_year_report():

    import datetime
    print '---- '
    # print datetime.date.today()
    # _year_end = (datetime.datetime.now() - datetime.timedelta(days=2*365)).date()
    _year_end = datetime.date.today() - datetime.timedelta(days=2*365)
    # print _year_end, datetime.date.today() - datetime.timedelta(days=2*365)
    # _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date <= str(_year_end))).select(orderby = ~db.Employee_Master_Leave.id).first()
    # for n in db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date != None) & (db.Employee_Master_Leave.from_effective_date > _year_end)).select(orderby = ~db.Employee_Master_Leave.id):
        # if n.from_effective_date > _year_end:
        # print n.id, n.from_effective_date, ' < ' , _year_end
    grid = SQLFORM.grid((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date != None) & (db.Employee_Master_Leave.from_effective_date > _year_end), orderby = ~db.Employee_Master_Leave.id )
    return dict(_que = grid)

def get_leave_file_report():
    import datetime
    _usr = db(db.Department_Users_Assignment.users_id == auth.user_id).select().first()        
    row = []
    ctr = 0 
    # _year_end = (datetime.datetime.now() - datetime.timedelta(days=2*365)).strftime('%Y-%m-%d')
    _year_end = datetime.date.today() - datetime.timedelta(days=2*365)
    head = THEAD(TR(TH('Transaction No'),TH('Transaction Date'),TH('Type of Leave'),TH('Date From'),TH('Date To'),TH('Name'),TH('Duration'),TH('Date Returned'),TH('Status'),TH('Dept Approved'),TH('HR Approved'),TH('Mngt Approved'),TH('Action Control')))
    if auth.has_membership('ROOT'):        
        if int(request.args(0)) == 1:             
            _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date != None) & (db.Employee_Master_Leave.from_effective_date > _year_end)).select(orderby = ~db.Employee_Master_Leave.id)                
        else:
            _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('MANAGEMENT'):
        if int(request.args(0)) == 1:             
            _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date != None) & (db.Employee_Master_Leave.from_effective_date > _year_end)).select(orderby = ~db.Employee_Master_Leave.id)                
        else:
            _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('HR MANAGER'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()        
        if int(request.args(0)) == 1:             
            _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date != None) & (db.Employee_Master_Leave.from_effective_date > _year_end)).select(orderby = ~db.Employee_Master_Leave.id)                
        else:
            _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('ADMINISTRATION MANAGER'): # show all employee leave         
        if int(request.args(0)) == 1:             
            _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.from_effective_date != None) & (db.Employee_Master_Leave.from_effective_date > _year_end)).select(orderby = ~db.Employee_Master_Leave.id)                
        else:
            _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)    

    elif auth.has_membership('DEPARTMENT MANAGERS'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()        
        _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.manager_assigned == _usr.sub_department_id)).select(orderby = ~db.Employee_Master_Leave.id)    
    else:        
        _que = db((db.Employee_Master_Leave.employee_id == _usr.employee_id) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == True))).select(orderby = ~db.Employee_Master_Leave.id)
    for n in _que:
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle btnHistory ', callback=URL(args = n.id))
        # view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'HR MANAGER'):
            prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle', _href = URL('leave_mngt_reports','get_application_leave_report_id',args = n.id, extension = False))            
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
    
        if n.application_date == None:
            _app_dat = 'None'
        else:            
            _app_dat = n.application_date#.strftime('%d%b%Y')
        if n.from_effective_date == None:
            _fro_dat = 'None'
        else:
            _fro_dat = n.from_effective_date#.strftime('%d')
        if n.to_effective_date == None:
            _to_dat = 'None'
        else:
            _to_dat = n.to_effective_date#.strftime('%d%b%Y')
        if n.date_returned == None:
            _dat_re = 'None'
        else:
            _dat_re = n.date_returned#.strftime('%d%b%Y')
        if n.canceled == True:
            _status = P('Canceled', _class='text-red')
        else:
            _status = n.status_id.status
        if n.mngt_approved_by == None:
            _mngt = 'None'
        else:
            _mngt = n.mngt_approved_by.first_name
        if n.hr_approved_by == None:            
            _hr = 'None'
        else:
            _hr = n.hr_approved_by.first_name        
        if n.dept_approved_by == None:
            _dept = 'None'
        else:
            _dept = n.dept_approved_by.first_name        
        row.append(TR(
            TD(n.transaction_no),
            TD(_app_dat),
            TD(n.type_of_leave_id.type_of_leave),
            TD(_fro_dat), 
            TD(_to_dat),
            TD(n.employee_id.first_name.upper(),' ', n.employee_id.last_name.upper()),
            TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),
            TD(_dat_re),
            TD(_status),TD(_dept),TD(_hr),TD(_mngt),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def get_application_report_grid():
    _usr = db(db.Department_Users_Assignment.users_id == auth.user_id).select().first()        
    row = []
    ctr = 0 

    head = THEAD(TR(TH('Transaction No',**{'_data-field':'transaction_no','_data-sortable':'true'}),TH('Transaction Date',**{'_data-field':'application_date','_data-sortable':'true'}),TH('Type of Leave', **{'_data-field':'type_of_leave', '_data-sortable':'true'}),TH('Date From',**{'_data-field':'from_effective_date','_data-sortable':'true'}),TH('Date To',**{'_data-field':'to_effective_date','_data-sortable':'true'}),TH('Name'),TH('Duration'),TH('Status'),TH('Action Control')))
    if auth.has_membership('ROOT'):
        _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('MANAGEMENT'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()        
        _que = db((db.Employee_Master_Leave.mngt_approved_by == auth.user_id) & (db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.canceled == False)).select(orderby = ~db.Employee_Master_Leave.id)    
    # elif auth.has_membership('ACCOUNTS'):
    #     print 'accounts:', auth.user_id
    #     _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()        
    #     # _que = db(db.Employee_Master_Leave.acct_approved_by == auth.user_id).select(orderby = ~db.Employee_Master_Leave.id)    
    #     _que = db((db.Employee_Master_Leave.employee_id == _usr.employee_id) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == True))).select(orderby = ~db.Employee_Master_Leave.id)
    elif auth.has_membership('HR MANAGER'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()        
        _que = db(db.Employee_Master_Leave.hr_approved_by == auth.user_id).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('ADMINISTRATION MANAGER'): # show all employee leave         
        _que = db(db.Employee_Master_Leave.status_id == 16).select(orderby = ~db.Employee_Master_Leave.id)    
    elif auth.has_membership('DEPARTMENT MANAGERS'):
        _usr = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()        
        _que = db(db.Employee_Master_Leave.dept_approved_by == auth.user_id).select(orderby = ~db.Employee_Master_Leave.id)    
        # _que = db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.manager_assigned == _usr.sub_department_id) & (db.Employee_Master_Leave.dept_approved_by == auth.user_id)).select(orderby = ~db.Employee_Master_Leave.id)    
    else:
        _que = db((db.Employee_Master_Leave.employee_id == _usr.employee_id) & ((db.Employee_Master_Leave.status_id == 16) | (db.Employee_Master_Leave.canceled == True))).select(orderby = ~db.Employee_Master_Leave.id)
    for n in _que:
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle disabled')
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle ', _href=URL('leave_mngt','get_application_leave_user_id', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')            
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership(role = 'HR MANAGER') | auth.has_membership(role = 'MANAGEMENT'):
            prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank', _class='btn btn-icon-toggle', _href = URL('leave_mngt_reports','get_application_leave_report_id',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
    
        if n.application_date == None:
            _app_dat = 'None'
        else:            
            _app_dat = n.application_date#.strftime('%d%b%Y')
        if n.from_effective_date == None:
            _fro_dat = 'None'
        else:
            _fro_dat = n.from_effective_date#.strftime('%d')
        if n.to_effective_date == None:
            _to_dat = 'None'
        else:
            _to_dat = n.to_effective_date#.strftime('%d%b%Y')
        if n.date_returned == None:
            _dat_re = 'None'
        else:
            _dat_re = n.date_returned#.strftime('%d%b%Y')
        if n.canceled == True:
            _status = P('Canceled', _class='text-red')
        else:
            _status = n.status_id.status
        row.append(TR(
            TD(n.transaction_no),
            TD(_app_dat),
            TD(n.type_of_leave_id.type_of_leave),
            TD(_fro_dat), 
            TD(_to_dat),
            TD(n.employee_id.first_name.upper(),' ', n.employee_id.last_name.upper()),
            TD(locale.format('%.1f',n.duration_leave or 0, grouping = True)),            
            TD(_status),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblRprt')
    return dict(table = table)

def get_doc_ref_report_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Transaction #'),TH('Ref. No.'),TH('Employee'),TH('Control Action')),_class='bg-primary')
    for n in db((db.Employee_Master_Leave.status_id == 16) & (db.Employee_Master_Leave.canceled == False) &(db.Employee_Master_Leave.doc_ref_no != '')).select(orderby = ~db.Employee_Master_Leave.id):
        ctr += 1        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _target=' blank', _type='button ', _role='button', _class='btn btn-icon-toggle', _href = URL('leave_mngt_reports','get_application_leave_report_id',args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(TD(ctr),TD(n.transaction_no),TD(n.doc_ref_no),TD(n.employee_id.title,n.employee_id.first_name.upper(), ' ',n.employee_id.last_name.upper() ),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def get_salary_adjustment_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Transaction No'),TH('Transaction Date'),TH('Name'),TH('Status'),TH('Action Required'),TH('Control Action')),_class='bg-primary')
    if int(request.args(0)) == 1:
        if auth.has_membership(role = 'ADMINISTRATION MANAGER') or auth.has_membership(role = 'HR MANAGER') or auth.has_membership(role = 'ROOT'): # hr grid
            _query = db((db.Salary_Adjustment.status_id <= 4) & ((db.Salary_Adjustment.status_id != 5) | (db.Salary_Adjustment.status_id != 6))).select(orderby = ~db.Salary_Adjustment.id)
        elif auth.has_membership(role = 'MANAGEMENT')  or auth.has_membership(role = 'ROOT'): # mngt grid
            _query = db(db.Salary_Adjustment.status_id == 3).select(orderby = ~db.Salary_Adjustment.id)
    elif int(request.args(0)) == 2: # reports
        _query = db(db.Salary_Adjustment.status_id == 5).select(orderby = ~db.Salary_Adjustment.id)

    for n in _query:
        ctr+=1
        _eed = db(db.Employee_Employment_Details.employee_id == n.employee_id).select().first()
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('leave_mngt','get_salary_adjustment_id', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = (URL('leave_mngt','put_salary_adjustment_id', args = n.id))) 
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        conf_lnk = A(I(_class='fa fa-check'), _title='Confirm Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        prin_lnk = A(I(_class='fa fa-print'), _title='Confirm Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        
        if int(n.status_id) == 3:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('leave_mngt','put_salary_adjustment_id', args = n.id)))             
        elif int(n.status_id) == 4:
            conf_lnk = A(I(_class='fa fa-check'), _title='Confirm Row', _type='button  ', _role='button', _class='btn btn-icon-toggle Confirm', callback= URL('leave_mngt','put_salary_adjustment_confirmation_id', args = n.id))        
        elif int(n.status_id) == 5:            
            prin_lnk = A(I(_class='fa fa-print'), _title='Confirm Row', _type='button  ', _role='button',_target='_blank', _class='btn btn-icon-toggle',_href=URL('leave_mngt_reports', 'get_salary_adjustment_report_id',args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, conf_lnk, prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_no),
            TD(n.transaction_date),
            TD(n.employee_id.title, n.employee_id.first_name, ' ',n.employee_id.middle_name,' ', n.employee_id.last_name, ', ',SPAN(_eed.account_code, _class='text-muted')),
            TD(n.status_id.status),
            TD(n.status_id.action_required),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def post_salary_adjustment():    
    ctr = db(db.Salary_Adjustment.id).count()
    ctr = str(datetime.now().year) + '-' + str(ctr+1)
    db.Salary_Adjustment.effectivity_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Salary_Adjustment.status_id.requires = IS_IN_DB(db(db.Salary_Adjustment_Status.id == 3), db.Salary_Adjustment_Status, '%(status)s', zero = 'Choose Status')
    db.Salary_Adjustment.status_id.default = 3
    form = SQLFORM(db.Salary_Adjustment)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        put_salary_adjustment_send_mngr_email()
        redirect(URL('leave_mngt','get_salary_adjustment_grid',args = 1))        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'              
    return dict(form = form, ctr = ctr)

def put_salary_adjustment_send_mngr_email():
    _id = db(db.Email_Notification).select().first()    
    _sender = _id.email_notification
    _login = str(_id.email_notification) + str(':') + str(_id.email_password)
    mail.settings.server = 'smtp.gmail.com:587'
    mail.settings.sender = _sender
    mail.settings.login = _login  
    # mail.settings.sender = 'merch.noreply@gmail.com'
    # mail.settings.login = 'merch.noreply@gmail.com:45Password123' # 45Password123
    # mail.settings.tls = 'smtp.tls'        
    _to = db(db.auth_membership.group_id == 2).select().first()   # testing 1 / change to 2 for management
    _msg = """\
            <html>
            <head></head>
            <body>
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">You have pending salary adjustment required for your approval.</p>                
                <p style="font-family:courier, courier new; font-size: 15px; color:black;">NOTE: This is an auto-generated email. Please do not reply.</p>
            </body>
            </html>
            """
    mail.send(        
        to=[_to.user_id.email],   
        subject='HR WORKFLOW REMINDER',
        message = _msg)
    # mail.settings.tls = 'smtp.tls'
    return dict()

def put_salary_adjustment_id():
    _row = db(db.Salary_Adjustment.id == request.args(0)).select().first()
    db.Salary_Adjustment.effectivity_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Salary_Adjustment.status_id.requires = IS_IN_DB(db((db.Salary_Adjustment_Status.id == 2) | (db.Salary_Adjustment_Status.id == 3) | (db.Salary_Adjustment_Status.id == 6)), db.Salary_Adjustment_Status, '%(status)s', zero = 'Choose Status')
    form = SQLFORM(db.Salary_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        redirect(URL('leave_mngt','get_salary_adjustment_grid', args = 1))        
    elif form.errors:
        responnse.flash = 'FORM HAS ERROR'        
    return dict(form = form, _row = _row)

def get_salary_adjustment_id():
    _row = db(db.Salary_Adjustment.id == request.args(0)).select().first()
    db.Salary_Adjustment.effectivity_date.requires = IS_DATE(format('%m-%d-%Y'))
    db.Salary_Adjustment.status_id.requires = IS_IN_DB(db((db.Salary_Adjustment_Status.id == 1) | (db.Salary_Adjustment_Status.id == 2) | (db.Salary_Adjustment_Status.id == 6)), db.Salary_Adjustment_Status, '%(status)s', zero = 'Choose Status')
    form = SQLFORM(db.Salary_Adjustment, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        redirect(URL('leave_mngt','get_salary_adjustment_grid'))        
    elif form.errors:
        responnse.flash = 'FORM HAS ERROR'        
    return dict(form = form, _row = _row)

def put_salary_adjustment_hr_remarks_id():    
    db(db.Salary_Adjustment.id == request.args(0)).update(hr_remarks = request.vars.hr_remarks)
    response.js = "jQuery(alertify.success('Remarks save...'))"

def put_salary_adjustment_mngt_remarks_id():    
    db(db.Salary_Adjustment.id == request.args(0)).update(mngt_remarks = request.vars.mngt_remarks)
    response.js = "jQuery(alertify.success('Remarks save...'))"

def get_salary_details_id():    
    _id = db(db.Employee_Master_Account_Info.employee_id == request.vars.employee_id).select().first()    
    response.js = "jQuery($('#Salary_Adjustment_basic_income').val(%s), $('#Salary_Adjustment_housing_allowances').val(%s), $('#Salary_Adjustment_car_allowances').val(%s),$('#Salary_Adjustment_petrol_allowances').val(%s),$('#Salary_Adjustment_food_allowances').val(%s),$('#Salary_Adjustment_others').val(%s),$('#Salary_Adjustment_incentive').val(%s),$('#Salary_Adjustment_mobile_allowances').val(%s))" % (_id.basic_income, _id.housing_allowances, _id.car_allowances, _id.petrol_allowances, _id.food_allowances, _id.others, _id.incentive, _id.mobile_allowances)
    
def put_salary_adjustment_confirmation_id():
    _id = db(db.Salary_Adjustment.id == request.args(0)).select().first()
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())
    _ckey = str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]        
    if auth.has_membership(role = 'HR MANAGER'):                                    
        _pre.update_record(serial_key = _skey)      
        _id.update_record(doc_ref_no = _ckey, status_id = 5, hr_approved_by = auth.user_id)  
        db.Memorandum.insert(memorandum_prefix_no_id = _pre.id,memorandum_no = _ckey,memorandum_date = request.now,memorandum_from = 'HUMAN RESOURCES',memorandum_to = str(_id.employee_id.first_name.upper()) + ' ' + str(_id.employee_id.last_name.upper()),memorandum_subject = 'SALARY ADJUSTMENT - ' + str(_id.employee_id.first_name.upper()) + ' ' + str(_id.employee_id.last_name.upper()),confidential = True)
        response.js = "jQuery(alertify.success('Confirmed'), window.setTimeout(function(){window.location.reload()}, 1000));"
    elif auth.has_membership(role = 'MANAGEMENT'):
        _id.update_record(status_id = 4, mngt_remarks = request.vars.mngt_remarks, mngt_approved_by = auth.user_id)        
        
def put_salary_adjustment_rejection_id():    
    db(db.Salary_Adjustment.id == request.args(0)).update(status_id = 2,hr_remarks = request.vars.hr_remarks, mngt_remarks = request.vars.mngt_remarks)

def get_salary_adjustment_history_load_id():
    _first = _id = db(db.Salary_Adjustment.id == request.args(0)).select().first()
    _last = db(db.Salary_Adjustment.id == _first.employee_id).select().first()

    _ac = db(db.Employee_Master_Account_Info.employee_id == _id.employee_id).select().first()
    _ed = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()

    if _first.id > _last.id:
        # print 'true', _first.id, _last.id
        _badj = abs(_first.basic_income - _last.basic_income )
        _hall = abs(_first.housing_allowances - _last.housing_allowances )
        _call = abs(_first.car_allowances - _last.car_allowances)
        _pall = abs(_first.petrol_allowances - _last.petrol_allowances )
        _fall = abs(_first.food_allowances - _last.food_allowances )
        _oall = abs(_first.others - _last.others)
        _iall = abs(_first.incentive - _last.incentive)
        _tgro = abs(_first.total_gross_pay - _last.total_gross_pay)
    else:
        # print 'false', _first.id, _last.id
        _badj = abs(_last.basic_income)
        _hall = abs(_last.housing_allowances )
        _call = abs(_last.car_allowances )
        _pall = abs(_last.petrol_allowances )
        _fall = abs(_last.food_allowances )
        _oall = abs(_last.others )
        _iall = abs(_last.incentive)
        _tgro = abs(_last.total_gross_pay )
    for n in db(db.Salary_Adjustment.employee_id == _id.employee_id).select(orderby = db.Salary_Adjustment.id):        
        if int(request.args(0)) > int(n.id):            
            _last = db(db.Salary_Adjustment.id == n.id).select().first()            
        else:
            _first = db(db.Salary_Adjustment.id == request.args(0)).select().first()        
    _badj = (_first.basic_income - _last.basic_income )
    _hall = (_first.housing_allowances - _last.housing_allowances )
    _call = (_first.car_allowances - _last.car_allowances)
    _pall = (_first.petrol_allowances - _last.petrol_allowances )
    _fall = (_first.food_allowances - _last.food_allowances )
    _oall = (_first.others - _last.others)
    _iall = (_first.incentive - _last.incentive)
    _tgro = (_first.total_gross_pay - _last.total_gross_pay)    
    table = TABLE(
        TR(TD('Details'),TD('Basic Salary'),TD('Housing Allowances'),TD('Car Allowances'),TD('Food Allowances'),TD('Petrol Allowances'),TD('Incentive/Bonus'),TD('Others'),TD('Total Gross')),
        TR(TD('Previous Month Wages.'),TD(_last.basic_income),TD(_last.housing_allowances),TD(_last.car_allowances),TD(_last.food_allowances),TD(_last.petrol_allowances),TD(_last.incentive),TD(_last.others),TD(_last.total_gross_pay)),
        TR(TD('Current Adjustment'),TD(_badj),TD(_hall),TD(_call),TD(_fall),TD(_pall),TD(_iall),TD(_oall),TD(_tgro)),
        TR(TD('New Month Wages'),TD(_id.basic_income),TD(_id.housing_allowances),TD(_id.car_allowances),TD(_id.food_allowances),TD(_id.petrol_allowances),TD(_id.incentive),TD(_id.others),TD(_id.total_gross_pay)),_class='table table-striped')            
    
    return XML(DIV(table))
# ------------------------------------------------------------------------------------------
# -------------------  P A Y R O L L  M A N A G E M E N T   S Y S T E M  -------------------
# ------------------------------------------------------------------------------------------
import calendar
import datetime
import locale
now = datetime.datetime.now()

def get_overtime_status_grid():
    row = []
    ctr = 0
    form = SQLFORM(db.Overtime_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Status'),TH('Description'),TH('Action')))
    for n in db().select(db.Overtime_Status.ALL, orderby = db.Overtime_Status.id):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('payroll_mngt','put_overtime_status_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def put_overtime_status_id():
    form = SQLFORM(db.Overtime_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('payroll_mngt','get_overtime_status_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def get_payroll_run():
    row = []
    ctr = 0 
    _days = calendar.monthrange(now.year, now.month)[1]
    _em = db(db.Employee_Master.employee_status_id == 1).count()
    _id = db().select(db.Employee_Master.ALL)
        
    thead = THEAD(TR(TH('Employees (', _em,')'),TH('Days Work'),TH('Basic'),TH('Others'),TH('Total Gross Pay'),TH('Total Deduction'),TH('Net Pay')))
    for n in db(db.Employee_Master.employee_status_id == 1).select(db.Employee_Master.ALL, db.Employee_Master_Account_Transaction_Temporary.ALL, orderby = db.Employee_Master.id, left = db.Employee_Master.on(db.Employee_Master.id == db.Employee_Master_Account_Transaction_Temporary.employee_id)):
        ctr += 1        
        _row_empl = ctr,'. ', n.Employee_Master.title, ' ', n.Employee_Master.first_name, ' ', n.Employee_Master.middle_name, ' ',n.Employee_Master.last_name
        _total_gross_pay = int(n.Employee_Master_Account_Transaction_Temporary.basic_income or 0) + int(n.Employee_Master_Account_Transaction_Temporary.housing_allowances or 0) + int(n.Employee_Master_Account_Transaction_Temporary.car_allowances or 0) + int(n.Employee_Master_Account_Transaction_Temporary.petrol_allowances or 0) + int(n.Employee_Master_Account_Transaction_Temporary.food_allowances or 0) + int(n.Employee_Master_Account_Transaction_Temporary.others or 0) + int(n.Employee_Master_Account_Transaction_Temporary.incentive or 0)
        _total_deductions = int(n.Employee_Master_Account_Transaction_Temporary.loan_or_advances or 0) + int(n.Employee_Master_Account_Transaction_Temporary.other_deductions or 0) + int(n.Employee_Master_Account_Transaction_Temporary.absent_deductions or 0) 
        _net_pay = float(_total_gross_pay) - float(_total_deductions)
        row.append(TR(            
            # TD(A(_row_empl, _href='#',**{'_data-toggle':'modal', '_data-target':'.bd-example-modal-xl', '_data-id':(n.Employee_Master_Account_Transaction_Temporary.id)})),
            TD(A(_row_empl, _href= URL('payroll_mngt','put_process_payroll_id', args = n.Employee_Master_Account_Transaction_Temporary.id))),
            TD(n.Employee_Master_Account_Transaction_Temporary.days_work, _align='right'),
            # TD(INPUT(_type='number', _class='form-control', _id='days_work', _name='days_work', _value = n.Employee_Master_Account_Transaction_Temporary.days_work, _style="width:80px; text-align:right")),
            TD(locale.format('%.2F',n.Employee_Master_Account_Transaction_Temporary.basic_income or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',n.Employee_Master_Account_Transaction_Temporary.others or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',_total_gross_pay or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',_total_deductions or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',_net_pay or 0, grouping = True),_align='right')))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _id='tblTemp',_class='table', **{
        '_data-search':'true', 
        '_data-show-refresh':'true',
        '_data-show-pagination-switch':'true',
        '_data-pagination':'true',
        '_data-toolbar':'#toolbar'})
    # _range = db(db.Employee_Master_Account_Transaction_Temporary.id ).select(db.Employee_Master_Account_Transaction_Temporary.start_transaction_date, db.Employee_Master_Account_Transaction_Temporary.end_transaction_date, groupby = db.Employee_Master_Account_Transaction_Temporary.start_transaction_date | db.Employee_Master_Account_Transaction_Temporary.end_transaction_date).first()
    _range = db(db.Employee_Master_Account_Transaction_Temporary.id > 0).select().first()    
    return dict(table=table, _range = _range)

def put_process_payroll_id():    
    _id = db(db.Employee_Master_Account_Transaction_Temporary.id == request.args(0)).select().first()
    db.Employee_Master_Account_Transaction_Temporary.start_transaction_date.writable = False
    db.Employee_Master_Account_Transaction_Temporary.end_transaction_date.writable = False
    db.Employee_Master_Account_Transaction_Temporary.id.default = _id.id
    form = SQLFORM(db.Employee_Master_Account_Transaction_Temporary, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
        redirect(URL('payroll_mngt','get_payroll_run'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    _range = db(db.Employee_Master_Account_Transaction_Temporary.id > 0).select().first()    
    return dict(form = form, _id = _id, _range = _range)

def push_payroll_run():
    # _today = datetime()    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    if 1 <= int(request.vars.month) <= 12:
        print "The month is", months[int(request.vars.month) - 1]
    if str(months[int(request.vars.month) - 1]) == str(request.now.strftime('%B')):
        print 'true', request.vars.month
    else:
        print 'false', request.vars.month

    print request.now.strftime('%B')
    # print 'first and end date of the month: ', 
    

def push_payroll_run_():
    # print request.vars.start_date, request.vars.end_date
    # _start_date = datetime.datetime.strptime(request.now, "%Y-%m-%d")
    # _end_date = datetime.datetime.strptime(request.now, "%Y-%m-%d")
    _days = (_end_date.day - _start_date.day) + 1
    # print _start_date, _end_date
    # _days = calendar.monthrange(now.year, now.month)[1]
    db.Employee_Master_Account_Transaction_Temporary.truncate()   
    print 'push'
    for n in db(db.Employee_Master_Account_Info).select(orderby = db.Employee_Master_Account_Info.id):
        # print 'process', n.id
        _total_gross_pay = int(n.basic_income or 0) + int(n.housing_allowances or 0) + int(n.car_allowances or 0) + int(n.petrol_allowances or 0) + int(n.food_allowances or 0) + int(n.others or 0) + int(n.incentive or 0)
        _total_deductions = int(n.loan_or_advances or 0) + int(n.other_deductions or 0) + int(n.absent_deductions or 0) 
        _net_pay = float(_total_gross_pay) - float(_total_deductions)
        print '_id ', n.id, auth.user_id, auth_db.auth_user
        db.Employee_Master_Account_Transaction_Temporary.insert(
            employee_id = n.id,
            start_transaction_date = request.now,
            end_transaction_date = request.now,
            days_work = _days,
            basic_income = n.basic_income,
            housing_allowances = n.housing_allowances,
            car_allowances = n.car_allowances,
            petrol_allowances = n.petrol_allowances,
            food_allowances = n.food_allowances,
            others = n.others,
            incentive = n.incentive,
            total_gross_pay = _total_gross_pay,
            bank_transfer = _net_pay,
            loan_or_advances = n.loan_or_advances,
            other_deductions = n.other_deductions,
            absent_deductions = n.absent_deductions,
            total_deductions = _total_deductions,
            net_pay = _net_pay)

def push_payroll_redo():    
    db.Employee_Master_Account_Transaction_Temporary.truncate()   

def get_employee_master_grid():
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Employee No'),TH('Account Code'),TH('Employee Name'),TH('Department'),TH('Designation'),TH('Status'),TH('Action')))
    for n in db().select(db.Employee_Master.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('payroll_mngt','get_employee_salary_info_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.employee_no),TD(n.account_code),TD(n.title, ' ', n.first_name.upper(), ' ', n.middle_name.upper(), ' ',n.last_name.upper()),TD(n.department_code_id.department_name),TD(n.designation_code_id.designation_name),TD(n.employee_status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    return dict(table=table)

def get_employee_salary_info_id():
    form = SQLFORM(db.Employee_Master_Account_Info, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERRORS'
    return dict(form = form)

def get_overtime_table():
    row = []
    ctr = 0
    thead = TR(TH('#'),TH('Account Code'),TH('Employee Name'),TH('Date'),TH('Hours'),TH('Status'),TH('Remarks'),TH('Action'))
    for n in db(db.Employee_Overtime_Transaction).select(db.Employee_Employment_Details.ALL, db.Employee_Overtime_Transaction.ALL, orderby = db.Employee_Overtime_Transaction.id, left = db.Employee_Employment_Details.on(db.Employee_Employment_Details.id == db.Employee_Overtime_Transaction.account_no_id)):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Employee_Overtime_Transaction.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('put_overtime_grid_id', args = n.Employee_Overtime_Transaction.id, extension = False))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Employee_Overtime_Transaction.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.Employee_Employment_Details.account_code),
            TD(n.Employee_Employment_Details.employee_id.first_name.upper(), ' ',n.Employee_Employment_Details.employee_id.middle_name.upper(), ' ',n.Employee_Employment_Details.employee_id.last_name.upper()),            
            TD(n.Employee_Overtime_Transaction.date_overtime),
            TD(n.Employee_Overtime_Transaction.excess_hours),
            TD(n.Employee_Overtime_Transaction.status_id.status),
            TD(n.Employee_Overtime_Transaction.remarks),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _id='tblOvertime', _class='table')    
    return dict(table = table)

def get_overtime_grid():
    db.Employee_Overtime_Transaction.account_no_id.widget = SQLFORM.widgets.autocomplete(request, db.Employee_Employment_Details.account_code, id_field = db.Employee_Employment_Details.id, limitby = (0,10), min_length = 2)    
    db.Employee_Overtime_Transaction.status_id.requires = IS_IN_DB(db(db.Overtime_Status.id == 1), db.Overtime_Status.id, '%(status)s', zero = 'Choose Status')
    db.Employee_Overtime_Transaction.status_id.default = 1
    db.Employee_Overtime_Transaction.account_no_id.requires = IS_NOT_EMPTY()
    form = SQLFORM(db.Employee_Overtime_Transaction)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        response.js = "$('#tblOvertime').get(0).reload()"
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def put_overtime_grid_id():
    _id = db(db.Employee_Overtime_Transaction.id == request.args(0)).select().first()
    # db.Employee_Overtime_Transaction.account_no_id.writable = False
    db.Employee_Overtime_Transaction.status_id.requires = IS_IN_DB(db(db.Overtime_Status.id == 1), db.Overtime_Status.id, '%(status)s', zero = 'Choose Status')
    form = SQLFORM(db.Employee_Overtime_Transaction, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'        
        redirect(URL('payroll_mngt','get_overtime_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, _id = _id)

def stat():
    db(db.Employee_Master).update(employee_status_id = 1)
    return locals()

def get_salary_details_report():    
    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Name',**{'_data-field':'name'}),TH('Department'),TH('Basic Income', **{'_data-align':'right','_data-halign':'left'}),TH('Housing Allow.', **{'_data-align':'right','_data-halign':'left'}),TH('Car Allow.', **{'_data-align':'right','_data-halign':'left'}),TH('Petrol Allow.', **{'_data-align':'right','_data-halign':'left'}),TH('Food Allow.', **{'_data-align':'right','_data-halign':'left'}),TH('Others', **{'_data-align':'right','_data-halign':'left'}),TH('Incentives', **{'_data-align':'right','_data-halign':'left'}),TH('Mobile Allow.', **{'_data-align':'right','_data-halign':'left'}),TH('Gross Pay', **{'_data-align':'right','_data-halign':'left'})),_class='bg-primary')
    for x in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
        for n in db(db.Employee_Employment_Details.employee_id == x.id).select():        
            ctr += 1            
            _act = db(db.Employee_Master_Account_Info.employee_id == n.employee_id).select().first()        
            row.append(TR(
                TD(ctr),
                TD(_act.employee_id.title, ' ',_act.employee_id.first_name,' ', _act.employee_id.middle_name, ' ', _act.employee_id.last_name, ', ', SPAN(n.account_code, _class='text-muted')),
                TD(n.department_code_id.department_name),
                TD(locale.format('%.2F',_act.basic_income or 0, grouping = True)),
                TD(locale.format('%.2F',_act.housing_allowances or 0, grouping = True)),
                TD(locale.format('%.2F',_act.car_allowances or 0, grouping = True)),
                TD(locale.format('%.2F',_act.petrol_allowances or 0, grouping = True)),
                TD(locale.format('%.2F',_act.food_allowances or 0, grouping = True)),
                TD(locale.format('%.2F',_act.others or 0, grouping = True)),
                TD(locale.format('%.2F',_act.incentive or 0, grouping = True)),
                TD(locale.format('%.2F',_act.mobile_allowances or 0, grouping = True)),
                TD(locale.format('%.2F',_act.total_gross_pay or 0, grouping = True))))
            body = TBODY(*row)
            table = TABLE(*[head, body], _class='table', _id='tblPayrollDet', **{
                '_data-toggle':'table',
                '_data-search':'true',
                '_data-pagination':'true',
                '_data-toolbar':'#toolbar',
                '_data-show-export':'true'})
    return dict(table = table)
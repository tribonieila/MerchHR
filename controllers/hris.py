# ------------------------------------------------------------------------------------------
# -----------------------------  C O R E  H R   S Y S T E M  -------------------------------
# ------------------------------------------------------------------------------------------
from gluon.tools import Mail
from gluon.tools import Recaptcha2
mail = Mail()
import string
import random
from datetime import date, datetime, timedelta
import locale
from fractions import Fraction
# ------------------------------------- S E T T I N G S ------------------------------------
def get_record_status_grid():
    row = []
    ctr = 0
    form = SQLFORM(db.Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Status.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def get_employee_status_grid():
    row = []    
    form = SQLFORM(db.Employee_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Description'), TH('Action')))
    for n in db().select(db.Employee_Status.ALL, orderby = db.Employee_Status.id):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_employee_status_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def put_employee_status_grid():
    form = SQLFORM(db.Employee_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
        redirect(URL('hris','get_employee_status_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'    
    return dict(form = form)

def get_department_grid():
    row = []
    ctr = 0
    db.Department.status_id.default = 1
    form = SQLFORM(db.Department)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Department Code'),TH('Department Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Department.ALL, orderby = db.Department.id):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_department_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.department_code),TD(n.department_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def put_department_id():
    form = SQLFORM(db.Department, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
        redirect(URL('hris','get_department_grid'))
    elif form.errors:
        response.flash = 'RECORD UPDATED'
    return dict(form = form)

def get_designation_grid():
    row = []
    ctr = 0
    db.Designation.status_id.default = 1
    form = SQLFORM(db.Designation)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Designation Code'),TH('Designation Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Designation.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_designation_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.designation_code),TD(n.designation_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def put_designation_id():
    form = SQLFORM(db.Designation, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def get_section_grid():
    row = []
    ctr = 0
    db.Section.status_id.default = 1
    form = SQLFORM(db.Section)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Section Code'),TH('Section Name'),TH('Status'),TH('Action')))
    for n in db().select(db.Section.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_section_id', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.section_code),TD(n.section_name),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def put_section_id():
    form = SQLFORM(db.Section, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def get_labor_card_profession_grid():
    row = []
    ctr = 0
    form = SQLFORM(db.Labor_Card_Profession)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Profession'),TH('Action')))
    for n in db().select(db.Labor_Card_Profession.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.labor_card_profession),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

def get_sector_grid():
    row = []
    ctr = 0
    form = SQLFORM(db.Sector)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Profession'),TH('Action')))
    for n in db().select(db.Sector.ALL):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.sector),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)

# ------------------------------------- S E T T I N G S ------------------------------------


def get_employee_master_grid():
    row = []
    ctr = 0
    # db.Employee_Employment_Details.department_code_id.represent = lambda id, r: db.Department[id].department_name if id else ''
    thead = THEAD(TR(TH('#'),TH('Employee Name'),TH('Department'),TH('Designation'),TH('Status'),TH('Action')))
    for n in db(db.Employee_Master.employee_status_id == 1).select(db.Employee_Master.ALL, db.Employee_Employment_Details.ALL, orderby = db.Employee_Master.id, join = db.Employee_Employment_Details.on(db.Employee_Master.id == db.Employee_Employment_Details.employee_id)):
        ctr += 1        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','get_employee_master_id',args = n.Employee_Master.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_employee_master_id', args = n.Employee_Master.id))
        prin_lnk = A(I(_class='fa fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle', _target='_blank', _href = URL('hris_reports','get_employee_master_id_print', args = n.Employee_Master.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Employee_Master.id))        
        if auth.has_membership(role = 'ADMINISTRATION MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'HR MANAGER') | auth.has_membership(role = 'ROOT'): 
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_employee_master_id', args = n.Employee_Master.id))
        else:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('hris','put_employee_master_id', args = n.Employee_Master.id))
        btn_lnk = DIV(view_lnk, edit_lnk, prin_lnk, dele_lnk)
        
        _dep = db(db.Department.id == n.Employee_Employment_Details.department_code_id).select().first()
        _des = db(db.Designation.id == n.Employee_Employment_Details.designation_code_id).select().first()
        _sta = db(db.Status.id == n.Employee_Master.employee_status_id).select().first()
        if n.Employee_Master.middle_name == None:
            _middle_name = ''
        else:
            _middle_name = n.Employee_Master.middle_name

        row.append(TR(
            TD(ctr),
            # TD(n.Employee_Employment_Details.employee_no),
            # TD(n.Employee_Employment_Details.account_code),
            TD(SPAN(n.Employee_Employment_Details.employee_no, ' - ',_class='text-muted'),n.Employee_Master.title, ' ', n.Employee_Master.first_name.upper(),' ', _middle_name, ' ', n.Employee_Master.last_name, ', ',SPAN(n.Employee_Employment_Details.account_code,_class='text-muted')),
            TD(n.Employee_Employment_Details.department_code_id.department_name),
            TD(n.Employee_Employment_Details.designation_code_id.designation_name),
            TD( _sta.status),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    # table = TABLE(*[thead, tbody], _class='table', **{'_data-show-export':'true','_data-search':'true', '_data-show-refresh':'true','_data-show-pagination-switch':'true','_data-pagination':'true'})
    return dict(table=table)

def get_in_active_employee_master_grid():
    row = []
    ctr = 0
    # db.Employee_Employment_Details.department_code_id.represent = lambda id, r: db.Department[id].department_name if id else ''
    thead = THEAD(TR(TH('#'),TH('Employee Name'),TH('Department'),TH('Designation'),TH('Status'),TH('Action')))
    for n in db(db.Employee_Master.employee_status_id != 1).select(db.Employee_Master.ALL, db.Employee_Employment_Details.ALL, orderby = db.Employee_Master.id, join = db.Employee_Employment_Details.on(db.Employee_Master.id == db.Employee_Employment_Details.employee_id)):
        ctr += 1        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','get_employee_master_id',args = n.Employee_Master.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('hris','put_employee_master_id', args = n.Employee_Master.id))
        prin_lnk = A(I(_class='fa fa-print'), _title='Print Row', _type='button ', _role='button', _class='btn btn-icon-toggle disabled', _target='_blank', _href = URL('hris_reports','get_employee_master_id_print', args = n.Employee_Master.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.Employee_Master.id))        
        # if auth.has_membership(role = 'ADMINISTRATION MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership(role = 'HR MANAGER') | auth.has_membership(role = 'ROOT'): 
        #     edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hris','put_employee_master_id', args = n.Employee_Master.id))
        # else:
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('hris','put_employee_master_id', args = n.Employee_Master.id))
        btn_lnk = DIV(view_lnk, edit_lnk, prin_lnk, dele_lnk)
        
        _dep = db(db.Department.id == n.Employee_Employment_Details.department_code_id).select().first()
        _des = db(db.Designation.id == n.Employee_Employment_Details.designation_code_id).select().first()
        _sta = db(db.Employee_Status.id == n.Employee_Master.employee_status_id).select().first()
        
        row.append(TR(
            TD(ctr),
            # TD(n.Employee_Employment_Details.employee_no),
            # TD(n.Employee_Employment_Details.account_code),
            TD(SPAN(n.Employee_Employment_Details.employee_no, ' - ',_class='text-muted'),n.Employee_Master.title, ' ', n.Employee_Master.first_name.upper(),' ', n.Employee_Master.middle_name, ' ', n.Employee_Master.last_name, ', ',SPAN(n.Employee_Employment_Details.account_code,_class='text-muted')),
            TD(n.Employee_Employment_Details.department_code_id.department_name),
            TD(n.Employee_Employment_Details.designation_code_id.designation_name),
            TD( _sta.status),
            TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    # table = TABLE(*[thead, tbody], _class='table', **{'_data-show-export':'true','_data-search':'true', '_data-show-refresh':'true','_data-show-pagination-switch':'true','_data-pagination':'true'})
    return dict(table=table)

def get_employee_master_id():
    _id = db(db.Employee_Master.id == request.args(0)).select()    
    _em = db(db.Employee_Master.id == request.args(0)).select(db.Employee_Master.ALL).first()
    _ead = db(db.Employee_Address_Details.employee_id == _em.id).select(db.Employee_Address_Details.ALL).first()
    _eed = db(db.Employee_Employment_Details.employee_id == request.args(0)).select(db.Employee_Employment_Details.ALL).first()
    _emai = db(db.Employee_Master_Account_Info.employee_id == request.args(0)).select(db.Employee_Master_Account_Info.ALL).first()
    db.Employee_Master_Account_Info.basic_income.writable = False
    db.Employee_Master_Account_Info.housing_allowances.writable = False
    db.Employee_Master_Account_Info.car_allowances.writable = False
    db.Employee_Master_Account_Info.petrol_allowances.writable = False
    db.Employee_Master_Account_Info.food_allowances.writable = False
    db.Employee_Master_Account_Info.others.writable = False
    db.Employee_Master_Account_Info.incentive.writable = False
    db.Employee_Master_Account_Info.mobile_allowances.writable = False
    db.Employee_Master_Account_Info.total_gross_pay.writable = False
    db.Employee_Employment_Details.sub_department_code_id.writable = False
    db.Employee_Employment_Details.back_office_code_id.writable = False

    db.Employee_Master.passport_image.writable = False
    db.Employee_Master.residence_permit_no_image.writable = False
    db.Employee_Master.labor_card_no_image.writable = False
    db.Employee_Master.health_card_no_image.writable = False
    db.Employee_Master.driver_license_no_image.writable = False
    db.Employee_Master.photo.writable = False
    db.Employee_Master.resume_image.writable = False
    db.Employee_Master.employment_contract.writable = False
    db.Employee_Master.medical_health_card_cert_no_image.writable = False
    db.Employee_Master.educational_certificate.writable = False
    


    form = SQLFORM.factory(db.Employee_Master, db.Employee_Address_Details, db.Employee_Employment_Details, db.Employee_Master_Account_Info,  table_name='Employee_Master')
    form.vars.title = _em.title
    form.vars.first_name = _em.first_name
    form.vars.middle_name = _em.middle_name
    form.vars.last_name = _em.last_name
    form.vars.gender = _em.gender 
    form.vars.telephone_no = _em.telephone_no    
    form.vars.mobile_no = _em.mobile_no
    form.vars.email = _em.email
    form.vars.marital_status = _em.marital_status
    form.vars.nationality = _em.nationality
    form.vars.religion = _em.religion 
    form.vars.languages = _em.languages
    form.vars.birth_place = _em.birth_place
    form.vars.birth_date = _em.birth_date
    form.vars.fathers_name = _em.fathers_name
    form.vars.education_qualification = _em.education_qualification
    form.vars.passport_no = _em.passport_no
    form.vars.passport_date_issued = _em.passport_date_issued
    form.vars.passport_date_expiration = _em.passport_date_expiration
    form.vars.date_given = _em.date_given
    form.vars.issuing_government = _em.issuing_government
    form.vars.place_issued = _em.place_issued
    form.vars.professional_passport = _em.professional_passport
    form.vars.residence_permit_no = _em.residence_permit_no
    form.vars.residence_permit_no_image = _em.residence_permit_no_image
    form.vars.residence_permit_no_expiration_date = _em.residence_permit_no_expiration_date
    form.vars.labor_card_no = _em.labor_card_no
    form.vars.labor_card_no_image = _em.labor_card_no_image
    form.vars.labor_card_no_expiration_date = _em.labor_card_no_expiration_date    
    
    form.vars.health_card_no = _em.health_card_no
    form.vars.health_card_no_image = _em.health_card_no_image
    form.vars.health_card_no_expiration_date = _em.health_card_no_expiration_date

    form.vars.medical_health_card_cert_no = _em.medical_health_card_cert_no
    form.vars.medical_health_card_cert_no_image = _em.medical_health_card_cert_no_image
    form.vars.medical_health_card_cert_no_expiration_date = _em.medical_health_card_cert_no_expiration_date

    form.vars.driver_license_no = _em.driver_license_no
    form.vars.driver_license_no_image = _em.driver_license_no_image
    form.vars.driver_license_no_expiration_date = _em.driver_license_no_expiration_date
    form.vars.last_job = _em.last_job
    form.vars.reason_leaving_previous_job = _em.reason_leaving_previous_job
    form.vars.previous_salary = _em.previous_salary
    form.vars.emergency_contant_name = _em.emergency_contant_name
    form.vars.emergency_contact_no = _em.emergency_contact_no
    form.vars.emergency_relationship = _em.emergency_relationship
    form.vars.residence_no = _em.residence_no
    form.vars.residence_no_date = _em.residence_no_date
    form.vars.residence_no_date_expiration = _em.residence_no_date_expiration    
    form.vars.photo = _em.photo
    form.vars.employee_status_id = _em.employee_status_id
    form.vars.resume_image = _em.resume_image

    form.vars.employee_id = _em.id
    form.vars.street = _ead.street
    form.vars.town = _ead.town
    form.vars.province = _ead.province
    form.vars.city = _ead.city
    form.vars.country = _ead.country
    form.vars.contact_no = _ead.contact_no
    form.vars.local_street = _ead.local_street
    form.vars.local_zone_no = _ead.local_zone_no
    form.vars.local_property_no = _ead.local_property_no
    form.vars.local_apartment_no = _ead.local_apartment_no
    form.vars.landlord_name = _ead.landlord_name
    form.vars.local_contact_no = _ead.local_contact_no

    # form.vars.basic_income = _emai.basic_income
    # form.vars.housing_allowances = _emai.housing_allowances
    # form.vars.car_allowances = _emai.car_allowances
    # form.vars.petrol_allowances = _emai.petrol_allowances
    # form.vars.food_allowances = _emai.food_allowances
    # form.vars.others = _emai.others
    # form.vars.incentive = _emai.incentive
    # form.vars.mobile_allowances = _emai.mobile_allowances
    
    # form.vars.loan_or_advances = _emai.loan_or_advances
    # form.vars.other_deductions = _emai.other_deductions
    # form.vars.absent_deductions = _emai.absent_deductions

    # _total_gross_pay = form.vars.basic_income + form.vars.housing_allowances + form.vars.car_allowances + form.vars.petrol_allowances + form.vars.food_allowances + form.vars.others + form.vars.incentive + form.vars.mobile_allowances        
    # _total_deductions = form.vars.loan_or_advances + form.vars.other_deductions + form.vars.absent_deductions
    # form.vars.total_gross_pay = _total_gross_pay #_emai.total_gross_pay
    # form.vars.total_deductions = _total_deductions
    # form.vars.net_pay = float(_total_gross_pay) - float(_total_deductions)
    # form.vars.bank_salary_name = _emai.bank_salary_name    
    form.vars.bank_transfer = _emai.bank_transfer
    form.vars.bank_account_name_id = _emai.bank_account_name_id
    form.vars.bank_account_no = _emai.bank_account_no
    form.vars.bank_branch = _emai.bank_branch
    form.vars.bank_iban_no = _emai.bank_iban_no

    form.vars.employee_no = _eed.employee_no
    form.vars.account_code = _eed.account_code
    form.vars.department_code_id = _eed.department_code_id
    form.vars.designation_code_id = _eed.designation_code_id
    form.vars.section_code_id = _eed.section_code_id
    form.vars.leave_entitlement = _eed.leave_entitlement
    form.vars.leave_days_per_year = _eed.leave_days_per_year
    form.vars.air_fare = _eed.air_fare
    form.vars.date_joined = _eed.date_joined
    form.vars.last_joining_date = _eed.last_joining_date
    form.vars.date_last_return = _eed.date_last_return
    form.vars.date_last_ticket = _eed.date_last_ticket
    form.vars.date_leave_due = _eed.date_leave_due
    form.vars.proposed_date = _eed.proposed_date
    form.vars.labor_card_profession_id = _eed.labor_card_profession_id
    form.vars.sector = _eed.sector
    form.vars.sponsors_id = _eed.sponsors_id
    form.vars.sponsors_occ = _eed.sponsors_occ

    if form.process(formname='Employee_Master').accepted:
        response.flash = 'RECORD UPDATED'        
        _em.update_record(**db.Employee_Master._filter_fields(form.vars))
        _ead.update_record(**db.Employee_Address_Details._filter_fields(form.vars))
        _emai.update_record(**db.Employee_Master_Account_Info._filter_fields(form.vars))
        _eed.update_record(**db.Employee_Employment_Details._filter_fields(form.vars))
        redirect(URL('get_employee_master_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
        response.js = "jQuery(console.log('error'))"
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Duration'),TH('Type'),TH('Remarks'),TH('Status'),TH('Action')))
    for n in db(db.Employee_Master_Leave.employee_id == request.args(0)).select():
        ctr += 1
        row.append(TR(
            TD(ctr), 
            TD(n.from_effective_date),
            TD(n.duration_leave),
            TD(n.type_of_leave_id.type_of_leave),
            TD(n.remarks),
            TD(n.status_id),
            TD()))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    _pics = db(db.Employee_Master.id == request.args(0)).select().first()
    # form2 = SQLFORM(db.Employee_Master, request.args(0))
    # if form2.process().accepted:
    #     response.flash = 'ok'
    # elif form2.errors():
    #     response.flash = 'not ok'
    return dict(form = form,_id = _id, table = table, pics = _pics, _eed = _eed, _emai = _emai)

def get_leave_chart_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Employee'),TH('Department'),TH('From'),TH('To')))    
    for n in db().select(orderby = db.Employee_Leave_Chart_Temporary.id):
        ctr += 1
        row.append(TR(
            TD(ctr, INPUT(_name='ctr',_value=n.id, _hidden=True)),            
            TD(n.employee_id.first_name, ' ', n.employee_id.last_name),
            TD(n.sub_department_id.sub_department_name),
            TD(INPUT(_class='form-control date from_effective_date', _type='text', _name='from_effective_date', _value=n.from_effective_date.strftime('%m-%d-%Y'), _style="width:160px;")),
            TD(INPUT(_class='form-control date to_effective_date', _type='text', _name='to_effective_date', _value=n.to_effective_date.strftime('%m-%d-%Y'), _style="width:160px;"))))            
    body = TBODY(*row)
    foot = TFOOT(TR(TD(INPUT(_id='btnDraft', _name= 'btnDraft', _type='submit', _value='save as draft',_class='btn btn-info'))))
    form = FORM(TABLE(*[head, body], _class='table', _id='table', **{'_data-toolbar':'#toolbar','_data-search':'true', '_data-show-refresh':'true','_data-show-pagination-switch':'true','_data-pagination':'true'}))
    if form.accepts(request, session):
        if request.vars.new_chart:
            print 'new chart click'
        elif request.vars.chart_update:
            print 'chart update'
    return dict(table = form)

def put_leave_chart_grid_generated():
    db.Employee_Leave_Chart_Temporary.truncate('RESTART IDENTITY CASCADE')    
    for n in db(db.Employee_Employment_Details).select(orderby = db.Employee_Employment_Details.id):
        db.Employee_Leave_Chart_Temporary.insert(
            transaction_date = request.now,
            employee_id = n.employee_id,
            department_code_id = n.department_code_id,
            from_effective_date = request.now,
            to_effective_date = request.now)
    return locals()

def put_leave_chart_grid_updated():    
    row = 0
    for n in request.vars['ctr']:        
        db(db.Employee_Leave_Chart_Temporary.id == n).update(from_effective_date = request.vars.from_effective_date[row], to_effective_date = request.vars.to_effective_date[row])        
        row += 1    

def get_basic_info_id():
    _id = db(db.Employee_Master.id == request.args(0)).select().first()
    _table = TABLE(TR(TD('Name: ', _id.title.upper(),' ', _id.first_name.upper(), ' ', _id.middle_name.upper(), ' ', _id.last_name.upper())))
    return dict(_table = _table)

def get_address_details_id():
   
    
    return dict(_id = db(db.Employee_Master.id == request.args(0)).select().first())

def get_account_details_id():
    _id = db(db.Employee_Master_Salary_Info.account_code_id == request.args(0)).select().first()
    if _id:
        redirect(URL('default','index'))
    else:
        return dict(_id = db(db.Employee_Master_Salary_Info.account_code_id == request.args(0)).select().first())

def get_employement_details_id():
    return dict(_table = 'table')

def get_other_details_id():
    return dict(_table = 'table')

def put_employee_master_id():
    _id = db(db.Employee_Master.id == request.args(0)).select()    
    _em = db(db.Employee_Master.id == request.args(0)).select(db.Employee_Master.ALL).first()
    _ead = db(db.Employee_Address_Details.employee_id == _em.id).select(db.Employee_Address_Details.ALL).first()
    _eed = db(db.Employee_Employment_Details.employee_id == request.args(0)).select(db.Employee_Employment_Details.ALL).first()
    _emai = db(db.Employee_Master_Account_Info.employee_id == request.args(0)).select(db.Employee_Master_Account_Info.ALL).first()
    db.Employee_Master_Account_Info.basic_income.writable = False
    db.Employee_Master_Account_Info.housing_allowances.writable = False
    db.Employee_Master_Account_Info.car_allowances.writable = False
    db.Employee_Master_Account_Info.petrol_allowances.writable = False
    db.Employee_Master_Account_Info.food_allowances.writable = False
    db.Employee_Master_Account_Info.others.writable = False
    db.Employee_Master_Account_Info.incentive.writable = False
    db.Employee_Master_Account_Info.mobile_allowances.writable = False
    db.Employee_Master_Account_Info.total_gross_pay.writable = False
    db.Employee_Employment_Details.sub_department_code_id.writable = False
    db.Employee_Employment_Details.back_office_code_id.writable = False

    db.Employee_Master.passport_image.writable = False
    db.Employee_Master.residence_permit_no_image.writable = False
    db.Employee_Master.labor_card_no_image.writable = False
    db.Employee_Master.health_card_no_image.writable = False
    db.Employee_Master.driver_license_no_image.writable = False
    db.Employee_Master.photo.writable = False
    db.Employee_Master.resume_image.writable = False
    db.Employee_Master.employment_contract.writable = False
    db.Employee_Master.medical_health_card_cert_no_image.writable = False
    db.Employee_Master.educational_certificate.writable = False
    


    form = SQLFORM.factory(db.Employee_Master, db.Employee_Address_Details, db.Employee_Employment_Details, db.Employee_Master_Account_Info,  table_name='Employee_Master')
    form.vars.title = _em.title
    form.vars.first_name = _em.first_name
    form.vars.middle_name = _em.middle_name
    form.vars.last_name = _em.last_name
    form.vars.gender = _em.gender 
    form.vars.telephone_no = _em.telephone_no    
    form.vars.mobile_no = _em.mobile_no
    form.vars.email = _em.email
    form.vars.marital_status = _em.marital_status
    form.vars.nationality = _em.nationality
    form.vars.religion = _em.religion 
    form.vars.languages = _em.languages
    form.vars.birth_place = _em.birth_place
    form.vars.birth_date = _em.birth_date
    form.vars.fathers_name = _em.fathers_name
    form.vars.education_qualification = _em.education_qualification
    form.vars.passport_no = _em.passport_no
    form.vars.passport_date_issued = _em.passport_date_issued
    form.vars.passport_date_expiration = _em.passport_date_expiration
    form.vars.date_given = _em.date_given
    form.vars.issuing_government = _em.issuing_government
    form.vars.place_issued = _em.place_issued
    form.vars.professional_passport = _em.professional_passport
    form.vars.residence_permit_no = _em.residence_permit_no
    form.vars.residence_permit_no_image = _em.residence_permit_no_image
    form.vars.residence_permit_no_expiration_date = _em.residence_permit_no_expiration_date
    form.vars.labor_card_no = _em.labor_card_no
    form.vars.labor_card_no_image = _em.labor_card_no_image
    form.vars.labor_card_no_expiration_date = _em.labor_card_no_expiration_date    
    
    form.vars.health_card_no = _em.health_card_no
    form.vars.health_card_no_image = _em.health_card_no_image
    form.vars.health_card_no_expiration_date = _em.health_card_no_expiration_date

    form.vars.medical_health_card_cert_no = _em.medical_health_card_cert_no
    form.vars.medical_health_card_cert_no_image = _em.medical_health_card_cert_no_image
    form.vars.medical_health_card_cert_no_expiration_date = _em.medical_health_card_cert_no_expiration_date

    form.vars.driver_license_no = _em.driver_license_no
    form.vars.driver_license_no_image = _em.driver_license_no_image
    form.vars.driver_license_no_expiration_date = _em.driver_license_no_expiration_date
    form.vars.last_job = _em.last_job
    form.vars.reason_leaving_previous_job = _em.reason_leaving_previous_job
    form.vars.previous_salary = _em.previous_salary
    form.vars.emergency_contant_name = _em.emergency_contant_name
    form.vars.emergency_contact_no = _em.emergency_contact_no
    form.vars.emergency_relationship = _em.emergency_relationship
    form.vars.residence_no = _em.residence_no
    form.vars.residence_no_date = _em.residence_no_date
    form.vars.residence_no_date_expiration = _em.residence_no_date_expiration    
    form.vars.photo = _em.photo
    form.vars.employee_status_id = _em.employee_status_id
    form.vars.resume_image = _em.resume_image

    form.vars.employee_id = _em.id
    form.vars.street = _ead.street
    form.vars.town = _ead.town
    form.vars.province = _ead.province
    form.vars.city = _ead.city
    form.vars.country = _ead.country
    form.vars.contact_no = _ead.contact_no
    form.vars.local_street = _ead.local_street
    form.vars.local_zone_no = _ead.local_zone_no
    form.vars.local_property_no = _ead.local_property_no
    form.vars.local_apartment_no = _ead.local_apartment_no
    form.vars.landlord_name = _ead.landlord_name
    form.vars.local_contact_no = _ead.local_contact_no

    # form.vars.basic_income = _emai.basic_income
    # form.vars.housing_allowances = _emai.housing_allowances
    # form.vars.car_allowances = _emai.car_allowances
    # form.vars.petrol_allowances = _emai.petrol_allowances
    # form.vars.food_allowances = _emai.food_allowances
    # form.vars.others = _emai.others
    # form.vars.incentive = _emai.incentive
    # form.vars.mobile_allowances = _emai.mobile_allowances
    
    # form.vars.loan_or_advances = _emai.loan_or_advances
    # form.vars.other_deductions = _emai.other_deductions
    # form.vars.absent_deductions = _emai.absent_deductions

    # _total_gross_pay = form.vars.basic_income + form.vars.housing_allowances + form.vars.car_allowances + form.vars.petrol_allowances + form.vars.food_allowances + form.vars.others + form.vars.incentive + form.vars.mobile_allowances        
    # _total_deductions = form.vars.loan_or_advances + form.vars.other_deductions + form.vars.absent_deductions
    # form.vars.total_gross_pay = _total_gross_pay #_emai.total_gross_pay
    # form.vars.total_deductions = _total_deductions
    # form.vars.net_pay = float(_total_gross_pay) - float(_total_deductions)
    # form.vars.bank_salary_name = _emai.bank_salary_name    
    form.vars.bank_transfer = _emai.bank_transfer
    form.vars.bank_account_name_id = _emai.bank_account_name_id
    form.vars.bank_account_no = _emai.bank_account_no
    form.vars.bank_branch = _emai.bank_branch
    form.vars.bank_iban_no = _emai.bank_iban_no

    form.vars.employee_no = _eed.employee_no
    form.vars.account_code = _eed.account_code
    form.vars.department_code_id = _eed.department_code_id
    form.vars.designation_code_id = _eed.designation_code_id
    form.vars.section_code_id = _eed.section_code_id
    form.vars.leave_entitlement = _eed.leave_entitlement
    form.vars.leave_days_per_year = _eed.leave_days_per_year
    form.vars.air_fare = _eed.air_fare
    form.vars.date_joined = _eed.date_joined
    form.vars.last_joining_date = _eed.last_joining_date
    form.vars.date_last_return = _eed.date_last_return
    form.vars.date_last_ticket = _eed.date_last_ticket
    form.vars.date_leave_due = _eed.date_leave_due
    form.vars.proposed_date = _eed.proposed_date
    form.vars.labor_card_profession_id = _eed.labor_card_profession_id
    form.vars.sector = _eed.sector
    form.vars.sponsors_id = _eed.sponsors_id
    form.vars.sponsors_occ = _eed.sponsors_occ

    if form.process().accepted:
        response.flash = 'RECORD UPDATED'              
        _em.update_record(**db.Employee_Master._filter_fields(form.vars))
        _ead.update_record(**db.Employee_Address_Details._filter_fields(form.vars))
        _emai.update_record(**db.Employee_Master_Account_Info._filter_fields(form.vars))
        _eed.update_record(**db.Employee_Employment_Details._filter_fields(form.vars))
        # redirect(URL('get_employee_master_grid'))
        response.js = "jQuery(console.log('updated'))"  
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
        response.js = "jQuery(console.log('error'))"
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Date'),TH('Duration'),TH('Type'),TH('Remarks'),TH('Status'),TH('Action')))
    for n in db(db.Employee_Master_Leave.employee_id == request.args(0)).select():
        ctr += 1
        row.append(TR(
            TD(ctr), 
            TD(n.from_effective_date),
            TD(n.duration_leave),
            TD(n.type_of_leave_id.type_of_leave),
            TD(n.remarks),
            TD(n.status_id),
            TD()))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table')
    _pics = db(db.Employee_Master.id == request.args(0)).select().first()
    # form2 = SQLFORM(db.Employee_Master, request.args(0))
    # if form2.process().accepted:
    #     response.flash = 'ok'
    # elif form2.errors():
    #     response.flash = 'not ok'
    return dict(form = form,_id = _id, table = table, pics = _pics, _eed = _eed, _emai = _emai)

def upload_image():
    record = db.Employee_Master(request.args(0))
    form = SQLFORM(db.Employee_Master, record, upload=URL('default','download'))
    if form.process().accepted:
        response.flash = 'updated'
        response.js = "$('#upload_files').get(0).reload();"        
    elif form.errors:
        response.flash = 'errors'
    return dict(form = form)

def get_employee_master_upload_file_id():
    db.Employee_Master.title.writable = False    
    db.Employee_Master.first_name.writable = False    
    db.Employee_Master.middle_name.writable = False
    db.Employee_Master.last_name.writable = False
    db.Employee_Master.gender.writable = False
    db.Employee_Master.telephone_no.writable = False
    db.Employee_Master.mobile_no.writable = False
    db.Employee_Master.email.writable = False
    db.Employee_Master.marital_status.writable = False
    db.Employee_Master.nationality.writable = False
    db.Employee_Master.religion.writable = False
    db.Employee_Master.languages.writable = False
    db.Employee_Master.birth_place.writable = False
    db.Employee_Master.birth_date.writable = False
    db.Employee_Master.fathers_name.writable = False
    db.Employee_Master.education_qualification.writable = False
    db.Employee_Master.passport_no.writable = False
    db.Employee_Master.passport_date_issued.writable = False
    db.Employee_Master.passport_date_expiration.writable = False
    db.Employee_Master.date_given.writable = False
    db.Employee_Master.issuing_government.writable = False
    db.Employee_Master.place_issued.writable = False
    db.Employee_Master.professional_passport.writable = False
    db.Employee_Master.residence_permit_no.writable = False
    db.Employee_Master.residence_permit_no_expiration_date.writable = False
    db.Employee_Master.labor_card_no.writable = False
    db.Employee_Master.labor_card_no_expiration_date.writable = False
    db.Employee_Master.health_card_no.writable = False
    db.Employee_Master.health_card_no_expiration_date.writable = False
    db.Employee_Master.medical_health_card_cert_no.writable = False
    db.Employee_Master.medical_health_card_cert_no_expiration_date.writable = False
    db.Employee_Master.driver_license_no.writable = False
    db.Employee_Master.driver_license_no_expiration_date.writable = False
    db.Employee_Master.last_job.writable = False
    db.Employee_Master.reason_leaving_previous_job.writable = False
    db.Employee_Master.previous_salary.writable = False
    db.Employee_Master.emergency_contant_name.writable = False
    db.Employee_Master.emergency_contact_no.writable = False
    db.Employee_Master.emergency_relationship.writable = False
    db.Employee_Master.next_of_ken.writable = False
    db.Employee_Master.residence_no.writable = False
    db.Employee_Master.residence_no_date.writable = False
    db.Employee_Master.residence_no_date_expiration.writable = False
    db.Employee_Master.employee_status_id.writable = False

    db.Employee_Master.title.readable = False    
    db.Employee_Master.first_name.readable = False    
    db.Employee_Master.middle_name.readable = False
    db.Employee_Master.last_name.readable = False
    db.Employee_Master.gender.readable = False
    db.Employee_Master.telephone_no.readable = False
    db.Employee_Master.mobile_no.readable = False
    db.Employee_Master.email.readable = False
    db.Employee_Master.marital_status.readable = False
    db.Employee_Master.nationality.readable = False
    db.Employee_Master.religion.readable = False
    db.Employee_Master.languages.readable = False
    db.Employee_Master.birth_place.readable = False
    db.Employee_Master.birth_date.readable = False
    db.Employee_Master.fathers_name.readable = False
    db.Employee_Master.education_qualification.readable = False
    db.Employee_Master.passport_no.readable = False
    db.Employee_Master.passport_date_issued.readable = False
    db.Employee_Master.passport_date_expiration.readable = False
    db.Employee_Master.date_given.readable = False
    db.Employee_Master.issuing_government.readable = False
    db.Employee_Master.place_issued.readable = False
    db.Employee_Master.professional_passport.readable = False
    db.Employee_Master.residence_permit_no.readable = False
    db.Employee_Master.residence_permit_no_expiration_date.readable = False
    db.Employee_Master.labor_card_no.readable = False
    db.Employee_Master.labor_card_no_expiration_date.readable = False
    db.Employee_Master.health_card_no.readable = False
    db.Employee_Master.health_card_no_expiration_date.readable = False
    db.Employee_Master.medical_health_card_cert_no.readable = False
    db.Employee_Master.medical_health_card_cert_no_expiration_date.readable = False
    db.Employee_Master.driver_license_no.readable = False
    db.Employee_Master.driver_license_no_expiration_date.readable = False
    db.Employee_Master.last_job.readable = False
    db.Employee_Master.reason_leaving_previous_job.readable = False
    db.Employee_Master.previous_salary.readable = False
    db.Employee_Master.emergency_contant_name.readable = False
    db.Employee_Master.emergency_contact_no.readable = False
    db.Employee_Master.emergency_relationship.readable = False
    db.Employee_Master.next_of_ken.readable = False
    db.Employee_Master.residence_no.readable = False
    db.Employee_Master.residence_no_date.readable = False
    db.Employee_Master.residence_no_date_expiration.readable = False
    db.Employee_Master.employee_status_id.readable = False
    
    form2 = SQLFORM(db.Employee_Master, request.args(0), upload=URL('default','download'))
    if form2.process().accepted:
        response.flash = 'updated'        
        response.js = "jQuery(location.reload())"

    elif form2.errors:
        response.flash = 'errors'
    return dict(form2 = form2)

def put_employee_master_upload_file_id():
    _id = db(db.Employee_Master.id == request.args(0)).select().first()
    db(db.Employee_Master.id == request.args(0)).update(
        passport_image = request.vars.passport_image,
        residence_permit_no_image = request.vars.residence_permit_no_image,
        labor_card_no_image = request.vars.labor_card_no_image,
        health_card_no_image = request.vars.health_card_no_image,
        medical_health_card_cert_no_image = request.vars.medical_health_card_cert_no_image,
        driver_license_no_image = request.vars.driver_license_no_image,
        photo = request.vars.photo,
        resume_image = request.vars.resume_image,
        employment_contract = request.vars.employment_contract,
    )
def get_salary_history_id():
    _id = db(db.Employee_Master.id == request.args(0)).select().first()
    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Date'),TH('Basic Income'),TH('Housing Allow.'),TH('Car Allow.'),TH('Petrol Allow.'),TH('Food Allow.'),TH('Others'),TH('Incentives'),TH('Mobile Allow.'),TH('Total Gross')))
    for n in db(db.Salary_Adjustment.employee_id == _id.id).select(orderby = ~db.Salary_Adjustment.id):
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.effectivity_date),
            TD(locale.format('%.2F',n.basic_income or 0, grouping = True)),
            TD(locale.format('%.2F',n.housing_allowances or 0, grouping = True)),
            TD(locale.format('%.2F',n.car_allowances or 0, grouping = True)),

            TD(locale.format('%.2F',n.petrol_allowances or 0, grouping = True)),
            TD(locale.format('%.2F',n.food_allowances or 0, grouping = True)),
            TD(locale.format('%.2F',n.others or 0, grouping = True)),
            TD(locale.format('%.2F',n.incentive or 0, grouping = True)),
            TD(locale.format('%.2F',n.mobile_allowances or 0, grouping = True)),
            TD(locale.format('%.2F',n.total_gross_pay or 0, grouping = True))))
    body = TBODY(*row)
    table = TABLE(*[head,body], _class='table table-striped')
    return XML(table)

def put_basic_info_id():
    form = SQLFORM(db.Employee_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def post_employee_master():
    form = SQLFORM.factory(db.Employee_Master, db.Employee_Address_Details, db.Employee_Employment_Details, db.Employee_Master_Account_Info)
    if form.process().accepted:
        _id = db.Employee_Master.insert(**db.Employee_Master._filter_fields(form.vars))
        form.vars.employee_id = _id
        _id = db.Employee_Address_Details.insert(**db.Employee_Address_Details._filter_fields(form.vars))
        _id = db.Employee_Employment_Details.insert(**db.Employee_Employment_Details._filter_fields(form.vars))
        _id = db.Employee_Master_Account_Info.insert(**db.Employee_Master_Account_Info._filter_fields(form.vars))
        _id = db.Salary_Adjustment.insert(**db.Salary_Adjustment._filter_fields(form.vars))
        # _total_gross_pay = float(form.vars.basic_income or 0) + float(form.vars.housing_allowances or 0) + float(form.vars.car_allowances or 0) + float(form.vars.petrol_allowances or 0) + float(form.vars.food_allowances or 0) + float(form.vars.others or 0) + float(form.vars.incentive or 0) + float(form.vars.mobile_allowances or 0)
        # db.Salary_Adjustment.insert(
        #     employee_id = form.vars.employee_id,
        #     basic_income = float(form.vars.basic_income or 0),
        #     housing_allowances = float(form.vars.housing_allowances or 0), 
        #     car_allowances = float(form.vars.car_allowances or 0),
        #     petrol_allowances = float(form.vars.petrol_allowances or 0),
        #     food_allowances = float(form.vars.food_allowances or 0), 
        #     others = float(form.vars.others or 0),
        #     incentive = float(form.vars.incentive or 0),
        #     mobile_allowances = float(form.vars.mobile_allowances or 0)
        #     total_gross_pay = _total_gross_pay)        
    elif form.errors:
        response.flash = 'ERROR'        
        response.js = "console.log('error')"
    return dict(form = form)

def echo_employee_name():
    _first_name = request.vars.first_name.upper()
    _middle_name = request.vars.middle_name.upper()
    _last_name = request.vars.last_name.upper()
    return XML(str(_first_name) + ' ' + str(_middle_name) + ' ' + _last_name)

def echo_designation():
    _id = db(db.Designation.id == request.vars.designation_code_id).select().first()    
    return XML(str(_id.designation_name))

def echo_department():
    _id = db(db.Department.id == request.vars.department_code_id).select().first()
    return XML(str(_id.department_name))

def echo_employee_no():    
    return XML(str(request.vars.employee_no))

def echo_account_code():        
    return XML(str(request.vars.account_code))

def echo_education():        
    return XML(str(request.vars.education_qualification))

def echo_nationality():        
    return XML(str(request.vars.nationality))

def get_employee_id():
    form = SQLFORM(db.Employee_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'SAVE'
        # redirect(URL('default','index'))
    elif form.errors:
        response.flash = 'ERROR'
    return dict(form = form)
def get_card_report_grid():
    return dict()
    
def get_employee_master_report_grid():    
    row = []
    ctr = 0
    head = THEAD(TR(
        TH('#'),
        TH('Name'),
        TH('Gender'),
        TH('Telephone No'),
        TH('mobile_no'),
        TH('email'),
        TH('marital_status'),
        TH('nationality'),
        TH('religion'),
        TH('languages'),
        TH('birth_place'),
        TH('birth_date'),
        TH('fathers_name'),
        TH('education_qualification'),
        TH('passport_no'),
        TH('passport_date_issued'),
        TH('passport_date_expiration'),
        TH('date_given'),
        TH('issuing_government'),
        TH('place_issued'),
        TH('professional_passport'),
        TH('residence_permit_no'),
        TH('residence_permit_no_expiration_date'),
        TH('labor_card_no'),
        TH('labor_card_no_expiration_date'),
        TH('health_card_no'),
        TH('health_card_no_expiration_date'),
        TH('medical_health_card_cert_no'),
        TH('medical_health_card_cert_no_expiration_date'),
        TH('driver_license_no'),
        TH('driver_license_no_expiration_date'),
        TH('last_job'),
        TH('reason_leaving_previous_job'),
        TH('previous_salary'),
        TH('emergency_contant_name'),
        TH('emergency_contact_no'),
        TH('emergency_relationship'),
        TH('next_of_ken'),
        TH('residence_no'),
        TH('residence_no_date'),
        TH('residence_no_date_expiration'),
        TH('employee_status_id'),        
        ))
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id, 
    left = db.Employee_Address_Details.on(db.Employee_Master.id == db.Employee_Address_Details.employee_id)):
        ctr+=1
        _name = n.Employee_Master.title, ' ', n.Employee_Master.first_name, ' ', n.Employee_Master.middle_name, ' ', n.Employee_Master.last_name
        row.append(TR(
            TD(ctr),
            TD(_name),
            TD(n.Employee_Master.gender),
            TD(n.Employee_Master.telephone_no),
            TD(n.Employee_Master.mobile_no),
            TD(n.Employee_Master.email),
            TD(n.Employee_Master.marital_status),
            TD(n.Employee_Master.nationality),
            TD(n.Employee_Master.religion),
            TD(n.Employee_Master.languages),
            TD(n.Employee_Master.birth_place),
            TD(n.Employee_Master.birth_date),
            TD(n.Employee_Master.fathers_name),
            TD(n.Employee_Master.education_qualification),
            TD(n.Employee_Master.passport_no),
            TD(n.Employee_Master.passport_date_issued),
            TD(n.Employee_Master.passport_date_expiration),
            TD(n.Employee_Master.date_given),
            TD(n.Employee_Master.issuing_government),
            TD(n.Employee_Master.place_issued),
            TD(n.Employee_Master.professional_passport),
            TD(n.Employee_Master.residence_permit_no),
            TD(n.Employee_Master.residence_permit_no_expiration_date),
            TD(n.Employee_Master.labor_card_no),
            TD(n.Employee_Master.labor_card_no_expiration_date),
            TD(n.Employee_Master.health_card_no),
            TD(n.Employee_Master.health_card_no_expiration_date),
            TD(n.Employee_Master.medical_health_card_cert_no),
            TD(n.Employee_Master.medical_health_card_cert_no_expiration_date),
            TD(n.Employee_Master.driver_license_no),
            TD(n.Employee_Master.driver_license_no_expiration_date),
            TD(n.Employee_Master.last_job),
            TD(n.Employee_Master.reason_leaving_previous_job),
            TD(n.Employee_Master.previous_salary),
            TD(n.Employee_Master.emergency_contant_name),
            TD(n.Employee_Master.emergency_contact_no),
            TD(n.Employee_Master.emergency_relationship),
            TD(n.Employee_Master.next_of_ken),
            TD(n.Employee_Master.residence_no),
            TD(n.Employee_Master.residence_no_date),
            TD(n.Employee_Master.residence_no_date_expiration),
            TD(n.Employee_Master.employee_status_id.status),            
        ))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def get_employee_address_report_grid():
    row = []
    ctr = 0
    head = THEAD(TR(
        TH('#'),
        TH('Name'),
        TH('Street'),
        TH('town'),
        TH('province'),
        TH('city'),
        TH('country'),
        TH('contact_no'),
        TH('local_street'),
        TH('local_zone_no'),
        TH('local_property_no'),
        TH('local_apartment_no'),
        TH('landlord_name'),
        TH('local_contact_no')))
    for n in db().select(orderby = db.Employee_Address_Details.employee_id):
        ctr+=1
        row.append(TR(
            TD(ctr),
            TD(n.employee_id.title,' ',n.employee_id.first_name, ' ', n.employee_id.middle_name,' ', n.employee_id.last_name),
            TD(n.street),
            TD(n.town),
            TD(n.province),
            TD(n.city),
            TD(n.country),
            TD(n.contact_no),
            TD(n.local_street),
            TD(n.local_zone_no),
            TD(n.local_property_no),
            TD(n.local_apartment_no),
            TD(n.landlord_name),
            TD(n.local_contact_no)
        ))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def get_employment_details_report_grid():
    row = []
    ctr = 0
    head = THEAD(TR(
        TH('#'),
        TH('employee_no'),
        TH('account_code'),
        TH('employee_id'),        
        TH('department_code_id'),
        TH('designation_code_id'),
        TH('section_code_id'),
        TH('leave_entitlement'),
        TH('leave_days_per_year'),
        TH('air_fare'),
        TH('date_joined'),
        TH('last_joining_date'),
        TH('date_last_return'),
        TH('date_last_ticket'),
        TH('date_leave_due'),
        TH('proposed_date'),
        TH('labor_card_profession_id'),
        TH('sector'),
        TH('sponsors_id'),                
        TH('sponsors_occ')        
        ))
    for n in db().select(orderby = db.Employee_Employment_Details.employee_id):
        ctr+=1
        row.append(TR(
            TD(ctr),
            TD(n.employee_no),
            TD(n.account_code),
            TD(n.employee_id.title, ' ', n.employee_id.first_name, ' ', n.employee_id.middle_name, ' ', n.employee_id.last_name),
            TD(n.department_code_id.department_name),
            TD(n.designation_code_id.designation_name),
            TD(n.section_code_id),
            TD(n.leave_entitlement),
            TD(n.leave_days_per_year),
            TD(n.air_fare),
            TD(n.date_joined),
            TD(n.last_joining_date),
            TD(n.date_last_return),
            TD(n.date_last_ticket),
            TD(n.date_leave_due),
            TD(n.proposed_date),
            TD(n.labor_card_profession_id),
            TD(n.sector),
            TD(n.sponsors_id),
            TD(n.sponsors_occ)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

def get_employment_account_info_report_grid():
    row = []
    ctr = 0
    head = THEAD(TR(
        TH('#'),
        TH('employee_id'),
        TH('basic_income'),
        TH('housing_allowances'),
        TH('car_allowances'),
        TH('petrol_allowances'),
        TH('food_allowances'),
        TH('others'),
        TH('incentive'),
        TH('mobile_allowances'),
        TH('total_gross_pay'),
        TH('bank_account_name_id'),
        TH('bank_account_no'),
        TH('bank_branch'),
        TH('bank_iban_no')
    ))
    for n in db().select(orderby = db.Employee_Master_Account_Info.employee_id):
        ctr+=1
        row.append(TR(
            TD(ctr),
            TD(n.employee_id.title, ' ' ,n.employee_id.first_name, ' ', n.employee_id.middle_name, ' ',n.employee_id.last_name),
            TD(n.basic_income),
            TD(n.housing_allowances),
            TD(n.car_allowances),
            TD(n.petrol_allowances),
            TD(n.food_allowances),
            TD(n.others),
            TD(n.incentive),
            TD(n.mobile_allowances),
            TD(n.total_gross_pay),
            TD(n.bank_account_name_id),
            TD(n.bank_account_no),
            TD(n.bank_branch),
            TD(n.bank_iban_no)
        ))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)
def get_residence_permit_report_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Name'),TH('Residence No'),TH('Expiration Date'),TH('Status'),TH('Control Action')),_class='bg-primary')
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):        
        _eed = db(db.Employee_Employment_Details.employee_id == n.id).select().first()
        if n.residence_permit_no_expiration_date != None:
            _15_days = date.today() + timedelta(days=15)
            _30_days = date.today() + timedelta(days=30)            
            if date.today() > n.residence_permit_no_expiration_date:
                ctr+=1 
                _status = SPAN('Expired', _class='badge bg-red')
                row.append(TR(TD(ctr, INPUT(_name='ctr',_value=n.id, _hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.residence_permit_no),TD(INPUT(_class='form-control date', _name='residence_permit_no_expiration_date',_value=n.residence_permit_no_expiration_date)),TD(_status),TD()))                      
            elif _15_days > n.residence_permit_no_expiration_date:
                ctr+=1 
                _status = SPAN('15 days due', _class='badge bg-yellow')
                row.append(TR(TD(ctr, INPUT(_name='ctr',_value=n.id, _hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.residence_permit_no),TD(INPUT(_class='form-control date', _name='residence_permit_no_expiration_date',_value=n.residence_permit_no_expiration_date)),TD(_status),TD()))                      
            elif _30_days > n.residence_permit_no_expiration_date:
                ctr+=1 
                _status = SPAN('30 days due', _class='badge bg-green')
                row.append(TR(TD(ctr, INPUT(_name='ctr',_value=n.id, _hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.residence_permit_no),TD(INPUT(_class='form-control date', _name='residence_permit_no_expiration_date',_value=n.residence_no_date_expiration)),TD(_status),TD()))
    body = TBODY(*row)
    table = FORM(TABLE(*[head, body], _class='table',_id='tblres', **{'_data-toolbar':'#restoolbar','_data-toggle':'table','_data-search':'true','_data-pagination':'true'}))
    if table.accepts(request, session):
        if request.vars.btnUpdate:
            x = 'updated'
    return dict(table = table)

def put_residence_permit_report_grid():    
    row = 0
    for n in request.vars.ctr:
        db(db.Employee_Master.id == n).update(residence_no_date_expiration = request.vars.residence_no_date_expiration[row])
        row += 1       

def get_drivers_license_report_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Name'),TH('License No'),TH('Expiration Date'),TH('Status'),TH('Control Action')),_class='bg-primary')
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):        
        _eed = db(db.Employee_Employment_Details.employee_id == n.id).select().first()
        if n.driver_license_no_expiration_date != None:
            _15_days = date.today() + timedelta(days=15)
            _30_days = date.today() + timedelta(days=30)            
            if date.today() > n.driver_license_no_expiration_date:
                ctr+=1 
                _status = SPAN('Expired', _class='badge bg-red')
                row.append(TR(TD(ctr,INPUT(_name='dri',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.driver_license_no),TD(INPUT(_class='form-control date',_name='driver_license_no_expiration_date',_value=n.driver_license_no_expiration_date)),TD(_status),TD()))                      
            elif _15_days > n.driver_license_no_expiration_date:
                ctr+=1 
                _status = SPAN('15 days due', _class='badge bg-yellow')
                row.append(TR(TD(ctr,INPUT(_name='dri',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.driver_license_no),TD(INPUT(_class='form-control date',_name='driver_license_no_expiration_date',_value=n.driver_license_no_expiration_date)),TD(_status),TD()))                      
            elif _30_days > n.driver_license_no_expiration_date:
                ctr+=1 
                _status = SPAN('30 days due', _class='badge bg-green')
                row.append(TR(TD(ctr,INPUT(_name='dri',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.driver_license_no),TD(INPUT(_class='form-control date',_name='driver_license_no_expiration_date',_value=n.driver_license_no_expiration_date)),TD(_status),TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toolbar':'#dritoolbar','_data-toggle':'table','_data-search':'true','_data-pagination':'true'})
    return dict(table = table)

def put_drivers_license_report_grid():    
    row = 0
    for n in request.vars.dri:        
        db(db.Employee_Master.id == n).update(driver_license_no_expiration_date = request.vars.driver_license_no_expiration_date[row])
        row += 1       

def get_passport_report_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Name'),TH('Passport No'),TH('Expiration Date'),TH('Status'),TH('Control Action')),_class='bg-primary')
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):        
        _eed = db(db.Employee_Employment_Details.employee_id == n.id).select().first()
        if n.passport_date_expiration != None:
            _15_days = date.today() + timedelta(days=15)
            _30_days = date.today() + timedelta(days=30)            
            if date.today() > n.passport_date_expiration:
                ctr+=1 
                _status = SPAN('Expired', _class='badge bg-red')
                row.append(TR(TD(ctr,INPUT(_name='pas',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.passport_no),TD(INPUT(_class='form-control date',_name='passport_date_expiration',_value=n.passport_date_expiration)),TD(_status),TD()))                      
            elif _15_days > n.passport_date_expiration:
                ctr+=1 
                _status = SPAN('15 days due', _class='badge bg-yellow')
                row.append(TR(TD(ctr,INPUT(_name='pas',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.passport_no),TD(INPUT(_class='form-control date',_name='passport_date_expiration',_value=n.passport_date_expiration)),TD(_status),TD()))                      
            elif _30_days > n.passport_date_expiration:
                ctr+=1 
                _status = SPAN('30 days due', _class='badge bg-green')
                row.append(TR(TD(ctr,INPUT(_name='pas',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.passport_no),TD(INPUT(_class='form-control date',_name='passport_date_expiration',_value=n.passport_date_expiration)),TD(_status),TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toolbar':'#pastoolbar','_data-toggle':'table','_data-search':'true','_data-pagination':'true'})
    return dict(table = table)

def put_passport_report_grid():
    row = 0
    for n in request.vars.pas:
        db(db.Employee_Master.id == n).update(passport_date_expiration = request.vars.passport_date_expiration[row])
        row += 1

def get_health_card_report_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Name'),TH('Health Card No'),TH('Expiration Date'),TH('Status'),TH('Control Action')),_class='bg-primary')
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):        
        _eed = db(db.Employee_Employment_Details.employee_id == n.id).select().first()
        if n.health_card_no_expiration_date != None:
            _15_days = date.today() + timedelta(days=15)
            _30_days = date.today() + timedelta(days=30)            
            if date.today() > n.health_card_no_expiration_date:
                ctr+=1 
                _status = SPAN('Expired', _class='badge bg-red')
                row.append(TR(TD(ctr,INPUT(_name='hea',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.health_card_no),TD(INPUT(_class='form-control date',_name='health_card_no_expiration_date',_value=n.health_card_no_expiration_date)),TD(_status),TD()))                      
            elif _15_days > n.health_card_no_expiration_date:
                ctr+=1 
                _status = SPAN('15 days due', _class='badge bg-yellow')
                row.append(TR(TD(ctr,INPUT(_name='hea',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.health_card_no),TD(INPUT(_class='form-control date',_name='health_card_no_expiration_date',_value=n.health_card_no_expiration_date)),TD(_status),TD()))                      
            elif _30_days > n.health_card_no_expiration_date:
                ctr+=1 
                _status = SPAN('30 days due', _class='badge bg-green')
                row.append(TR(TD(ctr,INPUT(_name='hea',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.health_card_no),TD(INPUT(_class='form-control date',_name='health_card_no_expiration_date',_value=n.health_card_no_expiration_date)),TD(_status),TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toolbar':'#heatoolbar','_data-toggle':'table','_data-search':'true','_data-pagination':'true'})
    return dict(table = table)

def put_health_card_report_grid():
    row = 0
    for n in request.vars.hea:
        db(db.Employee_Master.id == n).update(health_card_no_expiration_date = request.vars.health_card_no_expiration_date[row])
        row += 1

def get_medical_health_card_report_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Name'),TH('Health Card No'),TH('Expiration Date'),TH('Status'),TH('Control Action')),_class='bg-primary')
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):        
        _eed = db(db.Employee_Employment_Details.employee_id == n.id).select().first()
        if n.medical_health_card_cert_no_expiration_date != None:
            _15_days = date.today() + timedelta(days=15)
            _30_days = date.today() + timedelta(days=30)            
            if date.today() > n.medical_health_card_cert_no_expiration_date:
                ctr+=1 
                _status = SPAN('Expired', _class='badge bg-red')
                row.append(TR(TD(ctr,INPUT(_name='med',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.medical_health_card_cert_no),TD(INPUT(_class='form-control date',_name='medical_health_card_cert_no_expiration_date',_value=n.medical_health_card_cert_no_expiration_date)),TD(_status),TD()))                      
            elif _15_days > n.medical_health_card_cert_no_expiration_date:
                ctr+=1 
                _status = SPAN('15 days due', _class='badge bg-yellow')
                row.append(TR(TD(ctr,INPUT(_name='med',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.medical_health_card_cert_no),TD(INPUT(_class='form-control date',_name='medical_health_card_cert_no_expiration_date',_value=n.medical_health_card_cert_no_expiration_date)),TD(_status),TD()))                      
            elif _30_days > n.medical_health_card_cert_no_expiration_date:
                ctr+=1 
                _status = SPAN('30 days due', _class='badge bg-green')
                row.append(TR(TD(ctr,INPUT(_name='med',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.medical_health_card_cert_no),TD(INPUT(_class='form-control date',_name='medical_health_card_cert_no_expiration_date',_value=n.medical_health_card_cert_no_expiration_date)),TD(_status),TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toolbar':'#medtoolbar','_data-toggle':'table','_data-search':'true','_data-pagination':'true'})
    return dict(table = table)

def put_medical_health_card_report_grid():
    row = 0
    for n in request.vars.med:
        db(db.Employee_Master.id == n).update(medical_health_card_cert_no_expiration_date = request.vars.medical_health_card_cert_no_expiration_date[row])
        row += 1

def get_labour_card_report_grid():
    row = []
    ctr = 0    
    head = THEAD(TR(TH('#'),TH('Name'),TH('Labour Card No'),TH('Expiration Date'),TH('Status'),TH('Control Action')),_class='bg-primary')
    for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):        
        _eed = db(db.Employee_Employment_Details.employee_id == n.id).select().first()
        if n.labor_card_no_expiration_date != None:
            _15_days = date.today() + timedelta(days=15)
            _30_days = date.today() + timedelta(days=30)            
            if date.today() > n.labor_card_no_expiration_date:
                ctr+=1 
                _status = SPAN('Expired', _class='badge bg-red')
                row.append(TR(TD(ctr,INPUT(_name='lab',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.labor_card_no),TD(INPUT(_class='form-control date',_name='labor_card_no_expiration_date',_value=n.labor_card_no_expiration_date)),TD(_status),TD()))                      
            elif _15_days > n.labor_card_no_expiration_date:
                ctr+=1 
                _status = SPAN('15 days due', _class='badge bg-yellow')
                row.append(TR(TD(ctr,INPUT(_name='lab',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.labor_card_no),TD(INPUT(_class='form-control date',_name='labor_card_no_expiration_date',_value=n.labor_card_no_expiration_date)),TD(_status),TD()))                      
            elif _30_days > n.labor_card_no_expiration_date:
                ctr+=1 
                _status = SPAN('30 days due', _class='badge bg-green')
                row.append(TR(TD(ctr,INPUT(_name='lab',_value=n.id,_hidden=True)),TD(n.title, ' ', n.first_name, ' ', n.middle_name, ' ', n.last_name,', ', SPAN(_eed.account_code,_class='text-muted')),TD(n.labor_card_no),TD(INPUT(_class='form-control date',_name='labor_card_no_expiration_date',_value=n.labor_card_no_expiration_date)),TD(_status),TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', **{'_data-toolbar':'#labtoolbar','_data-toggle':'table','_data-search':'true','_data-pagination':'true'})
    return dict(table = table)

def put_labour_card_report_grid():
    row = 0
    for n in request.vars.lab:        
        db(db.Employee_Master.id == n).update(labor_card_no_expiration_date = request.vars.labor_card_no_expiration_date[row])
        row += 1

# ------------------------------------------------------------------------------------------
# ---------------------  E O S/ R E S I G N E D   S Y S T E M  -----------------------------
# ------------------------------------------------------------------------------------------
def get_hr_reminders_status_grid():
    form = SQLFORM(db.EOS_Status)
    if form.process().accepted:
        response.js = "jQuery(alertify.success('Form Save'))"
    elif form.errors:        
        response.js = "alertify.error('Form has error');"
    row = []
    head = THEAD(TR(TH('#'),TH('Status'),TH('Description'),TH('Action')))
    for n in db(db.EOS_Status).select(orderby = db.EOS_Status.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('hr_reminders','put_hr_reminders_status_id', args = n.id))        
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.description),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class= 'table')
    return dict(form = form, table = table)

def put_hr_reminders_status_id():
    form = SQLFORM(db.EOS_Status, request.args(0))
    if form.process().accepted:
        # response.js = "jQuery(alertify.success('Form Updated'));"
        response.js = "jQuery(console.log('ok na'));"
    elif form.errors:        
        response.js = "jQuery(alertify.error('Form has error'));"
        print form.errors
    return dict(form = form)

def get_hr_reminders_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Employee Name'),TH('Department'),TH('Designation'),TH('Status'),TH('Action')))
    for n in db(db.EOS).select(db.EOS.ALL, db.Employee_Employment_Details.ALL, orderby = db.EOS.id, join = db.Employee_Employment_Details.on(db.EOS.employee_id == db.Employee_Employment_Details.employee_id)):
        ctr+=1        
        action = DIV(DIV(A(I(_class='fa fa-sort-amount-desc'),_class='btn btn-outline-secondary dropdown-toggle',_type='button',**{'_data-toggle':'dropdown','_aria-haspopup':'true','aria-expanded':'false'}),
            DIV(LI(A('Company Work Certificate',_class='dropdown-item',_href='#')),
                LI(A('Bank Notification Letter',_class='dropdown-item',_target=' blank', _href=URL('hr_reminders','get_bank_notification_letter_id',args = n.EOS.id))),
                LI(A('Transfer of Sponsor',_class='dropdown-item',_href=URL('hr_reminders','put_hr_reminders_transfer_sponsor_id',args = n.EOS.id))),
                LI(A('Sponsor Details',_class='dropdown-item',_href=URL('hr_reminders','put_hr_reminders_transfer_sponsor_id',args = n.EOS.id))),
                LI(_class='divider',_role='separator'),
                LI(A('Issued',_class='dropdown-item',_id='issued',callback=URL('hr_reminders','put_hr_reminders_issued_id',args = n.EOS.id))),
                LI(A('Pending',_class='dropdown-item',_id='pending',callback=URL('hr_reminders','put_hr_reminders_pending_id',args=n.EOS.id))),
                LI(A('Not Applicable',_class='dropdown-item',_id='not',callback=URL('hr_reminders','put_hr_reminders_not_applicable_id',args=n.EOS.id))),
                _class='dropdown-menu'),_class='input-group_append'),_class='input-group')
        btn_lnk = DIV(action)
        row.append(TR(
            TD(ctr),            
            TD(n.EOS.employee_id.title, ' ', n.EOS.employee_id.first_name,' ', n.EOS.employee_id.middle_name, ' ', n.EOS.employee_id.last_name, ', ',SPAN(n.Employee_Employment_Details.account_code,_class='text-muted')),
            TD(n.Employee_Employment_Details.department_code_id.department_name),
            TD(n.Employee_Employment_Details.designation_code_id.designation_name),
            TD(n.EOS.status_id.status),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='tblEOS')
    return dict(table = table)

def put_hr_reminders_transfer_sponsor_id():
    form = SQLFORM(db.EOS, request.args(0))
    if form.process().accepted:        
        redirect(URL('hr_reminders','get_hr_reminders_grid'))
        response.js = 'jQuery(console.log("ok"))'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

def put_hr_reminders_issued_id():
    #$("#mydiv").load(location.href + " #mydiv");
    db(db.EOS.id == request.args(0)).update(status_id=1)
    response.js = "jQuery(alertify.success('Issued successfully.'), $('#tblEOS').load(window.location.href + ' #tblEOS'))"
    
def put_hr_reminders_pending_id():
    db(db.EOS.id == request.args(0)).update(status_id=2)
    response.js = "jQuery(alertify.success('Pending successfully.'), $('#tblEOS').load(window.location.href + ' #tblEOS'))"
    
def put_hr_reminders_not_applicable_id():
    db(db.EOS.id == request.args(0)).update(status_id=3)
    response.js = "jQuery(alertify.success('Not Applicable.'), $('#tblEOS').load(window.location.href + ' #tblEOS'))"
    

# ------------------------------------------------------------------------------------------
# ---------------  E O S/ R E S I G N E D   S Y S T E M  R E P O R T S----------------------
# ------------------------------------------------------------------------------------------

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time
from datetime import date
from time import gmtime, strftime
import locale
locale.setlocale(locale.LC_ALL,'')

import inflect 
from decimal import Decimal
w=inflect.engine()

# today = datetime.datetime.now()

MaxWidth_Content = 530
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
# styleN = styles['Normal']
styleH = styles['Heading1']

_style = ParagraphStyle('Courier',fontName="Courier", fontSize=9, leading = 15)
_style10 = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_style2 = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)
_style_space_14 = ParagraphStyle('Courier',fontName="Courier", fontSize=15, leading = 15, strikeGap = 10)
_style3 = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_style4 = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 9)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.5*inch, leftMargin=50, rightMargin=50, bottomMargin=110)#,showBoundary=1)
_landscape = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=50, leftMargin=15, rightMargin=15, bottomMargin=50)#,showBoundary=1)

def eos():
    print '-= * =-'
    for n in db(db.Employee_Master_Leave.type_of_leave_id == 10).select(orderby = db.Employee_Master_Leave.id):
        print n.id
    return dict()

def get_bank_notification_letter_id():
    _id = db(db.EOS.id == request.args(0)).select().first()
    _eml = db(db.Employee_Master_Leave.employee_id == _id.employee_id).select().first()
    _ema = db(db.Employee_Master_Account_Info.employee_id == _id.employee_id).select().first()
    _emm = db(db.Employee_Master.id == _id.employee_id).select().first()
    if _emm.title == 'Mr.':
        _con = 'His last day of duty will be ' + str(_eml.from_effective_date.strftime('%d-%B-%Y'))
    else:
        _con = 'Her last day of duty will be ' + str(_eml.from_effective_date.strftime('%d-%B-%Y'))

    if _eml.type_of_leave_id == 8:
        _leave = 'resigning from our company with effect from ' + str(_eml.from_effective_date.strftime('%d-%B-%Y'))
        _signa = 'GENERAL MANAGER'
    else:
        _leave = 'ended. ' + _con
        _signa = 'NOUR KHANFAR\nHR Manager'
        
    _content = [
        [str('Ref.: ') + str(_eml.doc_ref_no),_eml.from_effective_date.strftime('%d-%B-%Y')],
        ['The Manager\n' + str(_ema.bank_account_name_id.bank_account_name) + '\n' +str(_ema.bank_branch) + '\nDoha, Qatar',''],
        ['Dear Sir,'],
        [Paragraph('We are hereby notifitying you that ' + str(B(_id.employee_id.title)) + str(B(_id.employee_id.first_name)) + ' ' +str(B(_id.employee_id.middle_name)) + ' ' +str(B(_id.employee_id.last_name)) + ' with ' + str(_ema.bank_account_name_id.bank_account_name) + ' IBAN no. ' + str(B(_ema.bank_iban_no)) + ' is ' + str(_leave),style=_style10)],
        ['This is for your information and reference.'],
        ['Yours faithfully,\nMERCH & PARTNERS CO.,WLL.'],
        [_signa],
        ['c.c.: Personal File\n      Accts Dept.,Merch'],
        ['Administration Dept Tel No.: 44658656']]
    _row = Table(_content, colWidths='*')
    _row.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5,colors.Color(0,0,0,0.2)),
        ('FONTNAME',(0, 0),(-1,-1),'Courier'), 
        # ('FONTNAME',(0,6),(0,6),'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('FONTSIZE',(0,8),(0,8),8),
        ('SPAN',(0,3),(1,3)),
        ('TOPPADDING',(0,1),(0,1),40),
        ('TOPPADDING',(0,2),(0,2),40),
        ('TOPPADDING',(0,3),(0,5),15),
        ('TOPPADDING',(0,6),(0,6),50),
        ('TOPPADDING',(0,7),(0,7),50),
        ('TOPPADDING',(0,8),(0,8),90),
        ('ALIGN',(1,0),(1,0), 'RIGHT'),
    ]))
    row.append(_row)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data       
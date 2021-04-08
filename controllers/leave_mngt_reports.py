
##########          R E P O R T S           ##########

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
_style2 = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)
_style_space_14 = ParagraphStyle('Courier',fontName="Courier", fontSize=15, leading = 15, strikeGap = 10)
_style3 = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_style4 = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 9)
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=1.2*inch, leftMargin=20, rightMargin=20, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=50, leftMargin=50, rightMargin=50, bottomMargin=110)#,showBoundary=1)
_landscape = SimpleDocTemplate(tmpfilename,pagesize=A4, topMargin=50, leftMargin=15, rightMargin=15, bottomMargin=50)#,showBoundary=1)



merch = Paragraph('''<font size=8>Merch & Partners Co. WLL. <font color="black">|</font></font> <font size=7 color="black"> Merch ERP</font>''',styles["BodyText"])

def put_application_hr_leave_id_approved(): # approved from department head
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if (_id.type_of_leave_id == 1) or (_id.type_of_leave_id == 4) or (_id.type_of_leave_id == 5):
        db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 6)
    elif (_id.type_of_leave_id == 2) or (_id.type_of_leave_id == 7):
        _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
        _skey = _pre.serial_key
        _skey += 1    
        _usr_f = str(_id.employee_id.first_name.upper())
        _usr_l = str(_id.employee_id.last_name.upper())
        _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]        
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 16)
        _pre.update_record(serial_key = _skey)      
        # redirect(URL('leave_mngt_reports','get_application_leave_report_id', args = request.args(0)))
    elif (_id.type_of_leave_id == 3) or (_id.type_of_leave_id == 6):
        db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 10) # proceeds to accounts department for processing

def put_confirm_and_print_applicaton_id():   # approved from management head
    print 'put_confirm_and_print_applicaton_id'
    
def xput_confirm_and_print_applicaton_id():   # approved from management head
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if _id.doc_ref_no == None:
        _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
        _skey = _pre.serial_key
        _skey += 1    
        _usr_f = str(auth.user.first_name.upper())
        _usr_l = str(auth.user.last_name.upper())
        _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]            
        _pre.update_record(serial_key = _skey) 
        db(db.Employee_Master_Leave.id == request.args(0)).update(doc_ref_no = _ckey, status_id = 10)        
        redirect(URL('leave_mngt_reports','get_application_leave_report_id', args = request.args(0)))
    else:
        db(db.Employee_Master_Leave.id == request.args(0)).update(status_id = 10) # go to accounts department for processing
        redirect(URL('leave_mngt_reports','get_application_leave_report_id', args = request.args(0)))
    
def get_application_leave_report_id():    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    if _id.type_of_leave_id == 1:
        _heading = 'Annual Leave'
        x = 1
    elif _id.type_of_leave_id == 2:
        _heading = 'Compassionate Leave'
        x = 2
    elif _id.type_of_leave_id == 3:
        _heading = 'Sick Leave'
        x = 3
    elif _id.type_of_leave_id == 4:
        _heading = 'Bussiness Leave'
        # _id.update_record(status_id = 11)
        x = 4        
    elif _id.type_of_leave_id == 5:
        _heading = 'Emergency Leave'
        # _id.update_record(status_id = 11)
        x = 5
    elif _id.type_of_leave_id == 6:
        _heading = 'Maternity Leave'
        x = 6
    elif _id.type_of_leave_id == 7:
        _heading = 'Day Off(Excess Hours)'
        x = 7
    elif _id.type_of_leave_id == 8:
        _heading = 'Resignation'
        x = 8        
    elif _id.type_of_leave_id == 9:
        _heading = 'End of Services'
        x = 9        
    _ee = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()
    _row = [
        ['MEMORANDUM'],
        ['Reference No',':',_id.doc_ref_no,'Date',':',_id.updated_on.strftime('%d %B, %Y')],
        ['From',':','Personnel Department'],
        ['To',':',str(_id.employee_id.first_name) + ' ' + str(_id.employee_id.middle_name) + ' ' + str(_id.employee_id.last_name)]]
    _rows = Table(_row, colWidths=[80,20,210,40,20,'*'])
    _rows.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('FONTSIZE',(0,0),(-1,0),15),  
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
        ('SPAN',(0,0),(-1,0)),
        ('ALIGN',(0,0),(-1,1),'LEFT'),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('BOTTOMPADDING',(0,0),(0,0),20),
        ('BOTTOMPADDING',(0,3),(-1,3),10),
        ('LINEBELOW', (0,3), (-1,3), 0.25, colors.black,None, (2,2)),
        ]))        
    row.append(_rows)
    row.append(Spacer(1,1*cm))
    get_type_of_leave_report_id(x)
    doc.build(row)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data   

def get_type_of_leave_report_id(x):
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _ee = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()
    if x == 1: # annual leave
        _row = [        
            ['Subject',':','Applicaton for Annual Leave'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Annual Leave commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+'.'), style=_style) ],
            [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),    
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), 
            ('SPAN',(0,3),(2,3)), 
            ('SPAN',(0,4),(2,4)), 
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,3),(-1,3),20),
            ('TOPPADDING',(0,4),(-1,4),40),
            ]))        
        return row.append(_rows)
    elif x == 2: # compassionate leave
        _row = [        
            ['Subject',':','Applicaton for Compassionate Leave'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Compassionate Leave commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+ ' to ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + '.'), style=_style) ],
            # [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), #
            ('SPAN',(0,3),(2,3)),             
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,2),(-1,2),30),
            ('TOPPADDING',(0,3),(-1,3),40)]))        
        return row.append(_rows)   
    elif x == 3: # sick leave
        _row = [        
            ['Subject',':','Sick Leave'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Sick Leave commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+ ' to ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + '.'), style=_style) ],
            # [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), #
            ('SPAN',(0,3),(2,3)),             
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,2),(-1,2),30),
            ('TOPPADDING',(0,3),(-1,3),40)]))        
        return row.append(_rows)  
    elif x == 4: # business leave
        _row = [        
            ['Subject',':','Applicaton for Business Leave'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Business Leave commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+'.'), style=_style) ],
            [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), 
            ('SPAN',(0,3),(2,3)), 
            ('SPAN',(0,4),(2,4)), 
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,3),(-1,3),20),
            ('TOPPADDING',(0,4),(-1,4),40),
            ]))        
        return row.append(_rows)
    elif x == 5: # emergency leave
        _row = [        
            ['Subject',':','Applicaton for Emergency Leave'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Emergency Leave commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+'.'), style=_style) ],
            [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), 
            ('SPAN',(0,3),(2,3)), 
            ('SPAN',(0,4),(2,4)), 
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,3),(-1,3),20),
            ('TOPPADDING',(0,4),(-1,4),40),
            ]))        
        return row.append(_rows)
    elif x == 6: # maternity leave
        _row = [        
            ['Subject',':','Maternity Leave'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Maternity Leave commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+ ' to ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + '.'), style=_style) ],
            # [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), #
            ('SPAN',(0,3),(2,3)),             
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,2),(-1,2),30),
            ('TOPPADDING',(0,3),(-1,3),40)]))        
        return row.append(_rows)      
    elif x == 7: # day off (excess hours)
        _row = [        
            ['Subject',':','Applicaton for Day Off (Excess Hours)'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Day Off (Excess Hours) commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+ ' to ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + '.'), style=_style) ],
            # [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), #
            ('SPAN',(0,3),(2,3)),             
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,2),(-1,2),30),
            ('TOPPADDING',(0,3),(-1,3),40)]))        
        return row.append(_rows)        

    elif x == 8: # resignation        
        _row = [        
            ['Subject',':','Applicaton for Resignation'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) Resignation commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y') + '.'), style=_style) ],
            # [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), #
            ('SPAN',(0,3),(2,3)),             
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,2),(-1,2),30),
            ('TOPPADDING',(0,3),(-1,3),40)]))        
        return row.append(_rows)        
    elif x == 9: # termination/End of services        
        _row = [        
            ['Subject',':','Applicaton for End of Services'],
            [Paragraph('We are pleased to advise you that your application for leave has been approved and that you have been granted ' + str(locale.format('%.1f',_id.duration_leave or 0, grouping = True)) + ' day(s) End of Services commencing on ' + str(_id.from_effective_date.strftime('%d %B, %Y')+  '.'), style=_style) ],
            # [Paragraph('Accordingly we have made arrangements for your Airline Booking and would advise you that you are required to report back for duty on ' + str(_id.to_effective_date.strftime('%d %B, %Y')) + ' without fail.',style=_style)],
            ['Thank You,'],
            ['PERSONNEL DEPARTMENT']]
            
        _rows = Table(_row, colWidths=[70,20,'*'])
        _rows.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTSIZE',(0,0),(-1,-1),10),     
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),  
            ('SPAN',(0,1),(2,1)), 
            ('SPAN',(0,2),(2,2)), #
            ('SPAN',(0,3),(2,3)),             
            ('ALIGN',(0,0),(-1,1),'LEFT'),
            ('TOPPADDING',(0,1),(-1,2),15),
            ('TOPPADDING',(0,2),(-1,2),30),
            ('TOPPADDING',(0,3),(-1,3),40)]))        
        return row.append(_rows)              

def get_application_leave_account_report_id():
    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _ee = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()
    _ai = db(db.Employee_Master_Account_Info.employee_id == _id.employee_id).select().first()
    _ss = db(db.Leave_Salary_Slip.employee_master_leave_id == request.args(0)).select().first()
    _ea = db(db.Current_Month_Leave_Salary_Slip.employee_master_leave_id == request.args(0)).select().first()
    if _id.employee_id.middle_name == None:
        _middle_name = ''
    else:
        _middle_name = _id.employee_id.middle_name
    _employee_id = str(_id.employee_id.first_name + ' ' + _middle_name + ' ' + _id.employee_id.last_name)
    _row = [
        ['MERCH & PARTNERS WLL'],
        ['P.O. BOX 5511, DOHA, QATAR'],
        ['LEAVE SALARY SLIP FOR THE YEAR ' + str(_id.from_effective_date.strftime('%Y'))],
        ['Voucher No',':',_id.transaction_no,'','Date',':',_id.updated_on.strftime('%d-%b-%Y')],
        ['Employee Name',':',_employee_id,'','Account Code',':',_ee.account_code,],
        ['Engagement Date',':',_ee.date_joined.strftime('%d-%b-%Y'),'','Leave Days/Year',':',T('%s %%{day}',_ee.leave_days_per_year or 0)],
        ['Join Date',':',_ee.last_joining_date.strftime('%d-%b-%Y'),'','Working Days',':',T('%s %%{day}',_id.working_days or 0)],
        ['Leaving Date',':',_id.from_effective_date.strftime('%d-%b-%Y'),'','Entitled Days',':',T('%s %%{day}',_id.entitled_days or 0)]]
    _rows = Table(_row, colWidths=[100,20,'*',20,'*',20,100])
    _rows.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),        
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTSIZE',(0,0),(-1,0),12),  
        ('FONTSIZE',(0,2),(-1,2),10),  
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('SPAN',(0,2),(-1,2)),
        ('ALIGN',(0,0),(-1,2),'CENTER'),
        ('TOPPADDING',(0,2),(-1,2),10),
        ('BOTTOMPADDING',(0,2),(-1,2),10),        
        ('TOPPADDING',(0,0),(-1,1),1),
        ('BOTTOMPADDING',(0,0),(-1,1),1),        
        ('TOPPADDING',(0,3),(-1,-1),1),
        ('BOTTOMPADDING',(0,3),(-1,-1),1),        
        ('VALIGN',(0,0),(-1,-1),'TOP'),                        
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2))]))

    (_whole, _frac) = (locale.format('%d',round(_ss.net_total) or 0, grouping = True), locale.format('%d',round(_ss.net_total) or 0, grouping = True))
    # print _whole, _frac
    if _id.type_of_leave_id == 6:
        _title = 'Maternity Settlement'
        _salary_type = 'Maternity'        
        _others = 'Others'
    elif _id.type_of_leave_id == 8:
        _title = 'Final Settlement'
        _salary_type = 'Leave Salary'
        _others = 'Others/Gratuity'
    elif _id.type_of_leave_id == 9:
        _title = 'Final Settlement'
        _salary_type = 'Leave Salary'
        _others = 'Others/Gratuity'
    else:
        _title = 'Leave Salary Settlement'
        _salary_type = 'Leave Salary'
        _others = 'Others/Gratuity'
    _row2 = [
        [_title.upper()],
        ['','','','Amount QRs.',''],
        ['',_salary_type + str(' (' + T('%s %%{day}',_id.entitled_days or 0) +')'),':',locale.format('%.2F',round(_ss.leave_salary) or 0, grouping = True),''],
        ['','Air Ticket',':',locale.format('%.2F',round(_ss.air_ticket) or 0, grouping = True),''],
        ['','Comm./Bonus',':',locale.format('%.2F',round(_ss.commission_or_bonus) or 0, grouping = True),''],
        ['','Salary Due if any',':',locale.format('%.2F',round(_ss.salary_due) or 0, grouping = True),''],
        ['','Gratuity',':',locale.format('%.2F',round(_ss.gratuity) or 0, grouping = True),''],
        ['','Others',':',locale.format('%.2F',round(_ss.other_payments) or 0, grouping = True),''],
        ['',str(T('%s %%{day}',_id.from_effective_date.day - 1)) +  ' ' + str(_id.from_effective_date.strftime('%B')) + ' Month Salary',':',locale.format('%.2F',round(_ss.month_salary) or 0, grouping = True),''],
        ['','GROSS TOTAL',':',locale.format('%.2F',round(_ss.total_gross) or 0, grouping = True),''],                        
        ['','Less: DEDUCTIONS ',':',locale.format('%.2F',round(_ss.deductions) or 0, grouping = True),''],
        ['','NET TOTAL ',':',locale.format('%.2F',round(_ss.net_total) or 0, grouping = True),''],
        ['','QR ' + string.upper(w.number_to_words(_whole, andword='')) +  ' AND DIRHAMS 00/100 only' ]]
        # ['','QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2]) + '/100 DIRHAMS','']]
    _rows2 = Table(_row2, colWidths=[50,'*',25,'*',50])
    _rows2.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5,colors.Color(0,0,0,0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),        
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('FONTSIZE',(0,0),(-1,0),10),
        ('FONTSIZE',(0,-1),(-1,-1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME',(3,-2),(3,-2), 'Courier-Bold'),
        ('FONTNAME',(3,-4),(3,-4), 'Courier-Bold'),
        ('FONTNAME',(0,0),(-1,0), 'Courier-Bold'),
        ('ALIGN',(2,0),(-1,-1),'RIGHT'),
        # ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, None, None, 2, 2),
        ('LINEABOVE', (1,-2), (3,-2), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (1,-4), (3,-4), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (1,-2), (3,-2), 0.25, colors.black,None, (2,2))
        ]))

    _row3 = [        
        
        ['Cashier','','Accountant','','Received By'], #_employee_id = Paragraph(_id.employee_id.first_name,style=_style2)
        ['(Received all my dues in full up to date.)'],
        ['','','Approved By']

    ]
    _rows3 = Table(_row3, colWidths=['*',15,'*',15,'*'])
    _rows3.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5,colors.Color(0,0,0,0.2)),        
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('FONTSIZE',(0,1),(0,1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME',(0,0),(-1,0), 'Courier-Bold'),
        ('FONTNAME',(0,-1),(-1,-1), 'Courier-Bold'),
        ('VALIGN',(0,1),(-1,-1),'TOP'),                       
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(2,2),(2,2),'CENTER'),
        ('LINEABOVE', (0,0), (0,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (2,0), (2,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (4,0), (4,0), 0.25, colors.black,None, (2,2)),        
        ('LINEABOVE', (2,2), (2,2), 0.25, colors.black,None, (2,2)),
        ('TOPPADDING',(0,1),(-1,1),0),
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('BOTTOMPADDING',(0,1),(-1,1),30),
        ('SPAN',(0,1),(-1,1)),
        ('ALIGN',(0,1),(0,1),'RIGHT'),
        ]))
    
    _row4 = [
        ['Basic Salary:',locale.format('%.2F',round(_ai.basic_income) or 0, grouping = True),'Housing Allowances:',locale.format('%.2F',round(_ai.housing_allowances) or 0, grouping = True),'Car Allowances:',locale.format('%.2F',round(_ai.car_allowances) or 0, grouping = True)],
        ['Petrol Allowances:',locale.format('%.2F',round(_ai.petrol_allowances) or 0, grouping = True),'Food Allowances:',locale.format('%.2F',round(_ai.food_allowances) or 0, grouping = True), 'Others:',locale.format('%.2F',round(_ai.others) or 0, grouping = True)],
        ['Incd/Bonus:',locale.format('%.2F',round(_ai.incentive) or 0, grouping = True), 'Mobile Allowances:',locale.format('%.2F',round(_ai.mobile_allowances) or 0, grouping = True)],        
        ['','','','','GROSS SALARY',locale.format('%.2F',round(_ai.total_gross_pay) or 0, grouping = True)]]

    _rows4 = Table(_row4, colWidths='*')
    _rows4.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5,colors.Color(0,0,0,0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(1,0),(1,-1),'RIGHT'),
        ('ALIGN',(3,0),(3,-1),'RIGHT'),
        ('ALIGN',(5,0),(5,-1),'RIGHT'),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ]))
    
    _row5 = [
        ['Current Month Salary Breakdown'],
        ['Basic Sal.','Housing Alw.','Petrol Alw.','Car Alw.','Food Alw.','Others','Incd/Bonus','Total Amount'],
        [
            locale.format('%.2F',round(_ea.basic_salary) or 0, grouping = True),            
            locale.format('%.2F',round(_ea.housing_allowances) or 0, grouping = True),
            locale.format('%.2F',round(_ea.petrol_allowances) or 0, grouping = True),
            locale.format('%.2F',round(_ea.car_allowances) or 0, grouping = True),
            locale.format('%.2F',round(_ea.food_allowances) or 0, grouping = True),
            locale.format('%.2F',round(_ea.others) or 0, grouping = True),
            locale.format('%.2F',round(_ea.incentive_bonus) or 0, grouping = True),
            locale.format('%.2F',round(_ea.total_gross) or 0, grouping = True)],
        ['Prepared by: ' + str(auth.user.first_name.upper()) + ' ' + str(auth.user.last_name.upper()) + ' ' + str(request.now.strftime('%d%b%Y %I:%M:%S %p')),'','','','','','',''],
        ['Remarks: '+ str(_ss.remarks)]]        

    _rows5 = Table(_row5, colWidths='*')
    _rows5.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5,colors.Color(0,0,0,0.2)),
        ('FONTSIZE',(0,0),(-1,-1),8),
        # ('FONTSIZE',(0,3),(0,3),6),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,2),(-1,2),'RIGHT'),
        ('ALIGN',(7,3),(7,3),'RIGHT'),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,2), (-1,2), 0.25, colors.black,None, (2,2))]))

    row.append(_rows)
    row.append(_rows4)
    row.append(Spacer(1,.5*cm))
    
    row.append(_rows2)
    row.append(Spacer(1,1.2*cm))
    row.append(_rows3)
    row.append(Spacer(1,.1*cm))
    row.append(_rows5)
    # row.append(Spacer(1,.5*cm))
    

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data   

def put_application_hr_returned_id():
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()    
    _pre = db(db.Communication_Tranx_Prefix.prefix_key == 'MEM').select().first()
    _skey = _pre.serial_key
    _skey += 1    
    _usr_f = str(auth.user.first_name.upper())
    _usr_l = str(auth.user.last_name.upper())    
    _ckey = 'MP' + '/' + str(_pre.prefix) + '/' + str(_skey) + '/' + str(date.today().strftime("%Y")) + '/' + _usr_f[:1] + _usr_l[:1]        
    _duration = (_id.date_returned - _id.from_effective_date).days

    db(db.Employee_Master_Leave.id == request.args(0)).update(joining_doc_ref_no = _ckey, status_id = 16, to_effective_date=_id.date_returned,duration_leave=_duration) #, to_effective_date = _id.date_returned) #, joining_application_date = request.now)
    if _id.type_of_leave_id == 1:
        db(db.Employee_Employment_Details.employee_id == _id.employee_id).update(last_joining_date = _id.date_returned)
    else:
        db(db.Employee_Employment_Details.employee_id == _id.employee_id).update(date_last_return = _id.date_returned)
    _pre.update_record(serial_key = _skey)         

def get_joining_report_id():
    
    _id = db(db.Employee_Master_Leave.id == request.args(0)).select().first()
    _ee = db(db.Employee_Employment_Details.employee_id == _id.employee_id).select().first()
    _returned = (_id.date_returned - _id.to_effective_date).days - 1 
    # print _id.date_returned , _returned.days
    if _returned > 0:
        _late = 'late'       
        _msg = T('--- Returned %s %%{day} late. ---') % (abs(_returned))
    else:
        _late = 'early'        
        _msg = T('--- Returned %s %%{day} early. ---') % (abs(_returned))
    if _id.type_of_leave_id == 1:
        _leave = 'annual vacation'
    elif _id.type_of_leave_id == 4:
        _leave = 'bussiness leave'
    elif _id.type_of_leave_id == 5:
        _leave = 'emergency leave'
    elif _id.type_of_leave_id == 6:
        _leave = 'maternity leave'

    _row = [
        ['JOINING REPORT'],
        ['Reference No',':',_id.joining_doc_ref_no,'','','',_id.joining_application_date.strftime('%d %b. %Y')],
        ['The Accountant\nMerch & Partners W.L.L.,\nDoha-Qatar'],
        ['Subject',':',str(_id.employee_id.title) + ' ' + str(_id.employee_id.first_name.upper())+' '+str(_id.employee_id.middle_name.upper())+' '+str(_id.employee_id.last_name.upper()) + str('\n') + str(_ee.designation_code_id.designation_name) + str(' - ') + str(_ee.department_code_id.department_name)],
        [Paragraph('Please note that the above employee has returned to Doha from his/her ' + str(_leave )+ ' and resumed duty on ' + str(_id.date_returned.strftime('%d %b. %Y') + '.') ,style=_style3)],
        [Paragraph('This is for your information and necessary action.',style=_style3)],
        ['GENERAL MANAGEMENT'],
        ['C.C. Pesonnel File'],
        [_msg]]
    _rows = Table(_row, colWidths=[110,20,110,20,110,20,'*'])
    _rows.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('FONTSIZE',(0,0),(-1,0),15),  
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),             
        ('BOTTOMPADDING',(0,0),(0,0),25),
        ('BOTTOMPADDING',(0,1),(-1,1),25),
        ('BOTTOMPADDING',(0,2),(-1,2),25),
        ('BOTTOMPADDING',(0,3),(-1,3),25),
        ('BOTTOMPADDING',(0,4),(-1,4),25),
        ('BOTTOMPADDING',(0,5),(-1,5),50),
        ('BOTTOMPADDING',(0,6),(-1,6),20),
        ('BOTTOMPADDING',(0,7),(-1,7),20),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,4),(-1,4)),
        ('SPAN',(0,5),(-1,5)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('VALIGN',(0,3),(-1,3),'TOP'),
    ]))
    row.append(_rows)
    row.append(Spacer(1,1*cm))    
    doc.build(row)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'        
    return pdf_data       

def get_salary_adjustment_report_id():   
    
    _first = _id = db((db.Salary_Adjustment.id == request.args(0)) & (db.Salary_Adjustment.status_id == 5)).select().first()    
    _last = db((db.Salary_Adjustment.employee_id == _first.employee_id) & (db.Salary_Adjustment.status_id == 5)).select().first()

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

    # print '---', request.args(0)
    for n in db((db.Salary_Adjustment.employee_id == _id.employee_id) & (db.Salary_Adjustment.status_id == 5)).select(orderby = db.Salary_Adjustment.id):        
        if int(request.args(0)) > int(n.id):            
            _last = db((db.Salary_Adjustment.id == n.id) & (db.Salary_Adjustment.status_id == 5)).select().first()            
        else:
            _first = db((db.Salary_Adjustment.id == request.args(0)) & (db.Salary_Adjustment.status_id == 5)).select().first()
    #     print n.id
    # print _last.id, 
    _badj = abs(_first.basic_income - _last.basic_income )
    _hall = abs(_first.housing_allowances - _last.housing_allowances )
    _call = abs(_first.car_allowances - _last.car_allowances)
    _pall = abs(_first.petrol_allowances - _last.petrol_allowances )
    _fall = abs(_first.food_allowances - _last.food_allowances )
    _oall = abs(_first.others - _last.others)
    _iall = abs(_first.incentive - _last.incentive)
    _tgro = abs(_first.total_gross_pay - _last.total_gross_pay)    
        # print 'id: ', n.id, n.basic_income, n.housing_allowances, n.car_allowances, n.petrol_allowances, n.food_allowances, n.others, n.incentive, n.total_gross_pay        
    (_whole, _frac) = (int(_tgro), locale.format('%.2f',_tgro or 0, grouping = True))
    _adjustment = 'QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS ONLY'

    (_whole, _frac) = (int(_first.total_gross_pay), locale.format('%.2f',_first.total_gross_pay or 0, grouping = True))
    _amount_in_words = 'QR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS ONLY'
    _row = [
        ['Ref.: ' + str(_first.doc_ref_no),'',_first.transaction_date.strftime('%d %B, %Y')],
        [str(_last.employee_id.title) + str(_last.employee_id.first_name) + ' ' +str(_last.employee_id.last_name)  ],
        ['Merch Trading Co.W.L.L'],
        ['Doha - Qatar'],
        ['CONFIDENTIAL'],
        ['Subject: Wage Adjustment Advice'],
        [Paragraph('Effective from ' + str(_first.effectivity_date) + ', you will receive a monthly adjustment of QR. ' + str(_tgro) + ' (' + str(_adjustment) + ')  bringing your total monthly wage to QR. ' + str(_first.total_gross_pay) + ' ('+str(_amount_in_words) + '), as per the following details:', style=_style)]
    ]
    _table = Table(_row, colWidths=['*'])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'), 
        ('FONTSIZE',(0,0),(-1,-1),9),   
        ('FONTSIZE',(0,4),(0,4),12),   
        ('SPAN',(0,4),(-1,4)),
        ('SPAN',(0,6),(-1,6)),
        ('TOPPADDING',(0,1),(0,1),30),        
        ('TOPPADDING',(0,2),(-1,3),0),        
        ('TOPPADDING',(0,4),(0,4),20),
        ('TOPPADDING',(0,5),(0,5),20),
        ('TOPPADDING',(0,6),(0,6),10),
        ('BOTTOMPADDING',(0,1),(-1,3),0),
        ('ALIGN',(2,0),(2,0), 'RIGHT'),
        ('ALIGN',(0,4),(0,4), 'CENTER'),

        ]))
    _row = [
        ['Details','Bas.','H/A','C/A','P/A','F/A','O/A','In.','TG'],
        ['Prev.Mth.Wages',_last.basic_income,_last.housing_allowances,_last.car_allowances,_last.petrol_allowances,_last.food_allowances,_last.others,_last.incentive,_last.total_gross_pay],
        ['Current Adj.',_badj,_hall,_call,_pall,_fall,_oall,_iall,_tgro],
        ['New Mth.Wages',_id.basic_income,_id.housing_allowances,_id.car_allowances,_id.petrol_allowances,_id.food_allowances,_id.others,_id.incentive,_id.total_gross_pay]]

        # ['Prev.Mth.Wages',_ac.basic_income,_ac.housing_allowances,_ac.car_allowances,_ac.petrol_allowances,_ac.food_allowances,_ac.others,_ac.incentive,_ac.total_gross_pay],
        # ['Current Adj.',_badj,_hall,_call,_pall,_fall,_oall,_iall,_tgro],
        # ['New Mth.Wages',_id.basic_income,_id.housing_allowances,_id.car_allowances,_id.petrol_allowances,_id.food_allowances,_id.others,_id.incentive,_id.total_gross_pay]]
    _table2 = Table(_row, colWidths=['*',50,50,50,50,50,50,50,50])
    _table2.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'), 
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('ALIGN',(1,1),(-1,-1),'RIGHT'),
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),     
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),     
        ]))
    if _first.adjustment_type == "I":
        _row = [
            ['Note:'],        
            [Paragraph('Also we would like to thank you for all your past efforts, and we hope your progress will continue.',style=_style)],
            ['Your faithfully,'],
            ['GENERAL MANAGEMENT'],
            ['C.C. Accounts Dept. Merch, (for payroll action: ' + str(_ed.account_code) + ')'],
            ['     Personnel File ' + str(_ed.employee_no)],
            ['Note: This is a private issue and strictly confidential, do not discuss with others.'],
            ['Remarks: ' + str(_first.remarks)]]
    else:
        _row = [
            [''],        
            [''],
            ['Your faithfully,'],
            ['GENERAL MANAGEMENT'],
            ['C.C. Accounts Dept. Merch, (for payroll action: ' + str(_ed.account_code) + ')'],
            ['     Personnel File ' + str(_ed.employee_no)],
            ['Note: This is a private issue and strictly confidential, do not discuss with others.'],
            ['Remarks: ' + str(_first.remarks)]]
    _table3 = Table(_row, colWidths=['*'])
    _table3.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'), 
        ('FONTNAME', (0, 3), (-1, 3), 'Courier-Bold'),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,2),(0,2),15),
        ('TOPPADDING',(0,3),(0,3),30),
        ('TOPPADDING',(0,4),(0,4),15),
        ('BOTTOMPADDING',(0,4),(0,4),0),
        ('TOPPADDING',(0,5),(0,5),0),
        ('TOPPADDING',(0,6),(0,6),15),
        ]))
    row.append(_table)
    row.append(Spacer(1,.1*cm))
    row.append(_table2)
    row.append(Spacer(1,.1*cm))
    row.append(_table3)

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

def get_pending_leave_application_report():
    _ctr = 0
    if int(request.args(0)) == 1:
        _query = db((db.Employee_Master_Leave.status_id < 11) & (db.Employee_Master_Leave.canceled == False)).select(db.Employee_Master_Leave.ALL, db.Employee_Employment_Details.ALL, orderby=db.Employee_Employment_Details.department_code_id | ~db.Employee_Master_Leave.id, left = db.Employee_Employment_Details.on(db.Employee_Employment_Details.employee_id == db.Employee_Master_Leave.employee_id))
        _row = [['Pending Leave Applications']]
        _row += [['#','Date','Department','Type of Leave','Date From','Date To','Name','Duration','Status','Action Required']]

    else:
        _query = db((db.Employee_Master_Leave.status_id == 11) & (db.Employee_Master_Leave.canceled == False)).select(db.Employee_Master_Leave.ALL, db.Employee_Employment_Details.ALL, orderby=db.Employee_Employment_Details.department_code_id | ~db.Employee_Master_Leave.id, left = db.Employee_Employment_Details.on(db.Employee_Employment_Details.employee_id == db.Employee_Master_Leave.employee_id))
        _row = [['On-Leave']]
        _row += [['#','Date','Department','Type of Leave','Date From','Date To','Name','Duration','Status','Action Required']]

    for n in _query:
        _ctr+=1
        if int(n.Employee_Master_Leave.status_id) == 2:
            _status = str(n.Employee_Master_Leave.status_id.action_required) + ", " + str(n.Employee_Master_Leave.updated_by.first_name[:1])+str(n.Employee_Master_Leave.updated_by.last_name[:1])
        else:
            _status = n.Employee_Master_Leave.status_id.action_required
        _row.append([ #value[:10] + ('...' if len(value) > 10 else '')
            _ctr,
            n.Employee_Master_Leave.application_date,
            # str(n.Employee_Employment_Details.department_code_id.department_name[:15]) + str('...' if len(str(n.Employee_Employment_Details.department_code_id.department_name)) > 15 else ''),
            Paragraph(n.Employee_Employment_Details.department_code_id.department_name, style=_style2),
            n.Employee_Master_Leave.type_of_leave_id.type_of_leave,
            n.Employee_Master_Leave.from_effective_date,
            n.Employee_Master_Leave.to_effective_date,
            Paragraph(str(n.Employee_Master_Leave.employee_id.first_name.upper()) + ' ' + str(n.Employee_Master_Leave.employee_id.last_name.upper()),style=_style2),
            locale.format('%.1f',n.Employee_Master_Leave.duration_leave or 0, grouping=True),
            n.Employee_Master_Leave.status_id.status,
            Paragraph(_status,style=_style2)
            # str(n.Employee_Master_Leave.status_id.action_required[:15]) + str('...' if len(str(n.Employee_Master_Leave.status_id.action_required)) > 15 else '')
            ])
    _table = Table(_row, colWidths=[20,60,100,'*',60,60,'*',50,80,100])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('SPAN',(0,0),(-1,0)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTSIZE',(0,0),(-1,0),10),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME',(0,1),(-1,1), 'Courier-Bold'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,2), (-1,2), 0.25, colors.black,None, (2,2)),
        ]))
    row.append(_table)
    _landscape.pagesize = landscape(A4)
    _landscape.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data  
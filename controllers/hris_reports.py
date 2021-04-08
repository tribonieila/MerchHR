# ------------------------------------------------------------------------------------------
# -----------------------------  C O R E  H R   S Y S T E M  -------------------------------
# ------------------------------------------------------------------------------------------

# -----------------     R  E  P  O  R  T  S     -----------------
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
from datetime import date, datetime, timedelta
import inflect 
w=inflect.engine()
MaxWidth_Content = 530
styles = getSampleStyleSheet()
styles.leading = 24
styleB = styles["BodyText"]
styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=8, leading = 10)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=.5 * inch,bottomMargin=.5 * inch)#, showBoundary=1)

def get_employee_master_id_print():
    _id = db(db.Employee_Master.id == request.args(0)).select().first()
    _ad = db(db.Employee_Address_Details.employee_id == request.args(0)).select().first()
    _em = db(db.Employee_Employment_Details.employee_id == request.args(0)).select().first()
    _ac = db(db.Employee_Master_Account_Info.employee_id == request.args(0)).select().first()
    _row = [
        ['EMPLOYEE PROFILE REPORT'],
        ['Merch & Partners Co.WLL.'],
        [str(_id.title) + ' ' + str(_id.first_name) + str(_id.middle_name) + str(_id.last_name) + ' ' + str(_em.employee_no),'' ,'','','EMPLOYMENT INFORMATION','',''],
        [str(_ad.street) + str(_ad.town),'','','','Employee No',':', _em.employee_no ],
        [str(_ad.province) + str(_ad.city),'','','','Account Code',':', _em.account_code],
        [str(_ad.country),'','','','Department',':', _em.department_code_id.department_name],
        ['BASIC INFORMATION','','','','Designation',':', _em.designation_code_id.designation_name],
        ['Gender',':', _id.gender,'','Date Joined',':', _em.date_joined],
        ['Telephone No',':', _id.telephone_no,'','Date Last Return', ':',_em.date_last_return],
        ['Mobile No',':', _id.mobile_no,'','Date Last Ticket',':', _em.date_last_ticket],
        ['Email',':', _id.email,'','Date Leave Due',':', _em.date_leave_due],
        ['Marital Status',':', _id.marital_status,'','Proposed Date',':', _em.proposed_date],
        ['Nationality',':', _id.nationality,'','Labor Card Profession',':', _em.labor_card_profession_id],            
        ['PROFESSIONAL INFORMATION','','','','Sector',':', _em.sector],
        ['Education',':','_id.education_qualification','','Sponsors Name No',':', '_em.sponsors_name'],
        ['Passport No',':', _id.passport_no,'','Sponsors Occ',':', _em.sponsors_occ],
        ['Passport Wherabout',':', '_id.passport_wherabout','','ACCOUNTS INFORMATION'],
        ['Passport Date Issued',':', _id.passport_date_issued,'','Basic Income',':', _ac.basic_income],
        ['Passport Date Expiration',':', _id.passport_date_expiration,'','Housing Allowances',':', _ac.housing_allowances],
        ['Date Given',':', _id.date_given,'','Car Allowances',':', _ac.car_allowances],
        ['Issuing Government:',':', _id.issuing_government,'','Petrol Allowances',':', _ac.petrol_allowances],
        ['Place Issued',':', _id.place_issued,'','Food Allowances',':', _ac.food_allowances],
        ['Professional Passport',':', _id.professional_passport,'','Others',':', _ac.others],        
        ['Residence Permit No',':', _id.residence_permit_no,'','Incentive',':', _ac.incentive],
        ['Expiration Date',':', _id.residence_permit_no_expiration_date,'','Total Gross Pay',':', _ac.total_gross_pay],
        ['Labor Card No',':', _id.labor_card_no,'','Bank Transfer',':', _ac.bank_transfer],
        ['Expiration',':', _id.labor_card_no_expiration_date,'','Loan/Advances',':', _ac.loan_or_advances],
        ['Health Card No',':', _id.health_card_no,'','Other Deductions',':', _ac.other_deductions],
        ['Expiration Date',':', _id.health_card_no_expiration_date,'','Absent Deductions',':', _ac.absent_deductions],
        ['Last Job',':', _id.last_job,'','Total Deductions',':', _ac.total_deductions],
        ['Reason',':', _id.reason_leaving_previous_job,'','Net Pay',':', _ac.net_pay],
        ['Previous Salary',':', _id.previous_salary,'','Bank Salary Name',':', _ac.bank_account_name_id.bank_account_name],        
        ['ADDRESS INFORMATION','','','','Bank Account',':', _ac.bank_account_no],
        ['Street',':',str(_ad.local_street) + str(_ad.local_zone_no),'','Bank Account Name',':', _ac.bank_account_name_id.bank_account_name],
        ['Apartment',':',str(_ad.local_property_no) + str(_ad.local_apartment_no),'','Bank Branch',':', _ac.bank_branch],
        ['Landlord',':',_ad.landlord_name,'','IBAN No',':', _ac.bank_iban_no],
        ['OTHERS'],
        ['Religion',':', _id.religion],
        ['Languages',':', str(','.join(_id.languages))],
        ['Birth Place',':', _id.birth_place],
        ['Birth Date',':', _id.birth_date],
        ['Fathers Name',':', _id.fathers_name],        
        ['Emergency Contant Name',':', _id.emergency_contant_name],
        ['Emergency Contact No',':', _id.emergency_contact_no],
        ['Emergency Relationship',':', _id.emergency_relationship],
        ['Next of ken',':', _id.next_of_ken],
        ['Residence No',':', _id.residence_no],
        ['Residence No Date',':', _id.residence_no_date],
        ['Expiration Date',':', _id.residence_no_date_expiration],        
        ['Status',':', _id.employee_status_id.status]]
    _row_table = Table(_row, colWidths = ['*',10,'*',10,'*',10,'*'])
    _row_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(0,-1),12),
        ('FONTSIZE',(0,1),(1,-1),13),
        ('BOTTOMPADDING',(0,1),(-1,1),5),        
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,2),(-1,-1),8),
        ('TOPPADDING',(0,2),(-1,-1),0),
        ('BOTTOMPADDING',(0,2),(-1,-1),0),
        ('LINEBELOW', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('BACKGROUND',(4,2),(-1,2),colors.gray),
        ('BACKGROUND',(0,6),(2,6),colors.gray),
        ('BACKGROUND',(0,13),(2,13),colors.gray),
        ('BACKGROUND',(4,16),(-1,16),colors.gray),
        ('BACKGROUND',(0,32),(2,32),colors.gray)]))

    row.append(_row_table)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def get_cards_report():    
    ctr = 0    
    # _row = []
    if int(request.args(0)) == 1:                
        _row = [['#','Name','Residence Permit','Expiration Date','Status']]    
        for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
            if n.residence_permit_no_expiration_date != None:
                _str = str(n.title) + ' ' + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)            
                _15 = date.today() + timedelta(days = 15)
                _30 = date.today() + timedelta(days = 30)
                if date.today() > n.residence_permit_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.residence_permit_no,n.residence_permit_no_expiration_date.strftime('%d%b%Y'),'Expired'])                
                elif _15 > n.residence_permit_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.residence_permit_no,n.residence_permit_no_expiration_date.strftime('%d%b%Y'),'15 days due'])                
                elif _30 > n.residence_permit_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.residence_permit_no,n.residence_permit_no_expiration_date.strftime('%d%b%Y'),'30 days due'])                
            
        _table = Table(_row, colWidths=[25,'*',90,90,80])
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2))]))
        row.append(_table)
        doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data

    elif int(request.args(0)) == 2:
        _row = [['#','Name','Driver License','Expiration Date','Status']]    
        for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
            if n.driver_license_no_expiration_date != None:
                _str = str(n.title) + ' ' + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)            
                _15 = date.today() + timedelta(days = 15)
                _30 = date.today() + timedelta(days = 30)
                if date.today() > n.driver_license_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.driver_license_no,n.driver_license_no_expiration_date.strftime('%d%b%Y'),'Expired'])                
                elif _15 > n.driver_license_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.driver_license_no,n.driver_license_no_expiration_date.strftime('%d%b%Y'),'15 days due'])                
                elif _30 > n.driver_license_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.driver_license_no,n.driver_license_no_expiration_date.strftime('%d%b%Y'),'30 days due'])                
            
        _table = Table(_row, colWidths=[25,'*',90,90,80])
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2))]))

        row.append(_table)
        doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data

    elif int(request.args(0)) == 3:
        _row = [['#','Name','Passport No','Expiration Date','Status']]    
        for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
            if n.passport_date_expiration != None:
                _str = str(n.title) + ' ' + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)            
                _15 = date.today() + timedelta(days = 15)
                _30 = date.today() + timedelta(days = 30)
                if date.today() > n.passport_date_expiration:
                    ctr += 1
                    _row.append([ctr,_str,n.passport_no,n.passport_date_expiration.strftime('%d%b%Y'),'Expired'])                
                elif _15 > n.passport_date_expiration:
                    ctr += 1
                    _row.append([ctr,_str,n.passport_no,n.passport_date_expiration.strftime('%d%b%Y'),'15 days due'])                
                elif _30 > n.passport_date_expiration:
                    ctr += 1
                    _row.append([ctr,_str,n.passport_no,n.passport_date_expiration.strftime('%d%b%Y'),'30 days due'])                
            
        _table = Table(_row, colWidths=[25,'*',90,90,80])
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2))]))
        row.append(_table)
        doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data
    elif int(request.args(0)) == 4:
        _row = [['#','Name','Health Card No','Expiration Date','Status']]    
        for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
            if n.health_card_no_expiration_date != None:
                _str = str(n.title) + ' ' + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)            
                _15 = date.today() + timedelta(days = 15)
                _30 = date.today() + timedelta(days = 30)
                if date.today() > n.health_card_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.health_card_no,n.health_card_no_expiration_date.strftime('%d%b%Y'),'Expired'])                
                elif _15 > n.health_card_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.health_card_no,n.health_card_no_expiration_date.strftime('%d%b%Y'),'15 days due'])                
                elif _30 > n.health_card_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.health_card_no,n.health_card_no_expiration_date.strftime('%d%b%Y'),'30 days due'])                
            
        _table = Table(_row, colWidths=[25,'*',90,90,80])
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2))]))
        row.append(_table)
        doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data
    elif int(request.args(0)) == 5:
        _row = [['#','Name','Medical Health','Expiration Date','Status']]    
        for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
            if n.medical_health_card_cert_no_expiration_date != None:
                _str = str(n.title) + ' ' + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)            
                _15 = date.today() + timedelta(days = 15)
                _30 = date.today() + timedelta(days = 30)
                if date.today() > n.medical_health_card_cert_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.medical_health_card_cert_no,n.medical_health_card_cert_no_expiration_date.strftime('%d%b%Y'),'Expired'])                
                elif _15 > n.medical_health_card_cert_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.medical_health_card_cert_no,n.medical_health_card_cert_no_expiration_date.strftime('%d%b%Y'),'15 days due'])                
                elif _30 > n.medical_health_card_cert_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.medical_health_card_cert_no,n.medical_health_card_cert_no_expiration_date.strftime('%d%b%Y'),'30 days due'])                
            
        _table = Table(_row, colWidths=[25,'*',90,90,80])
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2))]))
        row.append(_table)
        doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data        
    elif int(request.args(0)) == 6:
        _row = [['#','Name','Labor Card No','Expiration Date','Status']]    
        for n in db(db.Employee_Master.employee_status_id == 1).select(orderby = db.Employee_Master.id):
            if n.labor_card_no_expiration_date != None:
                _str = str(n.title) + ' ' + str(n.first_name) + ' ' + str(n.middle_name) + ' ' + str(n.last_name)            
                _15 = date.today() + timedelta(days = 15)
                _30 = date.today() + timedelta(days = 30)
                if date.today() > n.labor_card_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.labor_card_no,n.labor_card_no_expiration_date.strftime('%d%b%Y'),'Expired'])                
                elif _15 > n.labor_card_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.labor_card_no,n.labor_card_no_expiration_date.strftime('%d%b%Y'),'15 days due'])                
                elif _30 > n.labor_card_no_expiration_date:
                    ctr += 1
                    _row.append([ctr,_str,n.labor_card_no,n.labor_card_no_expiration_date.strftime('%d%b%Y'),'30 days due'])                
            
        _table = Table(_row, colWidths=[25,'*',90,90,80])
        _table.setStyle(TableStyle([
            # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
            ('FONTNAME',(0,0),(-1,-1), 'Courier'),     
            ('FONTSIZE',(0,0),(-1,-1),9),
            ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
            ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2))]))

        row.append(_table)
        doc.build(row)
        pdf_data = open(tmpfilename,"rb").read()
        os.unlink(tmpfilename)
        response.headers['Content-Type']='application/pdf'    
        return pdf_data     

    

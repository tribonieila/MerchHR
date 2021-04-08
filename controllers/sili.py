@auth.requires_login()
def get_admin_grid():
    grid = SQLFORM.smartgrid(db.Employee_Master, fields=[db.Employee_Master.first_name, db.Employee_Master.last_name], linked_tables=['Employee_Employment_Details','Employee_Master_Account_Info'])
    return dict(grid = grid)

def generate():
    db(db.Employee_Master_Leave.id == 7459).update(status_id = 11)
    return dict()

def generate_image_():
    str = "this is string example....wow!!! this is really string"
    # print str.replace("is", "was")
    # print str.replace("is", "was", 1)
    for n in db((db.Employee_Master.medical_health_card_cert_no_image != None) | (db.Employee_Master.medical_health_card_cert_no_image != "")).select():
        str = n.passport_image
        # print n.passport_image
        # _replace = str.replace('no_table','Employee_Master')
        n.update_record(medical_health_card_cert_no_image = str.replace('no_table','Employee_Master'))
        # print n.passport_image
    return dict()

def generate_image():
    for n in db(db.Salary_Adjustment.id >= 1194).select():
        _now = request.now
        # if n.effectivity_date <= _now.date():            
            # update here the db.Employee_Master_Account_Info.ALL
        db(db.Employee_Master_Account_Info.employee_id == n.employee_id).update(
            basic_income = n.basic_income,
            housing_allowances = n.housing_allowances,
            car_allowances = n.car_allowances,
            petrol_allowances = n.petrol_allowances,
            food_allowances = n.food_allowances,                
            others = n.others,
            incentive = n.incentive,
            mobile_allowances = n.mobile_allowances,
            total_gross_pay = n.total_gross_pay,
            net_pay = n.total_gross_pay
        )
        # n.update_record(status_id = 5)
    return dict()
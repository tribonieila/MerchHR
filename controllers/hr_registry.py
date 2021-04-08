# ------------------------------------------------------------------------------------------
# -----------------------------  H R  R E G I S T Y   S Y S T E M  -------------------------
# ------------------------------------------------------------------------------------------

def get_hr_registry_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Name'),TH('Hours'),TH('Noted By:'),TH('Remarks'),TH('Action')))
    for n in db().select(db.HR_Registry.ALL, orderby = db.HR_Registry.id):
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = (URL('leave_mngt','put_leave_status_id', args = n.id))) 
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.registry_date),TD(n.employee_id.first_name,' ',n.employee_id.last_name),TD(n.hours),TD(n.noted_by.first_name,' ',n.noted_by.last_name),TD(n.remarks),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    form = SQLFORM(db.HR_Registry)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        print form.errors
    return dict(form = form, table = table)
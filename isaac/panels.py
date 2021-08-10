from flask import (flash, redirect, request, url_for)
from isaac.models import Record, Secrets, Public_update
from isaac import app, db
from config import Config
import csv


conf = Config()

# ==============================
# Admin/public panel actions 
# ==============================
@app.route('/admin_edit', methods = ['POST','GET'])
def admin_edit():
    q = Record.query.all()
    if request.method == 'POST':
        req = request.form
        access_admin = Secrets.query.filter(Secrets.key == req.get("secret_password")).first()
        if access_admin is not None:
            for record in q:
                curr = req.get(f"{record.name}_current")
                best = req.get(f"{record.name}_best")
                cat =  req.get(f"{record.name}_category")

                if int(curr) < 10000:
                    record.current = curr
                if int(best) < 10000:
                    record.best = best
                if cat in conf.CATEGORIES:
                    record.category = cat
            db.session.commit()
            flash("success")
        else:
            flash("access denied")

    return (redirect(url_for("admin_panel")))


@app.route('/public_edit', methods = ['POST','GET'])
def public_edit():
    q = Record.query.all()
    if request.method == 'POST':
        req = request.form
        for record in q:
            # if ((req.get(f"{record.name}_current") != record.current)
            #     or (req.get(f"{record.name}_best") != record.best)
            #     or (req.get(f"{record.name}_category") != record.category)):

            if req.get(f"{record.name}_category") in conf.CATEGORIES and req.get(f"{record.name}_category") != record.category:
                log_user_input(record.category,req.get(f"{record.name}_category"), "category",req.get(f"{record.name}") )
                Public_update.add_update(
                    old_value=record.category,
                    new_value=req.get(f"{record.name}_category"),
                    val_type="category",
                    channel_name=req.get(f"{record.name}"))
            if req.get(f"{record.name}_current") != record.current:
                log_user_input(record.current,req.get(f"{record.name}_current"), "current", req.get(f"{record.name}"))
                Public_update.add_update(
                    old_value=record.current,
                    new_value=req.get(f"{record.name}_current"),
                    val_type="current",
                    channel_name=req.get(f"{record.name}"))
            if req.get(f"{record.name}_best") != record.best:
                log_user_input(record.best,req.get(f"{record.name}_best"), "best", req.get(f"{record.name}"))
                Public_update.add_update(
                    old_value=record.best,
                    new_value=req.get(f"{record.name}_best"),
                    val_type="best",
                    channel_name=req.get(f"{record.name}"))


        flash("success")

    return (redirect(url_for("public_panel")))

@app.route('/public_edit_done/<id>', methods = ['POST','GET'])
def public_edit_done(id):
    pub_edit = Public_update.query.filter(Public_update.id == id).first()
    if pub_edit is not None:
        pub_edit.is_active = "False"
        db.session.commit()
    else:
        flash("err")

    return (redirect(url_for("admin_panel")))





def log_user_input(old_value, new_value, val_type, channel_name):
    with open(f'{conf.PUBLIC_UPDATE}','a', newline='') as csv_file:
        write_csv = csv.writer(csv_file,  delimiter=',')
        write_csv.writerow([request.remote_addr,
                            request.form.get("nickname"),
                            channel_name,
                            f"{old_value} -> {new_value}",
                            val_type])
        csv_file.close()


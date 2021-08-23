from flask import (flash, redirect, request, url_for)
from isaac.models import Record, Secrets
from isaac import app, db
from config import Config


conf = Config()

# ==============================
# Admin panel actions 
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


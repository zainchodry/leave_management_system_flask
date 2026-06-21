from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required
)

from app.models import (
    Department
)

from app.forms import (
    DepartmentForm,
    UpdateDepartmentForm
)

from app.utils.decorators import (
    admin_required
)
from app.extensions import db

department_bp = Blueprint(
    "department",
    __name__
)

@department_bp.route(
    "/departments/create",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def create_department():

    form = DepartmentForm()

    if form.validate_on_submit():

        department = Department(

            name=form.name.data,

            description=form.description.data,

            head_id=form.head_id.data
        )

        db.session.add(
            department
        )

        db.session.commit()

        flash(
            "Department Created",
            "success"
        )

        return redirect(
            url_for(
                "department.departments"
            )
        )

    return render_template(
        "departments/create.html",
        form=form
    )

@department_bp.route(
    "/departments"
)
@login_required
def departments():

    departments = Department.query.all()

    return render_template(
        "departments/list.html",
        departments=departments
    )

@department_bp.route(
    "/departments/update/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def update_department(id):

    department = Department.query.get_or_404(
        id
    )

    form = UpdateDepartmentForm(
        obj=department
    )

    if form.validate_on_submit():

        department.name = form.name.data

        department.description = (
            form.description.data
        )

        department.head_id = (
            form.head_id.data
        )

        db.session.commit()

        flash(
            "Department Updated",
            "success"
        )

        return redirect(
            url_for(
                "department.departments"
            )
        )

    return render_template(
        "departments/update.html",
        form=form
    )

@department_bp.route(
    "/departments/delete/<int:id>"
)
@login_required
@admin_required
def delete_department(id):

    department = Department.query.get_or_404(
        id
    )

    db.session.delete(
        department
    )

    db.session.commit()

    flash(
        "Department Deleted",
        "success"
    )

    return redirect(
        url_for(
            "department.departments"
        )
    )

from flask import render_template, request, redirect, url_for, abort, flash, current_app
from flask import Blueprint
from flask_login import current_user, login_user,logout_user, login_required
from .forms import TaskForm, DateSelectorForm
from .models import Task
from app.extensions import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def index():
    return render_template('home.html')

@views.route('/select-date', methods=['GET', 'POST'])
def select_date():
    form = DateSelectorForm()
    if form.validate_on_submit():
        selected_date = form.due_date.data.isoformat()
        return redirect(url_for("views.create_task", date=selected_date, title='Create task'))
    return render_template('select-date.html', form=form)


@views.route('/task/new', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()

    if form.validate_on_submit():
        selected_date = request.args.get('date')
        due_date = datetime.fromisoformat(selected_date).date()

        new_start = form.start_time.data
        new_end = form.finish_time.data

        overlapping = Task.query.filter_by(user_id=current_user.id, due_date=due_date).filter(
            db.or_(
                db.and_(Task.start_time <= new_start, Task.finish_time > new_start),
                db.and_(Task.start_time < new_end, Task.finish_time >= new_end),
                db.and_(Task.start_time >= new_start, Task.finish_time <= new_end)
            )
        ).first()

        if overlapping:
            flash("There is already a task scheduled during that time range.", "danger")
            return redirect(url_for("views.create_task", date=selected_date))

        new_task = Task(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            due_date=due_date,
            start_time=new_start,
            finish_time=new_end,
            completed=False
        )
        db.session.add(new_task)
        db.session.commit()

        flash("Task created successfully.", "success")
        return redirect(url_for('views.tasks'))

    return render_template('create_task.html', form=form, selected_date=request.args.get('date'))


@views.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    page = request.args.get("page", 1, type=int)
    sort = request.args.get("sort", "recent")

    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    for task in all_tasks:
        task.overdue = task.is_overdue()
    db.session.commit()

    query = Task.query.filter_by(user_id=current_user.id)

    if sort == "recent":
        query = query.order_by(Task.created_at.desc())
    elif sort == "due":
        query = query.order_by(Task.due_date.asc(), Task.start_time.asc())

    pagination = query.order_by(Task.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config["TASKS_PER_PAGE"],
        error_out=False
    )
    return render_template("tasks.html", tasks=pagination.items, pagination=pagination, title="Tasks")

@views.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def task(id):
    task = Task.query.get_or_404(id)
    return render_template('task.html', task=task)

@views.route('/task/delete/<int:id>', methods=['GET', 'POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    flash('Task deleted', 'info')
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('views.tasks'))
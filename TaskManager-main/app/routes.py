from flask import (
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    jsonify
)
from app import db
from app.models import Task, TaskPriority
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf.csrf import CSRFProtect

def init_routes(app):
    @app.route('/')
    def index():
        try:
            # Fetch tasks with smart sorting
            tasks = Task.query.order_by(
                Task.completed.asc(),  # Incomplete tasks first
                Task.due_date.asc(),   # Then by due date
                Task.created_at.desc() # Most recent tasks last
            ).all()
            
            # Calculate task statistics
            total_tasks = len(tasks)
            completed_tasks = len([task for task in tasks if task.completed])
            
            return render_template(
                'index.html', 
                tasks=tasks,
                total_tasks=total_tasks,
                completed_tasks=completed_tasks
            )
        
        except SQLAlchemyError as e:
            # Log the error for debugging
            app.logger.error(f"Database error: {str(e)}")
            flash("An error occurred while fetching tasks.", "error")
            return render_template('index.html', tasks=[])

    @app.route('/add_task', methods=['POST'])
    def add_task():
        try:
            # Extract form data
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip() or None
            due_date_str = request.form.get('due_date')
            priority = request.form.get('priority', 'MEDIUM')

            # Validate required fields
            if not name:
                flash('Task name is required!', 'error')
                return redirect(url_for('index'))

            # Parse due date
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                except ValueError:
                    flash('Invalid date format', 'error')
                    return redirect(url_for('index'))

            # Create new task
            new_task = Task(
                name=name,
                description=description,
                due_date=due_date,
                priority=priority,
                completed=False
            )

            db.session.add(new_task)
            db.session.commit()
            
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))

        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Error adding task: {str(e)}")
            flash('Error adding task. Please try again.', 'error')
            return redirect(url_for('index'))

    @app.route('/edit_task/<int:task_id>', methods=['POST'])
    def edit_task(task_id):
        try:
            task = Task.query.get_or_404(task_id)

            # Update task fields
            task.name = request.form.get('name', task.name).strip()
            task.description = request.form.get('description', task.description).strip() or None
            task.priority = request.form.get('priority', task.priority)

            # Update due date if provided
            due_date_str = request.form.get('due_date')
            if due_date_str:
                try:
                    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                except ValueError:
                    flash('Invalid date format', 'error')
                    return redirect(url_for('index'))

            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))

        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Error editing task: {str(e)}")
            flash('Error updating task. Please try again.', 'error')
            return redirect(url_for('index'))

    @app.route('/delete_task/<int:task_id>', methods=['POST'])
    def delete_task(task_id):
        try:
            task = Task.query.get_or_404(task_id)
            db.session.delete(task)
            db.session.commit()
            
            flash('Task deleted successfully!', 'success')
            return redirect(url_for('index'))

        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Error deleting task: {str(e)}")
            flash('Error deleting task. Please try again.', 'error')
            return redirect(url_for('index'))

    @app.route('/complete_task/<int:task_id>', methods=['POST'])
    def complete_task(task_id):
        try:
            task = Task.query.get_or_404(task_id)
            task.completed = not task.completed
            db.session.commit()
            
            status = "completed" if task.completed else "marked as incomplete"
            flash(f'Task {status} successfully!', 'success')
            return redirect(url_for('index'))

        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Error updating task status: {str(e)}")
            flash('Error updating task status. Please try again.', 'error')
            return redirect(url_for('index'))

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app


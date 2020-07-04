from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False,)
    dev_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(400), nullable=True)
    activation_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    projects = db.relationship(
        'Project', backref=db.backref('User', lazy=True), lazy=True)
    ideas = db.relationship(
        'Idea', backref=db.backref('User', lazy=True), lazy=True)
    tasks = db.relationship(
        'Task', backref=db.backref('User', lazy=True), lazy=True)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    picture = db.Column(db.String(400), nullable=False)
    github_link = db.Column(db.String(255), nullable=True)
    is_completed = db.Column(db.Boolean, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    tasks = db.relationship('Task', cascade='all, delete-orphan', backref=db.backref(
        'project', lazy=True), lazy=True)


class Idea(db.Model):
    __tablename__ = 'ideas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    premise = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)
    edits = db.relationship('EditIdea', cascade='all, delete-orphan',
                            backref=db.backref('Idea', lazy=True), lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=0)
    created_at = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)


class EditIdea(db.Model):
    __tablename__ = 'edit_ideas'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey('ideas.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now)


class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reset_token = db.Column(db.Text, nullable=False)
    time_expiry = db.Column(db.DateTime, nullable=False)

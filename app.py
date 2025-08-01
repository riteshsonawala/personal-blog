import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import bleach
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

    @property
    def content_html(self):
        # Convert markdown to HTML and sanitize
        html = markdown.markdown(self.content, extensions=['codehilite', 'fenced_code'])
        return bleach.clean(html, tags=[
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'a', 'code', 'pre', 'blockquote'
        ], attributes={'a': ['href', 'title'], 'code': ['class']})

# Forms
class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()],
                            render_kw={"rows": 15, "placeholder": "Write your blog post content here... (Markdown supported)"})
    submit = SubmitField('Publish Post')

# Routes
@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:id>')
def post_detail(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('post_detail.html', post=post)

@app.route('/write', methods=['GET', 'POST'])
def write_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your blog post has been published!', 'success')
        return redirect(url_for('post_detail', id=post.id))
    return render_template('write_post.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Your blog post has been updated!', 'success')
        return redirect(url_for('post_detail', id=post.id))
    return render_template('edit_post.html', form=form, post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Your blog post has been deleted!', 'info')
    return redirect(url_for('index'))

# Create tables
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
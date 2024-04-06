from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def valid_name(self, key, name):
        if not len(name):
            raise ValueError('Must supply a name')
        is_duplicate = Author.query.filter_by(name=name).first()
        if is_duplicate:
            raise ValueError('Author name must be unique')
        return name

    @validates('phone_number')
    def valid_phone(self, key, number):
        if len(str(number)) != 10 or not int(number):
            raise ValueError('Phone number must be exactly 10 digits')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def valid_title(self, key, title):
        required_title_words = ["Won't Believe", "Secret", "Top", "Guess"]
        title_is_valid = False
        for word in required_title_words:
            if word in title:
                title_is_valid = True
        if not title_is_valid:
            raise ValueError('Title must contain clickbait keywords!')
        return title
    
    @validates('content')
    def valid_post_length(self, key, content):
        if len(content) < 250:
            raise ValueError('Post length must be greater than 250 characters.')
        return content

    @validates('summary')
    def valid_summary_length(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be less than 250 characters')
        return summary

    @validates('category')
    def valid_category(self, key, cat):
        valid_cat_list = ['Fiction', 'Non-Fiction']
        if not cat in valid_cat_list:
            raise ValueError('Category is not valid.')
        return cat

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

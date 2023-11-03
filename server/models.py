from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Validation and constraints
    __table_args__ = (
        UniqueConstraint('name', name='unique_author_name'),
        CheckConstraint("length(phone_number) = 10 OR phone_number IS NULL", name='valid_phone_number_length'),
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name is required.")
        return name

    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number is not None:
            phone_number = phone_number.strip()  # Remove any whitespace
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise ValueError("Phone number must be exactly ten digits.")
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    category = Column(String)
    summary = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Add a custom validator for the title
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post title is required.")
        
        # Check if the title contains clickbait keywords
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        for keyword in clickbait_keywords:
            if keyword in title:
                return title
        
        # If none of the keywords are found, raise a validation error
        raise ValueError("Post title should contain at least one clickbait keyword: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")

    # Validation and constraints for content, summary, and category
    __table_args__ = (
        CheckConstraint("char_length(content) >= 250", name='content_length_constraint'),
        CheckConstraint("char_length(summary) <= 250", name='summary_length_constraint'),
        CheckConstraint("category IN ('Fiction', 'Non-Fiction')", name='valid_category_constraint')
    )

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError('Summary must be at most 250 characters long.')
        return summary
    
    @validates('category')
    def validate_category(self,key,category):
        if category not in ["Fiction",'Non-Fiction']:
            raise ValueError('Must be either Fiction or Non Fiction')
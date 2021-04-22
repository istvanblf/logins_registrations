from django.db import models
import bcrypt
import re
from datetime import datetime

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
    # Test names and related errors
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"
    # Test Email address and related errors
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        else:
            user_list = User.objects.filter(email = post_data['email'])
            if len(user_list) > 0:
                errors['email'] = "Email already in use"        
    # Test birthday date and related errors
        if len(post_data['birth_date']) < 1 :
            errors['birth_date'] = "You need to enter a bday!!!"
        else: 
            form_date = datetime.strptime(post_data['birth_date'], "%Y-%m-%d")
            if datetime.now() < form_date:
                errors['birth_date'] = "Future dates aren't accepted"
            elif datetime.now().year - form_date.year < 13:
                errors['birth_date'] = "You must be older than 13 to register"
    # Test password and related errors
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 4 characters!"

        if (post_data['password'] != post_data['confirm_password']):
            errors['password'] = "Passwords must match"

        return errors


    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email = post_data['email'])
    # Test login credentials
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid Credentials"
        else: 
            errors['email'] = "Invalid Credentials"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 55)
    last_name = models.CharField(max_length = 55)
    email = models.CharField(max_length = 75)
    password = models.CharField(max_length = 100)
    birth_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
1
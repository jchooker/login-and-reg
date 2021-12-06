import bcrypt, re
from django.db import models

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors={}
        if len(postData['first_name']) < 2:
            errors['first_name_min'] = "First name must be longer than 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name_min'] = "Last name must be longer than 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email_format'] = "Invalid email address!"
        if len(postData['pw']) < 8:
            errors['pw_length'] = "Password must be longer than 8 characters"
        if postData['pw'] != postData['pw_conf']:
            errors['conf_match'] = "Password and Confirmation must match!"
        return errors
    def login_validator(self, postData):
        errors={}
        user_test = User.objects.filter(email=postData['email2'])
        if user_test:
            if not bcrypt.checkpw(postData['pw2'].encode(), user_test[0].pw.encode()):
                errors['bad_pw_match'] = "Bad email-password combination"
        else:
            errors['no_such_user'] = "Bad email-password combination"
        return errors

            
# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email=models.EmailField()
    pw=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
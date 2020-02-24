from django.db import models
import bcrypt, datetime

class user_manager(models.Manager):
    def basic_validator(self, postData):
        userMatch = User.objects.filter (username = postData['username'])
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "Username should be at least 3 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['confirm_pw'] != postData['password']:
            errors["confirm_pw"] = "Passwords do not match"
        if len(userMatch) > 0:
            errors['userTaken'] = "Username has already been taken"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['username'] = "Username required to login"
        userMatch = User.objects.filter (username = postData['username'])
        if len(userMatch) == 0:
            errors['null'] = "Username could not be found, register new username"
        else:
            user = userMatch[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password matches")
            else:
                errors['pwmatch'] = "Wrong Password"
        return errors

    def Trip_validator(self, postData):
        errors = {}
        current = datetime.date.today()
        if len(postData['destination']) < 1:
            errors['dest'] = "Need a destination"
        if len(postData['desc']) < 1:
            errors['desc'] = "Need a description"
        if postData['date_from'] < str(current):
            errors['date_from'] = "Plan a Trip for the future! not the past!"
        if postData['date_to'] < postData['date_from']:
            errors['date_to'] = "You can't come back in the past! or are you a time traveler?"
        return errors


class User(models.Model):
    name = models.CharField(max_length = 45)
    username = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    confirm_pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = user_manager()

class Trip(models.Model):
    creator = models.ForeignKey(User, related_name = "trips", on_delete=models.CASCADE)
    travelers = models.ManyToManyField(User, related_name = "travels")
    destination = models.CharField(max_length = 45)
    desc = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = user_manager()
    
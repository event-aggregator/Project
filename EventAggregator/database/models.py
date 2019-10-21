from django.db import models


class UserManager(models.Manager):

    def validator(self, postData):
        errors = {}
        if postData['first_name'].isalpha() is False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name can not be shorter than 2 characters"

        if postData['last_name'].isalpha() is False:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors


class Areas(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Languages(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Cities(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Events(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    languages = models.ManyToManyField(Languages)
    areas = models.ManyToManyField(Areas)
    cities = models.ManyToManyField(Cities)


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=200)
    languages = models.ManyToManyField(Languages)
    areas = models.ManyToManyField(Areas)
    cities = models.ManyToManyField(Cities)
    objects = UserManager()


class ClientEvents(models.Model):
    user_email = models.ForeignKey(Client, on_delete=models.CASCADE)
    events_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    status = models.BooleanField()





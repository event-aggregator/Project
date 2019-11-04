from django.db import models


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
    # languages = models.ManyToManyField(Languages, related_name='ClientLanguages')
    # areas = models.ManyToManyField(Areas, related_name='ClientAreas')
    # cities = models.ManyToManyField(Cities, related_name='ClientCities')


class ClientEvents(models.Model):
    user_email = models.ForeignKey(Client, on_delete=models.CASCADE)
    events_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    status = models.BooleanField()

class ClientCities(models.Model):
    user_email = models.ForeignKey(Client, on_delete=models.CASCADE)
    city_name = models.ForeignKey(Cities, on_delete=models.CASCADE)


class ClientLanguages(models.Model):
    user_email = models.ForeignKey(Client, on_delete=models.CASCADE)
    language_name = models.ForeignKey(Languages, on_delete=models.CASCADE)


class ClientAreas(models.Model):
    user_email = models.ForeignKey(Client, on_delete=models.CASCADE)
    area_name = models.ForeignKey(Areas, on_delete=models.CASCADE)




from djongo import models

class Collection(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Title = models.CharField(max_length=200)
    Company = models.CharField(max_length=200)
    Experience = models.CharField(max_length=100)
    Salary = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    URL = models.URLField()
    Skills = models.TextField()

    def __str__(self):
        return self.Title
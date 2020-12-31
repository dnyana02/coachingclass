from django.db import models

# Create your models here.
class Contact(models.Model):
     YCLASS = (
        ('5th','5th'),
        ('6th','6th'),
        ('7th','7th'),
        ('8th','8th'),
        ('9th','9th'),
        ('10th','10th'),
    )
     sno = models.AutoField(primary_key=True)
     name = models.CharField(max_length=255)
     phone = models.CharField(max_length=13)
     yclass = models.CharField(max_length=200, null=True, choices = YCLASS)
     email = models.CharField(max_length=100)
     content = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True,blank=True)

     def __str__(self):
        return 'message from  ' + self.name + '   -' + self.email


class teacher(models.Model):
    name = models.CharField(max_length=200, null=True)
    education = models.CharField(max_length=200, null=True)
    subject = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class testinomial(models.Model):
    name = models.CharField(max_length=200, null=True)
    result = models.CharField(max_length=200, null=True)
    achive = models.CharField(max_length=200, null=True)
    test_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    written = models.CharField(max_length=200,null=True)
    data_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)

class resultslider(models.Model):
    yr = models.CharField(max_length=200, null=True)
    result_pic = models.ImageField(default="profile1.png", null=True, blank=True)


    def __str__(self):
        return str(self.yr)


class Student(models.Model):
     YCLASS = (
        ('5th','5th'),
        ('6th','6th'),
        ('7th','7th'),
        ('8th','8th'),
        ('9th','9th'),
        ('10th','10th'),
    )
     sno = models.AutoField(primary_key=True)
     name = models.CharField(max_length=255)
     phone = models.CharField(max_length=13)
     Yclass = models.CharField(max_length=200, null=True, choices = YCLASS)
     email = models.CharField(max_length=100)
     feespaid = models.FloatField(null = True)
     remainingfees = models.FloatField(null = True)
     timestamp = models.DateTimeField(auto_now_add=True,blank=True)

     def __str__(self):
        return str(self.name)

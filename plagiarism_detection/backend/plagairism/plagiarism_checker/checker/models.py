from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PlagiarismResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    similarity_score = models.FloatField()
    compared_with = models.TextField()
    checked_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
# class Document:
#     pass


# class PlagiarismResult:
#     pass


class RegiModel(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField()
    contact=models.IntegerField()
    password=models.CharField(max_length=50)
    option1='Student'
    option2='Teacher'
   
    CHOICES=[
        (option1,'Student'),
        (option2,'Teacher')
       
    ]
    role=models.CharField(max_length=20,choices=CHOICES,default=option1)    
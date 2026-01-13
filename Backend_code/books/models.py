from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    cover_image = models.ImageField(upload_to='covers/')
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

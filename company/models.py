from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="company_images")
    website = models.URLField()
    email = models.EmailField()
    contact = models.IntegerField() # requires validation 
    
    def __str__(self):
        return f"Company: {self.name}"
    
    class Meta:
        verbose_name_plural = "Companies"
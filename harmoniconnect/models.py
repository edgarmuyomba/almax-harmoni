from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.IntegerField()
    description = models.TextField()
    cover_image = models.ImageField(upload_to="cover_images")
    source_company = models.ForeignKey("company.Company", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Event: {self.name}"

class Booking(models.Model):
    client = models.ForeignKey("users.Client", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.event} by {self.client}"
    
class Review(models.Model):
    client = models.ForeignKey("users.Client", on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey("harmoniconnect.Event", on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.client}, review: {self.text[:50]}..."
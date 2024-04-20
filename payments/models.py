from django.db import models

class PaymentMethod(models.Model):
    METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]
    method = models.CharField(max_length=50, choices=METHODS)
    name_on_card = models.CharField(max_length=255) # requires validation
    card_number = models.IntegerField(blank=True, null=True) # requires validation
    csv = models.IntegerField(blank=True, null=True)
    contact = models.IntegerField() # requires validation
    email = models.EmailField()
    
    def __str__(self) -> str:
        return f"Payment Method: {self.method}"

class PaymentRecord(models.Model):
    STATUS = [
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]
    client = models.ForeignKey("users.Client", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS)
    amount = models.IntegerField() # requires validation
    event = models.ForeignKey("harmoniconnect.Event", on_delete=models.SET_NULL, null=True, blank=True)
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} on {self.date} "
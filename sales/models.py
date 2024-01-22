from django.db import models
from inventory.models import Product
from centers.models import center  # Assuming the center model is in the centers app

class Customer(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    center = models.ForeignKey(center, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.PositiveIntegerField()
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_of_sale = models.DateField()

    def __str__(self):
        return f"Sale {self.sale_id} to {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = self.quantity_sold * self.unit_selling_price
        super(Sale, self).save(*args, **kwargs)

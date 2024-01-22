from django.db import models
from inventory.models import RawMaterial
import datetime


class Supplier(models.Model):
    code = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code(prefix='S', length=5)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code(prefix, length):
        last_item = Supplier.objects.all().order_by('code').last()
        if not last_item:
            return prefix + '00001'
        last_code = last_item.code
        last_code_int = int(last_code.replace(prefix, ''))
        new_code_int = last_code_int + 1
        new_code = prefix + str(new_code_int).zfill(length)
        return new_code


class Purchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    purchase_code = models.CharField(max_length=20, primary_key=True, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    date_of_purchase = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    payment_details = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Purchase {self.purchase_code} - {self.raw_material.designation}"

    def save(self, *args, **kwargs):
        # Automatically set the total amount on save
        self.total_amount = self.quantity * self.unit_price

        if not self.purchase_code:
            # Generate a new purchase_code
            last_purchase = Purchase.objects.all().order_by('purchase_code').last()
            last_id = int(last_purchase.purchase_code[2:]) if last_purchase else 0
            self.purchase_code = f'PO{str(last_id + 1).zfill(6)}'

        super(Purchase, self).save(*args, **kwargs)

        # Update the supplier's balance
        self.supplier.balance += self.total_amount
        self.supplier.save()
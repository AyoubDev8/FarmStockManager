from django.db import models
from inventory.models import RawMaterial
from centers.models import center  # Assuming this is where Center is defined

class MaterialTransfer(models.Model):
    TRANSFER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    transfer_id = models.AutoField(primary_key=True)
    center = models.ForeignKey(center, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity_transferred = models.PositiveIntegerField()
    date_of_transfer = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Transfer {self.transfer_id} to {self.center.designation} - Status: {self.status}"

from django.db import models
from centers.models import center


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'



class Product(models.Model):
    code = models.CharField(max_length=20, primary_key=True, editable=False)
    designation = models.CharField(max_length=255)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    center = models.ForeignKey(center, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.designation
    
    class Meta:
        ordering = ['designation']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code(prefix='P', length=5)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code(prefix, length):
        last_item = Product.objects.all().order_by('code').last()
        if not last_item:
            return prefix + '00001'
        last_code = last_item.code
        last_code_int = int(last_code.replace(prefix, ''))
        new_code_int = last_code_int + 1
        new_code = prefix + str(new_code_int).zfill(length)
        return new_code

class RawMaterial(models.Model):
    code = models.CharField(max_length=20, primary_key=True, editable=False)
    designation = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey('purchases.Supplier', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.designation
    
    class Meta:
        ordering = ['designation']
        verbose_name = 'Raw Material'
        verbose_name_plural = 'Raw Materials'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code(prefix='RM', length=5)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code(prefix, length):
        last_item = RawMaterial.objects.all().order_by('code').last()
        if not last_item:
            return prefix + '00001'
        last_code = last_item.code
        last_code_int = int(last_code.replace(prefix, ''))
        new_code_int = last_code_int + 1
        new_code = prefix + str(new_code_int).zfill(length)
        return new_code













class RawMaterialInventory(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    center = models.ForeignKey(center, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.raw_material.designation} at {self.center.designation}"

class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    center = models.ForeignKey(center, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.designation} at {self.center.designation}"

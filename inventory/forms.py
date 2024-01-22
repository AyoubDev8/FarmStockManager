from django import forms
from .models import RawMaterial, RawMaterialInventory, Product, ProductInventory
from centers.models import center

class RawMaterialForm(forms.ModelForm):
    quantity_in_stock = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Quantity in Stock',
        initial=0
    )
    center = forms.ModelChoiceField(
        queryset=center.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='center',
        required=True
    )

    class Meta:
        model = RawMaterial
        fields = ['designation', 'purchase_price', 'supplier', 'category', 'center']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            # 'center' is used instead of 'location'
        }

    def __init__(self, *args, **kwargs):
        super(RawMaterialForm, self).__init__(*args, **kwargs)

        if 'initial' not in kwargs and not self.is_bound and self.instance:
            inventory = RawMaterialInventory.objects.filter(raw_material=self.instance).first()
            if inventory:
                self.fields['quantity_in_stock'].initial = inventory.quantity_in_stock
                self.fields['center'].initial = inventory.center
            else:
                # Set default center if needed, for example, the first center
                self.fields['center'].initial = center.objects.first()

    def save(self, commit=True):
        raw_material = super(RawMaterialForm, self).save(commit=False)
        if commit:
            raw_material.save()
            # Use a different variable name to avoid shadowing the 'center' model
            center_instance = self.cleaned_data.get('center')
            if not center_instance:
                center_instance = center.objects.first()

            quantity_in_stock = self.cleaned_data.get('quantity_in_stock', 0)
            
            # Create or update the inventory record
            inventory, created = RawMaterialInventory.objects.update_or_create(
                raw_material=raw_material,
                defaults={
                    'center': center_instance,
                    'quantity_in_stock': quantity_in_stock
                }
            )
        return raw_material


class ProductForm(forms.ModelForm):
    quantity_in_stock = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Quantity in Stock',
        initial=0
    )
    
    class Meta:
        model = Product
        fields = ['designation', 'selling_price', 'category', 'center']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'center': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        if 'initial' not in kwargs and not self.is_bound and self.instance:
            inventory = ProductInventory.objects.filter(product=self.instance).first()
            if inventory:
                self.fields['quantity_in_stock'].initial = inventory.quantity_in_stock

    def save(self, commit=True):
        product = super(ProductForm, self).save(commit=False)
        if commit:
            product.save()

            # Make sure to get the center instance, not just the ID
            center_instance = self.cleaned_data.get('center')
            
            # Check if the center instance is valid
            if not center_instance:
                raise forms.ValidationError("Center is required.")

            # Update or create the ProductInventory instance
            inventory, created = ProductInventory.objects.update_or_create(
                product=product, 
                defaults={
                    'center': center_instance,
                    'quantity_in_stock': self.cleaned_data.get('quantity_in_stock', 0)
                }
            )
        return product


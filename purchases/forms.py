from django import forms
from .models import Supplier, Purchase
from centers.models import center
from inventory.models import RawMaterialInventory, RawMaterial

class SupplierForm(forms.ModelForm):
    balance = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Balance',
        initial=0,
        max_digits=10, 
        decimal_places=2
    )

    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone_number', 'address', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        # If balance is not provided, set it to 0
        self.fields['balance'].initial = 0

    def save(self, commit=True):
        supplier = super(SupplierForm, self).save(commit=False)
        supplier.balance = self.cleaned_data.get('balance') or 0.00
        if commit:
            supplier.save()
        return supplier

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'raw_material', 'quantity', 'unit_price', 'status', 'payment_details', 'additional_notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'raw_material': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_details': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }


    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        # Get the main store center
        main_store_center = center.objects.get(name='Main Store')  # Make sure 'Main Store' is the correct name
        # Filter raw materials that are in the main store inventory
        main_store_raw_materials = RawMaterialInventory.objects.filter(
            center=main_store_center
        ).values_list('raw_material__code', flat=True)  # Use 'raw_material__code' instead of 'raw_material__id'
        # Set the queryset for the raw_material field to only include those raw materials
        self.fields['raw_material'].queryset = RawMaterial.objects.filter(
            code__in=main_store_raw_materials
        )
        

    def save(self, commit=True):
        # Save the Purchase instance
        purchase = super(PurchaseForm, self).save(commit=False)
        if commit:
            purchase.save()
            # Update the supplier's balance and save
            purchase.supplier.balance += purchase.total_amount
            purchase.supplier.save()
            
            # Update or create the RawMaterialInventory at the Main Store center
            main_store_center = center.objects.get(name='Main Store')  # Make sure 'Main Store' is the correct name
            inventory, created = RawMaterialInventory.objects.get_or_create(
                raw_material=purchase.raw_material,
                center=main_store_center,
                defaults={'quantity_in_stock': 0}
            )
            # Update the quantity in stock
            inventory.quantity_in_stock += purchase.quantity
            inventory.save()

        return purchase
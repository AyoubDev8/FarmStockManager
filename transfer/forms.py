from django import forms
from django.core.exceptions import ValidationError
from inventory.models import RawMaterialInventory, RawMaterial
from centers.models import center
from .models import MaterialTransfer

class MaterialTransferForm(forms.ModelForm):
    class Meta:
        model = MaterialTransfer
        fields = ['center', 'raw_material', 'quantity_transferred', 'status']
        widgets = {
            'center': forms.Select(attrs={'class': 'form-control'}),
            'raw_material': forms.Select(attrs={'class': 'form-control'}),
            'quantity_transferred': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MaterialTransferForm, self).__init__(*args, **kwargs)
        # Filter to show only non-main stores in the 'center' field
        main_store = center.objects.get(name='Main Store')
        self.fields['center'].queryset = center.objects.exclude(name='Main Store')
        # Filter raw materials to include only those that are available in the main store inventory
        self.fields['raw_material'].queryset = RawMaterial.objects.filter(
            rawmaterialinventory__center=main_store,
            rawmaterialinventory__quantity_in_stock__gt=0
        )

    def clean_quantity_transferred(self):
        quantity = self.cleaned_data.get('quantity_transferred')
        raw_material = self.cleaned_data.get('raw_material')
        main_store = center.objects.get(name='Main Store')
        # Check if the main store has enough stock
        stock = RawMaterialInventory.objects.get(center=main_store, raw_material=raw_material).quantity_in_stock
        if quantity > stock:
            raise forms.ValidationError("Not enough stock in the main store for the selected raw material.")
        return quantity

    def save(self, commit=True):
        transfer = super(MaterialTransferForm, self).save(commit=False)
        main_store = center.objects.get(name='Main Store')

        # Check if the main store has enough stock before saving
        try:
            main_store_inventory = RawMaterialInventory.objects.get(
                center=main_store, 
                raw_material=transfer.raw_material
            )
        except RawMaterialInventory.DoesNotExist:
            raise ValidationError('No inventory for this raw material in the main store.')

        if main_store_inventory.quantity_in_stock < transfer.quantity_transferred:
            raise ValidationError('Not enough stock in the main store for the selected raw material.')

        if commit:
            # Decrease quantity from the main store
            main_store_inventory.quantity_in_stock -= transfer.quantity_transferred
            main_store_inventory.save()

            # Increase quantity in the destination store
            destination_inventory, created = RawMaterialInventory.objects.get_or_create(
                center=transfer.center,
                raw_material=transfer.raw_material,
                defaults={'quantity_in_stock': 0}
            )
            destination_inventory.quantity_in_stock += transfer.quantity_transferred
            destination_inventory.save()

            transfer.save()
        return transfer

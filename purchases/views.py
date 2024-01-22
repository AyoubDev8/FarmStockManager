from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Supplier, Purchase
from .forms import SupplierForm, PurchaseForm


class AddSupplierView(View):
    def get(self, request, *args, **kwargs):
        form = SupplierForm()
        return render(request, 'purchase/addsupplier.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
        return render(request, 'purchase/addsupplier.html', {'form': form})

class SupplierListView(View):
    def get(self, request, *args, **kwargs):
        suppliers = Supplier.objects.all()
        return render(request, 'purchase/supplierlist.html', {'suppliers': suppliers})

class EditSupplierView(View):
    def get(self, request, code):
        supplier = get_object_or_404(Supplier, code=code)
        form = SupplierForm(instance=supplier)
        return render(request, 'purchase/editsupplier.html', {'form': form})

    def post(self, request, code):
        supplier = get_object_or_404(Supplier, code=code)
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
        return render(request, 'purchase/editsupplier.html', {'form': form})

class SupplierDeleteView(View):
    def get(self, request, code, *args, **kwargs):
        supplier = get_object_or_404(Supplier, code=code)
        return render(request, 'purchase/confirmsupplierdelete.html', {'supplier': supplier})

    def post(self, request, code, *args, **kwargs):
        supplier = get_object_or_404(Supplier, code=code)
        supplier.delete()
        return redirect('supplier_list')


class AddPurchaseView(View):
    def get(self, request, *args, **kwargs):
        form = PurchaseForm()
        return render(request, 'purchase/addpurchase.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
        return render(request, 'purchase/addpurchase.html', {'form': form})

class PurchaseListView(View):
    def get(self, request, *args, **kwargs):
        purchases = Purchase.objects.all()
        return render(request, 'purchase/purchaselist.html', {'purchases': purchases})

class EditPurchaseView(View):
    def get(self, request, purchase_code):
        purchase = get_object_or_404(Purchase, purchase_code=purchase_code)
        form = PurchaseForm(instance=purchase)
        return render(request, 'purchase/editpurchase.html', {'form': form})

    def post(self, request, purchase_code):
        purchase = get_object_or_404(Purchase, purchase_code=purchase_code)
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('purchase_list')
        return render(request, 'purchase/editpurchase.html', {'form': form})

class PurchaseDeleteView(View):
    def get(self, request, purchase_code, *args, **kwargs):
        purchase = get_object_or_404(Purchase, purchase_code=purchase_code)
        return render(request, 'purchase/confirmpurchasedelete.html', {'purchase': purchase})

    def post(self, request, purchase_code, *args, **kwargs):
        purchase = get_object_or_404(Purchase, purchase_code=purchase_code)
        purchase.delete()
        return redirect('purchase_list')


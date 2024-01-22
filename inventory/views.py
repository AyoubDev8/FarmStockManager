# inventory/views.py
# from audioop import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import ProductForm, RawMaterialForm
from .models import Product, ProductInventory, RawMaterial, RawMaterialInventory


class AddInventoryView(View):
    def get(self, request, *args, **kwargs):
        form = RawMaterialForm()
        return render(request, 'inventory/addinventory.html', {'raw_material_form': form})

    def post(self, request, *args, **kwargs):
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
        return render(request, 'inventory/addinventory.html', {'raw_material_form': form})

class EditInventoryView(View):
    def get(self, request, raw_material_code):
        raw_material = get_object_or_404(RawMaterial, code=raw_material_code)
        form = RawMaterialForm(instance=raw_material)
        # Initialize the quantity_in_stock from the RawMaterialInventory
        try:
            raw_material_inventory = RawMaterialInventory.objects.get(raw_material=raw_material)
            initial_quantity_in_stock = raw_material_inventory.quantity_in_stock
        except RawMaterialInventory.DoesNotExist:
            initial_quantity_in_stock = 0
        form.fields['quantity_in_stock'].initial = initial_quantity_in_stock
        
        context = {
            'form': form,
            'raw_material_inventory': initial_quantity_in_stock
        }
        return render(request, 'inventory/editinventory.html', context)

    def post(self, request, raw_material_code):

        raw_material = get_object_or_404(RawMaterial, code=raw_material_code)
        form = RawMaterialForm(request.POST, instance=raw_material)
        
        if form.is_valid():
            updated_raw_material = form.save(commit=False)

            # Assuming 'center' is a field in your form
            center = form.cleaned_data.get('center')

            # Ensure 'center' is not None
            if not center:
                form.add_error('center', 'This field is required.')
                return render(request, 'inventory/editinventory.html', {'form': form})

            updated_raw_material.save()

            quantity_in_stock = form.cleaned_data.get('quantity_in_stock', 0)

            RawMaterialInventory.objects.update_or_create(
                raw_material=updated_raw_material,
                defaults={'quantity_in_stock': quantity_in_stock, 'center': center}
            )
            return redirect('inventory_list')
        else:
            context = {'form': form}
            return render(request, 'inventory/editinventory.html', context)


class AddProductView(View):
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, 'inventory/addproduct.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to product list or any other appropriate page
            return redirect('product_list')  # Adjust the redirection as needed
        return render(request, 'inventory/addproduct.html', {'form': form})



class EditProductView(View):
    def get(self, request, product_code):
        product = get_object_or_404(Product, code=product_code)
        form = ProductForm(instance=product)
        try:
            product_inventory = ProductInventory.objects.get(product=product)
        except ProductInventory.DoesNotExist:
            product_inventory = None
        context = {
            'form': form,
            'product_inventory': product_inventory
        }
        return render(request, 'inventory/editproduct.html', context)

    def post(self, request, product_code):
        # print(f"Received POST request for product code: {product_code}")
        product = get_object_or_404(Product, code=product_code)
        form = ProductForm(request.POST, instance=product)
        
        # print(f"POST data: {escape(repr(request.POST))}")

        if form.is_valid():
            # print("Form is valid, saving...")
            updated_product = form.save(commit=False)

            # Additional print statements for debugging
            quantity_in_stock = form.cleaned_data.get('quantity_in_stock', 0)
            # print(f"quantity_in_stock from form.cleaned_data: {quantity_in_stock}")

            updated_product.save()
            # print(f"Updated product: {updated_product}")

            ProductInventory.objects.update_or_create(
                product=updated_product,
                defaults={'quantity_in_stock': quantity_in_stock}
            )
            # print("ProductInventory updated or created.")

            return redirect('product_list')
        else:
            # print("Form is not valid!")
            # print(f"Form errors: {form.errors.as_json()}")

            context = {'form': form}
            return render(request, 'inventory/editproduct.html', context)





class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.prefetch_related('productinventory_set').select_related('center').all()
        return render(request, 'inventory/productlist.html', {'products': products})


class InventoryListView(View):
    def get(self, request, *args, **kwargs):
        raw_materials = RawMaterial.objects.prefetch_related('rawmaterialinventory_set').all()
        return render(request, 'inventory/inventorylist.html', {'raw_materials': raw_materials})


class ProductDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'inventory/confirmdelete.html', {'product': product})

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product_list')

class InventoryDeleteView(View):
    def get(self, request, raw_material_code, *args, **kwargs):
        raw_material = get_object_or_404(RawMaterial, code=raw_material_code)
        return render(request, 'inventory/confirminventorydelete.html', {'raw_material': raw_material})

    def post(self, request, raw_material_code, *args, **kwargs):
        raw_material = get_object_or_404(RawMaterial, code=raw_material_code)
        raw_material.delete()
        return redirect('inventory_list')

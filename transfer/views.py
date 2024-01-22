from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import MaterialTransfer
from .forms import MaterialTransferForm

class TransferListView(View):
    def get(self, request, *args, **kwargs):
        transfers = MaterialTransfer.objects.all()
        return render(request, 'transfer/transferlist.html', {'transfers': transfers})

class AddTransferView(View):
    def get(self, request, *args, **kwargs):
        form = MaterialTransferForm()
        return render(request, 'transfer/addtransfer.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MaterialTransferForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('transfer_list')
            except ValidationError as e:
                # Handle the validation error
                for error in e:
                    form.add_error(None, error)
        return render(request, 'transfer/addtransfer.html', {'form': form})

class EditTransferView(View):
    def get(self, request, transfer_id):
        transfer = get_object_or_404(MaterialTransfer, pk=transfer_id)
        form = MaterialTransferForm(instance=transfer)
        return render(request, 'transfer/edittransfer.html', {'form': form, 'transfer': transfer})

    def post(self, request, transfer_id):
        transfer = get_object_or_404(MaterialTransfer, pk=transfer_id)
        form = MaterialTransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return redirect('transfer_list')
        return render(request, 'transfer/edittransfer.html', {'form': form, 'transfer': transfer})

class DeleteTransferView(View):
    def get(self, request, transfer_id, *args, **kwargs):
        transfer = get_object_or_404(MaterialTransfer, pk=transfer_id)
        return render(request, 'transfer/deletetransfer.html', {'transfer': transfer})

    def post(self, request, transfer_id, *args, **kwargs):
        transfer = get_object_or_404(MaterialTransfer, pk=transfer_id)
        transfer.delete()
        return redirect('transfer_list')

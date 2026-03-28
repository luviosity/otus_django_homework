from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from store.forms import ProductForm
from store.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store/product_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "store/product_detail.html", context)


@require_http_methods(["GET", "POST"])
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        product = form.save()
        messages.success(request, "Product created successfully.")
        return redirect("product_detail", pk=product.pk)
    return render(request, "store/product_form.html", {"form": form, "title": "Create Product"})


@require_http_methods(["GET", "POST"])
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect("product_detail", pk=product.pk)
    return render(request, "store/product_form.html", {"form": form, "title": "Edit Product"})

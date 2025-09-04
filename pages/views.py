from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from .utils import ImageLocalStorage


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: J.D",
            }
        )
        return context


"""class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 1200},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 50},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 200},
    ]"""


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.objects.all(),
        }
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Invalid product id")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse("home"))

        viewData = {
            "title": product.name + " - Online Store",
            "subtitle": product.name + " - Product information",
            "product": product,
        }
        return render(request, self.template_name, viewData)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # 👈 El modelo de models.py
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        return render(
            request, self.template_name, {"title": "Create product", "form": form}
        )

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "products/created.html")
        return render(
            request, self.template_name, {"title": "Create product", "form": form}
        )
class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Simulated database for products
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}

        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products,
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Get cart products from session and add the new product
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')


class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')
    
def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = "images/index.html"

        def get(self, request):
            image_url = request.session.get("image_url", "")
            return render(request, self.template_name, {"image_url": image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session["image_url"] = image_url
            return redirect("image_index")

    return ImageView

class ImageViewNoDI(View):
    template_name = "images/index.html"

    def get(self, request):
        image_url = request.session.get("image_url", "")
        return render(request, self.template_name, {"image_url": image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session["image_url"] = image_url
        return redirect("imagenodi_index")

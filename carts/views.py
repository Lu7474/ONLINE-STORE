from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from .mixins import CartMixin
from .models import Cart
from dashboard.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            messages.error(request, "Товар не найден")
            return redirect(request.META.get("HTTP_REFERER", "home"))

        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()

        else:
            cart = Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                product=product,
                quantity=1,
            )
        messages.success(request, "Товар добавлен в корзину")
        return redirect(request.META.get("HTTP_REFERER", "home"))


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        quantity = int(request.POST.get("quantity"))
        cart = self.get_cart(request, cart_id=cart_id)

        if cart:
            if quantity > 0:
                cart.quantity = quantity
                cart.save()
            else:
                cart.delete()

        return redirect(request.META.get("HTTP_REFERER", "cart"))


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        if cart:
            cart.delete()

        return redirect(request.META.get("HTTP_REFERER", "cart"))

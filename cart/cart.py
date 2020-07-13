from decimal import Decimal
from django.conf import settings
from online_shop.shop.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранение в сессии пустой корзины
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # добавление товара в корзину или обновление его количества
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # сохранение товара в корзине
    def save(self):
        # сессия помечается, как изменённая
        self.session.modified = True

    # удаление товара из корзины
    def remove(self, product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # прохождение по товарам корзины, получение соответствующих объектов Product
    def __iter__(self):
        product_ids = self.cart.keys()
        # получение объектов модели Product и передача их в корзинну
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
        yield item

    # общее количество товаров в корзине
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # общая стоимость корзины
    def get_total_price(self):
        return sum(
            Decimal(item['price']*item['quantity'] for item in self.cart.values())
        )

    # очистка корзины
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

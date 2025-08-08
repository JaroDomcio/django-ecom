from store.models import Product

class Cart():
    def __init__(self,request):
        self.session = request.session

        # Jeżeli użytkownik ma sesje, przypisz jego klucz sesji
        cart = self.session.get('cart')

        # Jeżeli nie ma to stwórz ją
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self,product,quantity = 1,override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity' : 0,
                                     'price' : str(product.price),}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)].copy()
            item['product'] = product
            yield item

    def save(self):
        self.session.modified = True

class Cart():
    def __init__(self,request):
        self.session = request.session

        # Jeżeli użytkownik ma sesje, przypisz jego klucz sesji
        cart = self.session.get('session_key')

        # Jeżeli nie ma to stwórz ją
        if 'session_key' in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart
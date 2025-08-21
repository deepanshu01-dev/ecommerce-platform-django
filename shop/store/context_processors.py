from .models import CartItem
from .models import Auth

def cart_quantity(request):
    cart_count = 0
    if request.session.get('user_id'):
        try:
            user = Auth.objects.get(id=request.session['user_id'])
            cart_count = CartItem.objects.filter(user=user).count()
        except Auth.DoesNotExist:
            pass

    return {'cart_count': cart_count}

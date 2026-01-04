def cart_processor(request):
    """Add cart count to all templates"""
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': cart_count}

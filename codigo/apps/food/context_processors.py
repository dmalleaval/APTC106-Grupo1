from .models import Pedido


def cart(request):
    """
    Cantidad total de productos en el carrito del usuario.
    """

    if not request.user.is_authenticated:
        return {
            "cart_count": 0
        }

    pedido = (
        Pedido.objects
        .filter(
            cliente=request.user,
            estado=Pedido.Estado.CARRITO
        )
        .prefetch_related("detalles")
        .first()
    )

    if pedido is None:
        return {
            "cart_count": 0
        }

    cantidad = sum(
        detalle.cantidad
        for detalle in pedido.detalles.all()
    )

    return {
        "cart_count": cantidad
    }
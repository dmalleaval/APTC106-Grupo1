from django.contrib import admin

from .models import Categoria, DetallePedido, Pedido, Producto

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)

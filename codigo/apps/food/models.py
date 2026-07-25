from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    imagen = models.ImageField(
        upload_to="productos/",
        blank=True,
        null=True,
    )
    disponible = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["categoria__nombre", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["categoria", "nombre"],
                name="producto_unico_por_categoria",
            )
        ]

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    class Estado(models.TextChoices):
        CARRITO = "carrito", "En carrito"
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADO = "confirmado", "Confirmado"
        PREPARANDO = "preparando", "En preparación"
        LISTO = "listo", "Listo"
        ENTREGADO = "entregado", "Entregado"
        CANCELADO = "cancelado", "Cancelado"

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.CARRITO,
    )
    observaciones = models.TextField(blank=True)
    direccion_entrega = models.CharField(max_length=255, blank=True)
    telefono_contacto = models.CharField(max_length=30, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado_en"]
        constraints = [
            models.UniqueConstraint(
                fields=["cliente"],
                condition=Q(estado="carrito"),
                name="un_carrito_activo_por_cliente",
            )
        ]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente}"

    @property
    def cantidad_productos(self):
        return sum(detalle.cantidad for detalle in self.detalles.all())

    @property
    def total(self):
        return sum(
            (detalle.subtotal for detalle in self.detalles.all()),
            Decimal("0.00"),
        )


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="detalles_pedido",
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    agregado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["agregado_en"]
        constraints = [
            models.UniqueConstraint(
                fields=["pedido", "producto"],
                name="producto_unico_por_pedido",
            ),
            models.CheckConstraint(
                condition=Q(cantidad__gte=1),
                name="cantidad_pedido_mayor_a_cero",
            ),
        ]

    def __str__(self):
        return f"{self.cantidad} × {self.producto.nombre}"

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, DetallePedido, Pedido, Producto


class FoodBaseTestCase(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="admin", password="clave12345", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="cliente", password="clave12345"
        )
        self.categoria = Categoria.objects.create(
            nombre="Bebidas", descripcion="Bebidas frías"
        )
        self.producto = Producto.objects.create(
            categoria=self.categoria,
            nombre="Coca-Cola",
            descripcion="Lata 350cc",
            precio=Decimal("1500"),
        )


class ProductoPermissionsTests(FoodBaseTestCase):
    def test_food_create_requires_staff(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse("food:foods-create"))
        self.assertEqual(response.status_code, 302)

    def test_food_create_allowed_for_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("food:foods-create"),
            {
                "categoria": self.categoria.pk,
                "nombre": "Sprite",
                "descripcion": "Lata 350cc",
                "precio": "1500",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(nombre="Sprite").exists())

    def test_food_delete_requires_staff(self):
        self.client.force_login(self.normal_user)
        response = self.client.post(
            reverse("food:foods-delete", args=[self.producto.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())


class ProductoDeleteTests(FoodBaseTestCase):
    def test_food_delete_hard_when_no_pedidos(self):
        self.client.force_login(self.staff_user)
        self.client.post(reverse("food:foods-delete", args=[self.producto.pk]))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_food_delete_soft_when_has_pedidos(self):
        pedido = Pedido.objects.create(
            cliente=self.normal_user, estado=Pedido.Estado.CARRITO
        )
        DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=1,
            precio_unitario=self.producto.precio,
        )

        self.client.force_login(self.staff_user)
        self.client.post(reverse("food:foods-delete", args=[self.producto.pk]))

        self.producto.refresh_from_db()
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())
        self.assertFalse(self.producto.activo)


class CategoriaTests(FoodBaseTestCase):
    def test_category_create_requires_staff(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse("food:category-create"))
        self.assertEqual(response.status_code, 302)

    def test_category_delete_soft_when_has_productos(self):
        self.client.force_login(self.staff_user)
        self.client.post(reverse("food:category-delete", args=[self.categoria.pk]))

        self.categoria.refresh_from_db()
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())
        self.assertFalse(self.categoria.activa)

    def test_category_delete_hard_when_no_productos(self):
        categoria_vacia = Categoria.objects.create(nombre="Postres")

        self.client.force_login(self.staff_user)
        self.client.post(reverse("food:category-delete", args=[categoria_vacia.pk]))

        self.assertFalse(Categoria.objects.filter(pk=categoria_vacia.pk).exists())


class ShopSearchTests(FoodBaseTestCase):
    def test_shop_filters_by_query(self):
        Producto.objects.create(
            categoria=self.categoria,
            nombre="Empanada de pino",
            descripcion="Empanada tradicional",
            precio=Decimal("2000"),
        )

        response = self.client.get(reverse("food:shop"), {"q": "Coca"})

        productos = list(response.context["productos"])
        self.assertIn(self.producto, productos)
        self.assertEqual(len(productos), 1)


class CarritoTests(FoodBaseTestCase):
    def test_confirmar_pedido_changes_estado_and_allows_new_cart(self):
        pedido = Pedido.objects.create(
            cliente=self.normal_user, estado=Pedido.Estado.CARRITO
        )
        DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=2,
            precio_unitario=self.producto.precio,
        )

        self.client.force_login(self.normal_user)
        response = self.client.post(reverse("food:cart-confirm"))

        self.assertEqual(response.status_code, 302)
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, Pedido.Estado.CONFIRMADO)

        nuevo_carrito = Pedido.objects.create(
            cliente=self.normal_user, estado=Pedido.Estado.CARRITO
        )
        self.assertNotEqual(nuevo_carrito.pk, pedido.pk)

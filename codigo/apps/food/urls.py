from django.urls import include, path

from apps.food import views

app_name = "food"

foods_patterns = [
    path("inicio/", views.food_list, name="home"),
    path("crear/", views.food_create, name="foods-create"),
    path("<int:pk>/detalle/", views.food_detail, name="foods-detail"),
    path("<int:pk>/editar/", views.food_update, name="foods-edit"),
    path("<int:pk>/eliminar/", views.food_delete, name="foods-delete"),
    path(
        "<int:pk>/agregar-carrito/",
        views.agregar_al_carrito,
        name="add-to-cart",
    ),
]

categories_patterns = [
    path("", views.category_list, name="category-list"),
    path("crear/", views.category_create, name="category-create"),
    path("<int:pk>/editar/", views.category_update, name="category-edit"),
    path("<int:pk>/eliminar/", views.category_delete, name="category-delete"),
]

urlpatterns = [
    path("", views.log_in, name="log-in"),
    path("log-out/", views.log_out, name="log-out"),
    path("categorias/", include(categories_patterns)),
    path("comidas/", include(foods_patterns)),
    path("carrito/", views.cart_detail, name="cart-detail"),
    path("tienda/", views.shop, name="shop"),
    path(
        "carrito/<int:pk>/aumentar/",
        views.cart_increase,
        name="cart-increase",
    ),
    path(
        "carrito/<int:pk>/disminuir/",
        views.cart_decrease,
        name="cart-decrease",
    ),
    path(
        "carrito/<int:pk>/eliminar/",
        views.cart_delete,
        name="cart-delete",
    ),
    path(
        "carrito/confirmar/",
        views.confirmar_pedido,
        name="cart-confirm",
    ),
]

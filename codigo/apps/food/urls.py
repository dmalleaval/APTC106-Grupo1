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

urlpatterns = [
    path("", views.log_in, name="log-in"),
    path("log-out/", views.log_out, name="log-out"),
    path("categorias/", views.category_list, name="category-list"),
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
]

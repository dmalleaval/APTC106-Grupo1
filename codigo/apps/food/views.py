from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import F
from django.db import transaction

from .forms import LoginForm, FoodsForm
from .models import Categoria
from .models import DetallePedido, Pedido, Producto


def log_in(request):
    if request.user.is_authenticated:
        return redirect("food:shop")

    form = LoginForm(request.POST or None)

    context = {
        "message": None,
        "form": form,
        "form_title": "Iniciar sesión",
        "form_subtitle": "Ingresa tus credenciales para continuar.",
        "form_icon": "login",
        "submit_text": "Ingresar",
        "submit_icon": "login",
        "cancel_url": "food:shop",
        "cancel_text": "Volver a la tienda",
    }

    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            **form.cleaned_data,
        )

        if user is not None:
            if user.is_active:
                login(request, user)

                next_url = request.GET.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("food:shop")

            context["message"] = "El usuario ha sido desactivado"

        else:
            context["message"] = "Usuario o contraseña incorrecta"

    return render(
        request,
        "foods/login.html",
        context,
    )


@login_required
@require_POST
def log_out(request):
    logout(request)
    return redirect("food:log-in")


@login_required
def food_list(request):
    foods = Producto.objects.select_related("categoria").all()
    return render(request, "foods/index.html", {"foods": foods})


@login_required
def food_detail(request, pk):
    food = get_object_or_404(Producto.objects.select_related("categoria"), pk=pk)
    return render(request, "foods/detail.html", {"food": food})


@login_required
def food_create(request):
    form = FoodsForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("food:home")

    context = {
        "form": form,
        "form_title": "Agregar producto",
        "form_subtitle": "Completa la información del producto.",
        "form_icon": "restaurant_menu",
        "submit_text": "Crear producto",
        "submit_icon": "save",
        "cancel_url": "food:home",
        "cancel_text": "Cancelar",
    }

    return render(
        request,
        "foods/form.html",
        context,
    )


@login_required
def food_update(request, pk):
    food = get_object_or_404(Producto, pk=pk)

    form = FoodsForm(
        request.POST or None,
        request.FILES or None,
        instance=food,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("food:home")

    context = {
        "form": form,
        "form_title": "Editar producto",
        "form_subtitle": "Actualiza la información del producto.",
        "form_icon": "edit",
        "submit_text": "Guardar cambios",
        "submit_icon": "save",
        "cancel_url": "food:home",
        "cancel_text": "Cancelar",
    }

    return render(
        request,
        "foods/form.html",
        context,
    )


@login_required
@require_POST
def food_delete(request, pk):
    food = get_object_or_404(Producto, pk=pk)
    food.delete()
    return redirect("food:home")


@login_required
def category_list(request):
    categories = Categoria.objects.all()
    return render(
        request,
        "foods/category/category_list.html",
        {"categories": categories},
    )


@login_required
@require_POST
@transaction.atomic
def agregar_al_carrito(request, pk):
    producto = get_object_or_404(
        Producto,
        pk=pk,
        activo=True,
        disponible=True,
    )

    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except (TypeError, ValueError):
        cantidad = 1

    cantidad = max(1, min(cantidad, 99))

    pedido, _ = Pedido.objects.get_or_create(
        cliente=request.user,
        estado=Pedido.Estado.CARRITO,
    )

    detalle, creado = DetallePedido.objects.get_or_create(
        pedido=pedido,
        producto=producto,
        defaults={
            "cantidad": cantidad,
            "precio_unitario": producto.precio,
        },
    )

    if not creado:
        DetallePedido.objects.filter(pk=detalle.pk).update(
            cantidad=F("cantidad") + cantidad
        )

    return redirect("food:shop")


@login_required
def cart_detail(request):
    pedido = (
        Pedido.objects.filter(
            cliente=request.user,
            estado=Pedido.Estado.CARRITO,
        )
        .prefetch_related("detalles__producto")
        .first()
    )

    return render(
        request,
        "foods/cart_detail.html",
        {"pedido": pedido},
    )


def shop(request):
    categoria_seleccionada = request.GET.get("categoria")

    productos = Producto.objects.filter(
        activo=True,
        disponible=True,
        categoria__activa=True,
    ).select_related("categoria")

    if categoria_seleccionada:
        productos = productos.filter(categoria_id=categoria_seleccionada)

    categorias = Categoria.objects.filter(activa=True).order_by("nombre")

    context = {
        "productos": productos,
        "categorias": categorias,
        "categoria_seleccionada": categoria_seleccionada,
    }

    return render(
        request,
        "foods/shop.html",
        context,
    )


@login_required
@require_POST
def cart_increase(request, pk):

    detalle = get_object_or_404(
        DetallePedido,
        pk=pk,
        pedido__cliente=request.user,
    )

    detalle.cantidad += 1
    detalle.save(update_fields=["cantidad"])

    return redirect("food:cart-detail")


@login_required
@require_POST
def cart_decrease(request, pk):

    detalle = get_object_or_404(
        DetallePedido,
        pk=pk,
        pedido__cliente=request.user,
    )

    if detalle.cantidad > 1:
        detalle.cantidad -= 1
        detalle.save(update_fields=["cantidad"])
    else:
        detalle.delete()

    return redirect("food:cart-detail")


@login_required
@require_POST
def cart_delete(request, pk):

    detalle = get_object_or_404(
        DetallePedido,
        pk=pk,
        pedido__cliente=request.user,
    )

    detalle.delete()

    return redirect("food:cart-detail")

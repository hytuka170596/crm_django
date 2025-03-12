from django.contrib.auth.models import User, Permission
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db import transaction
from django.db.models import QuerySet


from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

from core.base import MyDeleteView
from .forms import ProductCreateForm
from .models import Product
from .dto_product import ProductCreateDTO, ProductUpdateDTO
from .services import ProductService


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Представление для списка всех услуг.
    Пагинация настроена по выводу 10 услуг по умолчанию.
    Это можно изменить назначив paginate_by новое значение.
    Так же фильтрация стоит по не архивированным услугам.
    """

    permission_required: Permission = "view_product"
    model: Product = Product
    template_name: str = "service_product/products-list.html"
    queryset: QuerySet[Product, Product] = Product.objects.filter(archived=False)
    context_object_name: str = "products"
    paginate_by: int = 10


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление для создания услуги."""

    permission_required: Permission = "create_product"
    model: Product = Product
    form_class: ProductCreateForm = ProductCreateForm
    template_name: str = "service_product/products-create.html"

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном создании услуги, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy(
            "service_product:service_detail", kwargs={"pk": self.object.pk}
        )

    @transaction.atomic
    def form_valid(self, form: ProductCreateForm) -> HttpResponse:
        """
        Устанавливаем пользователя, создавшего услугу и делаем проверки различного уровня и создаём запись в бд.
        """
        if form.is_valid():
            form.instance.created_by = User.objects.get(id=self.request.user.pk)

            dto = ProductCreateDTO(
                **form.cleaned_data,
                created_by=form.instance.created_by,
            )
            try:
                ProductService.checking_before_creation(dto)
            except ValueError as error:
                form.add_error(None, str(error))
                return self.form_invalid(form)

            return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для отображения деталей услуги."""

    permission_required: Permission = "view_product"
    model: Product = Product
    template_name: str = "service_product/products-detail.html"
    context_object_name: str = "product"


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление для редактирования данных об услуге."""

    permission_required: Permission = "change_product"
    model: type[Product] = Product
    form_class: ProductCreateForm = ProductCreateForm
    template_name: str = "service_product/products-edit.html"

    @transaction.atomic
    def form_valid(self, form: ProductCreateForm) -> HttpResponse:
        """
        Устанавливаем пользователя, создавшего услугу и делаем проверки различного уровня и создаём запись в бд.
        """
        if form.is_valid():
            form.instance.updated_by = User.objects.get(id=self.request.user.pk)

            product_pk = self.object.pk

            dto = ProductUpdateDTO(
                pk=product_pk,
                **form.cleaned_data,
                updated_by=form.instance.updated_by,
            )
            try:
                ProductService.checking_before_update(dto)
            except ValueError as error:
                form.add_error(None, str(error))
                return self.form_invalid(form)

            return super().form_valid(form)

    def get_success_url(self) -> HttpResponseRedirect:
        """При успешном редактировании, перенаправляет на страницу с деталями этой услуги."""
        return reverse_lazy(
            "service_product:service_detail", kwargs={"pk": self.object.pk}
        )

    def test_func(self) -> bool:
        """
        Проверка прав доступа для изменения услуг, а точнее такие проверки:
            - если пользователь это суперюзер
            - если пользователь имеет права на изменения услуг
            иначе доступ будет закрыт.
        """
        if self.request.user.is_superuser or self.request.user.has_perm(
            "service_product.change_product"
        ):
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MyDeleteView):
    """
    Представление для подтверждения удаления услуги.
    """

    permission_required: Permission = "delete_product"
    model: Product = Product
    context_object_name: str = "product"
    success_url = reverse_lazy("service_product:service_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs) -> HttpResponse:
        return super().delete(request, *args, **kwargs)

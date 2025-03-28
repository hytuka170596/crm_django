from dataclasses import dataclass
from typing import Protocol, Optional

from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.http import Http404
from django.views.generic import DeleteView

import logging

logger = logging.getLogger("services")


# TODO подумать, какие интерфейсы обязаны иметь все сервисы
class ServiceProtocol(Protocol):
    """Класс задаёт интерфейсы для различных сервисов."""

    @staticmethod
    def _check_active_user(user_id: int) -> None:
        """
        Проверка, что пользователь активен.
        Метод должен быть реализован в подклассе.
        """
        raise NotImplementedError("Must be implemented by subclass")

    @staticmethod
    def _check_permissions_user(user: User) -> None:
        """
        Проверка прав пользователя.
        Метод должен быть реализован в подклассе.
        """
        raise NotImplementedError("Must be implemented by subclass")

    @classmethod
    def _get_service_name(cls) -> str:
        """
        Метод возвращает в зависимости от типа сервиса его строковое название.
        Метод должен быть реализован в подклассе.

        """
        raise NotImplementedError("Must be implemented by subclass")


@dataclass
class BaseService(ServiceProtocol):
    @classmethod
    def _get_service_name(cls) -> str:
        """
        Метод возвращает в зависимости от типа сервиса его строковое название.
        Examples:
            - ProductService
            - AdsCompanyService
        Returns:
            str: service name
        """
        return cls.__name__

    @staticmethod
    def _check_existing_name_by_field_in_db(
        model: type[models.Model], name: str, message: str
    ) -> None:
        """
        Проверка на существование у модели записей с таким названием, в поле 'name'
        Args:
            model: модель для фильтрации существования такого названия
            name: название
            message: сообщение об ошибке, которое увидит создающий новую запись
        Raises:
            ValueError(message) если такая запись существует
        """
        if model.objects.filter(name=name).exists():
            raise ValidationError(message)


@dataclass
class BaseDTO:
    """Базовый класс DTO"""

    def to_dict(self) -> dict[str, Optional[str]]:
        """Преобразует все атрибуты класса в словарь."""
        return {key: value for key, value in self.__dict__.items() if value is not None}


class BaseForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class MyDeleteView(DeleteView):
    """Кастомный Delete View для переопределения метода get_success_url всех его наследников."""

    def get_success_url(self) -> str:
        """
        Отправка сообщения об успешном удалении.
        И перенаправляет на заданную страницу или вызывает ошибку 404.
        """
        messages.success(self.request, f"{self.object.name!r} успешно удаленно.")
        if self.success_url:
            logger.info(
                f"{self.object.__class__.__name__} {self.object.name!r} удалён пользователем {self.request.user}."
            )
            return self.success_url
        else:
            raise Http404(
                "success_url  не был указан. Не понятно куда перенаправлять пользователя после удаления. Укажите, например, страницу со списком этого же объекта"
            )

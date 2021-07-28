
import logging

from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView


class BaseView(View):
    logger = logging.getLogger(__name__)

    @property
    def current_user(self):
        return self.request.user

    @property
    def is_authenticated_user(self):
        return self.current_user.is_authenticated

    @property
    def is_anonymous_user(self):
        return self.current_user.is_anonymous


class BaseTemplateView(TemplateView, BaseView):
    pass


class BaseFormView(FormView, BaseView):
    pass

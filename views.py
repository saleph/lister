from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Reader


class IndexView(generic.TemplateView):
    template_name = 'lister/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class EditReadersView(generic.ListView):
    template_name = 'lister/edit_readers.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EditReadersView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns the all readers, which owner is current user.
        """
        return Reader.objects.filter()


class PrepareTableView(generic.FormView):
    template_name = 'lister/prepare_table.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrepareTableView, self).dispatch(*args, **kwargs)


class LoggedOutView(generic.TemplateView):
    template_name = 'registration/logged_out.html'

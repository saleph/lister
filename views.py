from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy

from .models import Reader


class IndexView(generic.TemplateView):
    template_name = 'lister/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class ShowReadersView(generic.ListView):
    model = Reader
    template_name = 'lister/show_readers.html'
    context_object_name = 'readers_list'
    user = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.get_user(request)
        return super(ShowReadersView, self).dispatch(request, *args, **kwargs)

    def get_user(self, request):
        """Gets user from current request."""
        self.user = request.user

    def get_queryset(self):
        """
        Returns the all readers, which owner is current user.
        """
        return Reader.objects.filter(owner=self.user)


class PrepareTableView(generic.FormView):
    template_name = 'lister/prepare_table.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrepareTableView, self).dispatch(request, *args, **kwargs)


class DeleteReaderView(generic.DeleteView):
    model = Reader
    success_url = reverse_lazy('lister:show_readers')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteReaderView, self).dispatch(request, *args, **kwargs)

class ReaderDetailView(generic.DetailView):
    model = Reader
    template_name = 'lister/reader_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReaderDetailView, self).dispatch(request, *args, **kwargs)

class LoggedOutView(generic.TemplateView):
    template_name = 'registration/logged_out.html'

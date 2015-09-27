from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(generic.TemplateView):
    template_name = 'lister/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

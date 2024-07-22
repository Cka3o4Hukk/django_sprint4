from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render


class About(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html', status=403)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию;
    # выводить её в шаблон пользовательской страницы 404 мы не станем.
    return render(request, 'core/404.html', status=404)


#def server_error(request):
#    return render(request, 'pages/500.html', status=500)

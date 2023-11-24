from django.views.generic import ListView, DetailView

from companies.models import Company


class CompaniesView(ListView):
    template_name = 'companies/index.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        return Company.objects.all()


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/details.html'
    context_object_name = 'company'

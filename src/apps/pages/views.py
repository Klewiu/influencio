from django.shortcuts import render
from apps.pages.models import Movie
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import MovieFilter


# Create your views here.


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class MoviesView (AdminStaffRequiredMixin, FilterView):
    model=Movie
    template_name = 'pages/home.html'
    filterset_class = MovieFilter
    paginate_by = 10

    def get_queryset(self):
      qs = self.model.objects.all()
      movie_filtered_list = MovieFilter(self.request.GET, queryset=qs)
      return movie_filtered_list.qs


class HotTopView (AdminStaffRequiredMixin, FilterView):
    model=Movie
    template_name = 'pages/hot.html'
    filterset_class = MovieFilter
    paginate_by = 10

    
    def get_queryset(self):
        category_qs= self.model.objects.filter(category="HOT-TOP")
        return category_qs



# def home(request):

#     context = {
      
#         'title':'Strona główna',
#       }

#     return render (request,'pages/home.html', context)


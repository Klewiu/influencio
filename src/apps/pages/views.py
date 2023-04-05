from django.shortcuts import render
from apps.pages.models import Movie, IpModel
from .models import Post
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import MovieFilter
from django.contrib import messages
from django.core.mail import send_mail

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# Create your views here.

# Admin Staff Mixin
# class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser or self.request.user.is_staff

##################### CLASS - BASED VIEWS #####################

# Home View - all movies without category filter and django-filter

@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class MoviesView (FilterView):
    model = Movie
    template_name = 'pages/home.html'
    filterset_class = MovieFilter
    paginate_by = 6
    
    

# query_set for dajango-filter
    def get_queryset(self):
        qs = self.model.objects.all()
        movie_filtered_list = MovieFilter(self.request.GET, queryset=qs)
        return movie_filtered_list.qs.order_by('-date_posted')

# pass new query_set to template to work with promotion zone apart from paginator and search field(django-filter)
    def get_context_data(self, **kwargs):
        context = super(MoviesView, self).get_context_data(**kwargs)
        context['movie_promotions'] = Movie.objects.all()
        context['submitButton'] = 'Szukaj'
        context['title'] = ' Strona Główna'
        return context

# Hot-Top View - parent is MoviesView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class TravelView (MoviesView):
    category = 'TRAVEL'

    # query_set for dajango-filter with category filter
    
    def get_queryset(self):
        category_qs = self.model.objects.filter(category=self.category)
        return category_qs.order_by('-date_posted')

    # pass a context=label for submit Button that search movies in chosen category
    def get_context_data(self, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        context['submitButton'] = f'Szukaj w {self.category}'
        context['title'] = f' {self.category}'
        return context

# Mix View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class MixView (MoviesView):
    template_name = 'pages/mix.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        movie_filtered_list = MovieFilter(self.request.GET, queryset=qs)
        return movie_filtered_list.qs.order_by('?') # Question mark gives us random results #

# Odkrycia View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class OdkryciaView (TravelView):
    category = 'ODKRYCIA'

# Beauty View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class BeautyView (TravelView):
    category = 'BEAUTY'

# Funny View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class FunnyView (TravelView):
    category = 'ŚMIESZNE'

# Gamming View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class GamingView (TravelView):
    category = 'GAMING'

# Lifestyle View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class LifestyleView (TravelView):
    category = 'LIFESTYLE'

# Sport View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class SportView (TravelView):
    category = 'SPORT'

# Sport View - prarent is HotTopView
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class SztukaView (TravelView):
    category = 'SZTUKA'

#Creators List View - Lista Twórców
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class CreatorsView (ListView):
    model = Movie
    template_name = 'pages/creators.html'
    queryset = Movie.objects.values('author').distinct()
    ordering = ["author"]
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Lista Twórców'
        return context


#Articles View
@method_decorator(cache_page(60 * 60 * 2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class ArticlesListView(ListView):
    model = Post
    template_name = 'pages/articles.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' Artykuły'
        return context
    

##################### FUNCTION VIEWS #####################

#privacy view

def privacy(request):
    context = {
        'title':' Polityka Prywatności',
      }
    return render (request,'pages/privacy.html', context )

#about view

def about(request):
    context = {
        'title':' O Influencio',
      }
    return render (request,'pages/about.html', context )

#contact view with contact form

def contact(request):
    
    spam_list = ['Robot','pieniądze','robot',"BTC","help","Capital","crypto","Crypto","Financial","salary","millionaire","sex"]
    
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        if message_name and message_email and message:
            if ('Crytofet') in message_name:
                messages.warning(request, 'Nie przyjmujemy spamu!')
            elif ('@pinkinbox.org') in message_email:
                messages.warning(request, 'Nie przyjmujemy spamu!')
            elif any(spam in message for spam in spam_list):
                messages.warning(request, 'Nie przyjmujemy spamu!')
            else:
                send_mail(
                    f'Formularz Kontaktowy, wiadomość od {message_name}',
                    f'Wiadomość z formularza kontaktowego INFLUENCIO.PL\n Użytkownik: {message_name}\n Email: {message_email}\n Wiadomość: {message}',
                    message_email,
                    ['kontakt.influencio@gmail.com'],)
                messages.success(request, f'Dziękujemy za kontakt {message_name}, Twój email został wysłany ! ')
        else:
            messages.warning(request, 'Wypełnij wszystkie pola formularza przed wysłaniem !')

        context = {
            'message_name': message_name,
            'message_email': message_email,
            'message': message,
            'title':' Kontakt',
        }

        return render(request, 'pages/contact.html', context)

    else:
        context = {
        'title':' Kontakt',
    }
        return render(request, 'pages/contact.html', context)



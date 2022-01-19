from django.shortcuts import render
from apps.pages.models import Movie, IpModel
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import MovieFilter
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.

# Admin Staff Mixin
# class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_superuser or self.request.user.is_staff

##################### CLASS - BASED VIEWS #####################

# Home View - all movies without category filter and django-filter

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
        return context

# Hot-Top View - parent is MoviesView

class HotTopView (MoviesView):
    category = 'HOT-TOP'
    # query_set for dajango-filter with category filter
    
    def get_queryset(self):
        category_qs = self.model.objects.filter(category=self.category)
        return category_qs.order_by('-date_posted')

    # pass a context=label for submit Button that search movies in chosen category
    def get_context_data(self, **kwargs):
        context = super(__class__, self).get_context_data(**kwargs)
        context['submitButton'] = f'Szukaj w {self.category}'
        return context

# Odkrycia View - prarent is HotTopView
class OdkryciaView (HotTopView):
    category = 'ODKRYCIA'

# Beauty View - prarent is HotTopView
class BeautyView (HotTopView):
    category = 'BEAUTY'

# Funny View - prarent is HotTopView
class FunnyView (HotTopView):
    category = 'ŚMIESZNE'

# Gamming View - prarent is HotTopView
class GamingView (HotTopView):
    category = 'GAMING'

# Lifestyle View - prarent is HotTopView
class LifestyleView (HotTopView):
    category = 'LIFESTYLE'

# Sport View - prarent is HotTopView
class SportView (HotTopView):
    category = 'SPORT'
   

##################### FUNCTION VIEWS #####################

#privacy view

def privacy(request):
    context = {
        'title':'Polityka Prywatności',
      }
    return render (request,'pages/privacy.html', context )

#about view

def about(request):
    context = {
        'title':'O Influencio',
      }
    return render (request,'pages/about.html', context )

#contact view with contact form

def contact(request):

    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        if message_name and message_email and message:
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
        }

        return render(request, 'pages/contact.html', context)

    else:
        context = {
        
    }
        return render(request, 'pages/contact.html', context)


    
    

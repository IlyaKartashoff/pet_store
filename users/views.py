from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("index"))
    else:
        
        
        form = UserLoginForm()
    context = {
        "form": form,
    }
    return render(request, "users/login.html", context)

class UserRegistrationView(CreateView):
    """Контроллер для регистрации пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url =reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'Store - Регистрация'
        return context
    

class UserProfileView(UpdateView):
    """Контроллер для профиля, отображения и обновления информации пользователя"""
    model = auth.get_user_model()
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))
    
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context
    
    
    

# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрировались!')
#             return HttpResponseRedirect(reverse("users:login"))
#     else:
#         form = UserRegistrationForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "users/registration.html", context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)

#     baskets = Basket.objects.filter(user=request.user)
#     total_sum = sum(basket.sum() for basket in baskets)
#     total_quantity = sum(basket.quantity for basket in baskets)

#     # for basket in baskets:
#     #     total_sum += basket.sum()
#     #     total_quantity += basket.quantity

#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#         'total_sum': total_sum,
#         'total_quantity': total_quantity,
#     }
#     return render(request, "users/profile.html", context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
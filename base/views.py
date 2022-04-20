from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect, render
from django.db import transaction

from .models import Task
from .forms import PositionForm


class UserLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasklist')


class UserLogoutView(LogoutView):
    next_page = 'login'


# class UserRegisterView(FormView):
#     template_name = 'base/register.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('tasklist')
#     redirect_authenticated_user = True
#
#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             login(self.request, user)
#         return super(UserRegisterView, self).form_valid(form)
#
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('tasklist')
#         return super(UserRegisterView, self).get(*args, **kwargs)

def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User Name Taken")
                return redirect('register')

            else:
                user = User.objects.create_user(first_name='first_name', last_name='last_name', username=username,
                                                password=password1, email=None)
                user.save()
                if user is not None:
                    login(request, user)
                return redirect('tasklist')
        else:
            messages.info(request, "Password Not Matching")
            return redirect('register')

    else:
        return render(request, 'base/register.html')
    return redirect('tasklist')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/tasklist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # to create search functionality
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/taskdetail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasklist')
    template_name = 'base/taskcreate.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasklist')
    template_name = 'base/taskupdate.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/taskdelete.html'
    success_url = reverse_lazy('tasklist')


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasklist'))

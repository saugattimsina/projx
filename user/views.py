from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render

from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView,CreateView,ListView,DeleteView,FormView
from django.views.generic.edit import FormMixin

from .forms import UserGroup,UserCreationForm,UserEditForm,UserKeyForm,LoginForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login

# from view_breadcrumbs import CreateBreadcrumbMixin,ListBreadcrumbMixin
from .models import UserKey
User = get_user_model()


class UserDetailView(LoginRequiredMixin, FormMixin,DetailView):

    model = User
    form_class = UserEditForm
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name="users/user_detail.html"

    pk = id
    
    def get_success_url(self):
        # return reverse('users:detail', kwargs={'username': self.object.username})
        return reverse("users:detail", kwargs={"username": self.object.username})

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        wallet = UserKey.objects.filter(user=self.object).first()
        context['form'] = UserEditForm(instance=self.object)
        context['wallet'] = wallet
        return context

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class GroupView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = reverse_lazy('users:login')
    permission_required = ('auth.add_group',)
    form_class= UserGroup
    template_name="users/group.html"
    # context_obj_name="form"
    success_url = reverse_lazy('users:group-list')
    success_message = "%(name)s was created successfully!"


class GroupList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    login_url = reverse_lazy('users:login')
    permission_required = ('auth.view_group',)
    model = Group
    context_object_name='obj'
    template_name = "users/group_list.html"


class ListUsersView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    login_url = reverse_lazy('users:login')
    permission_required = ('users.view_user',)
    model = User
    ordering = "-id"
    context_object_name='obj'    
    template_name = "users/list.html"

class GroupEditView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:login')
    permission_required = ('auth.change_group',)
    model = Group
    form_class = UserGroup
    template_name = "users/edit_group.html"
    success_url = reverse_lazy('users:group-list')
    success_message = "%(name)s was updated successfully!"
    pk = id 


class GroupDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:login')
    permission_required = ('auth.delete_group',)
    model = Group
    template_name = "users/delete_group.html"
    success_url = reverse_lazy('users:user_list')
    # success_message = "%(name)s was deleted successfully!"
    pk = id


class UserCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = reverse_lazy('users:login')
    permission_required = ('users.add_user',)
    model = User
    form_class = UserCreationForm
    template_name = "users/create_user.html"
    success_url = reverse_lazy('users:user_list')
    add_home = False
    # success_message = "%(name)s was created successfully!"
    def form_valid(self, form):
        # self.object = personal_form(self.request.POST or None)        
        if form.is_valid():
            user = form.save(commit=False)

            # Cleaned(normalized) data
            # username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #  Use set_password here
            user.set_password(password)
            user.save()
            return super().form_valid(form)

    # def form_valid(self, form):
    #     if form.is_valid():
    #         user = form.save(commit=False)

    #         # Cleaned(normalized) data
    #         # username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']

    #         #  Use set_password here
    #         user.set_password(password)
    #         user.save()
    #         return super().form_valid(form)
            
class UserEditView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = reverse_lazy('users:login')
    permission_required = ('users.change_user',)
    model = User
    form_class = UserEditForm
    template_name = "users/edit_user.html"
    success_url = reverse_lazy('users:user_list')
    pk = id
    def form_valid(self, form):
        print(form)
        # self.object = personal_form(self.request.POST or None)        
        if form.is_valid():
            user = form.save(commit=False)

            # Cleaned(normalized) data
            # username = form.cleaned_data['username']

            # password = form.cleaned_data['password']
            # # print("new pass",password)
            # #  Use set_password here
            # if password:
            #     # print("insidenew")
            #     user.set_password(password)
            user.save()
            # else:
            #     # print("not in new")
            #     user.save()
            return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = reverse_lazy('users:login')
    permission_required = ('users.delete_user',)
    model = User
    template_name = "users/delete_user.html"
    success_url = reverse_lazy('users:list')
    pk = id

class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    success_url = reverse_lazy('enq:dashboard')
    success_message = "%(name)s password was updated successfully!"
    template_name = 'users/password_change.html'


change_password_view = UserPasswordChange.as_view()


def change_user_password(request,id):
    user_obj=User.objects.get(id=id)
    if request.method=="POST":
        form=PasswordChangeForm(data=request.POST,user=user_obj)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('enq:dashboard'))
        else:
            return render(request,'users/password_change_user.html',context={'form':form,'id':user_obj.id})
    else:
        form = PasswordChangeForm(user=user_obj)
        try:
            return render(request,'users/password_change_user.html',context={'form':form,'id':user_obj.id})
        except Exception as exc:
            return render(request,'users/password_change_user.html',context={'form':form,'id':user_obj.id})
        



class CreateKeyView(CreateView):
    model = UserKey
    form_class = UserKeyForm
    template_name = "users/create_key.html"
    success_url = "/" 


class UserLoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"

    def post(self, request):
        form = self.form_class(request.POST)  # Initialize the form with POST data
        if form.is_valid():

            print(form.cleaned_data)  # This will print the cleaned form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # user = authenticate(username=username, password=password)
            user = User.objects.filter(username=username).first()
            if user: 
                # and user.is_staff:
                login(request, user)
                return redirect('/list')
            else:
                return render(request, self.template_name, {'form': form,"message":f"{user} username or password is incorrect"})
        else:
            # Handle the case when the form is not valid
            # You might want to render the form again with errors
            return render(request, self.template_name, {'form': form, 'message':"invalid data"})


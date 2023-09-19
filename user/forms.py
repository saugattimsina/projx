# from allauth.account.forms import SignupForm
# from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import Group

# User = get_user_model()
from .models import User,UserKey

class UserKeyForm(forms.ModelForm):
    class Meta:
        model = UserKey
        fields = '__all__'

class UserCreationForm(forms.ModelForm):
    # confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',
                #   'cell_number_1','cell_number_2','home_number','address',
                  'password','groups',
                  'is_staff','is_active','is_client')
        # fields = ('company_name','contact_person','contact_number','address','username','email','password','groups','image','is_staff','is_agent')
        # password = forms.PasswordInput(requ)
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            # 'cell_number_1':forms.TextInput(attrs={'class':'form-control'}),
            # 'cell_number_2':forms.TextInput(attrs={'class':'form-control'}),
            # 'home_number':forms.TextInput(attrs={'class':'form-control'}),
            # 'address':forms.TextInput(attrs={'class':'form-control'}),    
            
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            # 'confirm_password':forms.PasswordInput(attrs={'class':'form-control'}),
            'groups':forms.SelectMultiple(attrs={"class": "select2 form-control","multiple":"","tabindex":"-1","aria-hidden":"true","style":"height: 36px;width: 100%;"}),
            'is_staff':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_active':forms.CheckboxInput(attrs={'class':'form-control'}),
            # 'is_agent':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_client':forms.CheckboxInput(attrs={'class':'form-control'}),
        }


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


# class UserSignupForm(SignupForm):
#     """
#     Form that will be rendered on a user sign up section/screen.
#     Default fields will be added automatically.
#     Check UserSocialSignupForm for accounts created from social.
#     """


# class UserSocialSignupForm(SocialSignupForm):
#     """
#     Renders the form when user has signed up using social accounts.
#     Default fields will be added automatically.
#     See UserSignupForm otherwise.
#     """

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',
        # 'cell_number_1','cell_number_2','home_number','address',
        'password','groups',
                  'is_staff','is_active','is_client')
        # fields = ('company_name','contact_person','contact_number','address','username','email','password','groups','image','is_staff','is_agent')
        # password = forms.PasswordInput(requ)
        exclude = ('password',)
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            # 'cell_number_1':forms.TextInput(attrs={'class':'form-control'}),
            # 'cell_number_2':forms.TextInput(attrs={'class':'form-control'}),
            # 'home_number':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),    
            
            # 'password':forms.PasswordInput(attrs={'class':'form-control'}),
            # 'confirm_password':forms.PasswordInput(attrs={'class':'form-control'}),
            'groups':forms.SelectMultiple(attrs={"class": "select2 form-control","multiple":"","tabindex":"-1","aria-hidden":"true","style":"height: 36px;width: 100%;"}),
            'is_staff':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_active':forms.CheckboxInput(attrs={'class':'form-control'}),
            # 'is_agent':forms.CheckboxInput(attrs={'class':'form-control'}),
            'is_client':forms.CheckboxInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # self.fields['password'].required = False

        # fields = ('username','email','groups','is_staff')
        # widgets={
        #     'username':forms.TextInput(attrs={'class':'form-control'}),
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     'groups':forms.SelectMultiple(attrs={"class": "select2 form-control","multiple":"","tabindex":"-1","aria-hidden":"true","style":"height: 36px;width: 100%;"}),
        #     'is_staff':forms.CheckboxInput(attrs={'class':'form-control'}),
        # 
        # }

class UserGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'permissions':forms.SelectMultiple(attrs={"class": "select2 form-control","multiple":"","tabindex":"-1","aria-hidden":"true","style":"height: 36px;width: 100%;"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
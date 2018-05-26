from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'type': "text", 'id': "inputEmail", 'class': "form-control", 
                                    'placeholder': "Username", 'required':"", 'autofocus':""}),
                                max_length=30,
                                required=True,
                                help_text='Usernames may contain <strong>alphanumeric</strong>,\
                                             <strong>_</strong> and <strong>.</strong> characters')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': "password", 'id': "inputPassword", 'class': "form-control",
                                         'placeholder': "Password", 'required': ""}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
       
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"type": "text", "name": "name", "class": "form-control", 
                                                            "id": "name", "placeholder": "John Doe", "required": "", 
                                                            "autofocus": ""}),
                                max_length=30,
                                required=True,
                                help_text='Usernames may contain <strong>alphanumeric</strong>,\
                                             <strong>_</strong> and <strong>.</strong> characters')
    email = forms.CharField(widget=forms.TextInput(attrs={"type": "text", "name": "email", "class": "form-control", 
                                                        "id":"email", "placeholder":"you@example.com", "required": "",
                                                         "autofocus": ""}),
                            max_length=75,
                            required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "name": "password", 
                                                                "class": "form-control", "id":"password", 
                                                                "placeholder":"Password", "required": ""}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"type": "password", "name": "password-confirmation", 
                                                                "class": "form-control", "id":"password-confirm", 
                                                                "placeholder":"Confirm Password", "required": ""}),
                                        label="Confirm your password",
                                        required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password'] 

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)


    def clean(self):
        super(UserForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data
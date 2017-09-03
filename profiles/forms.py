from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторить пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = {'email','username',}

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qsu = User.objects.filter(username__iexact=username)
        if qsu.exists():
            raise forms.ValidationError("Такой логин уже существует")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Данный почтовый адрес используется другим пользователем")
        return email

    def clean_password2(self):
        #Traslite
        #check that the two passord entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # create a new user hash for activating email
        if commit:
            user.save()
            user.profile.send_activation_email()
        return user
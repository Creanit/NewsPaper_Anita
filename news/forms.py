from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=20)
    class Meta:
       model = Post
       fields =  [
           'author',
            'title',
            'content',
            'post_categories',
       ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Текст статьи/новости не должно быть идентичен заголовку."
            )

        return cleaned_data

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

#class PostForm(forms.ModelForm):
#   class Meta:
#       model = Post
#       fields = '__all__'


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django import forms
from .models import Owner, Reviewer

from django.utils.safestring import mark_safe

class CustomErrorList(ErrorList):

    def __str__(self):

        if not self:

            return ''

        return mark_safe(''.join([ f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))


class CustomUserCreationForm(UserCreationForm):

    role_choices = [
        ('isOwner', 'I own a restaurant and want reviews'),
        ('isReviewer', 'I want to review restaurants'),
    ]

    selected_choices = forms.MultipleChoiceField(
        choices=role_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_selected_choices(self):
        selected_items = self.cleaned_data.get('selected_choices')
        
        # Require at least one checkbox
        if not selected_items:
            raise forms.ValidationError("Please select at least one option.")
            
        return selected_items
    
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('selected_choices',)

    def __init__(self, *args, **kwargs):

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:

            self.fields[fieldname].help_text = None

            self.fields[fieldname].widget.attrs.update(

                {'class': 'form-control'}

            )
        
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=True)
        selected_choices = self.cleaned_data.get('selected_choices', [])
        
        if 'isOwner' in selected_choices:
            Owner.objects.create(user=user)

        if 'isReviewer' in selected_choices:
            Reviewer.objects.create(user=user)

        return user

        
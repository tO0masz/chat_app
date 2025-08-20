from django import forms
from . import models
from user_auth.models import get_friends

class NewChatForm(forms.ModelForm):
    class Meta:
        model = models.Chat
        fields = [
            'name',
            'participants'
        ]
        widgets={
            'participants': forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        if 'single_user' in kwargs:
            user = kwargs.pop('single_user')
            super().__init__(*args, **kwargs)
            self.fields['participants'].queryset = user
            self.initial['participants'] = list(user.values_list('id', flat=True))
            self.fields['participants'].disabled = True
        else:
            user = kwargs.pop('user')
            super().__init__(*args, **kwargs)
            self.fields['participants'].queryset = get_friends(user)
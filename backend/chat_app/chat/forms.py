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
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = get_friends(user)

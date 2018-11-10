from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'required': True,
                   }))
    reply_to = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'required': True,
                   }))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 10, 
                   'class': 'form-control',
                   'required': True,
                   }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Your name:'
        self.fields['reply_to'].label = 'Your email:'
        self.fields['message'].label = 'Message:'

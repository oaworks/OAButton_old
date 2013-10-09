from django import forms

class SigninForm(forms.Form):
    PRIVACY_CHOICES =  (
            ('PUBLIC', 'Public'),
            ('PRIVATE', 'Private'),
        )

    email = forms.EmailField(required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Email address (required)'})
            )
    name = forms.CharField(required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
            )
    profession = forms.CharField(required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Profession'})
            )
    university = forms.CharField(required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Institution'})
            )
    privacy =  forms.ChoiceField(required=True, choices=PRIVACY_CHOICES,)

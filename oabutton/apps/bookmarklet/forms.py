from django import forms


class OpenAccessForm(forms.Form):
    author_email = forms.EmailField(required=True,
                                    label='Author Email address',
                                    widget=forms.TextInput(attrs={'placeholder': 'Email address (required)'}))

    blocked_url = forms.URLField(required=True,
                                 label='Paywalled Article URL',
                                 widget=forms.TextInput())

    open_url = forms.URLField(required=True,
                              label='Open Access URL',
                              widget=forms.TextInput(attrs={'placeholder': 'Open Access URL'}))

    slug = forms.CharField(widget=forms.HiddenInput, required=True)

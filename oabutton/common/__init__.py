from django import forms


class SigninForm(forms.Form):
    PRIVACY_CHOICES = (('PUBLIC', 'Public'),
                       ('PRIVATE', 'Private'))

    email = forms.EmailField(required=True,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Email address (required)'}))
    name = forms.CharField(required=False,
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Full Name'}))
    profession = forms.CharField(required=False,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Profession'}))
    university = forms.CharField(required=False,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'Institution'}))
    privacy = forms.ChoiceField(required=True, choices=PRIVACY_CHOICES,)


class Bookmarklet(forms.Form):
    name = forms.CharField(required=True,
                           label="Your name",
                           widget=forms.TextInput(
                               attrs={'placeholder': 'e.g. Dr John Doe',
                                      'data-remember': "data-remember",
                                      'class': 'input-block-level',
                                      }))

    accessed = forms.CharField(widget=forms.HiddenInput,
                               required=False)

    profession = forms.CharField(required=False,
                                 label="Profession",
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'e.g. Doctor',
                                            'data-remember': "data-remember",
                                            'class': "input-block-level"}))

    remember = forms.BooleanField(required=False)

    location = forms.CharField(required=False,
                               label="Location",
                               widget=forms.TextInput(
                                   attrs={'placeholder': "e.g. London, United Kingdom",
                                          'class': "input-block-level"}))

    coords = forms.CharField(widget=forms.HiddenInput, required=False)

    doi = forms.CharField(required=False,
                          label="DOI",
                          widget=forms.TextInput(attrs={'class': "input-block-level"}))

    url = forms.URLField(required=True,
                         label='Article URL',
                         widget=forms.TextInput(
                             attrs={'placeholder': "http://www.publisher.com/journal?id=XXXX",
                                    'class': "input-block-level"}))

    story = forms.CharField(required=False,
                            label="Why do you need access?",
                            widget=forms.Textarea(
                                attrs={'rows': "4",
                                       'placeholder': "e.g. I'm trying to save lives, dammit!",
                                       'class': "input-block-level"}))

    description = forms.CharField(required=False,
                                  label="Description",
                                  widget=forms.Textarea(
                                      attrs={'placeholder': 'Title, Authors, Journal',
                                             'data-remember': "data-remember",
                                             'rows': '4',
                                             'class': "input-block-level"}))

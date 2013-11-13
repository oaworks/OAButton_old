from django import forms
import json

class SigninForm(forms.Form):
    PROFESSION_CHOICES = (('STUDENT', 'Student'),
                          ('DOCTOR', 'Doctor'),
                          ('PATIENT', 'Patient'),
                          ('ADVOCATE', 'Advocate'),
                          ('OTHER', 'Other'),
                          ('ACADEMIC', 'Academic'),
                          ('RESEARCHER', 'Researcher'),
                          ('BLANK', 'Prefer not to say'))

    email = forms.EmailField(required=True,
                             label='Email address',
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Email address (required)'}))
    name = forms.CharField(required=True,
                           label="Full Name",
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Full Name (required)'}))

    profession = forms.ChoiceField(required=True,
                                   label="Profession",
                                   choices=PROFESSION_CHOICES)

    confirm_public = forms.BooleanField(label="I understand that information obtained by this button will be publicly accessible",
                                        required=True)

    mailinglist = forms.BooleanField(label="I would like to be added to the Open Access Button Mailing List",
                                        required=False)


class Bookmarklet(forms.Form):
    accessed = forms.CharField(widget=forms.HiddenInput,
                               required=False)

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

class HomeData:
    team = json.loads('''[
          {
              "link": "http://twitter.com/Mcarthur_Joe",
              "thumb_url": "/static/img/joe.jpg",
              "name": "Joe",
              "twitter": "Mcarthur_Joe"
          },{
              "link": "http://twitter.com/davidecarroll",
              "thumb_url": "/static/img/david.jpg",
              "name": "David",
              "twitter": "davidecarroll"
          },{
              "link": "http://twitter.com/nicholascwng",
              "thumb_url": "https://secure.gravatar.com/avatar/9637895e310caf25237e89155157b2a7?s=200",
              "name": "Nick",
              "twitter": "nicholascwng"
          },{
              "link": "http://twitter.com/andylolz",
              "thumb_url": "https://secure.gravatar.com/avatar/bbb9eb1af3b427f8259df33f6e8844aa?s=200",
              "name": "Andy",
              "twitter": "andylolz"
          },{
              "link": "http://twitter.com/frathgeber",
              "thumb_url": "https://secure.gravatar.com/avatar/d178a6201be696c466c41c355c671707?s=200",
              "name": "Florian",
              "twitter": "frathgeber"
          },{
              "link": "#",
              "thumb_url": "/static/img/elliot.jpg",
              "name": "Elliot"
          }
      ]''')
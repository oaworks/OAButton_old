# coding: latin-1
from django import forms


class SigninForm(forms.Form):
    PROFESSION_CHOICES = (('Student', 'Student'),
                          ('Doctor', 'Doctor'),
                          ('Patient', 'Patient'),
                          ('Advocate', 'Advocate'),
                          ('Other', 'Other'),
                          ('Academic', 'Academic'),
                          ('Researcher', 'Researcher'),
                          ('Undisclosed', 'Prefer not to say'))

    email = forms.EmailField(required=True,
                             label='Email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Email address (required)'}))

    name = forms.CharField(required=True,
                           label="Full Name",
                           widget=forms.TextInput(attrs={'placeholder': 'Full Name (required)'}))

    profession = forms.ChoiceField(required=True,
                                   label="Profession",
                                   choices=PROFESSION_CHOICES)

    confirm_public = forms.BooleanField(label="I understand that information obtained by this button will be publicly accessible", required=True)

    mailinglist = forms.BooleanField(label="I would like to be added to the Open Access Button Mailing List", required=False)


class Bookmarklet(forms.Form):
    user_id = forms.CharField(widget=forms.HiddenInput, required=True)
    accessed = forms.CharField(widget=forms.HiddenInput, required=False)
    coords = forms.CharField(widget=forms.HiddenInput, required=False)

    location = forms.CharField(required=False, 
            label="Location", 
            widget=forms.TextInput(attrs={'placeholder': "e.g. London, United Kingdom", 
                'class': "form-control input-block-level"}))

    doi = forms.CharField(required=False, label="Digital Object Identifier (DOI)",
            widget=forms.TextInput(attrs={'class': "form-control input-block-level"},
                                    ))

    url = forms.URLField(required=True, label='Article URL',
            widget=forms.TextInput(attrs={'placeholder':
                "http://www.publisher.com/journal?id=XXXX", 'class': "form-control input-block-level"}))

    story = forms.CharField(required=False, label="Why do you need access?", 
            widget=forms.Textarea(attrs={'rows': "4",
                'placeholder': "e.g. I'm trying to save lives, dammit!", 
                'class': "form-control input-block-level"}))

    description = forms.CharField(required=False, label="Description",
            widget=forms.Textarea(attrs={'placeholder': 'Title, Authors, Journal', 'data-remember': "data-remember",
                'rows': '4', 'class': "form-control input-block-level"}))

teamdata = [{"name": "Joseph McArthur",
             "link": "http://twitter.com/Mcarthur_Joe",
             "thumb": "/static/img/joe.jpg",
             "twitter": "Mcarthur_Joe",
             "blurb": "Founder, pharmacology student and generally the guy who bugged everyone"
             }, {
            "name": "David Carroll",
            "link": "http://twitter.com/davidecarroll",
            "thumb": "https://pbs.twimg.com/profile_images/378800000708431454/2af90ed4438f3f1ae314f54948fd7d1d.png",
            "twitter": "davidecarroll",
            "blurb": "Founder, medical student and twitter addict"
            }, {
            "name": "Nicholas Ng",
            "link": "http://twitter.com/nicholascwng",
            "thumb": "https://secure.gravatar.com/avatar/9637895e310caf25237e89155157b2a7?s=200",
            "twitter": "nicholascwng",
            "blurb": "Awesome developer from the BMJ Hackday  who was instrumental in getting us 3rd place"
            }, {
            "name": "Andy Lulham",
            "link": "http://twitter.com/andylolz",
            "thumb": "https://1.gravatar.com/avatar/bbb9eb1af3b427f8259df33f6e8844aa?s=200",
            "twitter": "andylolz",
            "blurb": "Lead developer and central to the project from the first second at the BMJ hackday"
            }, {
            "name": "Florian Rathgeber",
            "link": "http://twitter.com/frathgeber",
            "thumb": "https://lh5.googleusercontent.com/-TQyLDuEMj1E/Umm1CqZohdI/AAAAAAAAZAA/PdCXgUG5d0Y/s200-no",
            "twitter": "frathgeber",
            "blurb": "Joined the project at the BMJ hackday and helped throughout providing solutions to our many problems"
            }, {
            "name": "Jez Cope",
            "link": "#",
            "thumb": "https://2.gravatar.com/avatar/6c1c67fa04add9cada803f13ae2ff050?d=https%3A%2F%2Fidenticons.github.com%2Fd21376bdaa2b8b7a308f9a28315bbd98.png&r=x&s=440",
            "blurb": "Lead Developer who designed and implemented a way for us to link papers behind paywalls to available copies"
            }, {
            "name": "Alf Eaton",
            "link": "#",
            "thumb": "/static/img/aperson.png",
            "blurb": "Developer at PeerJ who lended a hand at several points"
            }, {
            "name": "Ayesha Garrett",
            "link": "#",
            "thumb": "/static/img/aperson.png",
            "blurb": "Helped design much of the imaging around the project"
            }, {
            "name": "Victor Ng",
            "link": "#",
            "thumb": "http://www.gravatar.com/avatar/c5ab90719801dfa47055338ba47f5580.png",
            "blurb": "One of our best developers, instrumental in bring it to completion. Elsevier's biggest fan"
            }, {
            "name": "Oleg Lavrovsky",
            "link": "http://utou.ch",
            "thumb": "https://pbs.twimg.com/profile_images/378800000404422761/3bde338af1f5fcdbe24dda38ed36b9d1.jpeg",
            "twitter": "loleg",
            "blurb": "Lead designer and web developer, also creator of an awesome spin off, the Open Data Button"
            }, {
            "name": "Tom Pollard",
            "link": "#",
            "thumb": "/static/img/aperson.png",
            "blurb": "Developer. PhD student in University College London. Co-founder of Ubiquity Press"
            }, {
            "name": "Martin Paul Eve",
            "link": "#",
            "thumb": "https://0.gravatar.com/avatar/3645eb2857da226a58ca23a582a0b859?d=https%3A%2F%2Fidenticons.github.com%2Fea2c5f96ab2f153cc5389f62891168d2.png&r=x&s=440",
            "blurb": "Developer. Lecturer in English Literature. Director of Open Library of Humanities"
            }, {
            "name": "Emanuil Tolev",
            "link": "#",
            "thumb": "https://pbs.twimg.com/profile_images/378800000606651539/5651bffd1905807bcdd4b619d0a7e13d.jpeg",
            "blurb": "Developer. Computer Science Student. Associate at Cottage Labs"
            }, {
            "name": "Cameron Stocks",
            "link": "#",
            "thumb": "/static/img/aperson.png",
            "twitter": "",
            "blurb": "National Director of Medsin, the UK’s student global health network who provided great input"
            }, {
            "name": "Nicole Allen",
            "link": "#",
            "thumb": "https://pbs.twimg.com/profile_images/3151008497/5c42187852b2ef7e5492a6f6e792a21b.jpeg",
            "twitter": "",
            "blurb": "Open Educational Resources Program Director at SPARC who helped with training and project planning"
            }, {
            "name": "Nicholas Shockey",
            "link": "#",
            "thumb": "http://conf11.freeculture.org/files/2011/01/Nick-Shockey1.jpg",
            "twitter": "",
            "blurb": "Director of the Right to Research Coalition and of Student Advocacy at SPARC, who provided invaluable input at all stages"
            }, {
            "name": "Medsin UK",
            "link": "http://www.medsin.org/",
            "thumb": "http://www.medsin.org/public/images/medsin-ukmedium.png",
            "twitter": "MedsinUK",
            "blurb": "The Open Access Button is a Medsin-UK programme"
            }, {
            "name": "Right to Research Coalition",
            "link": "http://www.righttoresearch.org/",
            "thumb": "http://www.righttoresearch.org/bm~pix/r2r-logo.png",
            "twitter": "R2RC",
            "blurb": "An invaluable source of support, ideas and money"
            }
            ]

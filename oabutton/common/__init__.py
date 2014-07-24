# coding: latin-1
from django import forms


class SigninForm(forms.Form):
    PROFESSION_CHOICES = (('Student', 'Student'),
                          ('Doctor', 'Doctor'),
                          ('Patient', 'Patient'),
                          ('Advocate', 'Advocate'),
                          ('Academic', 'Academic'),
                          ('Researcher', 'Researcher'),
                          ('Librarian', 'Librarian'),
                          ('Other', 'Other'),
                          ('Undisclosed', 'Prefer not to say'))

    email = forms.EmailField(required=True,
                             label='Email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Email address (required)'}))

    name = forms.CharField(required=True,
                           label="Name",
                           widget=forms.TextInput(attrs={'placeholder': 'Name (required, preferably full name)'}))

    profession = forms.ChoiceField(required=True,
                                   label="Profession",
                                   choices=PROFESSION_CHOICES)

    confirm_public = forms.BooleanField(label="I understand that information obtained by this button will be publicly accessible", required=True)

    mailinglist = forms.BooleanField(label="I would like to be added to the Open Access Button Mailing List", required=False, initial=True)


class Bookmarklet(forms.Form):
    slug = forms.CharField(widget=forms.HiddenInput, required=True)
    accessed = forms.CharField(widget=forms.HiddenInput, required=False)
    coords = forms.CharField(widget=forms.HiddenInput, required=False)

    location = forms.CharField(required=False,
            label="Your location",
            widget=forms.TextInput(attrs={
                'placeholder': "e.g. London, United Kingdom",
                'class': "form-control input-block-level",
                # 'required': False
            }))

    doi = forms.CharField(required=False, label="Digital Object Identifier (DOI)",
            widget=forms.TextInput(attrs={'class': "form-control input-block-level"},
                                    ))

    url = forms.CharField(required=True, label='Article URL',
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
             "thumb": "/static/img/photo-joe.jpg",
             "twitter": "Mcarthur_Joe",
             "blurb": "Founder, project lead and apparently also a pharmacology student"
             }, {
            "name": "David Carroll",
            "link": "http://twitter.com/davidecarroll",
            "thumb": "/static/img/photo-david.jpg",
            "twitter": "davidecarroll",
            "blurb": "Founder, medical student and twitter addict"
            }, {
            "name": "Nicholas Ng",
            "link": "http://twitter.com/nicholascwng",
            "thumb": "https://secure.gravatar.com/avatar/9637895e310caf25237e89155157b2a7?s=144",
            "twitter": "nicholascwng",
            "blurb": "Awesome developer from the BMJ Hackday  who was instrumental in getting us 3rd place"
            }, {
            "name": "Andy Lulham",
            "link": "http://twitter.com/andylolz",
            "thumb": "https://1.gravatar.com/avatar/bbb9eb1af3b427f8259df33f6e8844aa?s=144",
            "twitter": "andylolz",
            "blurb": "Lead developer and central to the project from the first second at the BMJ hackday"
            }, {
            "name": "Florian Rathgeber",
            "link": "http://twitter.com/frathgeber",
            "thumb": "https://lh5.googleusercontent.com/-TQyLDuEMj1E/Umm1CqZohdI/AAAAAAAAZAA/PdCXgUG5d0Y/s144-no",
            "twitter": "frathgeber",
            "blurb": "Joined the project at the BMJ hackday and helped throughout providing solutions to our many problems"
            }, {
            "name": "Jez Cope",
            "link": "#",
            "thumb": "https://2.gravatar.com/avatar/6c1c67fa04add9cada803f13ae2ff050?s=144",
            "blurb": "Lead Developer who designed and implemented a way for us to link papers behind paywalls to available copies"
            }, {
            "name": "Alf Eaton",
            "link": "http://twitter.com/invisiblecomma",
            "thumb": "https://lh3.googleusercontent.com/-EHMuXvuZH1k/AAAAAAAAAAI/AAAAAAAAFeE/Z93Ix4IW-BY/s120-c/photo.jpg",
            "twitter": "invisiblecomma",
            "blurb": "Developer at PeerJ who lended a hand at several points"
            }, {
            "name": "Ayesha Garrett",
            "link": "http://londonlime.net/",
            "thumb": "/static/img/thumbs/851b0bf48a4eb7968873cfa622662c58.jpg",
            "twitter": "londonlime",
            "blurb": "Helped design much of the imaging around the project"
            }, {
            "name": "Victor Ng",
            "link": "#",
            "thumb": "/static/img/thumbs/c5ab90719801dfa47055338ba47f5580.jpeg",
            "blurb": "One of our best developers, instrumental in bring it to completion. Elsevier's biggest fan"
            }, {
            "name": "Oleg Lavrovsky",
            "link": "http://utou.ch",
            "thumb": "https://pbs.twimg.com/profile_images/378800000404422761/3bde338af1f5fcdbe24dda38ed36b9d1.jpeg",
            "twitter": "loleg",
            "blurb": "Lead designer and web developer, also creator of an awesome spin off, the Open Data Button"
            }, {
            "name": "Tom Pollard",
            "link": "https://twitter.com/tompollard",
            "thumb": "/static/img/thumbs/TomPollardPhoto.jpg",
            "twitter": "tompollard",
            "blurb": "Developer. PhD student in University College London. Co-founder of Ubiquity Press"
            }, {
            "name": "Martin Paul Eve",
            "link": "#",
            "thumb": "https://0.gravatar.com/avatar/3645eb2857da226a58ca23a582a0b859?s=144",
            "blurb": "Developer. Lecturer in English Literature. Director of Open Library of Humanities"
            }, {
            "name": "Emanuil Tolev",
            "link": "#",
            "thumb": "https://pbs.twimg.com/profile_images/378800000606651539/5651bffd1905807bcdd4b619d0a7e13d.jpeg",
            "blurb": "Developer. Computer Science Student. Associate at Cottage Labs"
            }, {
            "name": "Cameron Stocks",
            "link": "http://twitter.com/cam_stocks",
            "thumb": "https://pbs.twimg.com/profile_images/3666850209/e8c8b7281daccb2fcccae1f538c6d82a_bigger.jpeg",
            "twitter": "cam_stocks",
            "blurb": "National Director of Medsin, the UK’s student global health network, and founder"
            }, {
            "name": "Nicole Allen",
            "link": "https://twitter.com/txtbks",
            "thumb": "https://pbs.twimg.com/profile_images/3151008497/5c42187852b2ef7e5492a6f6e792a21b.jpeg",
            "twitter": "txtbks",
            "blurb": "Open Educational Resources Program Director at SPARC who helped with training and project planning"
            }, {
            "name": "Nicholas Shockey",
            "link": "#",
            "thumb": "/static/img/thumbs/Nick-Shockey1.jpg",
            "blurb": "Director of the Right to Research Coalition and of Student Advocacy at SPARC, who provided invaluable input at all stages"
            }, {
            "name": "Medsin",
            "link": "http://www.medsin.org/",
            "thumb": "/static/img/logo-medsin.jpg",
            "twitter": "medsin",
            "blurb": "The Open Access Button is a Medsin programme"
            }, {
            "name": "Right to Research Coalition",
            "link": "http://www.righttoresearch.org/",
            "thumb": "/static/img/thumbs/r2r-logo.png",
            "twitter": "R2RC",
            "blurb": "An invaluable source of support, ideas and money"
            }
            ]

thanksdata = [{
            "link": "http://opensciencefederation.com/",
            "name": "Open Science Federation"
            },{
            "link": "http://originalcontentlondon.com/",
            "name": "Original Content London"
            },{
            "link": "https://twitter.com/McDawg",
            "name": "Graham Steel"
            },{
            "link": "http://okfn.org/",
            "name": "Open Knowledge Foundation"
            },{
            "link": "http://rewiredstate.org/",
            "name": "Rewired State"
            },{
            "link": "http://www.bmj.com/",
            "name": "BMJ"
            },{
            "link": "http://www.plos.org/",
            "name": "PLOS"
            },{
            "link": "https://twitter.com/Protohedgehog",
            "name": "Jon Tennant"
            },{
            "link": "https://twitter.com/petermurrayrust",
            "name": "Peter Murray-Rust"
            },{
            "link": "http://sparc.arl.org/",
            "name": "SPARC"
            },{
            "link": "https://twitter.com/CameronNeylon",
            "name": "Cameron Neylon"
            },{
            "link": "https://twitter.com/evomri",
            "name": "Daniel Mietchen"
            }]

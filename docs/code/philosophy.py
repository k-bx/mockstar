# file sample_app/blog/forms.py

class PostForm(forms.Form):
    title = forms.CharField()
    content = forms.TextField()

    def clean(self):
        if is_post_exist(self.cleaned_data['title']):
            raise ValidationError(_(u"Post with this title already exists"))
        return self.cleaned_data

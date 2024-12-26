from django import forms
from movie_app.models import Movie


class insert_form(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
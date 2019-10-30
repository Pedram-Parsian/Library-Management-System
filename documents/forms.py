from django import forms


class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    text = forms.CharField(max_length=600, required=False)

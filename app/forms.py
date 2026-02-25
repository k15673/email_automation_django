from django import forms

class EmailForm(forms.Form):
    to=forms.EmailField()
    subject=forms.CharField()
    message=forms.CharField(widget=forms.Textarea)
    attachment=forms.FileField(required=False)
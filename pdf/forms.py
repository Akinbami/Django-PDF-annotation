from django import forms

# from pagedown.widgets import PagedownWidget

from .models import PDF


class PDFForm(forms.ModelForm):
    # title = forms.CharField(widget=PagedownWidget(show_preview=False))
    title = forms.CharField(widget=forms.TextInput(attrs={"type": "text", "class": "form-control",
                                                         "placeholder":"PDF title"}),
                                max_length=30,
                                required=True,
                               )
    comment = forms.CharField(widget=forms.TextInput(attrs={"type": "text", "class": "form-control",
                                                         "placeholder":"Commit Message"}),
                                max_length=30,
                                required=True,
                               )
    class Meta:
        model = PDF
        fields = [
            "title",
            "comment",
            "file",
            ]
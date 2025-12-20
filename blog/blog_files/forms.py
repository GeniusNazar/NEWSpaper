from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "description", "status", "category", "due_date"]

        def __init__(self, *args, **kwargs):
            super(ArticleForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({"class": "form-control"})

            self.fields["due_date"].widget.attrs["class"] += "my-custom=datepicker"


class ArticleFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ("", "Всі"),
        ("Технології", "Технології"),
        ("Кухня", "Кухня"),
        ("Навчання", "Навчання")
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label="Категорія")

    def __init__(self, *args, **kwargs):
        super(ArticleFilterForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs.update({"class": "form-control"})


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media']
        widgets = {
            "media": forms.FileInput()
        }
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

    def clean_text(self):
        data = self.cleaned_data['text']
        error = 'Поле "Текст поста" должно быть заполнено'
        if not data:
            raise forms.ValidationError(error)
        return data

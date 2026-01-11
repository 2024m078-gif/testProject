from django import forms
from .models import Post  # Postだけインポート

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=None,  # 一旦None
        empty_label="未選択",
        required=False
    )

    class Meta:
        model = Post
        fields = ("name", "content", "price", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category  # ここで遅延インポート
        self.fields['category'].queryset = Category.objects.all()

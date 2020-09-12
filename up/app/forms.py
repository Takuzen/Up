from django import forms

from .models import Item, Comment, Images
from ..users.models import User


class ItemForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """

    class Meta:
        model = Item
        fields = '__all__'

        # 以下のフィールド以外が入力フォームに表示される
        # AutoField
        # auto_now=True
        # auto_now_add=Ture
        # editable=False


class SignUpForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, label="パスワード")
    email = forms.EmailField(label="メールアドレス")

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class PostForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """

    restaurant_name = forms.CharField(required=False, label="",
                                      widget=forms.TextInput(
                                          attrs={
                                              'placeholder': 'タイトル',
                                          }
                                      ))

    restaurant_memo = forms.CharField(required=False, label="",
                                      widget=forms.TextArea(
                                          attrs={
                                              'placeholder': 'あなたの思いを記録しよう...',
                                          }
                                      ))

    class Meta:
        model = Item
        fields = ['restaurant_name', 'restaurant_memo']

        # 以下のフィールド以外が入力フォームに表示される
        # AutoField
        # auto_now=True
        # auto_now_add=Ture
        # editable=False


class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(required=False, label="",
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'あなたの気持ちを相手に伝えよう...',
                                       }
                                   ))

    class Meta:
        model = Comment
        fields = ['comment_text', ]
        labels = {
            "comment_text": ""
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    image.widget.attrs.update({'name': 'image', 'class': 'clearablefileinput', 'id': 'post_restaurant_image', 'multiple': True, 'required': True, 'accept': "image/*"})
    class Meta:
        model = Images
        fields = ('image', )

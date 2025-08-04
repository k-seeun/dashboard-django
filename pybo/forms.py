from django import forms
from .models import Post, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': '댓글을 입력하세요',
            }),
        }
        # 템플릿의 <h2> 태그가 라벨 역할을 하므로, 폼 라벨은 비워둡니다.
        labels = {'content': ''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': '게시글 제목을 입력하세요',
            }),
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': '내용을 입력하세요',
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
        }
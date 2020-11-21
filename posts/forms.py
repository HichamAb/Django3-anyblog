from django import forms 
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Post,Comment

  
class PostForm(forms.ModelForm): 
    content = forms.CharField( 
        widget=SummernoteWidget( 
            attrs={'required': False,} 
        ) 
    ) 
    class Meta: 
        model = Post
        fields = ('title','overview','content','thumbnail','categories','previous_post','next_post','featured')
class CommentForm(forms.ModelForm) : 
    content = forms.CharField(widget=forms.Textarea(attrs = {
        'class' :"form-control" , 
        'placeholder' : 'Type your comment',
        'id':'usercomment' , 
        'rows': 4 ,
    }))
    class Meta : 
        model = Comment
        fields = ('content',)
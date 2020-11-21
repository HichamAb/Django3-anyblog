from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . models import Category,Author,Post,Comment
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
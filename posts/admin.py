from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    #alterado herdado de admin para ->summernote
    list_display = ('id','titulo_post', 'autor_post','data_post','categoria_post','publicado_post',)
    list_editable = ('publicado_post',)
    list_display_links =('id', 'titulo_post',)#o que seja exibido
    summernote_fields = ('conteudo_post',)#os campos que teram summernotes

admin.site.register(Post, PostAdmin)
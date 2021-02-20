from django.contrib import admin
from .models import Comentario

# Register your models here.
class ComentarioAdmin(admin.ModelAdmin):
    #PARA MOSTRAR O QUE SERÁ EXIBIDO
    list_display = ('id', 'nome_comentario', 'email_comentario', 'post_comentario', 'data_comentario', 'publicado_comentario')
    list_editable = ('publicado_comentario',)
    #quais os links são clicaveis
    list_display_links = ('id', 'nome_comentario', 'email_comentario', )

admin.site.register(Comentario, ComentarioAdmin)
from django.db import models
# Create your models here.
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
#criando os campos do comentario
class Comentario(models.Model):
    nome_comentario=models.CharField(max_length=150, verbose_name='Nome')
    email_comentario=models.EmailField(verbose_name='E-mail')
    comentario=models.TextField(verbose_name='Comentário')
    post_comentario=models.ForeignKey(Post,on_delete=models.CASCADE)#quando um post for deletado tds os comentarios tbem serão apagados
    usuario_comentario=models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=True, null=True)#se um usuario for apagado os post não será deletado
    data_comentario=models.DateTimeField(default=timezone.now)
    publicado_comentario=models.BooleanField(default=False)

    def __str__(self):
        return self.nome_comentario #para poder retornar o label da categoria,comentario,etc

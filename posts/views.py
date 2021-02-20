from django.shortcuts import render, redirect
from django.views.generic.list import ListView # para cria  classe do view
from django.views.generic.edit import UpdateView #cria detalhes no post

from .models import Post
from django.db.models import Q,Count,Case, When
# Create your views here.

from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages

class PostIndex(ListView):
    #sobrescrevendo alguns objetos
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 2
    context_object_name = 'posts'#nome do objeto iteravel para pegar no index

    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.order_by('-id').filter(publicado_post=True)#para ordenar invertido, e filtrado se pulicado comentario ou não
        #para injetar comentarios
        qs=qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)#comentario=foreikey do post
                )
            )
        )

        return qs

class PostBuca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs=super().get_queryset()
        #para saer o termo da busca
        #print(self.request.GET.get('termo'))
        termo=self.request.GET.get('termo')
        #PARA SABER SE TERM O CONTEUDO DO TERMO BUSCA
        if not termo:
            return qs

        qs=qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs




class PostCategoria(PostIndex):
    template_name ='posts/post_categoria.html' #sorescrevendo da listview

    def get_queryset(self):
        qs = super().get_queryset()
        # para saber qual a categoria
        categoria = self.kwargs.get('categoria', None)  # print no self.kwargs()-dicionario-kwags
        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    #usará o formulario de comentarios
    form_class = FormComentario
    #abrindo com o nome do contexto
    context_object_name = 'post'

    #PARA PODER INJETAR OS COMENTARIO NA PAGINA
    def get_context_data(self, **kwargs):
        contexto=super().get_context_data(**kwargs)#CONTEXTO DO POST_DETALHES.HTML
        #pega o post atual
        post =self.get_object()
        comentarios=Comentario.objects.filter(publicado_comentario=True,post_comentario=post.id)
        #injetando novo contexto
        contexto['comentarios']=comentarios
        return contexto


    def form_valid(self,form):
        post=self.get_object()
        comentario=Comentario(**form.cleaned_data)
        comentario.post_comentario=post
        #verificar se o usuario esta logado ou não
        if self.request.user.is_authenticated:
            comentario.usuario_comentario=self.request.user

        comentario.save()
        messages.success(self.request,'Comentario enviado com sucesso. ')
        return redirect('post_detalhes',pk=post.id)#pk vindo da url




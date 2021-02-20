from django.forms import ModelForm
from .models import Comentario

class FormComentario(ModelForm):
    # validando formularios
    def clean(self):
        data =self.cleaned_data
        nome =data.get('nome_comentario')
        email = data.get('email_comentario')
        comentario = data.get('comentario')
        #print(data)

        if len(nome)<5:
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais que 5 letras'
            )#valida tamanho dos campos comentario
        #
        # if not comentario:
        #     self.add_error(
        #         'comentario',
        #         'Campo não pode ser acessado '
        #     )
    class Meta:
        model=Comentario
        fields=('nome_comentario', 'email_comentario', 'comentario')

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post #Import a classe Post do arquivo models que está dentro desta pasta(.)
from .forms import PostForm

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request, pk):
    post=get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

def post_new(request):
    if request.method=="POST": #Vai ver se a view está executando o retorno dos dados.(Form após clicar o botão de Salvar, e cuja elemento form tem o method setado como Post)
        form=PostForm(request.POST) #Obtém o formulário correspondente aos dados preenchidos na página. Para que posteriormente possa ter seu conteúdo verificado e enviado ao banco de dados caso seja um formulário válido.
        
        if form.is_valid(): #Verifica se todos os campos requeridos do form estão prontos, e os valores incorretos não serão salvos.
            post=form.save(commit=False) #Salva o formulário atual para retornar a instancia desse objeto, porém não o envia ao banco de dados.
            post.author=request.user #Define o autor da publicação atual como sendo o usuário atual.
            post.published_date=timezone.now() #Define a data de publicação como sendo a data atual de acordo com o fuso horário local.
            post.save() #Salva o objeto atual do Post que acabamos de criar, retorna a sua instância de objeto. E o envia  ao banco de dados(commit).

            return redirect('post_detail',pk=post.pk) #Após salvar a postagem recém criada no banco de dados, caso ela atenda aos requisitos de criação de formulário. Ele redireciona a página atual, para a página de detalhates de postagem correspondente a esta postagem.
    else:  #Vai ver se a view está executando essa página pela primeira vez, e não o retorno dos dados. Consequentemente deve retornar uma form vazia com os campos a serem preenchidos.
        form=PostForm()

    return render(request,'blog/post_edit.html',{'form':form})

def post_edit(request, pk):
    post=get_object_or_404(Post,pk=pk) #Procura pelo Post cuja chave primária seja igual a passada para essa view. Caso não encontra retorna um erro 404.

    if request.method=="POST":
        form=PostForm(request.POST, instance=post) #Obtém o formulário correspondente aos dados preenchidos na página, e a instância desse objeto Post em específico. Para que posteriormente possa ter seu conteúdo verificado e enviado ao banco de dados caso seja um formulário válido.

        if form.is_valid():
            post=form.save(commit=False)#Salva o formulário atual para retornar a instancia desse objeto, porém não o envia ao banco de dados.
            post.author=request.user#Define o autor da publicação atual como sendo o usuário atual.
            post.published_date=timezone.now()#Define a data de publicação como sendo a data atual de acordo com o fuso horário local.
            post.save()#Salva o objeto atual do Post que acabamos de criar, retorna a sua instância de objeto. E o envia  ao banco de dados(commit).

            return redirect('post_detail',pk=post.pk)#Após salvar a postagem recém editada no banco de dados, caso ela atenda aos requisitos de criação de formulário. Ele redireciona a página atual, para a página de detalhates de postagem correspondente a esta postagem.

    else: #Vai ver se a view está executando essa página pela primeira vez, e não a alteração dos dados. Consequentemente deve retornar uma form com os campos com os valores que forem fornecidos nesse post.
        form=PostForm(instance=post) #Cria uma instância de formulário, cujos dados sejam referentes ao Post com a chave primária fornecida.(Caso exista ou retorna erro)

    return render(request,'blog/post_edit.html',{'form':form})


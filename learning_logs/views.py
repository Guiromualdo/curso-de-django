from django.shortcuts import render # type: ignore
from .models import Topic, Entry # type: ignore
from .forms import TopicForm, EntryForm # type: ignore
from django.http import HttpResponseRedirect, Http404 # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.decorators import login_required



def index(request):
    """Página principal de learning_logs."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os assuntos."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas."""
    topic = Topic.objects.get(id=topic_id)

    #garante que o assunto pertence ao usuário logado.
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != 'POST':
        # Nenhum dado submetido foi enviado; cria um formulário em branco.
        form = TopicForm()
    else:
        # Dados de Post submetidos; processa os dados.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    # Exibe um formulário em branco ou inválido.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adiciona uma nova entrada para um assunto específico."""
    topic = Topic.objects.get(id=topic_id)

     #garante que o assunto pertence ao usuário logado.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco.
        form = EntryForm()
    else:
        # Dados de Post submetidos; processa os dados.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))

    # Exibe um formulário em branco ou inválido.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

     #garante que o assunto pertence ao usuário logado.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Solicitação inicial; preenche o formulário com os dados atuais da entrada.
        form = EntryForm(instance=entry)
    else:
        # Dados de Post submetidos; processa os dados.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    # Exibe um formulário com os dados atuais ou inválidos.
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
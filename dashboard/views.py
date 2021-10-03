from django import contrib
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from requests.api import request
from dashboard.models import Notes
from django.views.generic import *
from .forms import *
from youtubesearchpython import VideosSearch, search
import requests
import wikipedia
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Eslatma {request.user.username} tomonidan muvaffaqiyatli qo'shildi!")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {
        'notes':notes,
        'form':form,
    }
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDeatilView(DetailView):
    model = Notes


@login_required
def homework(request):
    if request.method == "POST":
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            try:
                finishedd = request.POST['finished']
                if finishedd == 'on':
                    finishedd = True
                else:
                    finishedd = False
            except:
                finishedd = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                finished = finishedd
            )
            homeworks.save()
            messages.success(request,f"Uy vazifa {request.user.username} tomonidan qo'shildi!!!")
    else:
        form = HomeWorkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks':homeworks,
        'homework_done':homework_done,
        'form':form,
    }
    return render(request, "dashboard/homework.html",context)


@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.finished == True:
        homework.finished = False
    else:
        homework.finished = True
    homework.save()

    return redirect("homework")
@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=20)
        result_list = []
        for x in video.result()['result']:
            result_dict = {
                'input':text,
                'title':x['title'],
                'duration':x['duration'],
                'thumbnail':x['thumbnails'][0]['url'],
                'channel':x['channel']['name'],
                'link':x['link'],
                'viewcount':x['viewCount']['short'],
                'published':x['publishedTime'],
            }
            desc = ''
            if x['descriptionSnippet']:
                for j in x['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list,
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    context = {
        'form':form,
    }
    return render(request, "dashboard/youtube.html",context)


@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finishedd = request.POST['finished'],
                if finishedd == "on":
                    finishedd = True
                else:
                    finishedd = False
            except:
                finishedd = False
            todoss = Todo(
                user = request.user,
                title = request.POST['title'],
                finished = finishedd
            )
            todoss.save()
            messages.success(request,f"Kun tartibi {request.user.username} tomonidan muvaffaqiyatli qo'shildi!")
    else:
        form = TodoForm()
    # todos = Todo.objects.filter(user=request.user)
    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        "todos":todos,
        "form":form,
        'todos_done':todos_done,
    }
    return render(request, "dashboard/todo.html",context)

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.finished == True:
        todo.finished = False
    else:
        todo.finished = True
    todo.save()

    return redirect("todo")
@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        # video = VideosSearch(text,limit=20)
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for x in range(10):
            result_dict = {
                'title':answer['items'][x]['volumeInfo']['title'],
                'subtitle':answer['items'][x]['volumeInfo'].get('subtitle'),
                'description':answer['items'][x]['volumeInfo'].get('description'),
                'count':answer['items'][x]['volumeInfo'].get('count'),
                'categories':answer['items'][x]['volumeInfo'].get('categories'),
                'rating':answer['items'][x]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][x]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][x]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list,
            }
        return render(request,'dashboard/books.html',context)
    else:
        form = DashboardForm()
    context = {
        'form':form,
    }
    return render(request, "dashboard/books.html",context)



def Dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        # video = VideosSearch(text,limit=20)
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                "form":form,
                "input":text,
                "phonetics":phonetics,
                "audio":audio,
                "definition":definition,
                "example":example,
                "synonyms":synonyms,
            }
        except:
            context = {
                "form":form,
                "input":'',
            }
        return render(request,'dashboard/dictionary.html',context)
    else:
        form = DashboardForm()
        context = {
        "form":form,
        }
    return render(request,'dashboard/dictionary.html',context)



def Wiki(request):
    if request.method == "POST":
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary,
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
        context = {
            "form":form,
        }
    return render(request,'dashboard/wiki.html',context)



def Conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['Process'] == 'lenght':
            measurement_form = ConversionLenghtForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                "input":True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'  
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer,
                }
        if request.POST['Process'] == 'mass':
            measurement_form = ConversionMasstForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                "input":True,
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'  
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer,
                }  
                

    else:
        form = ConversionForm()
        context = {
            "form":form,
            'input':False
        }
    return render(request, 'dashboard/conversion.html',context)



def Register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account {username} tomonidan muvaffaqiyatli yaratildi!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        "form":form,
    }
    return render(request, 'dashboard/register.html',context)
 

@login_required
def Profile(request):
    homeworks = Homework.objects.filter(finished=False,user=request.user)
    todos = Todo.objects.filter(finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        "homeworks":homeworks,
        "todos":todos,
        'homework_done':homework_done,
        'todos_done':todos_done,
    }
    return render(request, 'dashboard/profile.html',context)
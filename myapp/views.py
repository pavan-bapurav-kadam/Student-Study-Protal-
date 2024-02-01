from django.shortcuts import render,HttpResponseRedirect,redirect
from .models import Notes,homework,Todo
from .forms import NotesForm,homeworkForm,DashboardForm,todoForm,ConversionForm,ConversionLength,ConversionMassForm,UserRegistrtionForm
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import json
import wikipedia
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request,'dashbord/home.html')
    else:
        return HttpResponseRedirect('/login/')

def notes(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = NotesForm(request.POST)
            if form.is_valid():
                notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
                notes.save()
                form = NotesForm()
            messages.success(request,f"Notes Added from {request.user.username} Succesfully")    
        else:    
            form = NotesForm()
        notes = Notes.objects.filter(user=request.user)
        context = {'notes':notes,'form':form}
        return render(request,'dashbord/notes.html',context)
    else:
        return HttpResponseRedirect('/login/')

def Delete_note(request,pk=None):
    notes = Notes.objects.get(id=pk)
    notes.delete()
    messages.success(request,'Notes Are Delete Successfully')
    return HttpResponseRedirect('/notes/')



# class NotesDetailsViews(generic.DetailView):
#     model = Notes

def NotesDetail(request,id):
    note = Notes.objects.get(pk=id)
    return render(request,'dashbord/NotesDetails.html',{'note':note})    
#============= Home Work ================    
    
def Homework(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = homeworkForm(request.POST)
            if form.is_valid():
                try:
                    finished = request.POST['is_finished']
                    if finished == 'on':
                        finished = True
                    else:
                        finished = False
                except:
                    finished = False   
                work = homework(
                    user = request.user,
                    subject = request.POST['subject'],
                    title = request.POST['title'],
                    description = request.POST['description'],
                    due = request.POST['due'],
                    is_finished = finished
                )
                work.save()
                messages.success(request,f'Homework added form {request.user.username} !!!')
        form = homeworkForm()       
        work = homework.objects.filter(user=request.user)
        if len(work) == 0:
            work_done = True
        else:
            work_done = False    
        return render(request,'dashbord/homework.html',{'homework':work,'homework_done':work_done,'form':form})    
    else:
        return HttpResponseRedirect('/login/')



def homework_Delete(request,pk=None):
    work = homework.objects.get(id=pk)
    work.delete()
    messages.success(request,'Data is Deleted Sucessfully !')
    return HttpResponseRedirect('/homework/')


def homework_update(request,pk=None):    
    work = homework.objects.get(id=pk)
    if work.is_finished == True:
        work.is_finished == False
    else:
        work.is_finished == True
    work.save()        
    return HttpResponseRedirect('/homework')


#-------------------- You Tube Section ----------------------

def youtube(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = DashboardForm(request.POST,request.FILES)
            text = request.POST['text']
            video = VideosSearch(text,limit=10)
            result_list = []
            for i in video.result()['result']:
                result_dict = {
                    'input':text,
                    'input':i['title'],
                    'duration':i['duration'],
                    'thumbnail':i['thumbnails'][0]['url'],
                    'channel':i['channel']['name'],
                    'link':i['link'],
                    'views':i['viewCount']['short'],
                    'published':i['publishedTime'],
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description']=desc
                result_list.append(result_dict)
                
            return render(request,'dashbord/youtube.html',{'form':form,'results':result_list})                
        else:    
            form = DashboardForm()
        return render(request,'dashbord/youtube.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
        


#///////////////////////// To Do List ////////////////////////////

def Todos(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = todoForm(request.POST,request.FILES)
            if form.is_valid():
                try:
                    finished = request.POST['is_finished']
                    if finished == 'on':
                        finished = True
                    else:
                        finished = False
                except:
                    finished = False
                    todos = Todo(
                        user = request.user,
                        title = request.POST['title'],
                        is_finished = finished
                    )        
                    todos.save()
                    messages.success(request,'Todo Added Sucessfully !')
        form = todoForm()
        todo = Todo.objects.filter(user=request.user)
            
        return render(request,'dashbord/todo.html',{'todo':todo,'form':form})
    else:
        return HttpResponseRedirect('/login/')


def Delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return HttpResponseRedirect('/todo/')


def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()        
    return HttpResponseRedirect('/todo/')


# /////////////// / Book Section Start //////////////////




def books(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = DashboardForm(request.POST)
            text = request.POST['text']
            url = "https://www.googleapis.com/books/v1/volumes?q="+text
            r = requests.get(url)
            answer = r.json()
            result_list = []
            for i in range(10):
                result_dict = {
                    'input':answer['items'][i]['volumeInfo']['title'],
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description':answer['items'][i]['volumeInfo'].get('description'),
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':answer['items'][i]['volumeInfo'].get('categories'),
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                }
                
                result_list.append(result_dict)
                
            return render(request,'dashbord/books.html',{'form':form,'results':result_list})                

        else:    
            form = DashboardForm()

        return render(request,'dashbord/books.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')



# @@@@@@@@@@@@@@@@@@@@@@@@@@  Dictionary Secetion Start @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def Dictionary(request):
    if request.method=='POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        r = requests.get(url)
        answer = r.json()
        print(answer)
        # try:
        phonetics = answer[0]['phonetics'][0]['text']
        audio = answer[0]['phonetics'][0]['audio']
        defination = answer[0]['meanings'][0]['definitions'][0]['definition']
        synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

        context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'defination':defination,
                'synonyms':synonyms
        }
        print(form,text,phonetics,audio,defination,synonyms)
        # except:
        #     context = {
        #         'form':form,
        #         'input':''
        #     }    
        return render(request,'dashbord/dictionary.html',context)    
    else:        
        form = DashboardForm()
        context = {'form':form,'text':text}
    return render(request,'dashbord/dictionary.html',context)

# Wikipedia section++++++++++++++++++++++++++++++

def Wiki(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            text = request.POST['text']
            form = DashboardForm(request.POST)
            search = wikipedia.page(text)
            context ={
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary
            }
            return render(request,'dashbord/wiki.html',context)
        else:
            form = DashboardForm()
            context = {
                'form':form
            }
        return render(request,'dashbord/wiki.html',context)
    else:
        return HttpResponseRedirect('/login/')



#  ********************* Conversion Section start &&&&&&&&&&&&&&&&&&&&&&

def conversion(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ConversionForm(request.POST)
            if request.POST['measurement']=='length':
                measurement_form = ConversionLength()
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True
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
                    
            if request.POST['measurement']=='mass':
                measurement_form = ConversionMassForm()
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True
                }
                if 'input' in request.POST:
                    first = request.POST['measure1']
                    second = request.POST['measure2']
                    input = request.POST['input']
                    answer = ''
                    if input and int(input) >= 0:
                        if first=='pound' and second=='kilogram':
                            answer = f'{input} pound = {int(input)*0.453592} kilogram'
                        if first=='kilogram' and second=='pound':
                            answer = f'{input} kilogrem = {int(input)*2.20462} pound'

                    context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer,
                }
        else:    
            form = ConversionForm()
            context = {
            'form':form,
            'input':False
            }
        return render(request,'dashbord/conversion.html',context)
    else:
        return HttpResponseRedirect('/login/')



# ,,,,,,,,,,,,,,,,,,, ,,, Registration From Start  ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

# def register(request):
#     if request.method=='POST':
#         form = UserRegistrtionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request,f"Account created for {username} !!")
#             return HttpResponseRedirect('/login/')
#     else:
#         form = UserRegistrtionForm()
#     return render(request,'dashbord/register.html',{'form':form })


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        if request.method=='POST':
            pname = request.POST.get('uname')
            email = request.POST.get('email')
            password = request.POST.get('pass') 
            User.objects.create_user(pname,email,password)
            return HttpResponseRedirect('/login/')
        return render(request,'dashbord/register.html')

# $$$$$$$$$$$$$$$$ Login function Start     $$$$$$$$$$$$$$$$$$$$$


def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        if request.method=='POST':
            username = request.POST.get('uname')
            password = request.POST.get('pass')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/home/')
        return render(request,'dashbord/login.html')


# 22222222   2222222222  LOgout Page  222222222222

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# Profile Page Start\\\\\\\\\\\\\\\\\\\

def profile(request):
    if request.user.is_authenticated:
        Homework = homework.objects.filter(is_finished=False,user=request.user)
        todo = Todo.objects.filter(is_finished=False,user=request.user)
        if len(Homework)==0:
            Homework_done = True
        else:
            Homework_done = False    
        if len(todo)==0:
            todo_done = True
        else:
            todo_done = False    
        return render(request,'dashbord/profile.html',{'homework':Homework,'todo':todo,'homework_done':Homework_done,'todo_done':todo_done})
    else:
        return HttpResponseRedirect('/login/')






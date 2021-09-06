from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import*
from .auth import *

@login_required
def index(request):
    
    user=User.objects.get(id =request.session['user']['id'])
    context = {
        'user':user,
        'messages_index': user.messages.all(), 
        'comments_index':user.comments.all(),
        }
    return render(request,'index.html',context) #arreglar 
    

@login_required
def wall(request):

    context = {
        'messages_lista': Message.objects.all().order_by("-created"), #TODO falta revisar el codigo
        'comments_lista':Comment.objects.all().order_by("created")
    }
    
    return render(request, 'wall.html', context) 

@login_required
def post_message(request):
    if request.POST['message'] == "":
        messages.warning(request,"No se permiten los post vacios")
        return redirect('/wall')
    else:
        Message.objects.create(message = request.POST['message'], user = User.objects.get(id = request.session['user']['id']))
        return redirect('/wall')
    
@login_required
def post_comment(request, id):
    if request.POST['comment'] == "":
        messages.warning(request,"No se permiten los comentarios vacios")
        return redirect('/wall')
    else:
        user = User.objects.get(id = request.session['user']['id'])
        message = Message.objects.get(id = id)
        Comment.objects.create(
        comment = request.POST['comment'],
        user = user,
        message = message,
        )
    return redirect('/wall')

#el wraper no me captura el id
@login_required
def delete_comment(request,id):
    poster = Comment.objects.get(id=id)
    if request.session['user']['id'] == poster.user.id:
        poster.delete()
        messages.success(request, f"se he eliminado el comentario de {request.session['user']['first_name']}")
        return redirect('/wall')
    else:
        messages.warning(request, "no puede eliminar comentarios de otros usuarios")
        return redirect('/wall')
    return 

@login_required
def profile(request,id):
    user=User.objects.get(id=id)
    context = {
        'user':user,
        'messages_user': user.messages.all(), 
        'comments_user':user.comments.all(),
        }

    return render(request, 'profile.html',context)



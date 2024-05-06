from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        valid_password = validate_senha(senha, confirmar_senha, request)
        valid_user = validate_username(username, request)
        valid_email = validate_useremail(email, request)

        if not valid_password or not valid_user or not valid_email: # Para que todas as validações sejam rodadas e todos os erros sejam retornados
            return redirect('/usuarios/cadastro')

        # if not validate_senha(senha, confirmar_senha, request) or not validate_username(username, request):
        #     return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(
            username = username,
            email = email,
            password = senha
        )

        return redirect('/usuarios/login')

# --------

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha  = request.POST.get('senha')

    user = auth.authenticate(request, username=username, password=senha)
    if user:
        auth.login(request, user)
        return redirect('/pacientes/home')
    
    else:
        messages.add_message(request, constants.ERROR, 'O username e/ou a senha inválido(s).')
        return redirect('/usuarios/login')
    

def logout(request):
    auth.logout(request)
    return redirect('/usuarios/login')

# --------
def validate_senha(senha, confirmar_senha, request):
    if senha != confirmar_senha:
        messages.add_message(request, constants.ERROR, 'A senhas não são iguais.')
        return False
    
    if len(senha) < 6:
        messages.add_message(request, constants.ERROR, 'A senha precisa ter no mínimo 6 caracteres.')
        return False
    
    else:
        return True
    
def validate_username(username, request):
    if len(username) < 5:
        messages.add_message(request, constants.ERROR, 'O nome de usuário precisa ter no mínimo 5 caracteres.')
        return False
    
    users = User.objects.filter(username=username)
    if users.exists():
        messages.add_message(request, constants.ERROR, 'O nome de usuário já está em uso.')
        return False
    
    else:
        return True
    
def validate_useremail(email,request):
    try:
        validate_email(email)
    except ValidationError as e:
        messages.add_message(request, constants.ERROR, 'Insira um email válido.')
        return False
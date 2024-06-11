from django.shortcuts import redirect, render
from .models import Especialidades, DadosMedico
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants

def cadastro_medico(request):
    if request.method == 'GET':
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades': especialidades})
    
    elif request.method == 'POST':
        if check_user(request):
            return redirect('/medicos/cadastro_medico')
        else:
            crm = request.POST.get('crm')
            nome = request.POST.get('nome')
            cep = request.POST.get('cep')
            rua = request.POST.get('rua')
            bairro = request.POST.get('bairro')
            numero = request.POST.get('numero')
            cim = request.FILES.get('cim')
            rg = request.FILES.get('rg')
            foto = request.FILES.get('foto')
            especialidade = request.POST.get('especialidade')
            descricao = request.POST.get('descricao')
            valor_consulta = request.POST.get('valor_consulta')

            dados_medico = DadosMedico(
                crm=crm,
                nome=nome,
                cep=cep,
                rua=rua,
                bairro=bairro,
                numero=numero,
                cedula_identidade_medica=cim,
                rg=rg,
                foto=foto,
                especialidade_id=especialidade,
                descricao=descricao,
                valor_consulta=valor_consulta,
                user = request.user
            )
            dados_medico.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso!')

            return redirect('/medico/abrir_horario')

def check_user(request):
    dm = DadosMedico.objects.filter(user=request.user)
    print(dm.exists())
    if dm.exists():
        messages.add_message(request, constants.ERROR, 'Usuário já cadastrado.')
        return True
    
def abrir_horario(request):
    if request.method == 'POST':
        return render(request, 'abrir_horario.html')
from django.shortcuts import render
from .models import Alumnos, ComentarioContacto #Accedemos al modelo Alumnos que contiene la estructura de la tabla.
from .models import Comentario
from .forms import ComentarioContactoForm

# Create your views here.
def registros(request):
    alumnos = Alumnos.objects.all() # all recuperar todos los objetos del modelo (registros de la tabla alumnos)
    comentario = Comentario.objects.all()
    
    return render(request, "registros/principal.html", {'alumnos': alumnos})
    #indicamso el lugar donde se renderiza el resultado de esta vista y enviamos la lista de alumnos recuperados

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #si es valido el formulario
            form.save() #inserta el registro en la tabla
            comentarios = ComentarioContacto.objects.all() #comentarios es igual a todos los comentarios de la tabla ComentarioContacto
            return render(request, "registros/consultaContacto.html", {'comentarios': comentarios}) #retorna al usuario a la vista de consultaContacto.html
    form = ComentarioContactoForm()
    #Si sale mal reenvian al formulario los datos ingresados
    return render(request, 'registros/contacto.html', {'form': form})

def contacto(request):
    return render(request, "registros/contacto.html")
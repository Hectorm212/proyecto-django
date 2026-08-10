from datetime import date# esta importacion es para poder hacer consulta por un rango de fechas
import datetime
from django.shortcuts import render
from .models import Alumnos, ComentarioContacto #Accedemos al modelo Alumnos que contiene la estructura de la tabla.
from .models import Comentario
from .forms import ComentarioContactoForm
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages
from django.shortcuts import get_object_or_404

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

def consultarContacto(request):
    comentarios = ComentarioContacto.objects.all() #comentarios es igual a todos los comentarios de la tabla ComentarioContacto
    return render(request, "registros/consultaContacto.html", {'comentarios': comentarios}) #retorna al usuario a la vista de consultaContacto.html

def contacto(request):
    return render(request, "registros/contacto.html")

def eliminarComentario(request, id, confirmacion = 'registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method == 'POST':
        comentario.delete()
        comentarios = ComentarioContacto.objects.all()
        return render(request, "registros/consultaContacto.html", {'comentarios': comentarios})
    return render(request, confirmacion, {'object': comentario})

def consultarComentarioIndivicual(request, id):
    comentario = ComentarioContacto.objects.get(id=id)
    #get permite establecer una condicionanete a la consulta y recupera el objedor del comedlo que cumple la condición (regusro de la tabla CeometariosContacto.)
    #get se emplea cuando se sabe que solo hay un objeto que coicide con su consulta.
    return render(request, "registros/editarComentario.html", {'comentario': comentario})
#Indicamos el lugar donde se renderizará el resultado de esta vista y enviamos la lista de alumnos recuperados

def editarComentario(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #Teferenciamos que el elemento del formulario pertenec al comentario ya existente
    if form.is_valid():
        form.save() #si el registro ya existe, se modifica.
        comentarios = ComentarioContacto.objects.all()
        return render(request, "registros/consultaContacto.html", { 'comentarios': comentarios })
    #Si el formulario no es valido nos reguresa al formulario para verificar datos
    return render(request, "registros/editarComentario.html", { 'comentario': comentario})
#Indicamos el lugar donde se renderizará el resultado de esta vista y enviamos la lista de alumnos recuperados

def consultas(request):
    alumnos = Alumnos.objects.all()
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar1(request):
    #con una sola condicion
    alumnos = Alumnos.objects.filter(carrera="Tecnologias de la informacion")
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar2(request):
    #con una sola condicion
    alumnos = Alumnos.objects.filter(carrera="Tecnologias de la informacion").filter(turno="Matutino")
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar3(request):
    #Si sp;p deseamps recuperar ciertos datos agregamos la funcion only, listando los campos que queremos obtener de la consulta emplear filter() o en el ejemplo all()
    alumnos = Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar4(request):
    # con un lookup que verifica si el nombre inicia con una letra en este caso la A
    alumnos = Alumnos.objects.filter(nombre__startswith="A",)
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar5(request):
    # con un lookup que verifica si el turno está dentro de un conjunto de valores
    alumnos = Alumnos.objects.filter(turno__in=["Matutino", "Vespentino"])
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar6(request):
    # consultamos por rango de fechas
    alumnos = Alumnos.objects.filter(created__range=[date(2026, 8, 3), date(2026, 12, 31)])
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

#Tarea
def consultar7(request):
    alumnos =  Alumnos.objects.filter(nombre__in=["ANA", "Teresa"])
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar8(request):
    fechaInicio = datetime.date(2026, 6, 1)
    fechaFin = datetime.date(2026, 8, 4)
    alumnos =  Alumnos.objects.filter(created__range = (fechaInicio, fechaFin))
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultar9(request):
    #Consultando entre modelos
    alumnos =  Alumnos.objects.filter(comentario__coment__contains = 'Panchito triste')
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultasSQL(request):
    alumnos = Alumnos.objects.raw('SELECT id, matricula, nombre, carrera, turno, created FROM registros_alumnos WHERE carrera = "Tecnologias de la informacion" ORDER BY turno DESC')
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultasSQL2(request):
    alumnos = Alumnos.objects.raw(
        "SELECT * FROM registros_alumnos WHERE nombre IN ('ANA', 'Teresa')"
    )
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultasSQL3(request):
    # '2026-06-01' y '2026-08-04' son las fechas de inicio y fin
    alumnos = Alumnos.objects.raw(
        "SELECT * FROM registros_alumnos WHERE created BETWEEN '2026-06-01' AND '2026-08-04'"
    )
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def consultasSQL4(request):
    alumnos = Alumnos.objects.raw(
        """
        SELECT registros_alumnos.* 
        FROM registros_alumnos 
        INNER JOIN registros_comentario 
            ON registros_alumnos.id = registros_comentario.alumno_id 
        WHERE registros_comentario.coment LIKE '%Panchito triste%'
        """
    )
    return render(request, "inicio/consultas.html", {'alumnos': alumnos})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo = titulo, descripcion = descripcion, archivo = archivo)
            insert.save()
            return render(request, "registros/archivos.html")
        else:
            return render(request, "registros/archivos.html", {'archivo': Archivos})
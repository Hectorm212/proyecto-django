from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto

# Register your models here.
class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('created', 'updated') #Campos que se muestran pero no se pueden modificar
    list_display = ('matricula', 'nombre', 'carrera', 'turno', 'created') #Una tupla o lista con los nombres de los campos que quieres que aparezcan como columnas.
    search_fields = ('matricula', 'nombre', 'carrera', 'turno') #Habilita una barra de búsqueda.
    date_hierarchy = 'created'
    list_filter = ('carrera', 'turno') #Activa un panel lateral derecho para filtrar los registros por campos específicos (fechas, booleanos, llaves foráneas).
    
    def get_readonly_fields(self, request, obj=None):
        #si el usuario pertenece al grupo de "Usuarios"
        if request.user.groups.filter(name='Usuarios').exists():
            #Bloque los campos
            return ('matricula', 'nombre', 'carrera', 'turno')
        if request.user.groups.filter(name='Directores').exists():
            return ('matricula', 'turno', 'created', 'updated')
        #Cualquier otro usuario que no pertenece al grupo
        else:
            #Bloque los campos
            return('created', 'updated',)
admin.site.register(Alumnos, AdministrarModelo)

class AdministrarComentario(admin.ModelAdmin):
    list_display = ('id', 'coment',)
    search_fields = ('id', 'created',)
    date_hierarchy = 'created'
    list_filter = ('created', 'id')
    #exclude = ('coment',) #excluimos el campo que aparecera en el formulario de la tabla
admin.site.register(Comentario, AdministrarComentario)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display = ('id', 'mensaje')
    search_fields = ('id','created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')
admin.site.register(ComentarioContacto, AdministrarComentariosContacto)

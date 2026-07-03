from django.shortcuts import render

def principal(request):
    return render(request, "inicio/principal.html")

def nombre(request):
    return render(request, "inicio/nombre.html")

def contacto (request):
    return render(request, "registros/contacto.html")

def formulario (request):
    return render(request, "inicio/formulario.html")

def ejemplo (request):
    return render(request, "inicio/ejemplo.html")
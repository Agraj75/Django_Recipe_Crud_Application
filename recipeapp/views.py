from django.shortcuts import render,redirect
from django.http import HttpResponse
from recipeapp.models import receipes
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request, "home.html")

def receipe(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipes.objects.create(
            receipe_image=receipe_image,
            receipe_name=receipe_name,
            receipe_description=receipe_description
        )
        return redirect("receipes")
    
    all_receipes = receipes.objects.all()
    return render(request,'receipelist.html',{"receipes":all_receipes})

def receipe_details(request, id):
    try:
        recipe = receipes.objects.get(id=id)  # Fetch a single recipe by ID
    except receipes.DoesNotExist:
        return HttpResponse("Recipe not found", status=404)

    return render(request, "receipedetails.html", {"recipe": recipe})


def delete_receipe(request,id):
    queryset = receipes.objects.get(id=id)
    queryset.delete()
    return redirect("receipes")

def update_receipe(request, id):
    queryset = receipes.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image=receipe_image
        queryset.save()
        return redirect("receipes")
    
    context = {"receipes" : queryset}
    return render(request, "update_receipe.html", context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the username exists
        if not User.objects.filter(username=username).exists():  
            messages.error(request, "Invalid user..")
            return redirect("/login/")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid password..")
            return redirect("login")
        else:
            login(request, user)  
            return redirect("/receipes/")

    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("login")

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)

        if user.exists():
            messages.error(request, "username already exist..")


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully..")
        return redirect("register")
    return render(request, "register.html")
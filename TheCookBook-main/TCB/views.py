from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import Users
from django.contrib import messages
from django.contrib.auth.models import auth, User
# Create your views here.
from .models import *
from django.contrib.auth.decorators import login_required   
from django.shortcuts import render, get_object_or_404
from .models import Recipe

def home(request):
    if request.method == 'POST':
        rname = request.POST['recipe']
        category_id = request.POST['category']
        cuisine_id = request.POST['cuisine']
        veg = request.POST['veg']
        non = request.POST['non-veg']

        recipe = Recipe.objects.filter(recipe_name=rname).values()

        context = {
            'recipe' : recipe,
        }
        return render(request,'home.html',context)
    category = Category.objects.all()
    cuisine = Cuisine.objects.all()
    recipe = Recipe.objects.all()
    context={
        'category':category,
        'cuisine':cuisine,
        'recipe': recipe,
    }
    return render(request,'home.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST['user-name']
        password = request.POST['password']
        
        user = auth.authenticate(username= username, password= password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Wrong Username or Password')
            return redirect('login')

    else:   
        return render(request,'login.html')

def signup(request):

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['user-name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['passwordcd']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            elif len(username) > 16:
                messages.info(request,'Username must be under 16 characters')
                return redirect('signup')
            elif not username.isalnum():
                messages.info(request,'Username must be alphanumeric')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname)
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')

    else:
        return render(request,'signup.html')

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def aboutus(request):
    return render(request,"aboutus.html")

@login_required(login_url='/login')
def account(request):
    return render(request,"account.html")

@login_required(login_url='/login')
def urecipe(request):
    if request.method == 'POST':
        recipe_name = request.POST['recipename']
        category_id = request.POST['category']
        cuisine_id = request.POST['cuisine']
        veg = request.POST['veg']
        ingredients = request.POST['ingredients']
        steps = request.POST['steps']
        cooktime = request.POST['cooktime']
        serving = request.POST['serving']
        recipeimage = request.FILES['recipeimage']

        category = Category.objects.get(pk=category_id)
        cuisine = Cuisine.objects.get(pk=cuisine_id)

        recipe = Recipe.objects.create(
            user = request.user,
            recipe_name = recipe_name,
            recipe_image = recipeimage,
            recipe_steps = steps,
            ingredients = ingredients,
            cooking_time = cooktime,
            serving = serving,
            cuisine = cuisine, 
            category = category,
            veg = veg
        )
        print(recipe)
        recipe.save()
        messages.success(request,'Recipe Added Successfully')
        return redirect(account)

    else:
        category = Category.objects.all()
        cuisine = Cuisine.objects.all()
        context={
            "category": category,
            "cuisine": cuisine,
        }
        return render(request,"urecipe.html",context)



from django.shortcuts import render, get_object_or_404
from .models import Recipe

@login_required(login_url='/login')
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)

    context = {
        'recipe': recipe,
    }
    return render(request, 'vrecipe.html', context)

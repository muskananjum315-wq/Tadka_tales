from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404 , redirect

from .models import Restaurant,Dish,FavouriteDish

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import ContactMessage



def restaurants(request):
    region = request.GET.get('region', '').strip()

    if region:
        restaurants = Restaurant.objects.filter(
            region__iexact=region
        )
    else:
        restaurants = Restaurant.objects.all()

    return render(request, 'cafe/restaurants.html', {
        'restaurants': restaurants,
        'selected_region': region,
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    return render(request, 'cafe/restaurant_detail.html', {
        'restaurant': restaurant
    })



def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        from django.contrib.auth.models import User

        if not User.objects.filter(username=username).exists():
            error = "No account found. Please sign up."
        else:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = "Incorrect password. Please try again."

    return render(request, 'cafe/login.html', {'error': error})


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('home')

    return render(request, 'cafe/signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'cafe/home.html')

def menu(request):
    return render(request, 'cafe/menu.html')

def region(request):
    return render(request, 'cafe/region.html')


def all_dishes(request):
    dishes = Dish.objects.all()
    favourite_ids = []

    if request.user.is_authenticated:
        favourite_ids = FavouriteDish.objects.filter(
            user=request.user
        ).values_list('dish_id', flat=True)

    return render(request, 'cafe/all_dishes.html', {
        'dishes': dishes,
        'favourite_ids': favourite_ids,
    })


def about(request):
    return render(request, 'cafe/about.html')

# def contact(request):
#     return render (request,'cafe/contact.html')

def contact(request):
    if request.method == 'POST':
        print("CONTACT FORM POST RECEIVED")
        print(request.POST)

        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        return render(request, 'cafe/contact.html', {
            'success': 'Your message has been sent successfully!'
        })

    return render(request, 'cafe/contact.html')

# def contact(request):
#     if request.method == 'POST':
#         ContactMessage.objects.create(
#             name=request.POST.get('name'),
#             email=request.POST.get('email'),
#             subject=request.POST.get('subject'),
#             message=request.POST.get('message')
#         )
#         return render(request, 'cafe/contact.html', {
#             'success': 'Your message has been sent successfully!'
#         })

#     return render(request, 'cafe/contact.html')

def dish_detail(request, dish_name):
    dish = get_object_or_404(Dish, slug=dish_name)

    return render(request,'cafe/dish_detail.html',{
        'dish': dish,
        'dish_name':dish_name
    })



@login_required
def toggle_favourite(request, dish_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=405)

    dish = get_object_or_404(Dish, id=dish_id)

    favourite, created = FavouriteDish.objects.get_or_create(
        user=request.user,
        dish=dish
    )

    if not created:
        favourite.delete()
        is_favourite = False
    else:
        is_favourite = True

    return JsonResponse({'is_favourite': is_favourite})


@login_required
def my_favourites(request):
    favourites = FavouriteDish.objects.filter(
        user=request.user
    ).select_related('dish')

    return render(
        request,
        'cafe/my_favourites.html',
        {'favourites': favourites}
    )

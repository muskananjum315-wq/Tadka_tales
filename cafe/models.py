from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)

    dishes = models.ManyToManyField(
    'Dish',
    blank=True,
    related_name='restaurants'
    )
    
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    location = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name

class RestaurantInteriorImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='interior_images'
    )
    image = models.ImageField(upload_to='restaurant_interiors/')
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.restaurant.name} - Interior Image"    


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    background_image = models.ImageField(upload_to='region_backgrounds/')

    def __str__(self):
        return self.name   
    
class Dish(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    story = models.TextField()
    ingredients = models.TextField()
    known_for = models.CharField(max_length=200)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)

    region_ref = models.ForeignKey(
    Region,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='dishes'
    )

    def __str__(self):
        return self.name    


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('Customer Support', 'Customer Support'),
        ('Feedback', 'Feedback'),
        ('Restaurant Partnership', 'Restaurant Partnership'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class FavouriteDish(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='favourite_dishes'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='favourited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dish')

    def __str__(self):
        return f"{self.user.username} - {self.dish.name}"

     

    


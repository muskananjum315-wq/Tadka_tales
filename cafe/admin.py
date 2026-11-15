from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Restaurant,
    Dish,
    ContactMessage,
    Region,
    RestaurantInteriorImage,
)
# from .models import Restaurant, Dish, ContactMessage , Region

class RestaurantInteriorImageInline(admin.TabularInline):
    model = RestaurantInteriorImage
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    filter_horizontal = ('dishes',)
    inlines = [RestaurantInteriorImageInline]    
    

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if obj.region_ref:
            obj.region = obj.region_ref.name
        super().save_model(request, obj, form, change)

admin.site.register(Region)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    readonly_fields = ('gmail_reply_button',)

    fields = (
        'name',
        'email',
        'subject',
        'message',
        'gmail_reply_button',
    )

    @admin.display(description="Reply to Customer")
    def gmail_reply_button(self, obj):
        if not obj or not obj.email:
            return "No customer email available"

        subject = f"Re: {obj.subject}"
        gmail_url = (
            "https://mail.google.com/mail/?view=cm&fs=1"
            f"&to={obj.email}"
            f"&su={subject.replace(' ', '%20')}"
        )

        return format_html(
            '<a href="{}" target="_blank" '
            'style="display:inline-block; padding:10px 16px; '
            'background:#176b3a; color:white; border-radius:6px; '
            'text-decoration:none; font-weight:bold;">'
            '✉ Reply via Gmail</a>',
            gmail_url,
        )


admin.site.logout_template = "admin/logged_out.html"


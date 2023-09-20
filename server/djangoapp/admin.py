from django.contrib import admin
# <HINT> Import any new Models here
from .models import CarMake, CarModel

# <HINT> Register QuestionInline and ChoiceInline classes here
class CarModelInLine(admin.StackedInline):
    model = CarModel
    extra = 2

class CarMakeInLine(admin.StackedInline):
    model = CarMake
    extra = 2


# Register your models here.
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]
    list_display = ('name', 'description')
    search_fields = ['name', 'description']


class CarModelAdmin(admin.ModelAdmin):

    list_display = ['car_model', "dealer_id", "name", 'type_model', 'year']
    search_fields = ['car_model', "dealer_id", "name", 'type_model', 'year']


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# from .models import related models


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here

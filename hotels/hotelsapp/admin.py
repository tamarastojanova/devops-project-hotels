from django.contrib import admin
from .models import Room, Employee, Reservation, EmployeeRoom
from django.core.exceptions import ValidationError
# Register your models here.

class EmployeeRoomInlineAdmin(admin.TabularInline):
    model = EmployeeRoom
    extras = 1

class ReservationAdmin(admin.ModelAdmin):
    exclude = ('user', )
    list_display = ('code', 'room',)
    def save_model(self, request, obj, form, change):
        if obj.room.is_clean:
            obj.user = request.user
            return super(ReservationAdmin, self).save_model(request, obj, form, change)
        else:
            return ValidationError("Cannot make a reservation for a room that is not clean.")

    def has_change_permission(self, request, obj=None):
        print(obj and obj.user == request.user)
        print(Employee.objects.filter(user=request.user, type='Receptionist'))
        print(Employee.objects.filter(user=request.user, type='Manager'))
        if obj and (obj.user == request.user
                    or Employee.objects.filter(user=request.user, type='Receptionist').exists()
                    or Employee.objects.filter(user=request.user, type='Manager').exists()):
            return True
        return False

class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_clean',)

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    def has_change_permission(self, request, obj=None):
        if obj and Employee.objects.filter(user=request.user, type='Maid').exists():
            return True
        return False

class EmployeeAdmin(admin.ModelAdmin):
   # exclude = ('user', )
    inlines = [EmployeeRoomInlineAdmin, ]
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(EmployeeAdmin, self).save_model(request, obj, form, change)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
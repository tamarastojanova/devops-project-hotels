from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.PositiveIntegerField()
    num_beds = models.PositiveIntegerField()
    has_balcony = models.BooleanField()
    is_clean = models.BooleanField()

    def __str__(self):
        return f'Room number {self.number.__str__()}, with {self.num_beds.__str__()} beds'

class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    Type = models.TextChoices("Type", "Maid Receptionist Manager")
    type = models.CharField(blank=True, choices=Type, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rooms = models.ManyToManyField(Room,
                                   through="EmployeeRoom",
                                   through_fields=("employee", "room"))
    def __str__(self):
        return f'{self.name} {self.surname}'

class Reservation(models.Model):
    code = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='./images')
    is_approved = models.BooleanField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reservation {self.code}, {self.start.__str__()} - {self.end.__str__()}, room: {self.room}'

class EmployeeRoom(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

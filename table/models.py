from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



class Table(models.Model):
    id = models.AutoField(primary_key=True)
    number_of_seats = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    is_available = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'id = {self.id} - #= {self.number_of_seats} - available= {self.is_available}'


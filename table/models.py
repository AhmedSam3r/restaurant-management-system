from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import connection


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    number_of_seats = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    is_deleted = models.BooleanField(default=False)
    
    @classmethod
    def get_smallest_table(self, number_of_seats):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, min(number_of_seats) FROM table_table WHERE number_of_seats >= %s GROUP BY id LIMIT 1", [number_of_seats])
            result = cursor.fetchone()
            return {'table_id': result[0], 'number_of_seats': result[1]}

    def __str__(self):
        return f'id = {self.id} - #= {self.number_of_seats} - available= {self.is_available}'


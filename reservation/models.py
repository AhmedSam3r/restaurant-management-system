from django.db import models
from django.utils import timezone

from staff.models import Staff
from table.models import Table
from django.db import connection
from datetime import time, datetime, timedelta

from .constants import OPEN_TIME, CLOSE_TIME


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    starting_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)


    @classmethod
    def get_available_reservations(self, table_id, starting_time, ending_time=CLOSE_TIME):
        current_date = datetime.now().date()
        # set the starting time for the current date        
        starting_datetime = datetime.combine(current_date, starting_time) 

        # calculate the end time for the current date
        end_datetime = datetime.combine(current_date, ending_time)
        # get all reservations for the current date that overlap with the desired time range
        reservations = []
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT starting_date + interval '2 hours' AS starting_time,  end_date + interval '2 hours' FROM reservation_reservation 
                WHERE starting_date >= %s + interval'2 hours' AND table_id = %s
                ORDER BY starting_date
            """, [starting_datetime, table_id])
            reservations = cursor.fetchall()
        
        return reservations


    @classmethod
    def get_available_time_slots(self,table_id, starting_time):
        current_date = datetime.now().date()
        # set the starting time for the current date        
        starting_datetime = datetime.combine(current_date, starting_time) 
        close_datetime = datetime.combine(current_date, CLOSE_TIME) 
        # create a list of all reserved time slots
        reservations = self.get_available_reservations(table_id, starting_time)
        if len(reservations) == 0:
            return [{'starting_date': starting_datetime.time(), 'ending_date':datetime.combine(current_date, CLOSE_TIME)}]
        available_time_slots = []

        if starting_datetime < reservations[0][0]:
            available_time_slots.append([starting_time,reservations[0][0]])
        for i in range(1, len(reservations)-1):
            next_start_date = reservations[i+1][0]
            current_end_date = reservations[i][1]
            if next_start_date > current_end_date:
                available_time_slots.append([current_end_date, next_start_date])
        last_end_date = reservations[-1][1]
        if close_datetime > last_end_date:
            available_time_slots.append([last_end_date, close_datetime])

        return available_time_slots



    @classmethod
    def is_overlapping_reservation(self, table_id, starting_datetime, ending_datetime):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT starting_date AS starting_time, end_date FROM reservation_reservation 
                WHERE (%s >= starting_date AND %s < end_date) OR (%s >= starting_date AND %s < end_date) AND table_id = %s
                ORDER BY starting_date
            """, [starting_datetime, starting_datetime, ending_datetime, ending_datetime, table_id])
            reservation = cursor.fetchall()
            
            if len(reservation) >= 1:
                return True
            
            return False
            


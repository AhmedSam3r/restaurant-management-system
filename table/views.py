from django.shortcuts import get_object_or_404
from django.utils import timezone

from datetime import datetime

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from .models import Table
from staff.models import Staff
from reservation.models import Reservation

from reservation.constants import OPEN_TIME, CLOSE_TIME

class TableAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    model = Staff
    
    
    def post(self, request):
        table_id = request.data['table_id']
        number_of_seats = request.data['number_of_seats']
        if Table.objects.filter(id=table_id).exists():
            return Response({'success': False, 'message': 'Table with given ID already exists'}, status=400)

        table = Table(id=table_id, number_of_seats=number_of_seats)
        try:
            # Validate the table's contraints that we setted 
            table.full_clean()

            table.save()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        
        return Response({'success': True, 'message':'table has been created successfully'}, status=201)

    def get(self, request):
        tables =  Table.objects.all(is_deleted=False).values()
        return Response(tables, status=200)
    
    def delete(self, request):
        table_id = request.data['table_id']
        table = get_object_or_404(Table, pk=table_id)
        starting_datetime = datetime.combine(datetime.now(), OPEN_TIME).replace(tzinfo=timezone.utc)
        closing_datetime = datetime.combine(datetime.now(), CLOSE_TIME).replace(tzinfo=timezone.utc)
        reservation = Reservation.objects.filter(starting_date__gte=starting_datetime, end_date__lte=closing_datetime, table_id=table_id)
        if reservation:
            return Response({'success': False, 'message':'table is reserved cannot be deleted'}, status=200)
        table.is_deleted = True
        table.save()    
        return Response({'success': True, 'message':'table has been deleted successfully'}, status=200)


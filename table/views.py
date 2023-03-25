from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404

from django.http import JsonResponse
from rest_framework.response import Response



from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from .models import Table
from staff.models import Staff

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
        tables =  Table.objects.all().values()
        return Response(tables, status=200)
    
    def delete(self, request):
        table_id = request.data['table_id']
        table = Table.objects.filter(id=table_id, is_available=False)
        if not table:
            return Response({'success': True, 'message':'Currently this table doesnot exist at the moment.'}, status=200)

        #TODO DELETE THE TABLE IF THE TABLE ISNOT RESERVED AT THE RESERVATION TABLE

        return Response({'success': True, 'message':'table has been deleted successfully'}, status=200)


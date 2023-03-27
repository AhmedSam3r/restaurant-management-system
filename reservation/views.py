from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated, IsAdminUser
from datetime import datetime
from table.models import Table
from .models import Reservation
from staff.models import Staff
from table.models import Table
from .constants import OPEN_TIME, CLOSE_TIME
from .serializers import ReservationSerializer

from datetime import timedelta

from .pagination import MyPagination

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_available_time_slots(request):
    number_of_seats = int(request.data['number_of_seats'])  
    table_object = Table.get_smallest_table(number_of_seats)
    if len(table_object) == 0:
        return Response([], status=200)
    
    available_time_slots =  Reservation.get_available_time_slots(table_object["table_id"], starting_time=(datetime.now() - timedelta(hours=10)).time)

    return Response(available_time_slots)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reserve_time_slot(request):
    table_id = request.data['table_id']
    starting_datetime = datetime.strptime(request.data['starting_datetime'], '%Y-%m-%d %H:%M:%S')
    ending_datetime = datetime.strptime(request.data['ending_datetime'], '%Y-%m-%d %H:%M:%S')

    current_date = datetime.now().date()
    if starting_datetime < datetime.combine(current_date, OPEN_TIME) or starting_datetime > datetime.combine(current_date, OPEN_TIME) or ending_datetime > datetime.combine(current_date, CLOSE_TIME):
        return Response({'success': False, 'message': 'You are trying to reserve at wrong time'})

    is_overlapping = Reservation.is_overlapping_reservation(table_id, starting_datetime, ending_datetime)
    if is_overlapping:
        return Response({'success': False, 'message': 'The time slot is already reserved.'})

    reservation = Reservation(starting_date=starting_datetime, end_date=ending_datetime, staff_id=request.user.id, table_id=table_id)
    reservation.save()
    return Response({'reservation_id' : reservation.id,'success': True, 'message': 'Congrats, you reserved successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservations_today(request):
    queryset = Reservation.objects.filter(starting_date__gte=datetime.now())
    paginator = MyPagination()  # instantiate your custom pagination class
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = ReservationSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_reservations_history(request):
    queryset = Reservation.objects.all()
    paginator = MyPagination()  # instantiate your custom pagination class
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serializer = ReservationSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reservation(request):
    reservation_id = request.data['reservation_id']
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    starting_date = reservation.starting_date
    closing_datetime = datetime.combine(datetime.now(), CLOSE_TIME).replace(tzinfo=timezone.utc)
    #Ensure that the reservation date is still in the current day
    if timezone.now() > starting_date or starting_date > closing_datetime:
        return Response({'success':False, 'message':'Cannot delete old reservation'}, status=200)

    reservation.delete()    
    return Response({'success':True, 'message':'Reservation is deleted successfully'})

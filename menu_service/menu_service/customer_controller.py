from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count
from django.http import JsonResponse

from .models import Menus
from .serializers import MenuSerializer


@api_view(['GET'])
def menus_list(request):
    today_date = request.data.get('date')

    today_menus = Menus.objects.filter(date=today_date)

    serializer = MenuSerializer(today_menus, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def choose_menu(request):
    current_user_username = request.user.username

    menu_id = request.data.get("menu_id")

    try:
        menu = Menus.objects.get(pk=menu_id)
    except Menus.DoesNotExist:
        return Response({"message": "Menu not found"}, status=status.HTTP_404_NOT_FOUND)

    employers = menu.employers
    if current_user_username not in employers:
        employers[current_user_username] = None
        menu.save()

        return Response({"message": f"Added {current_user_username} to employers"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": f"{current_user_username} already exists in employers"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def winning_menu(request):
    today_date = request.data.get('date')

    # Query menus for the specified date and find the menu with the most votes
    try:
        today_menus = Menus.objects.filter(date=today_date)
        max_menu = today_menus.annotate(employer_count=Count(
            'employers')).order_by('-employer_count').first()

        if max_menu:
            response_data = {'menu_id': max_menu.id}
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"error": "No menu found for today"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from inventoryapp.serializers import ItemSerializer
from rest_framework import status
from .models import Item


class SortItemsView(APIView):
    def get(self, request):
        items = Item.objects.all().order_by('-price')  # Corrected variable name
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class QueryItemsView(APIView):
    def get(self, request, category):
        items = Item.objects.filter(category=category)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    

class inventoryItemsView(APIView):
    def get(self, request):
        items = Item.objects.all()  # Corrected model reference
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)  # Corrected 'dat' to 'data'
        if serializer.is_valid():
            barcode = serializer.validated_data['barcode']
            if Item.objects.filter(barcode=barcode).exists():  # Added missing '.' before 'filter'
                return Response({'barcode': ['inventory with this barcode already exists.']}, 
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)  # Corrected 'items' to 'item'
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # Corrected 400 to 404
        item.delete()  # Corrected 'items.delete()' to 'item.delete()'
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf  import csrf_exempt
import json
import requests

from .models import Category


def home_view(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'index.html', {'categories': categories})

def category_detail(request, category_path):
    slugs = category_path.strip('/').split('/')
    category = None
    parent = None
    
    for slug in slugs:
        category = get_object_or_404(Category, slug=slug, parent=parent)
        parent = category
    
    return render(request, 'index.html', 
                  {
                      'current_category': category,
                      'subcategories': category.children.all()
                  })


@csrf_exempt
def get_address(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')
            
            if not lat or not lon:
                return JsonResponse({'address': 'Координаты не получены'}, status=400)
            yandex_api_key = '678cceaa-c509-4503-a72a-ca33a253a07a'
            url = 'https://geocode-maps.yandex.ru/1.x/'
            params = {
                'format': 'json',
                'apikey': yandex_api_key,
                'geocode': f'{lon}, {lat}',
                'lang': 'ru_RU'
            }
            response = requests.get(url, params=params)
            geo_data = response.json()
            
            feature_members = geo_data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
            if feature_members:
                address = feature_members[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            else:
                address = 'Адрес не найден'
            return JsonResponse({'address': address})
        except Exception as e:
            return JsonResponse({'address': f'Ошибка: {str(e)}'}, status=500)
        
    return JsonResponse({'error': 'Только POST запрос разрешен'}, status=405)
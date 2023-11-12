from django.shortcuts import render
import requests
from django.core.paginator import Paginator

def index(request):
    api_url = "https://pokeapi.co/api/v2/pokemon?limit=100"
    response = requests.get(api_url)
    data = response.json()
    results = data.get('results', [])

    # Crea una lista de diccionarios con los nombres y las urls de las imágenes
    pokemon_list = []
    for pokemon in results:
        name = pokemon['name']
        id = pokemon['url'].split('/')[-2]
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png"
        pokemon_list.append({'id': id, 'name': name.capitalize(), 'image_url': image_url})
        
    # Filtra por nombre o id
    query = request.GET.get('q')
    if query:
        query = query.lower()
        pokemon_list = [
            pokemon for pokemon in pokemon_list
            if (query in pokemon['name'].lower()) or (query in str(pokemon['id']))
        ]
    
    # Agrega paginación
    paginator = Paginator(pokemon_list, 20)
    page = request.GET.get('page')
    try:
        pokemon_list = paginator.page(page)
    except Exception as e:
        pokemon_list = paginator.page(1)

    context = {'pokemon_list': pokemon_list, 'query': query}
    return render(request, 'main/index.html', context)


def pokemon_detail(request, pokemon_id):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(api_url)
    data = response.json()

    name = data.get('name', '').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    height = data.get('height')
    weight = data.get('weight')
    abilities = [ability['ability']['name'] for ability in data.get('abilities', [])]

    context = {
        'id': pokemon_id,
        'name': name,
        'image_url': image_url,
        'height': height,
        'weight': weight,
        'abilities': abilities,
    }
    return render(request, 'main/pokemon_detail.html', context)
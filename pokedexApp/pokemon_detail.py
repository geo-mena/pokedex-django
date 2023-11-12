from django.shortcuts import render
import requests

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
        'name': name,
        'image_url': image_url,
        'height': height,
        'weight': weight,
        'abilities': abilities,
    }
    return render(request, 'pokemonapp/pokemon_detail.html', context)

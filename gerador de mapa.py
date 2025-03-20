# -*- coding: utf-8 -*-
"""Mapa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jS29hNAu7NGo2KuO-DZ4jkPMMFICy8IE
"""

import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
import time

def consultar_cep(cep):
    cep = str(cep).replace("-", "").replace(".", "").strip()
    if len(cep) != 8 or not cep.isdigit():
        return None, "CEP inválido."
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        if "erro" in dados:
            return None, "CEP não encontrado."
        endereco = f"{dados.get('logradouro', 'Não informado')}, {dados.get('bairro', 'Não informado')}, {dados['localidade']}, {dados['uf']}"
        resultado = (
            f"CEP: {dados['cep']}\n"
            f"Logradouro: {dados.get('logradouro', 'Não informado')}\n"
            f"Bairro: {dados.get('bairro', 'Não informado')}\n"
            f"Cidade: {dados['localidade']}\n"
            f"UF: {dados['uf']}"
        )
        return endereco, resultado
    except requests.exceptions.RequestException as e:
        return None, f"Erro: {e}"

def geocodificar_endereco(endereco):
    if not endereco or not isinstance(endereco, str):
        return 0, 0
    geolocator = Nominatim(user_agent="cep_to_map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    try:
        location = geocode(endereco)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            if (-90 <= latitude <= 90) and (-180 <= longitude <= 180):
                return latitude, longitude
            else:
                return 0, 0
        else:
            return 0, 0
    except Exception:
        return 0, 0

# Carrega o CSV
# Substitua 'seus_ceps.csv' pelo nome do seu arquivo e 'CEP' pelo nome da coluna
df = pd.read_csv('/content/CEPcsv - Página1.csv')

# Verifica as primeiras linhas do CSV
df.head()

# Supondo que a coluna com os CEPs se chama 'CEP'
ceps = df['CEP'].tolist()

# Lista para armazenar os resultados
resultados = []

# Processa cada CEP
print("\nProcessando CEPs...")
for cep in ceps:
    endereco, resultado = consultar_cep(cep)
    if endereco:
        lat, lon = geocodificar_endereco(endereco)
        coordenadas = f"({lat}, {lon})" if lat != 0 and lon != 0 else 0
        resultados.append({
            "CEP": cep,
            "Endereço Encontrado": endereco,
            "Latitude": lat,
            "Longitude": lon,
            "Coordenadas": coordenadas
        })
        print(f"CEP {cep} processado: {endereco} -> {coordenadas}")
    else:
        resultados.append({
            "CEP": cep,
            "Endereço Encontrado": 0,
            "Latitude": 0,
            "Longitude": 0,
            "Coordenadas": 0
        })
        print(f"CEP {cep} falhou: {resultado}")

# Converte para DataFrame e salva em um novo CSV
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv('ceps_processados.csv', index=False)
print("\nResultados salvos em 'ceps_processados.csv'")
print("Primeiras linhas do resultado:")
print(df_resultados.head())

import folium

# Cria um mapa centrado no Brasil
mapa = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)

# Adiciona marcadores apenas para CEPs com coordenadas válidas (diferentes de 0)
for _, row in df_resultados.iterrows():
    if row['Latitude'] != 0 and row['Longitude'] != 0:
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"CEP: {row['CEP']}\nEndereço: {row['Endereço']}",
            icon=folium.Icon(color="blue")
        ).add_to(mapa)

# Salva o mapa
mapa.save('mapa_ceps.html')
print("Mapa gerado em 'mapa_ceps.html'")
# Para exibir no notebook, use:
# mapa






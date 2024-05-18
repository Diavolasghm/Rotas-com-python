 #############Importar as Bibliotecas
import pandas as pd
import folium
import requests

##############Cria as funções
def obter_rota_osrm(coordenadas):
    coordenadas_str = ";".join([f"{lon},{lat}" for lat, lon in coordenadas])
    
    url = f"http://router.project-osrm.org/route/v1/driving/{coordenadas_str}?overview=full&geometries=geojson"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        rota_geojson = dados['routes'][0]['geometry']
        return rota_geojson
    else:
        raise Exception("Erro ao solicitar a rota à API do OSRM")
    
def carregar_csv(nome_arquivo):
    try:
        df = pd.read_csv(nome_arquivo)
        return df
    except Exception as e:
        print("Erro ao carregar o arquivo CSV", e)
        return None
    
def extrair_lat_long(df, coluna_latlong):
    latitudes =[]
    longitudes = []
    for coord in df[coluna_latlong]:
        if ',' in str(coord):
            lat, lon = map(float, str(coord).split(','))
            latitudes.append(lat)
            longitudes.append(lon)
        else:
            print("Coordenada inválida:", coord)
    return latitudes, longitudes

def criar_rota_latlong(latitudes, longitudes, nome_arquivo):
    mapa = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=10)

    #Melhorar para colocar nome nos pontos ao invés das coordenadas
    for lat, lon in zip(latitudes, longitudes):
        folium.Marker(location=[lat, lon], popup=str(lat)+', '+str(lon)).add_to(mapa)

    mapa.save(nome_arquivo + '.html')

#Essa função tem que ser colocada dentro da criar_rota_
def criar_mapa_com_rota():
    coordenadas = list(zip(latitudes, longitudes))
    rota_geojson = obter_rota_osrm(coordenadas)
    mapa = folium.Map(location=coordenadas[0], zoom_start=13)
    folium.GeoJson(rota_geojson, name="route").add_to(mapa)

    #Adiciona marcadores para as coordenadas com sequências numéricas
    for idx, (lat, lon) in enumerate(coordenadas):
        folium.Marker(location=[lat,lon], popup=f"Ponto {idx+1}").add_to(mapa)

    mapa.save("mapa_com_rota.html")



#######Inicia as variáveis Globais e Funções
nome_arquivo_csv = "coordenadas.csv"
df = carregar_csv(nome_arquivo_csv)

if df is not None:
    nome_arquivo_html = "rota_open_street_view"
    latitudes, longitudes = extrair_lat_long(df, 'Coordenadas')
    criar_rota_latlong(latitudes, longitudes, nome_arquivo_html)
else:
    print("Não foi possível carregar o arquivo CSV")

criar_mapa_com_rota()
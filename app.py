import streamlit as st
import pandas as pd
import geopandas
import shapely.geometry
import folium
import requests
from github import Github
import json
APP_TITLE = 'Κ.Ο.Μ.Υ. backend 1.6'
APP_SUB_TITLE = 'by CMT Prooptiki'
def geojson_maker(file1,file2):
    #map_data3 = pd.read_excel('komgeodata_despina.xlsx',dtype={'KALCODE':str})
    
    #map_data4 = pd.read_excel('komygeodataper2_despina.xlsx',dtype={'KALCODE':str})
    map_data3 = pd.read_excel(file1,dtype={'KALCODE':str})
    map_data4 = pd.read_excel(file2,dtype={'KALCODE':str})

    geojson_url = 'https://raw.githubusercontent.com/michalis-raptakis/greece-region-units-geojson/master/greece-region-units-geojson.json'
    response = requests.get(geojson_url)
    geojson = response.json()
    
    geojson_url2 = 'https://geodata.gov.gr/geoserver/wfs/?service=WFS&version=1.0.0&request=GetFeature&typeName=geodata.gov.gr:d7f50467-e5ef-49ac-a7ce-15df3e2ed738&outputFormat=application/json&srsName=epsg:4326'
    response = requests.get(geojson_url2)
    geojson2 = response.json()
    
    geodf = geopandas.read_file(geojson_url)
    geodf2 = geopandas.read_file(geojson_url2)
    
    merge=pd.merge(geodf,map_data3,how='outer',on='KALCODE')
    
    map_data4v_2=map_data4.groupby(['Περιφέρεια','periferies','KALCODE']).sum().reset_index()
    
    merge2=pd.merge(geodf2,map_data4v_2,how='outer', left_on="PER", right_on="periferies")
    merge2['ΚΟΜΥ']=merge2['Νοσηλευτές']
    merge['ΚΟΜΥ']=merge['Νοσηλευτές']
    merge.rename(columns={'Νοσηλευτές':'Νοσηλευτές και λοιποί επαγγελματίες υγείας',
                      'Νοσηλευτές & Επισκέπτες υγείας που εμβολιάζουν':'Νοσηλευτές και λοιποί επαγγελματίες υγείας που εμβολιάζουν',
                      'ΥΠΟΛΟΙΠΕΣ  ΕΙΔΙΚΟΤΗΤΕΣ':'Λοιποί επαγγελματίες υγείας που δεν εμβολιάζουν',
                      'Μοριακοί Ιατροί/Βιολόγοι':'Ιατροί/Βιολόγοι που πραγματοποιούν μοριακά τεστ',
                       'Μοριακοί νοσηλευτές':'Νοσηλευτές που πραγματοποιούν μοριακά τεστ',
                       'Μοριακοί νοσηλευτές & Επισκέπτες υγείας που εμβολιάζουν':'Επαγγελματίες υγείας που πραγματοποιούν μοριακά τεστ και εμβολιάζουν'},inplace=True)
    merge2.rename(columns={'Νοσηλευτές':'Νοσηλευτές και λοιποί επαγγελματίες υγείας',
                      'Νοσηλευτές & Επισκέπτες υγείας που εμβολιάζουν':'Νοσηλευτές και λοιποί επαγγελματίες υγείας που εμβολιάζουν',
                      'ΥΠΟΛΟΙΠΕΣ  ΕΙΔΙΚΟΤΗΤΕΣ':'Λοιποί επαγγελματίες υγείας που δεν εμβολιάζουν',
                      'Μοριακοί Ιατροί/Βιολόγοι':'Ιατροί/Βιολόγοι που πραγματοποιούν μοριακά τεστ',
                       'Μοριακοί νοσηλευτές':'Νοσηλευτές που πραγματοποιούν μοριακά τεστ',
                       'Μοριακοί νοσηλευτές & Επισκέπτες υγείας που εμβολιάζουν':'Επαγγελματίες υγείας που πραγματοποιούν μοριακά τεστ και εμβολιάζουν'},inplace=True)
    merge['Περιφερειακή Ενότητα'] = [f'<b>{x}</b>' for x in merge['Περιφερειακή Ενότητα']]
    merge2['Περιφέρεια'] = [f'<b>{x}</b>' for x in merge2['Περιφέρεια']]
    st.write(merge)
    merge1geo=merge.to_file('testgeo1.geojson',driver="GeoJSON")
    merge2geo=merge2.to_file('testgeo2.geojson',driver="GeoJSON")
    upload(merge,merge2)
def upload(merge1geo,merge2geo):
    #json_contents1 = json.dumps(merge1geo).encode("utf-8")
    #json_contents2 = json.dumps(merge2geo).encode("utf-8")
    # create a Github instance with your Github access token
    g = Github(st.secrets["access_token"])
        
    # get the repository where you want to upload the file
    repo = g.get_repo("A-PALIOS/livemap_backend")
    
    #file_contents="hello 1"
    #file_contents2="hello 2"
    
    # file = repo.get_contents("data/example1.txt")
    file1=''
    file2=''
    
    # define the file path and content for the new GeoJSON file
    #file_path = "data/geojson1.geojson"
    #file_contents = {"type": "FeatureCollection", "features": ['hello','there']}

    # serialize the GeoJSON object to a JSON string and encode as bytes
    #json_contents = json.dumps(merge).encode("utf-8")
    json_contents1= merge1geo.to_json()
    json_contents1= merge2geo.to_json()

    try:
        file1 = repo.get_contents("data/geojson1.geojson")
    except :
        print ('error1')
    try:
        file2 = repo.get_contents("data/geojson2.geojson")
    except :
        print ('error2')
        
    if((file1 and file2)and(file1!='' and file2!='')):
        print('hello')
        # create a new file in the repository with the uploaded file contents
        repo.update_file("data/geojson1.geojson", "Upload from Streamlit", json_contents1,file1.sha)
        repo.update_file("data/geojson2.geojson", "Upload from Streamlit", json_contents2,file2.sha)

    #file_contents="hello 3"
    #file_contents2="hello 4"

    if(not(file)):
        # create a new file in the repository with the uploaded file contents
        repo.create_file("data/geojson1.geojson", "Upload from Streamlit", json_contents1)
    if(not(file2)):
        # create a new file in the repository with the uploaded file contents
        repo.create_file("data/geojson2.geojson", "Upload from Streamlit", json_contents2)
    return "done"
def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    file1=st.file_uploader("Επελεξε περιφεριες", type=["xlsx"], key="key1")
    file2=st.file_uploader("Επελεξε περιφεριακες ενοτητες", type=["xlsx"], key="key2")
    if (file1 is not None)and (file2 is not None):
        st.button("koybi",on_click=geojson_maker(file1,file2))
if __name__ == "__main__":
    main()
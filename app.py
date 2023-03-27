import streamlit as st
import pandas as pd
import geopandas
import shapely.geometry
import folium
import requests

APP_TITLE = 'Κ.Ο.Μ.Υ. backend 1.2'
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
    merge.to_file('testgeo1.geojson',driver="GeoJSON")
    merge2.to_file('testgeo2.geojson',driver="GeoJSON")
def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    file1=st.file_uploader("Επελεξε περιφεριες", type=["xlsx"], key="key1")
    file2=st.file_uploader("Επελεξε περιφεριακες ενοτητες", type=["xlsx"], key="key2")
    st.button("koybi",on_click=geojson_maker(file1,file2))
if __name__ == "__main__":
    main()
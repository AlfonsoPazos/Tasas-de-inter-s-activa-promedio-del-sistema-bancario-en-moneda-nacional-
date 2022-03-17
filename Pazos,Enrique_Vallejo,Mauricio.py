
"""
Created on Wed Mar  9 17:17:50 2022

@author: Alfonso
"""
# Usaremos la librería selenium y beautiful soup para hacer web scraping
from selenium import webdriver
import datetime
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests import get
import re

#Ubicamos el chromedriver y la página web de donde vamos a scrapear
path_driver = "C:/Users/Alfonso/AppData/Local/Temp/Rar$DRa0.456/chromedriver.exe"
driver = webdriver.Chrome(path_driver)   
driver.get("https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=B")


#generamos un dataframe vacío que nos servirá más adelante
resultado = pd.DataFrame()

#Insertar los años a consultar
lista_fechas = ['29/01/2021', '26/02/2021','31/03/2021', '30/04/2021','31/05/2021', 
'30/06/2021', '30/07/2021','31/08/2021', '30/09/2021','29/10/2021', 
'30/11/2021', '31/12/2021' ]  

#Iteramos por cada observación para que cada elemento de la lista ingrese en la fecha a consultar de la 
#página web.
for i in lista_fechas:     
    fecha_str = i
    tasas_input = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_rdpDate_dateInput"]')
    tasas_input.clear()
    tasas_input.send_keys(fecha_str) 
    time.sleep(5)
    buttonConsultar = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_btnConsultar"]')
    buttonConsultar.click()
    time.sleep(30)
    soup  = BeautifulSoup(driver.page_source, 'html.parser')
    Nombre_Tasas = soup.find_all("td", class_="rpgRowHeaderField rpgRowHeader APLI_fila1_new")
    Lista_Tasas = list ()
    for k in Nombre_Tasas:
        Lista_Tasas.append(k.text)
    Valor_Tas_Promed = list ()
    Valor_Tasas_Prom = soup.find_all("td", class_= "rpgDataCell APLI_fila1_new")
    for n in Valor_Tasas_Prom:
        Valor_Tas_Promed.append(n.text)
    df = pd.DataFrame({'Tasas': Lista_Tasas, 'Valor promedio':Valor_Tas_Promed})
    table_d = df.iloc[[0, 7, 14, 21, 28, 37, 44], :]
    table_d.index = ['Corporativos', 'Grandes Empresas', 'Medianas Empresas', 'Pequeñas Empresas', 'Microempresas', 'Consumo', 'Hipotecarios']
    table_d=table_d.transpose()
    table_d=table_d.drop(["Tasas"], axis=0)
    table_d = table_d.rename(index = lambda x: i)
    resultado = resultado.append(table_d)

resultado_copia = resultado
resultado_copia = resultado_copia.rename_axis('index').reset_index()
resultado_copia['orden']=resultado_copia.index
resultado_copia['orden'] = pd.to_numeric(resultado_copia['orden'])
resultado_copia['Corporativos'] = pd.to_numeric(resultado_copia['Corporativos'])
resultado_copia['Grandes Empresas'] = pd.to_numeric(resultado_copia['Grandes Empresas'])
resultado_copia['Medianas Empresas'] = pd.to_numeric(resultado_copia['Medianas Empresas'])
resultado_copia['Pequeñas Empresas'] = pd.to_numeric(resultado_copia['Pequeñas Empresas'])
resultado_copia['Microempresas'] = pd.to_numeric(resultado_copia['Microempresas'])
resultado_copia['Consumo'] = pd.to_numeric(resultado_copia['Consumo'])
resultado_copia['Hipotecarios'] = pd.to_numeric(resultado_copia['Hipotecarios'])

#GRÁFICO #1

graph=resultado_copia.plot.line(x= "orden", y={"Corporativos","Grandes Empresas","Medianas Empresas","Pequeñas Empresas","Microempresas" })
graph.legend(bbox_to_anchor=(1.02, 1),loc='upper left', borderaxespad=0, title='Leyenda')

#GRÁFICO #2

graph2 = resultado_copia.plot.bar(x="orden", y={"Corporativos","Grandes Empresas","Medianas Empresas","Pequeñas Empresas","Microempresas" }, rot=0)
graph2.legend(bbox_to_anchor=(1.02, 1),loc='upper left', borderaxespad=0, title='Leyenda')








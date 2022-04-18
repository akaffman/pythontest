# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 10:56:36 2021

@author: a592989
"""
import pandas as pd
import matplotlib.pyplot as plt
import datetime

archivo= 'COVID.xlsx'
hoja = pd.read_excel(archivo, sheet_name=0, header=10, usecols="C:R")

hoja = hoja.loc[hoja['Tipo de empleado'] == 'EMPLEADO DE CARGILL']

hoja = hoja.loc[hoja['Causa'] == 'Síntomas']
#hoja = hoja.loc[hoja['Localidad del Enablon'] == 'PUERTO QUEBRACHO']
#hoja = hoja.loc[hoja['Localidad del Enablon'] == 'OILSEEDS-SAN MARTIN']
hoja = hoja.drop(['Nombre','Localidad del Enablon','Status (O/C)','Cargill ID','Dia','Testeado?','Tipo de empleado','Considerado un accidente en el trabajo?','Acción tomada','Pérdida de olfato / sabor?','Causa','Fiebre?','Tos?'],axis=1)
hoja = hoja.dropna()
hoja['Año'] = hoja['Año'].astype(int)
hoja['Mes'] = hoja['Mes'].astype(int)
grupo =hoja.groupby(['Año', 'Mes'])['Confirmado?'].count() #juntar datos de las mismas fechas
vacia = pd.DataFrame(columns=['Año','Mes','Casos'])
ejex= []
for j in range(3): #2020 y 2021
    for i in range(12): #meses
        for k in range(len(grupo)): #barro la matriz
            if grupo.index[k][0] == j+2020 and grupo.index[k][1] == (i+1):
                valor = grupo.loc[grupo.index[k]]
                break
            else: valor = 0
        
        vacia = vacia.append({'Año': j+2020,'Mes':i+1,'Casos':valor}, ignore_index=True)
        
        fecha = datetime.datetime(j+2020,i+1,1)
        ejex.append(fecha)
limpiar = 7
ejex = ejex[limpiar:] #saco los primeros limpiar valores
vacia = vacia[limpiar:] #saco los primeros limpiar valores


#plt.grid(True)
#plt.show()

df = pd.read_json(r'query.json')


#df = df.loc[df['Departamento'] == 'San Lorenzo'] #df queda solo con dpto Rosario

#df = df.loc[df['Localidad'] == 'ROSARIO']

 #convierto la columna Fecha a formato.

#elimino las columnas que ya no sirven
df = df.drop(labels=['Departamento','Localidad','Descartados','En estudio','Notificaciones'],axis=1)

df =df.groupby('Fecha')['Confirmados'].sum() #juntar datos de las mismas fechas
df = df[100:] #saco los primeros 150 valores
#graficar por dia
poblacion = 1
#poblacion = 3600000
print(df.max()/poblacion)

df = df.diff() #hago las diferencias

ejex1=[]
for k in range(len(df)):
    fecha = datetime.datetime(int(df.index[k][0:4]),int(df.index[k][5:7]),int(df.index[k][8:10]))
    ejex1.append(fecha)

x = 21

ak = df.rolling(int(x)).mean()
ak = ak.shift(periods=-int(x/2)) #desplazo para que coincida

bk = df.rolling(int(7)).mean()
#bk = bk.shift(periods=-int(7/2)) #desplazo para que coincida

print(ak.describe())
print(df.describe())




#agrego la media y los dos máximos el maximo general lo marco con un punto y el valor

#x1 = [ejex[0], ejex[len(ejex)-1]]
x1 = [ejex1[0], ejex1[-1]]
y2 = [ak.max(), ak.max()]
y3 = [bk.max(), bk.max()]
y5 = [ak.mean(), ak.mean()]

x4,y4 = ejex1[df.argmax()],df.max()
plt.title('Complejo vs Población') 
plt.stem(ejex,vacia['Casos'], markerfmt = 's', basefmt = ':', use_line_collection=True, linefmt= '--')
plt.ylabel('Casos Complejo')
plt.xticks(rotation=70)
plt.twinx()
#plt.plot(ejex,df)
plt.plot(ejex1,ak)
plt.plot(ejex1,bk)
plt.xticks(rotation=70)
plt.grid(True)

plt.plot(x1,y2,x1,y3,x1,y5)

plt.plot(x4,y4,marker = 'o')
plt.text(x4,y4,y4)
plt.ylabel('Casos Santa Fe')

plt.tight_layout()

plt.show()

print(x4)

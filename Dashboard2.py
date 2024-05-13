"""
****** Important! *******
If you run this app locally, un-comment line 127 to add the theme change components to the layout
"""

from dash import Dash, dcc, html, Input, Output, State, callback, Patch, clientside_callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_ag_grid as dag
import pandas as pd
import os
import json
import plotly.io as pio
import plotly.graph_objects as go
from unidecode import unidecode
import plotly.colors as pc


df=pd.read_csv('SuicidioArg.csv')
df2=pd.read_csv('SuicidiosArg2.csv')

Vcat=['provincia_nombre','suicida_sexo','modalidad','tipo_lugar']
Vtem=['suicida_edad','año']
Vtem2=['mes','dias','hora']

Vpro=['BUENOS AIRES','CIUDAD AUTONOMA DE BUENOS AIRES','TUCUMAN', 'TIERRA DEL FUEGO, ANTARTIDA E ISLAS DEL ATLANTICO SUR',
 'SANTIAGO DEL ESTERO', 'SANTA FE', 'SANTA CRUZ' ,'SAN LUIS' ,'SAN JUAN',
 'SALTA', 'RIO NEGRO', 'NEUQUEN', 'MISIONES', 'MENDOZA' ,'LA RIOJA' ,'LA PAMPA',
 'JUJUY', 'FORMOSA', 'ENTRE RIOS' ,'CORDOBA' ,'CORRIENTES','CHUBUT' ,'CHACO' ,'CATAMARCA',]


# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
texto_style = {'fontSize': '0.6rem', 'maxHeight': '30px'}  # Modifica el valor de 'maxHeight' según el tamaño deseado
dropdown_width = {'width': '130px'}  # Define el ancho deseado para los dropdowns
dropdown_width2 = {'width': '130px'}  # Define el ancho deseado para los dropdowns


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css],suppress_callback_exceptions=True)

#color_texto = pc.qualitative.Dark24[3]
color_texto="rgba(255, 255, 255, 0.9)" 
color_paper = "rgba(217, 217, 217, 0.1)" 
color_plot="rgba(217, 217, 217, 0.1)" 


# Definir tu propio tema personalizado
custom_template = {
    "layout": {
        "font": {"family": "Arial","size": 12,"color": color_texto # Cambia el color del texto según tus preferencias
                 },
        "plot_bgcolor": color_plot,  # Cambia el color de fondo del gráfico
        "paper_bgcolor": color_paper,    # Cambia el color de fondo del papel
    }
}

# Asignar el tema personalizado como el tema predeterminado
pio.templates["custom"] = custom_template
pio.templates.default = "custom"


color_header_bg = "rgba(0, 0, 255, 0.1)"  # Color de fondo del encabezado (rojo)
color_header_text = "rgba(0, 0, 0, 1)"  # Color del texto del encabezado (negro)

# Definir el encabezado con el color personalizado
header = html.H4(
    "Suicido en Argentina",
    className="bg-danger text-black p-2 mb-2 text-center",
    style={"backgroundColor": color_header_bg, "color": color_header_text}
)

#header = html.H4("Suicido en Argentina", className="bg-primary text-white p-2 mb-2 text-center")

#======================Define los controladores TAB1======================================
#======================Define los controladores TAB1======================================
dropdown = html.Div(
    [dbc.Label("Pie-Chart",style=texto_style),
     dcc.Dropdown(Vcat,Vcat[0],id="indicador",
                  clearable=False,style={**texto_style, **dropdown_width}),
    ],className="mb-4",
)

dropdown1b = html.Div(
    [dbc.Label("Bar-Chart",style=texto_style),
     dcc.Dropdown(Vtem,Vtem[0],id="indicator1b",
                  clearable=False,style={**texto_style, **dropdown_width}),
    ],className="mb-4",
)

dropdown1c = html.Div(
    [dbc.Label("Bar-Chart2",style=texto_style),
     dcc.Dropdown(Vtem2,Vtem2[0],id="indicator1c",
                  clearable=False,style={**texto_style, **dropdown_width}),
    ],className="mb-4",
)

dropdown1d = html.Div(
    [dbc.Label("Tab2-Map",style=texto_style),
     dcc.Dropdown(Vpro,Vpro[0],id="indicator1d",
                  clearable=False,style={**texto_style, **dropdown_width}),
    ],className="mb-4",
)



#pio.templates.default = "plotly_white"


control1=dbc.Card([dropdown,dropdown1b,dropdown1c,dropdown1d],body=True,)
control =dbc.Col([control1], width=2)

#Tab1
#·············Definimos algunas funciones.......
def total_minutos():
    # Definir las fechas de inicio y fin
    inicio = pd.to_datetime('2017-01-01')
    fin = pd.to_datetime('2022-12-31')

    # Calcular el número total de minutos entre las dos fechas
    total_minutos = (fin - inicio).total_seconds() / 60
    return total_minutos

def tiempo_suicidio():
    df1=df
    total_ambos=len(df1)
    total_masculino=len(df1[df1['suicida_sexo']=='Masculino'])
    total_femenino=len(df1[df1['suicida_sexo']=='Femenino'])

    totmin= total_minutos()
    # Calcular cuántos minutos transcurren entre un suicidio y otro
    minutos_ambos = totmin / (total_ambos- 1)
    minutos_masculino = totmin / (total_masculino- 1)
    minutos_femenino = totmin / (total_femenino- 1)
    # Convertir minutos a un timedelta
    
    intervalo_masculino = pd.to_timedelta(minutos_masculino, unit='m').round('s')
    valor_masculino =f"{intervalo_masculino}"
    
    intervalo_femenino = pd.to_timedelta(minutos_femenino, unit='m').round('s')
    valor_femenino =f"{intervalo_femenino}"

    intervalo_ambos = pd.to_timedelta(minutos_ambos, unit='m').round('s')
    valor_ambos =f"{intervalo_ambos}"
    #································································
    tiempo={'Tambos':valor_ambos,
           'Tmasculino':valor_masculino,
            'Tfemenino':valor_femenino,}

    
    return tiempo

# Llamamos a la función para obtener el resultado
Delta_T= tiempo_suicidio()

# Creamos el html.Div con el texto que contiene el resultado del cálculo
texto_titulo1 = html.Div(html.Strong("Tiempo medio entre suicidios sucesivos.", 
        style={"fontSize": "16px", "fontFamily": "Arial", "fontWeight": "bold", "display":  "block",
               "textAlign": "center"}),)
Vspace1=html.Div(style={"height": "20px"})
Vspace2=html.Div(style={"height": "5px"})

# Creamos un contenedor para los tres textos con estilo de Flexbox
texto_container = html.Div([
    html.Div([html.Strong("Ambos sexos:", style={"fontSize": "14px", "fontFamily": "Arial", "fontWeight": "bold", "textAlign": "center"}),
              Vspace2,
            html.Span(Delta_T['Tambos'], style={"fontSize": "12px", "fontFamily": "Arial", "fontWeight": "bold", "textAlign": "center"})
    ], style={"flex": "1"}),  # Establece el primer elemento en flex-grow: 1
    html.Div([html.Strong("Sexo masculino:", style={"fontSize": "14px", "fontFamily": "Arial", "fontWeight": "bold", "textAlign": "center"}),
             Vspace2,
             html.Span(Delta_T['Tmasculino'], style={"fontSize": "12px", "fontFamily": "Arial", "fontWeight": "bold", "textAlign": "center"})
    ], style={"flex": "1"}),  # Establece el segundo elemento en flex-grow: 1
    html.Div([html.Strong("Sexo femenino:", style={"fontSize": "14px", "fontFamily": "Arial", "fontWeight": "bold", "textAlign": "center"}),
              Vspace2,
              html.Span(Delta_T['Tfemenino'], style={"fontSize": "12px", "fontFamily": "Arial", "fontWeight": "bold", "textAlign": "center"})
    ], style={"flex": "1",  
                        }
    )  # Establece el tercer elemento en flex-grow: 1
], style={"display": "flex", "justifyContent": "space-around",
          'background-color': 'rgba(217, 217, 217, 0.1)',  # color_paper
          'border': '1px solid rgba(255, 255, 255, 0.9)'  # color_texto 
          
          })  # Establece el contenedor principal como flex y justifica el contenido



grafico1=dbc.Col([dcc.Graph(id="Pie1", figure=px.pie())] ,width=6)
grafico2=dbc.Col([texto_titulo1,texto_container,Vspace1,
                  dcc.Graph(id="Bar1", figure=px.bar()),Vspace1,
                  dcc.Graph(id="line1", figure=px.line())],width=6)

grafico3=dbc.Col([dcc.Graph(id="Map1", figure=px.choropleth_mapbox())] ,width=6)


grafico4=dbc.Col([
                  html.Div(id='filtered-data-html', style={'display': 'flex', 'justify-content': 'center',
                        'background-color': 'rgba(217, 217, 217, 0.1)',  # color_paper
                        'border': '1px solid rgba(255, 255, 255, 0.9)'  # color_texto   
                        }),                                   
                           Vspace1,
                  dcc.Graph(id="Bar2", figure=px.bar())],
                  width=6, style={'textAlign': 'center'}
                  )

tab1 = dbc.Tab([dbc.Row([grafico1,grafico2])],style={'height': '550px'},label="Tab 1")

tab2=dbc.Tab([dbc.Row([grafico3,grafico4])],style={'height': '550px'},label="Tab 2")


tabs = dbc.Col( dbc.Card(dbc.Tabs([tab1,tab2])), width=10)


app.layout = dbc.Container([header, dbc.Row([control,tabs,]),],fluid=True,className="dbc dbc-ag-grid",
                           style={'height': '550px'}
)


@callback(Output("Pie1", "figure"), Input("indicador", "value")
)

def update(indicador):
    global df
#--------------------------------------------------------------------------
    #print('indicador',indicador)
    total_casos = len(df)
# Agrupa por la columna 'provincia_nombre' y cuenta los casos por cada provincia
    df1 = df.groupby(indicador).size().reset_index(name='casos')
# Calcula el porcentaje de casos por provincia respecto al total
    df1['porcentaje'] = (df1['casos'] / total_casos) * 100
    df1=df1.sort_values(by='porcentaje', ascending=False)
    df1['porcentaje'] = df1['porcentaje'].round(2)
    
   
    fig = px.pie(df1[df1['porcentaje'] >= 2], values='porcentaje', names=indicador,custom_data=['porcentaje'])
    
    fig.update_traces(textinfo='label+value', hoverinfo='label+text', text=df1['porcentaje'].astype(str) + '%')
    fig.update_layout(title={'text': 'Porcentaje de Suicidios por Provincia >5%', 'x':0.5, 'xanchor': 'center'})
    fig.update_layout(legend={'font': {'size': 8}})  # Achicar la leyenda
    fig.update_layout(height=550) 

    #··········································································
    return fig


#······························calback 1b·················································
@callback(
    Output("Bar1", "figure" ),Input("indicator1b", "value"),)

def update(indicator1b):
    global df
    # Calcula el porcentaje total combinado de ambos sexos
    
    total =df.shape[0]
    if indicator1b =='año':
        orden_etiquetas = ['2017','2018','2019','2020','2021','2022']
    else:
        orden_etiquetas = ['5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
                    '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                    '80-84', '85-89', '+90']
    
    # Añade una nueva fila al DataFrame con el porcentaje total
    df1=df.groupby(['suicida_sexo',indicator1b]).size().reset_index(name='casos')
    df1['porcentaje']=(df1['casos']/total)*100
    

    fig = px.bar(df1, y='porcentaje', x=indicator1b, color='suicida_sexo', category_orders={indicator1b: orden_etiquetas},
                    barmode='stack')
    # Actualiza la configuración de la figura para ajustar el espaciado entre las barras
    fig.update_layout(title={'text': f'Porcentaje de Suicidios por {indicator1b}', 'x':0.5, 'xanchor': 'center'})
    
    
    if indicator1b =='año':
        orden_etiquetas = ['2017','2018','2019','2020','2021','2022']
        fig.update_layout(xaxis=dict(range=['2016', '2023']))
        fig.update_layout(yaxis=dict(range=[0, 20]))
        #fig.add_annotation(x='2017', y=25, text=titulo_anotacionM, showarrow=False, font=dict(size=10))

    else:
        orden_etiquetas = ['5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
                    '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                    '80-84', '85-89', '+90']
        fig.update_layout(yaxis=dict(range=[0, 15]))

    fig.update_layout(height=200) 

    return fig



#······························calback 1c·················································
@callback(
    Output("line1", "figure" ),
    Input("indicator1c", "value"),
)

def update(indicator1c):
    global df
    
    total =df.shape[0]
    
    if indicator1c =='mes':
        orden_etiquetas = [ 1,  2,  3,  5,  4,  6,  7,  8,  9, 10, 11, 12]
    elif indicator1c =='dias':
        orden_etiquetas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 
                           11, 12, 13, 14, 15, 16,17, 18, 19, 20,
                           21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                           31]
    elif indicator1c =='hora':
        orden_etiquetas = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
       
    # Añade una nueva fila al DataFrame con el porcentaje total
    df1=df.groupby([indicator1c]).size().reset_index(name='casos')
    df1['porcentaje']=(df1['casos']/total)*100
    #print(df1)

    fig = px.line(df1, y='porcentaje', x=indicator1c,
                  category_orders={indicator1c: orden_etiquetas}
                  ,markers=True)
    # Actualiza la configuración de la figura para ajustar el espaciado entre las barras
    fig.update_layout(title={'text': f'Porcentaje de Suicidios por {indicator1c}', 'x':0.5, 'xanchor': 'center'})
    
    
    if indicator1c =='mes':
        fig.update_layout(xaxis=dict(range=[0,13]))
        fig.update_layout(yaxis=dict(range=[0, 14]))
        #fig.add_annotation(x='2017', y=25, text=titulo_anotacionM, showarrow=False, font=dict(size=10))

    elif indicator1c =='dias':
        fig.update_layout(xaxis=dict(range=[1,31]))
        fig.update_layout(yaxis=dict(range=[0,4]))
    elif indicator1c =='hora': 
        fig.update_layout(xaxis=dict(range=[0,23]))
        fig.update_layout(yaxis=dict(range=[0, 10])) 

    fig.update_layout(height=200) 

    return fig


#······························callback1d··················································
@callback(Output("Map1", "figure" ),Input("indicator1d", "value"))


def update(indicator1d):
    from unidecode import unidecode
    global df

    df1=df

    df_2a = df1.groupby(['provincia_nombre']).size().reset_index(name='casos_provincia')
    df_2a = df_2a.round(2)

    df_2b = df1.groupby(['provincia_nombre','departamento_nombre']).size().reset_index(name='casos_departamento').sort_values(by=['provincia_nombre'],ascending=False)
    df_2b = df_2b.round(2)

    df_2c = pd.merge(df_2b, df_2a, on='provincia_nombre')
    df_2c.rename(columns={'casosprovincias': 'casos_provincias'}, inplace=True)
    df_2c=df_2c[['provincia_nombre','departamento_nombre','casos_provincia','casos_departamento']]


    input_provincia = indicator1d
    casos='casos_departamento'

    df_2d = df_2c[df_2c['provincia_nombre']==input_provincia]

    #** importamos geojson
    ruta_archivo = '/home/julio/jupyter_files/ArgentinaSeguridad/suicidio/VISUALIACION/departamentos-argentina.json'
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as f:
            geojson_data = json.load(f)
    else:
        print(f"El archivo {ruta_archivo} no existe.")
    
    departamentos_filtrar = df_2d['departamento_nombre'].unique()
    provincias_filtrar = df_2d['provincia_nombre'].unique()
    features_filtrados = []
    
    for feature in geojson_data['features']:
        atributos = feature['properties']
        departamento = atributos.get('departamento')
        provincia = atributos.get('provincia')
        
        if (provincia in provincias_filtrar) and (departamento in departamentos_filtrar) :
            features_filtrados.append(feature)
    
    geojson_b = {'type': 'FeatureCollection','features': features_filtrados}
    a=geojson_b['features']
    # Iterar sobre cada feature en la lista 'a'
    i=1
    for feature in a:
        #print('··········i····················',i)
        # Acceder a los atributos del feature
        atributos = feature['properties']
        # Obtener el valor de la provincia y el departamento
        provincia = atributos['provincia']
        departamento = atributos['departamento']
        # Imprimir la provincia y el departamento
        #print('atributos',atributos)
        #print("Provincia:", provincia)
        #print("Departamento:", departamento)
        i=i+1

    #print(df_2d)
    # Crear el mapa utilizando el GeoJSON filtrado
    fig = px.choropleth_mapbox(df_2d,
                            geojson=geojson_b,
                            locations='departamento_nombre',  
                            featureidkey='properties.departamento',
                            #color='casos_provincia',  
                            color=casos,
                            color_continuous_scale="Viridis",  
                            mapbox_style="carto-positron",  
                            center={"lat": -38.4161, "lon": -63.6167},  
                            zoom=4,  
                            opacity=0.5,  
                            title='Mapa de Calor de Precios en Argentina',  
                            )
    fig.update_layout(height=550) 

    return fig





@callback(
    Output("Bar2", "figure" ),Input("indicator1d", "value"),Input("indicator1b", "value"))

def update(indicator1d,indicator1b):
    global df
    # Calcula el porcentaje total combinado de ambos sexos

    df['provincia_nombre'] = df['provincia_nombre'].apply(lambda x: x.upper())
    df['departamento_nombre'] = df['departamento_nombre'].apply(lambda x: x.upper())
    
    total =df.shape[0]
    #print('AQUI',indicator1d)
    df1=df[df['provincia_nombre']==indicator1d]
    total2=df1.shape[0]
    if indicator1b =='año':
        orden_etiquetas = ['2017','2018','2019','2020','2021','2022']
    else:
        orden_etiquetas = ['5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
                    '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79',
                    '80-84', '85-89', '+90']
    
    # Añade una nueva fila al DataFrame con el porcentaje total
    df1=df1.groupby(['suicida_sexo',indicator1b]).size().reset_index(name='casos')
    df1['porcentaje']=(df1['casos']/total2)*100
    
    #prtn()
    fig = px.bar(df1, y='porcentaje', x=indicator1b, color='suicida_sexo', category_orders={indicator1b: orden_etiquetas},
                    barmode='stack')
    # Actualiza la configuración de la figura para ajustar el espaciado entre las barras
    fig.update_layout(title={'text': f'Porcentaje de Suicidios por {indicator1b}', 'x':0.5, 'xanchor': 'center'})
    
    
    if indicator1b =='año':
        fig.update_layout(xaxis=dict(range=['2016', '2023']))
        #fig.update_layout(yaxis=dict(range=[0, 20]))
        #fig.add_annotation(x='2017', y=25, text=titulo_anotacionM, showarrow=False, font=dict(size=10))

    #else:
        #fig.update_layout(yaxis=dict(range=[0, 6]))

    fig.update_layout(height=250) 

    return fig


@callback(
    Output('filtered-data-html', 'children')
    ,Input("indicator1d", "value")#,Input("indicator1b", "value")
    )

def update(indicator1d):
    input_value=indicator1d
    global df2


    filtered_df = df2[df2['provincia_nombre'] == input_value]
   
    # Obtener las columnas desde la segunda hasta la última
    filtered_columns = filtered_df.columns[1:]
    
    # Construir las filas de la tabla HTML
    rows = []
    for i in range(0, len(filtered_columns), 3):
        row = []
        for j in range(3):
            col_index = i + j
            if col_index < len(filtered_columns):
                column_name = filtered_columns[col_index]
                column_value = filtered_df.iloc[0][column_name]
                row.append(html.Td([html.Strong(column_name), html.Br(), column_value]))
        rows.append(html.Tr(row))

        
    # Construir la tabla HTML
    filtered_data_html =html.Div([  
        html.H4(f'{indicator1d}:',  style={'display': 'flex', 'justify-content': 'center', 'font-size': '14px', 'font-family': 'Arial'}
                ),
        html.Table(rows,style={'margin': 'auto', 'text-align': 'center', 'font-size': '12px', 'font-family': 'Arial'}
                   )
    ])
    # Retornar el HTML generado
    return filtered_data_html



if __name__ == "__main__":
    app.run_server(debug=True)
#Import libs
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CONTENT_STYLE = {
    #'margin-left': '18%',
    #'margin-left': '5%',
    'margin-right': '5%',
    'padding' : '10px 5px 15px 20px'
}

#Import ultimate df 
df = pd.read_csv('ultimate_df.csv')

#region figures

#Create figures 

#Fig 1 : Distribution des pays dans le dataframe

data,index = pd.factorize(df.country)
labels = [index[i] for i in data]
labels = pd.DataFrame(pd.Series(labels).value_counts()).reset_index()
labels.columns = ['Country',"Nb_occurences"]
most_represented_countries = labels[labels.Nb_occurences > 200]['Country']

fig1 = px.bar(labels[labels.Nb_occurences > 200].sort_values('Nb_occurences'), x="Nb_occurences", y="Country", orientation='h')

# fig1.update_layout(
#     paper_bgcolor='rgba(255, 255, 255, 0.8)',
#     plot_bgcolor='rgba(255, 255, 255, 0.8)'
# )

#Fig 2 : Score et prix moyens selon le pays 
data_fig2=df[df.country.isin(most_represented_countries)].groupby('country').mean()[['points','price']].sort_values(by=['price','points']).reset_index()
countries_fig2 = data_fig2.country
countries = data_fig2.country

fig2 = go.Figure(data=[
                go.Bar(name='Price', y=countries, x = data_fig2['price'],orientation='h'),    
                go.Bar(name='Points',y=countries, x = data_fig2['points'],orientation='h')
])

fig2.update_layout(barmode="group")


#Fig 3 : Score et prix moyen selon les dates 
data_fig3 = df.groupby('millesime').median()[['points','price']].sort_values(by='price').reset_index()

date_fig3 = data_fig3.millesime

fig3 = go.Figure(data=[
                go.Bar(name='Price', y=list(range(len(date_fig3))), x = data_fig3['price'],orientation='h'),    
                go.Bar(name='Points',y=list(range(len(date_fig3))), x = data_fig3['points'],orientation='h')
])


#Fig 4 : Distribution des prix 
fig4 = px.box(y=np.log(df.price))


fig4.update_layout(yaxis = dict(
        tickmode = 'array',
        tickvals = list(range(2,8)),
        ticktext = [np.exp(i) for i in range(2,9)]
    ))

#Fig 5 : Les millesimes les plus représentés 
data,index = pd.factorize(df.millesime)
labels = [index[i] for i in data]
labels = pd.DataFrame(pd.Series(labels).value_counts()).reset_index()
labels.columns = ['millesime',"Nb_occurences"]
labels = labels[labels.Nb_occurences > 200].sort_values('Nb_occurences',ascending=False)
fig5 = px.bar(labels, x="Nb_occurences", y="millesime", orientation='h')


df = pd.read_csv('ultimate_df.csv')
#Fig 6 : Evolution des points et price moyen par millesime par province 
columns = [i for i in df[df['country'] == 'France'].province.unique()]
evolution = pd.DataFrame(index=list(range(2000,2022)),columns=columns)
for i in columns:
     evolution[i] = df[(df['country'] == 'France') & (df['province'] == i)].groupby(by=['millesime']).mean()['price']
fig6 = px.line(evolution.reset_index().melt(id_vars=['index']).interpolate(), x="index", y="value", 
color="variable",line_shape='spline',color_discrete_sequence=px.colors.qualitative.Antique)


result = pd.read_csv('result.csv')
features = list(result.columns)
features.remove('description')
features.remove('Unnamed: 0')
fig7 = go.Figure(data=[go.Table(header=dict(values=list(result[features].columns)),
                 cells=dict(values=[list(result[i]) for i in result[features].columns]))
                     ])


# map_df = pd.read_csv('map_df.csv')

# map_df.description = map_df.description.apply(lambda x : float(x))

# print(map_df)

# fig7 = px.choropleth(map_df, 
#                     locations="locations", 
#                     color="description", 
#                     hover_name="country", 
#                     )



#endregion


#region main content

main_title = dbc.Row(align='center',justify='center',children=[
    html.H1('Analyse des prix du vins')]
)


title_fig1 = dbc.Row(align='center',justify='left',children=[
    html.H3('Distribution des pays')
])

fig_1 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig1',
                config = {'displayModeBar' : True,
                },
                figure = fig1
                )
        ]),
        dbc.Col(children=[
            html.Div('''On voit ici les plus représentés ''')
        ])

]
)

title_fig2 = dbc.Row(align='center',justify='left',children=[
    html.H3('Points et prix moyen par pays')
])

fig_2 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig2',
                config = {'displayModeBar' : True,
                },
                figure = fig2
                )
        ]),
        dbc.Col(children=[
            html.Div(''' Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an 
            unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, 
            remaining essentially unchanged. It was popularised in the 1960s with the release of
             Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing 
             software like Aldus PageMaker including versions of Lorem Ipsum.''')
        ])

]
)

title_fig3 = dbc.Row(align='center',justify='left',children=[
    html.H3('Points et prix moyens par date')
])

fig_3 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig3',
                config = {'displayModeBar' : True,
                },
                figure = fig3
                )
        ]),
        dbc.Col(children=[
            html.Div(''' Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an 
            unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, 
            remaining essentially unchanged. It was popularised in the 1960s with the release of
             Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing 
             software like Aldus PageMaker including versions of Lorem Ipsum.''')
        ])

]
)

title_fig4 = dbc.Row(align='center',justify='left',children=[
    html.H3('Distribution des prix')
])

fig_4 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig4',
                config = {'displayModeBar' : True,
                },
                figure = fig4
                )
        ]),
        dbc.Col(children=[
            html.Div(''' Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an 
            unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, 
            remaining essentially unchanged. It was popularised in the 1960s with the release of
             Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing 
             software like Aldus PageMaker including versions of Lorem Ipsum.''')
        ])

]
)


title_fig5 = dbc.Row(align='center',justify='left',children=[
    html.H3('Les millesimes les plus représentés')
])

fig_5 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig5',
                config = {'displayModeBar' : True,
                },
                figure = fig5
                )
        ]),
        dbc.Col(children=[
            html.Div(''' Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an 
            unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, 
            remaining essentially unchanged. It was popularised in the 1960s with the release of
             Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing 
             software like Aldus PageMaker including versions of Lorem Ipsum.''')
        ])

]
)


title_fig6 = dbc.Row(align='center',justify='left',children=[
    html.H3('Evolution des points et du prix par millesime par province')
])

fig_6 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig6',
                config = {'displayModeBar' : True,
                },
                figure = fig6
                )
        ])
      

]
)

dropdown_fig6 =   html.Div( dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in df.country.unique()],
                value='France'
            ))


title_fig_7 = dbc.Row(align='center',justify='left',children=[
    html.H3('Préconisation des prix pour le domaine de Croix')
])

fig_7 = dbc.Row(align='center',justify='left',
    children=[
        dbc.Col(children=[
            dcc.Graph(id='fig7',
                config = {'displayModeBar' : True,
                },
                figure = fig7
                )
        ])
      

]
)


#endregion


content = html.Div(
    [
        main_title,
        title_fig1,
        fig_1,
        title_fig2,
        fig_2,
        title_fig3,
        fig_3,
        title_fig4,
        fig_4,
        title_fig5,
        fig_5,
        title_fig6,
        dropdown_fig6,
        fig_6,
        title_fig_7,
        fig_7
    ],
    style=CONTENT_STYLE
)


#use bootstrap stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#define page layout, which contains sidebar and content
# app.layout = html.Div([sidebar, content])
app.layout = html.Div(style={
# 'background-image': 'url("/assets/apero.jpg")',
# 'background-color': 'transparent'

# 'background-repeat': 'no-repeat',
# 'background-position': 'right top',
# 'background-size': '150px 100px'
},children = [
content
])


@app.callback(
    Output('fig6','figure'),
    [Input('country','value')])
def update_figure(value):
    columns = [i for i in df[df['country'] == value].province.unique()]
    evolution = pd.DataFrame(index=list(range(2000,2022)),columns=columns)
    for i in columns:
        evolution[i] = df[(df['country'] == value) & (df['province'] == i)].groupby(by=['millesime']).mean()['price']
    fig6 = px.line(evolution.reset_index().melt(id_vars=['index']).interpolate(), x="index", y="value", 
    color="variable",line_shape='spline',color_discrete_sequence=px.colors.qualitative.Antique)
    return fig6
    




#Run the server at port 8085
#Accessible through : http://localhost:8085
if __name__ == '__main__':
    app.run_server(port='8085')
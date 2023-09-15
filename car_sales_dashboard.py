import pandas as pd
import plotly.express as px
import dash
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output

data = pd.read_csv('../historical_automobile_sales.csv')

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Automobile Sales Statistics Dashboard',style={'textAlign':'center','color':'#503D36','font-size':24}),
    html.Div(dcc.Dropdown(id='dropdown-statistics',
                          options=[{'label': 'Yearly Statistics','value':'Yearly Statistics'},
                                   {'label':'Recession Period Statistics','value':'Recession Period Statistics'}],
                          placeholder='Select a report type'),
                          style={'width':'80%', 'padding':'3px','font-size':'20px','text-align-last':'center'}),
    html.Div(dcc.Dropdown(id='select-year',
                          options=[{'label':i,'value':i} for i in [j for j in range(1980,2024)]],
                          placeholder='Select Year',
                          style={'width':'80%','padding':'3px','font-size':'20px','text-align-last':'center'})),
    html.Div([html.Div(id='output-container',className='chart-grid',style={'display':'flex'})])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))
def update_input_container(opt_input):
    if opt_input =='Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics',component_property='value'),Input(component_id='select-year',component_property='value')])
def update_output_container(dropIn,year):
    if dropIn == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year',y='Automobile_Sales',
                                            title="Fluctuation of Automobile sales during Recession"))

        type_rec = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(type_rec,x='Vehicle_Type',y='Automobile_Sales',
                                           title='Avg. No. of Vehicles Sold by Type'))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec,values='Advertising_Expenditure',names='Vehicle_Type',
                                           title='Expenditure Share by Vehicle Type'))

        emp_rec = recession_data.groupby(['Vehicle_Type','Automobile_Sales'])['unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(emp_rec,x='unemployment_rate',y='Automobile_Sales',color='Vehicle_Type',
                                           title='Effect of Unemployment Rate on Type and Sales'))

        return [html.Div(className='chart-item',children=[html.Div(children=[R_chart1]),html.Div(children=[R_chart2])]),
                html.Div(className='chart-item',children=[html.Div(children=[R_chart3]),html.Div(children=[R_chart4])])]

    elif (year and dropIn=='Yearly Statistics'):
        yearly_data = data[data['Year']==year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas,x='Year',y='Automobile_Sales',
                                            title='Yearly Automobile Sales'))

        tms = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(tms,x='Month',y='Automobile_Sales',
                                            title='Monthly Automobile Sales for the year {}'.format(year)))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,x='Vehicle_Type',y='Automobile_Sales',
                                           title='Average Vehicles Sold by Vehicle Type in the year {}'.format(year)))

        adex = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(adex,values='Advertising_Expenditure',names='Vehicle_Type',
                                           title='Advertisement Expenditure by Vehicle Type in the year {}'.format(year)))

        return [html.Div(className='chart-item',children=[html.Div(children=[Y_chart1]),html.Div(children=[Y_chart2])]),
                html.Div(className='chart-item',children=[html.Div(children=[Y_chart3]),html.Div(children=[Y_chart4])])]

if __name__ == '__main__':
    app.run_server()
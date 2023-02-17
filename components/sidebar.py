import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *


# ========= Layout ========= #
layout = dbc.Col([
    html.H1("MyBudget", className="text-primary"),
    html.P("by ASIMOV", className="text-info"),
    html.Hr(),
    # ====== Seção Perfil ====== #
    dbc.Button(id='avatar_btn', children=[
               html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')], style={'background-color': 'transparent', 'border-color': 'transparent'}),
    # ====== Seção Novo ======== #
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='open_new_recipe',
                       children=['+ Receita'])
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='open_new_expense',
                       children=['- Despesa'])
        ], width=6)
    ]),
    # ====== Modal Receita ===== #
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Receita')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição: '),
                    dbc.Input(
                        placeholder='Ex.: Dividendos, Herança...', id='text_recipe'),
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder='$100.00',
                              id='recipe_valor', value='')
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(id='date_recipes', min_date_allowed=date(2020, 1, 1), max_date_allowed=date(
                        2030, 12, 31), date=datetime.today(), style={'width': '100%'}),
                ], width=4),
                dbc.Col([
                    dbc.Label('Extras: '),
                    dbc.Checklist(options=[{'label': 'Foi recebida', 'value': 1}, {'label': 'Receita Recorrente', 'value': 2}], value=[1],
                                  id='switches_input_recipes', switch=True)
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da Receita'),
                    dbc.Select(id='select_recipe', options=[
                               {'label': i, 'value': i} for i in cat_receitas], value=cat_receitas[0])
                ], width=4)
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Adicionar Categoria',
                                            style={'color': 'green'}),
                                dbc.Input(
                                    type='text', placeholder='Nova categoria...', id='input_add_recipe', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success',
                                           id='add_category_recipe', style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(
                                    id='category-div-add-recipe', style={}),
                            ], width=6),
                            dbc.Col([
                                html.Legend('Excluir Categorias',
                                            style={'color': 'red'}),
                                dbc.Checklist(id='checklist_selected_style_recipe', options=[{'label': i, 'value': i, } for i in cat_receitas], value=[], label_checked_style={
                                              'color': 'red'}, input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},),
                                dbc.Button('Remover', color='warning', id='remove_category_recipe', style={
                                           'margin-top': '20px'}),
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion_recipe'),
                html.Div(id='id_test_recipe', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar Receita',
                               id='save_recipe', color='success'),
                    dbc.Popover(dbc.PopoverBody(
                        'Receita Salva'), target='save_recipe', placement='left', trigger='click'),
                ])
            ], style={'margin-top': '25px'})
        ]),
    ], style={'background-color': 'rgba(17, 140, 79, 0.05)'}, id='new_modal_recipe', size='lg', is_open=False, centered=True, backdrop=True),
    # ====== Modal Despesa ===== #
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Despesa')),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição: '),
                    dbc.Input(
                        placeholder='Ex.: Aluguel, Alimentação...', id='text_expense'),
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder='$100.00',
                              id='expense_valor', value='')
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(id='date_expenses', min_date_allowed=date(2020, 1, 1), max_date_allowed=date(
                        2030, 12, 31), date=datetime.today(), style={'width': '100%'}),
                ], width=4),
                dbc.Col([
                    dbc.Label('Extras: '),
                    dbc.Checklist(options=[{'label': 'Foi recebida', 'value': 1}, {'label': 'Receita Recorrente', 'value': 2}], value=[1],
                                  id='switches_input_expenses', switch=True)
                ], width=4),
                dbc.Col([
                    html.Label('Categoria da Despesa'),
                    dbc.Select(id='select_expense', options=[
                               {'label': i, 'value': i} for i in cat_despesas], value=cat_despesas[0])
                ], width=4)
            ], style={'margin-top': '25px'}),
            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Adicionar Categoria',
                                            style={'color': 'green'}),
                                dbc.Input(
                                    type='text', placeholder='Nova categoria...', id='input_add_expense', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success',
                                           id='add_category_expense', style={'margin-top': '20px'}),
                                html.Br(),
                                html.Div(
                                    id='category-div-add-expense', style={}),
                            ], width=6),
                            dbc.Col([
                                html.Legend('Excluir Categorias',
                                            style={'color': 'red'}),
                                dbc.Checklist(id='checklist_selected_style_expense', options=[{'label': i, 'value': i, } for i in cat_despesas], value=[], label_checked_style={
                                              'color': 'red'}, input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},),
                                dbc.Button('Remover', color='warning', id='remove_category_expense', style={
                                           'margin-top': '20px'}),
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion_expense'),
                html.Div(id='id_test_expense', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar Despesa',
                               id='save_expense', color='success'),
                    dbc.Popover(dbc.PopoverBody(
                        'Despesa Salva'), target='save_expense', placement='left', trigger='click'),
                ])
            ], style={'margin-top': '25px'})
        ]),
    ], style={'background-color': 'rgba(17, 140, 79, 0.05)'}, id='new_modal_expense', size='lg', is_open=False, centered=True, backdrop=True),
    # ====== Seção NAV ========= #
    html.Hr(),
    dbc.Nav([
            dbc.NavLink("Dashboard", href='/dashboards', active='exact'),
            dbc.NavLink("Extratos", href='/extratos', active='exact'),
            ], vertical=True, pills=True, id='nav_buttons', style={'margin-bottom': '50px'}),
], id='sidebar_complete')


# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output('new_modal_recipe', 'is_open'),
    Input('open_new_recipe', 'n_clicks'),
    State('new_modal_recipe', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Pop-up despesa


@app.callback(
    Output('new_modal_expense', 'is_open'),
    Input('open_new_expense', 'n_clicks'),
    State('new_modal_expense', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


@app.callback(
    Output('store-receitas', 'data'),
    Input('save_recipe', 'n_clicks'),
    [
        State('text_recipe', 'value'),
        State('recipe_valor', 'value'),
        State('date_recipes', 'date'),
        State('switches_input_recipes', 'value'),
        State('select_recipe', 'value'),
        State('store-receitas', 'data')
    ]
)
def salve_form_receita(n, descricao, valor, date, switches, categoria, dict_receitas):
    df_receitas = pd.DataFrame(dict_receitas)

    if n and not(valor == '' or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0]
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_receitas.loc[df_receitas.shape[0]] = [
            valor, recebido, fixo, date, categoria, descricao]
        df_receitas.to_csv('df_receitas.csv')

    data_return = df_receitas.to_dict()
    return data_return


@app.callback(
    Output('store-despesas', 'data'),
    Input('save_expense', 'n_clicks'),
    [
        State('text_expense', 'value'),
        State('expense_valor', 'value'),
        State('date_expenses', 'date'),
        State('switches_input_expenses', 'value'),
        State('select_expense', 'value'),
        State('store-despesas', 'data')
    ]
)
def salve_form_despesa(n, descricao, valor, date, switches, categoria, dict_despesas):
    df_despesas = pd.DataFrame(dict_despesas)

    if n and not(valor == '' or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_despesas.loc[df_despesas.shape[0]] = [
            valor, recebido, fixo, date, categoria, descricao]
        df_despesas.to_csv('df_despesas.csv')

    data_return = df_despesas.to_dict()
    return data_return


@app.callback(
    [
        Output('select_expense', 'options'),
        Output('checklist_selected_style_expense', 'options'),
        Output('checklist_selected_style_expense', 'value'),
        Output('store-cat-despesas', 'data')
    ],
    [
        Input('add_category_expense', 'n_clicks'),
        Input('remove_category_expense', 'n_clicks')
    ],
    [
        State('input_add_expense', 'value'),
        State('checklist_selected_style_expense', 'value'),
        State('store-cat-despesas', 'data')
    ]
)
def add_category(n, n2, txt, check_delete, data):
    cat_despesa = list(data['Categoria'].values())

    if n and not (txt == '' or txt == None):
        cat_despesa = cat_despesa + \
            [txt] if txt not in cat_despesa else cat_despesa

    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]

    opt_despesa = [{'label': i, 'value': i} for i in cat_despesa]
    df_cat_despesas = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesas.to_csv('df_cat_despesas.csv')
    data_return = df_cat_despesas.to_dict()

    return [opt_despesa, opt_despesa, [], data_return]


@app.callback(
    [
        Output('select_recipe', 'options'),
        Output('checklist_selected_style_recipe', 'options'),
        Output('checklist_selected_style_recipe', 'value'),
        Output('store-cat-receitas', 'data')
    ],
    [
        Input('add_category_recipe', 'n_clicks'),
        Input('remove_category_recipe', 'n_clicks')
    ],
    [
        State('input_add_recipe', 'value'),
        State('checklist_selected_style_recipe', 'value'),
        State('store-cat-receitas', 'data')
    ]
)
def add_category(n, n2, txt, check_delete, data):
    cat_receita = list(data['Categoria'].values())

    if n and not (txt == '' or txt == None):
        cat_receita = cat_receita + \
            [txt] if txt not in cat_receita else cat_receita

    if n2:
        if len(check_delete) > 0:
            cat_receita = [i for i in cat_receita if i not in check_delete]

    opt_receita = [{'label': i, 'value': i} for i in cat_receita]
    df_cat_receitas = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receitas.to_csv('df_cat_receitas.csv')
    data_return = df_cat_receitas.to_dict()

    return [opt_receita, opt_receita, [], data_return]

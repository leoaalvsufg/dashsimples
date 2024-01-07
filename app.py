from datetime import datetime
from flask import Flask, jsonify, render_template, request
import pandas as pd
import plotly
import plotly.express as px
import json

app = Flask(__name__)

# Read the data
df = pd.read_excel('templates/notasdev.xlsx')
df['DATA'] = pd.to_numeric(df['DATA'], errors='coerce')
df['DATA'] = pd.to_datetime(df['DATA'], unit='D', origin='1899-12-30')

# Agregando os dados para contar o número de notas fiscais por data
df_aggregated = df.groupby('DATA')['NOTA FISCAL'].count().reset_index()
df_aggregated.columns = ['DATA', 'QUANTIDADE']

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/datac')
def datac():
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)

        # Filtrar o DataFrame com base nas datas selecionadas
        df_filtrado = df[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
    else:
        df_filtrado = df

    # Agora, usar df_filtrado para criar o gráfico
    df_filtrado_aggregated = df_filtrado.groupby('DATA')['NOTA FISCAL'].count().reset_index()
    df_filtrado_aggregated.columns = ['DATA', 'QUANTIDADE']

    #fig = px.bar(df_filtrado_aggregated, x='DATA', y='QUANTIDADE',
    #             title='Número de Notas Fiscais Devolvidas por Dia')
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return jsonify(graphJSON)
        # Criando o gráfico com cores personalizadas
    fig = px.bar(df_filtrado_aggregated, x='DATA', y='QUANTIDADE',
                 title='Número de Notas Fiscais Devolvidas por Dia',
                 color='QUANTIDADE',  # Isso adicionará uma escala de cor baseada na quantidade
                 color_continuous_scale=px.colors.sequential.Viridis)  # Escolha uma paleta de cores

    # Personalização do layout do gráfico
    fig.update_layout(
        plot_bgcolor='rgba(128, 128, 128, 0.1)',  # Fundo cinza claro (ajuste a opacidade conforme necessário)
        paper_bgcolor='rgba(128, 128, 128, 0.1)',  # Fundo do papel (área em torno do gráfico)
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON)

@app.route('/data')
def data():
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)

        # Filtrar o DataFrame com base nas datas selecionadas
        df_filtrado = df[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
    else:
        df_filtrado = df

    # Agora, usar df_filtrado para criar o gráfico
    df_filtrado_aggregated = df_filtrado.groupby('DATA')['NOTA FISCAL'].count().reset_index()
    df_filtrado_aggregated.columns = ['DATA', 'QUANTIDADE']

    #fig = px.bar(df_filtrado_aggregated, x='DATA', y='QUANTIDADE',
    #             title='Número de Notas Fiscais Devolvidas por Dia')
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #return jsonify(graphJSON)
        # Criando o gráfico com cores personalizadas
   # Criando o gráfico de linhas
    fig = px.line(df_filtrado_aggregated, x='DATA', y='QUANTIDADE',
                  title='Número de Notas Fiscais Devolvidas por Dia')

    # Adicionando marcadores (pontos) ao gráfico de linhas
    fig.add_scatter(x=df_filtrado_aggregated['DATA'], y=df_filtrado_aggregated['QUANTIDADE'],
                    mode='markers+text', text=df_filtrado_aggregated['QUANTIDADE'],
                    textposition='top center')

    # Personalização do layout do gráfico
    fig.update_layout(
        plot_bgcolor='rgba(128, 128, 128, 0.1)',  # Fundo cinza claro
        paper_bgcolor='rgba(128, 128, 128, 0.1)',  # Fundo do papel
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON)

@app.route('/get-dados-comprador')
def get_dados_comprador():
    comprador_selecionado = request.args.get('comprador')
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    # Filtrar por comprador
    if comprador_selecionado:
        dados_filtrados = df[df['COMPRADOR'] == comprador_selecionado]
    else:
        dados_filtrados = df.copy()

    # Converte as strings de data para objetos datetime, se fornecidas
    if data_inicio:
        data_inicio = pd.to_datetime(data_inicio)
    if data_fim:
        data_fim = pd.to_datetime(data_fim)

    # Aplica o filtro de datas
    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        dados_filtrados = dados_filtrados[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
        dados_filtrados['DATA'] = dados_filtrados['DATA'].apply(lambda x: x.strftime('%Y-%m-%d'))
    print("get-dados-comprador")
    print(dados_filtrados)
    # Retorna um JSON com os dados filtrados
    
    return dados_filtrados.to_json(orient='records')

@app.route('/get-dados-filtrados')
def get_dados_filtrados():
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    # Converta as strings de data para objetos datetime
    #data_inicio = pd.to_datetime(data_inicio, format='%Y-%m-%d', errors='coerce')
    #data_fim = pd.to_datetime(data_fim, format='%Y-%m-%d', errors='coerce')

    # Aqui você precisa assegurar que as datas estão no formato correto ou fazer a conversão.
    # A função pd.to_datetime() pode ajudar com isso.
    
    df_filtrado = df
    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        df_filtrado = df_filtrado[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]


    #df_filtrado = df[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
    #print(df_filtrado)

    # Converta o DataFrame filtrado para JSON e retorne.
    print("get-dados-filtrados")
    print(df_filtrado)
    return df_filtrado.to_json(orient='records')

@app.route('/get-compradores')
def get_compradores():
    # Suponha que você deseja incluir as colunas 'LOJA' e 'NOTA FISCAL'
    if 'LOJA' in df.columns and 'NOTA FISCAL' in df.columns:
        dados_compradores = df[['COMPRADOR', 'LOJA', 'NOTA FISCAL']].drop_duplicates().to_dict(orient='records')
        return jsonify(dados_compradores)
    else:
        return jsonify({'error': 'Colunas necessárias não encontradas'}), 400

@app.route('/get-compradores-unicos')
def get_compradores_unicos():
    compradores_unicos = df['COMPRADOR'].drop_duplicates().sort_values().to_list()
    return jsonify(compradores_unicos)


@app.route('/data-comprador')
def data_comprador():
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)

        df_filtrado = df[(df['DATA'] >= data_inicio) & (df['DATA'] <= data_fim)]
    else:
        df_filtrado = df

    comprador_aggregated = df_filtrado.groupby('COMPRADOR')['NOTA FISCAL'].count().reset_index()
    comprador_aggregated.columns = ['COMPRADOR', 'QUANTIDADE_PEDIDOS']

    fig_comprador = px.bar(comprador_aggregated, x='COMPRADOR', y='QUANTIDADE_PEDIDOS',
                           title='Quantidade de Pedidos por Comprador')

    graphJSON_comprador = json.dumps(fig_comprador, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON_comprador)


@app.route('/get-ocorrencias-comprador')
def get_ocorrencias_comprador():
    comprador_selecionado = request.args.get('comprador')
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    df_filtrado = df
    if comprador_selecionado:
        df_filtrado = df_filtrado[df_filtrado['COMPRADOR'] == comprador_selecionado]
    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        df_filtrado = df_filtrado[(df_filtrado['DATA'] >= data_inicio) & (df_filtrado['DATA'] <= data_fim)]

    ocorrencias = df_filtrado['MOTIVO DA DEVOLUÇÃO'].value_counts().reset_index()
    ocorrencias.columns = ['Retorno do Fornecedor', 'Quantidade de Ocorrências']
    return ocorrencias.to_dict(orient='records')

@app.route('/get-ocorrencias-por-comprador')
def get_ocorrencias_por_comprador():
    comprador_selecionado = request.args.get('comprador')
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    df_filtrado = df
    if comprador_selecionado:
        df_filtrado = df_filtrado[df_filtrado['COMPRADOR'] == comprador_selecionado]
    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        df_filtrado = df_filtrado[(df_filtrado['DATA'] >= data_inicio) & (df_filtrado['DATA'] <= data_fim)]

    ocorrencias = df_filtrado.groupby(['COMPRADOR', 'MOTIVO DA DEVOLUÇÃO']).size().reset_index(name='Quantidade de Ocorrências')
    return ocorrencias.to_json(orient='records')

@app.route('/get-ocorrencias-por-motivo')
def get_ocorrencias_por_motivo():
    comprador_selecionado = request.args.get('comprador')
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    df_filtrado = df
    if comprador_selecionado:
        df_filtrado = df_filtrado[df_filtrado['COMPRADOR'] == comprador_selecionado]
    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        df_filtrado = df_filtrado[(df_filtrado['DATA'] >= data_inicio) & (df_filtrado['DATA'] <= data_fim)]

    ocorrencias = df_filtrado.groupby('MOTIVO DA DEVOLUÇÃO').size().reset_index(name='Quantidade de Ocorrências')
    print("ocorrencias")
    print(ocorrencias)
    return ocorrencias.to_json(orient='records')

@app.route('/get-datas')
def get_datas():
    # Filtrar valores NaN ou inválidos
    datas_validas = df['DATA'].dropna()

    # Converter as datas para string e ordenar
    datas_unicas = sorted(datas_validas.dt.strftime('%Y-%m-%d').unique())
    return jsonify(datas_unicas)

@app.route('/get-retorno-fornecedor')
def get_retorno_fornecedor():
    # Filtra o DataFrame com base nos parâmetros, se fornecidos
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')
    comprador = request.args.get('comprador')

    df_filtrado = df
    if data_inicio and data_fim:
        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)
        df_filtrado = df_filtrado[(df_filtrado['DATA'] >= data_inicio) & (df_filtrado['DATA'] <= data_fim)]

    if comprador:
        df_filtrado = df_filtrado[df_filtrado['COMPRADOR'] == comprador]

    # Agrega os dados para obter a contagem por fornecedor
    retorno_fornecedor = df_filtrado['FORNECEDOR'].value_counts().reset_index()
    retorno_fornecedor.columns = ['Retorno do Fornecedor', 'Quantidade de Ocorrências']
    return retorno_fornecedor.to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

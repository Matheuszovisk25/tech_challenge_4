import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from api_key import NEWS_API_KEY
import matplotlib as plt 



def carregar_dados(caminho_arquivo):
    dados = pd.read_excel(caminho_arquivo, sheet_name='Planilha1')

    dados = dados.loc[:, ~dados.columns.duplicated()]

    if 'Preço - petróleo bruto - Brent (FOB)' in dados.columns:
        dados = dados.rename(columns={'Preço - petróleo bruto - Brent (FOB)': 'Preco_petroleo_bruto_Brent_FOB'})
        
    dados['Data'] = pd.to_datetime(dados['Data'], errors='coerce')
    dados['Preco_petroleo_bruto_Brent_FOB'] = pd.to_numeric(dados['Preco_petroleo_bruto_Brent_FOB'], errors='coerce')
    return dados

def buscar_noticias(api_key, query='petróleo', language='pt'):
    url = f'https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        artigos = response.json().get('articles')
        # Filtra as notícias que mencionam petróleo no título ou na descrição
        artigos_filtrados = [
            artigo for artigo in artigos 
            if ('petróleo' in artigo['title'].lower() if artigo['title'] else False) or 
               ('petróleo' in artigo['description'].lower() if artigo['description'] else False)
        ]
        return artigos_filtrados
    else:
        return None
    
#------------------------------------------------------INTRODUÇÃO--------------------------------------------------------------------------
def introducao(dados):
    """
    Exibe a introdução da aplicação.
    """
    st.title("Introdução")
    st.write(""" O petróleo é uma das commodities mais importantes do mundo, desempenhando um papel crucial na economia global. Ele é essencial não apenas como fonte de energia, mas também como matéria-prima para uma vasta gama de produtos, desde plásticos até produtos químicos. A produção de petróleo é, portanto, um indicador vital de poder econômico e estabilidade para muitos países.\n   
    A extração do petróleo envolve uma técnica de detonação de rochas com uma carga explosiva a uma profundidade específica, afim de identificar potencial reservas.\n
    Com essa matéria prima é possível produzir diversos produtos essenciais como:\b
    - Combustível: gasolina, disel e querosene\b
    - Lubrificante: óleo e graxas\b
    - Materiais: plásticos, asfalto e fibras sintéticas\b
    - Produtos Químicos: solventes e fertilizantes""")    
    st.write(""" Para poder medir a quantidade de extração dessa material é utilizada uma medida comumente usada na indústria petrolífera para quantificar o volume de petrólio bruto, sendo essa unidade chamada que "barril de petróleo" que equivale a 159 litros. Contudo a conversão exata de 1 barril é de 42 galões americanos que é exatamente 3,78541 litros. \n
    Portanto o cálculo é exatamente 42 galões americanos x 3,78541 litros = galão 159 litros.""")
    st.write(""" Para promover a elaboração de políticas sólidas, mercados eficientes e a compreensão pública da energia e da sua interação com a economia e o ambiente, a instituição "EIA.gov" recolhe, analisa e divulga informações energéticas e disponibiliza em seu site com ampla gama de informações como produção de energia, estoques, demanda, importações, exportações e preços que é o assunto principal da nossa consultoria.\n
    Nossos dashboard é interativo com insights relevantes para colaborar na tomada de decisão com a análise do preço petróleo brent, além de nosso modelo de Machine Learning com o Forecasting dos custos com base no histórico de preços apresentado no site EIA.gov "Energy Information Administration.\n
    Para facilitar na compreensão da nossa consultoria apresentarmos-ei os momentos das crises econômicas e as demandas globais do petróleo que diretamente influenciam na alta e baixa dos custos referente ao barril.""")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados['Data'], y=dados['Preco_petroleo_bruto_Brent_FOB'], mode='lines', name='Preço do Brent (FOB)', line=dict(color='blue')))

    # Anotações para eventos importantes
    eventos = [
        {'data': '1990-08-02', 'evento': 'Guerra do Golfo', 'cor': 'red'},
        {'data': '2008-09-15', 'evento': 'Crise do Subprime', 'cor': 'orange'},
        {'data': '2010-12-17', 'evento': 'Primavera Árabe', 'cor': 'green'},
        {'data': '2020-03-11', 'evento': 'Pandemia de COVID-19', 'cor': 'purple'}
    ]

    for evento in eventos:
        fig.add_shape(
            type="line",
            x0=evento['data'], y0=dados['Preco_petroleo_bruto_Brent_FOB'].min(),
            x1=evento['data'], y1=dados['Preco_petroleo_bruto_Brent_FOB'].max(),
            line=dict(color=evento['cor'], width=2, dash="dash")
        )
        fig.add_annotation(
            x=evento['data'], y=dados['Preco_petroleo_bruto_Brent_FOB'].max(),
            ax=0, ay=-30,
            text=evento['evento'], showarrow=True, arrowhead=2,
            arrowcolor=evento['cor'], arrowsize=1, arrowwidth=2,
            font=dict(color=evento['cor'], size=12),
            textangle=-45
        )

    # Adicionando trace para cada evento para incluir na legenda
    for evento in eventos:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            line=dict(color=evento['cor'], dash='dash'),
            showlegend=True,
            name=evento['evento']
        ))

    fig.update_layout(
        title='Evolução dos Preços do Petróleo',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=100)  # Margem inferior para espaço das legendas
    )

    st.plotly_chart(fig)

#------------------------------------------------------FIM INTRODUÇÃO--------------------------------------------------------------------------


#------------------------------------------------------CONCLUSÃO--------------------------------------------------------------------------
def conclusao():
    """
    Exibe a conclusão da aplicação.
    """
    st.title("Conclusão")
    st.write("""
        Obrigado por usar nossa aplicação para analisar os preços do petróleo Brent,
        esperamos que tenha encontrado as informações úteis.
        Se tiver alguma dúvida ou sugestão, por favor, entre em contato.\n
        O petróleo é um recurso natural de extrema importância, tanto histórica quanto economicamente, mas que também apresenta grandes desafios ambientais. 
        O futuro da energia deve equilibrar a demanda por combustíveis com a necessidade de práticas sustentáveis.
    """)
#------------------------------------------------------FIM CONCLUSÃO--------------------------------------------------------------------------


#------------------------------------------------------INICIO EXIBIR--------------------------------------------------------------------------
def exibir(dados):
    """
    Exibe as diferentes análises dos dados do preço do petróleo Brent.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.title("Análise do Preço do Petróleo Brent")

    submenu = option_menu(
        menu_title="",  
        options=["Dados Brutos", "Preço ao Longo do Tempo", "Estatísticas Descritivas", "Análise de Tendências", "GeoPlot"],
        icons=["table", "line-chart", "bar-chart", "trend-up"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Dados Brutos":
        st.subheader("Dados Brutos")
        st.write("Visualize os dados brutos do preço do petróleo Brent.")
        st.write(dados)

    elif submenu == "Preço ao Longo do Tempo":
        st.subheader("Preço do Petróleo Brent ao Longo do Tempo")
        st.write("Selecione um intervalo de datas para visualizar a evolução do preço do petróleo Brent.")
        data_min = dados['Data'].min().date()
        data_max = dados['Data'].max().date()

        data_inicio, data_fim = st.slider("Selecione o intervalo de datas", min_value=data_min, max_value=data_max, value=(data_min, data_max), format="DD/MM/YYYY")

        if data_inicio > data_fim:
            st.error("Data de início não pode ser maior que a data de fim.")
        else:
            dados_filtrados = plotar_evolucao_preco_interativo(dados, data_inicio, data_fim)

            csv = dados_filtrados.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name='preco_petroleo_brent_filtrado.csv',
                mime='text/csv',
            )

    elif submenu == "Estatísticas Descritivas":
        st.subheader("Estatísticas Descritivas")
        st.write("Veja as estatísticas descritivas dos preços do petróleo Brent.")
        st.write(dados.describe())

        st.subheader("Valores Importantes")
        estatisticas = {
            "Menor Valor": dados['Preco_petroleo_bruto_Brent_FOB'].min(),
            "Maior Valor": dados['Preco_petroleo_bruto_Brent_FOB'].max(),
            "Média": dados['Preco_petroleo_bruto_Brent_FOB'].mean(),
            "Mediana": dados['Preco_petroleo_bruto_Brent_FOB'].median(),
            "Desvio Padrão": dados['Preco_petroleo_bruto_Brent_FOB'].std()
        }
        st.write(pd.DataFrame(estatisticas, index=[0]))

    elif submenu == "Análise de Tendências":
        st.write("Explore as tendências nos preços do petróleo Brent.")
        plotar_analise_tendencias(dados)
    
    elif submenu == "GeoPlot":
        geoplot_submenu = option_menu(
            menu_title="GeoPlot",  
            options=["Produção", "Exportação", "Consumo"],
            icons=["globe", "arrow-up", "arrow-down"],
            menu_icon="map",
            default_index=0,
            orientation="horizontal"
        )
        
        if geoplot_submenu == "Produção":
            plotar_mapa_producao()
        elif geoplot_submenu == "Exportação":
            plotar_mapa_exportacao()
        elif geoplot_submenu == "Consumo":
            plotar_mapa_consumo()
    
#------------------------------------------------------FIM EXIBIR--------------------------------------------------------------------------



#------------------------------------------------------INICIO PLOTS--------------------------------------------------------------------------

#Todos os gráficos devem ser inseridos dentro destes limites.


#------------------------------------------------------PLOTS DADOS BRUTOS--------------------------------------------------------------------------

#------------------------------------------------------INICIO plotar_evolucao_preco_interativo--------------------------------------------------------------------------
def plotar_evolucao_preco_interativo(dados, data_inicio, data_fim):
    """
    Plota a evolução do preço do petróleo Brent em um intervalo de datas específico.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    data_inicio (str): A data de início do intervalo.
    data_fim (str): A data de fim do intervalo.

    Retorna:
    DataFrame: Um DataFrame filtrado contendo os dados no intervalo de datas especificado.
    """
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    dados_filtrados = dados[(dados['Data'] >= data_inicio) & (dados['Data'] <= data_fim)]
    fig = px.line(dados_filtrados, x='Data', y='Preco_petroleo_bruto_Brent_FOB', title='Evolução do Preço do Petróleo Brent')
    fig.update_xaxes(title_text='Data')
    fig.update_yaxes(title_text='Preço (USD)')
    st.plotly_chart(fig)
    return dados_filtrados
#------------------------------------------------------FIM plotar_evolucao_preco_interativo--------------------------------------------------------------------------

#------------------------------------------------------INICIO plotar_analise_tendencias--------------------------------------------------------------------------
def plotar_analise_tendencias(dados):
    """
    Plota a análise de tendências nos preços do petróleo Brent utilizando médias móveis e permite o download dos dados.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.subheader("Análise de Tendências")
    st.write("Explore as tendências nos preços do petróleo Brent.")

    # Correção da Média Móvel
    dados['Media_Movel_30'] = dados['Preco_petroleo_bruto_Brent_FOB'].rolling(window=30).mean()

    st.write("Selecione um intervalo de datas para visualizar a análise de tendências.")
    data_min = dados['Data'].min().date()
    data_max = dados['Data'].max().date()

    data_inicio, data_fim = st.slider("Selecione o intervalo de datas", min_value=data_min, max_value=data_max, value=(data_min, data_max), format="DD/MM/YYYY")

    if data_inicio > data_fim:
        st.error("Data de início não pode ser maior que a data de fim.")
    else:
        dados_filtrados = dados[(dados['Data'] >= pd.to_datetime(data_inicio)) & (dados['Data'] <= pd.to_datetime(data_fim))]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Preco_petroleo_bruto_Brent_FOB'], mode='lines', name='Preço do Brent (FOB)'))
        fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Media_Movel_30'], mode='lines', name='Média Móvel 30 Dias'))

        fig.update_layout(title='Análise de Tendências nos Preços do Petróleo Brent',
                          xaxis_title='Data',
                          yaxis_title='Preço (USD)')

        st.plotly_chart(fig)

        # Botão para baixar os dados filtrados
        csv = dados_filtrados.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name='analise_tendencias_preco_petroleo_brent.csv',
            mime='text/csv',
        )
#------------------------------------------------------FIM plotar_analise_tendencias--------------------------------------------------------------------------

#------------------------------------------------------FIM DADOS BRUTOS--------------------------------------------------------------------------




#------------------------------------------------------PLOTS COVID-19--------------------------------------------------------------------------


#------------------------------------------------------INICIO plotar_impacto_covid--------------------------------------------------------------------------
def plotar_impacto_covid(dados):
    """
    Plota o impacto da COVID-19 no preço do petróleo Brent e permite o download dos dados.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.subheader("Impacto da COVID-19")
    st.write("""
        A pandemia de COVID-19 teve um impacto profundo e significativo nos mercados globais, incluindo o mercado de petróleo. 
        Durante a pandemia, a demanda por petróleo caiu drasticamente devido ao lockdown global e às restrições de viagem. 
        Isso resultou em uma queda acentuada nos preços do petróleo em 2020. Com a recuperação gradual da economia e o ajuste da produção pela OPEP+, 
        os preços começaram a se recuperar no final de 2020 e ao longo de 2021.
    """)

    dados_covid = dados[(dados['Data'] >= '2019-01-01') & (dados['Data'] <= '2021-12-31')]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados_covid['Data'], y=dados_covid['Preco_petroleo_bruto_Brent_FOB'],
                             mode='lines', name='Preço do Brent (FOB)',
                             line=dict(color='blue')))

    fig.add_shape(type="line",
                  x0='2020-03-11', y0=dados_covid['Preco_petroleo_bruto_Brent_FOB'].min(),
                  x1='2020-03-11', y1=dados_covid['Preco_petroleo_bruto_Brent_FOB'].max(),
                                    line=dict(color="red", width=2, dash="dash"))

    fig.add_annotation(x='2020-03-11', y=dados_covid['Preco_petroleo_bruto_Brent_FOB'].max(),
                       text="Início da Pandemia ",
                       showarrow=True, arrowhead=1)

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='red', dash='dash'),
        showlegend=True,
        name='Início da Pandemia '
    ))

    fig.update_layout(title='Impacto da COVID-19 no Preço do Petróleo Brent (2019-2021)',
                      xaxis_title='Data',
                      yaxis_title='Preço (USD)')
    st.plotly_chart(fig)

    # Permite o download dos dados filtrados da COVID-19 como CSV
    csv = dados_covid.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='impacto_covid_preco_petroleo_brent.csv',
        mime='text/csv',
    )
#------------------------------------------------------FIM plotar_impacto_covid--------------------------------------------------------------------------

#------------------------------------------------------INICIO plotar_comparacao_pre_pandemia_pandemia--------------------------------------------------------------------------
def plotar_comparacao_pre_pandemia(dados):
    st.subheader("Comparação de Preços Antes, Durante e Pós-Pandemia")
    st.write("""
        Este gráfico compara os preços do petróleo Brent em três períodos distintos: antes da pandemia (2019), durante a pandemia (2020) e pós-pandemia (2021). 
        Ele ajuda a visualizar como a pandemia afetou os preços e como eles se comportaram após o fim das restrições mais rigorosas.
    """)

    pre_covid_2019 = dados[(dados['Data'] >= '2019-01-01') & (dados['Data'] < '2020-01-01')]
    durante_covid_2020 = dados[(dados['Data'] >= '2020-01-01') & (dados['Data'] < '2021-01-01')]
    pos_covid_2021 = dados[(dados['Data'] >= '2021-01-01') & (dados['Data'] < '2022-01-01')]

    fig = go.Figure()

    fig.add_trace(go.Box(
        y=pre_covid_2019['Preco_petroleo_bruto_Brent_FOB'],
        name='Antes da Pandemia (2019)',
        marker_color='blue'
    ))

    fig.add_trace(go.Box(
        y=durante_covid_2020['Preco_petroleo_bruto_Brent_FOB'],
        name='Durante a Pandemia (2020)',
        marker_color='red'
    ))

    fig.add_trace(go.Box(
        y=pos_covid_2021['Preco_petroleo_bruto_Brent_FOB'],
        name='Pós Pandemia (2021)',
        marker_color='green'
    ))

    fig.update_layout(
        title='Comparação de Preços do Petróleo Brent Antes (2019), Durante (2020) e Pós Pandemia (2021)',
        yaxis_title='Preço (USD)',
        boxmode='group'
    )

    st.plotly_chart(fig)
#------------------------------------------------------FIM plotar_comparacao_pre_pandemia_pandemia--------------------------------------------------------------------------

#------------------------------------------------------INICIO plotar_eventos_vacina--------------------------------------------------------------------------
def plotar_eventos_vacina(dados):
    """
    Plota os impactos de eventos específicos durante a pandemia no preço do petróleo Brent.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """

    st.subheader("Impacto de Eventos Específicos Durante a Pandemia")
    st.write("""
        Durante a pandemia de COVID-19, vários eventos específicos tiveram um impacto significativo nos preços do petróleo Brent. 
        Dois dos eventos mais marcantes foram o início dos lockdowns em março de 2020 e o início da vacinação em dezembro de 2020.

        **Início dos Lockdowns (Março de 2020):**
        Em 11 de março de 2020, a Organização Mundial da Saúde (OMS) declarou o COVID-19 como uma pandemia global. 
        Isso levou a uma série de lockdowns em vários países ao redor do mundo, resultando em uma drástica redução na demanda por petróleo. 
        O gráfico a seguir mostra uma queda acentuada nos preços do petróleo Brent imediatamente após esse anúncio, refletindo a incerteza e a contração econômica global.

        **Início da Vacinação (Dezembro de 2020):**
        Com o desenvolvimento rápido das vacinas contra o COVID-19, a vacinação em massa começou em muitos países em dezembro de 2020. 
        Este evento marcou o início de uma recuperação econômica gradual, aumentando as esperanças de um retorno à normalidade. 
        O gráfico mostra uma recuperação nos preços do petróleo Brent à medida que a confiança dos investidores começou a retornar com o progresso das campanhas de vacinação.

        Este gráfico detalha as flutuações nos preços do petróleo Brent durante esses eventos críticos, destacando a volatilidade do mercado em resposta às mudanças globais.
    """)
    dados_eventos = dados[(dados['Data'] >= '2020-01-01') & (dados['Data'] <= '2021-12-31')]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_eventos['Data'], y=dados_eventos['Preco_petroleo_bruto_Brent_FOB'],
                             mode='lines', name='Preço do Brent (FOB)', line=dict(color='blue')))
    
    # Anúncio de lockdowns
    fig.add_shape(type="line", x0='2020-03-11', y0=dados_eventos['Preco_petroleo_bruto_Brent_FOB'].min(),
                  x1='2020-03-11', y1=dados_eventos['Preco_petroleo_bruto_Brent_FOB'].max(), line=dict(color="red", width=2, dash="dash"))
    fig.add_annotation(x='2020-03-11', y=dados_eventos['Preco_petroleo_bruto_Brent_FOB'].max(),
                       text="Início da Pandemia", showarrow=True, arrowhead=1)
    
    # Início da vacinação
    fig.add_shape(type="line", x0='2020-12-14', y0=dados_eventos['Preco_petroleo_bruto_Brent_FOB'].min(),
                  x1='2020-12-14', y1=dados_eventos['Preco_petroleo_bruto_Brent_FOB'].max(), line=dict(color="green", width=2, dash="dash"))
    fig.add_annotation(x='2020-12-14', y=dados_eventos['Preco_petroleo_bruto_Brent_FOB'].max(),
                       text="Início da Vacinação", showarrow=True, arrowhead=1)

    fig.update_layout(title='Impacto das vacinas Durante a Pandemia no Preço do Petróleo Brent (2020-2021)',
                      xaxis_title='Data',
                      yaxis_title='Preço (USD)')
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', dash='dash'), showlegend=True, name='Início da Pandemia'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='green', dash='dash'), showlegend=True, name='Início da Vacinação'))
    st.plotly_chart(fig)
#------------------------------------------------------FIM plotar_eventos_vacina--------------------------------------------------------------------------

#------------------------------------------------------FIM COVID-19--------------------------------------------------------------------------




#------------------------------------------------------INICIO Geográficos--------------------------------------------------------------------------

#------------------------------------------------------INICIO mapa_producao--------------------------------------------------------------------------
def plotar_mapa_producao():
    """
    Plota um mapa dos principais produtores de petróleo em 2020.
    """
    produtores = pd.DataFrame({
        'País': ['United States', 'Russia', 'Saudi Arabia', 'Canada', 'Iraq', 'China', 'United Arab Emirates', 'Brazil', 'Iran', 'Kuwait'],
        'Produção (milhões de barris/dia)': [11.307, 9.865, 9.264, 4.201, 4.102, 3.888, 3.138, 2.939, 2.665, 2.625],
        'Código País': ['USA', 'RUS', 'SAU', 'CAN', 'IRQ', 'CHN', 'ARE', 'BRA', 'IRN', 'KWT']
    })

    fig = px.choropleth(produtores, 
                        locations='Código País', 
                        color='Produção (milhões de barris/dia)',
                        hover_name='País', 
                        title='Principais Produtores de Petróleo (dados de 2020)',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        projection='natural earth')

    fig.update_geos(showland=True, landcolor="lightgray",
                    showcountries=True, countrycolor="Black")

    st.plotly_chart(fig)

    st.write("### Legenda")
    st.table(produtores[['País', 'Produção (milhões de barris/dia)','Código País']])

def plotar_mapa_exportacao():
    """
    Plota um mapa dos principais exportadores de petróleo em 2018.
    """
    exportadores = pd.DataFrame({
        'País': ['Saudi Arabia', 'Russia', 'Iraq', 'United States', 'Canada', 'United Arab Emirates', 'Kuwait', 'Nigeria', 'Qatar', 'Angola'],
        'Exportação (milhões de barris/dia)': [10.600, 5.225, 3.800, 3.770, 3.596, 2.296, 2.050, 1.979, 1.477, 1.420],
        'Código País': ['SAU', 'RUS', 'IRQ', 'USA', 'CAN', 'ARE', 'KWT', 'NGA', 'QAT', 'AGO']
    })

    fig = px.choropleth(exportadores, 
                        locations='Código País', 
                        color='Exportação (milhões de barris/dia)',
                        hover_name='País', 
                        title='Principais Exportadores de Petróleo (dados de 2018)',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        projection='natural earth')

    fig.update_geos(showland=True, landcolor="lightgray",
                    showcountries=True, countrycolor="Black")

    st.plotly_chart(fig)

    st.write("### Legenda")
    st.table(exportadores[['País', 'Exportação (milhões de barris/dia)']])

def plotar_mapa_consumo():
    """
    Plota um mapa dos principais consumidores de petróleo em 2019.
    """
    consumidores = pd.DataFrame({
        'País': ['United States', 'China', 'India', 'Japan', 'Saudi Arabia', 'Russia', 'South Korea', 'Canada', 'Brazil', 'Germany'],
        'Consumo (milhões de barris/dia)': [19.400, 14.056, 5.271, 3.812, 3.788, 3.317, 2.760, 2.403, 2.398, 2.281],
        'Código País': ['USA', 'CHN', 'IND', 'JPN', 'SAU', 'RUS', 'KOR', 'CAN', 'BRA', 'DEU']
    })

    fig = px.choropleth(consumidores, 
                        locations='Código País', 
                        color='Consumo (milhões de barris/dia)',
                        hover_name='País', 
                        title='Principais Consumidores de Petróleo (dados de 2019)',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        projection='natural earth')

    fig.update_geos(showland=True, landcolor="lightgray",
                    showcountries=True, countrycolor="Black")

    st.plotly_chart(fig)

    st.write("### Legenda")
    st.table(consumidores[['País', 'Consumo (milhões de barris/dia)']])

#------------------------------------------------------FIM mapa_producao--------------------------------------------------------------------------

#------------------------------------------------------FIM Geográficos--------------------------------------------------------------------------

def plotar_falencia_lehman_brothers(dados):
    """
    Plota o impacto da falência do Lehman Brothers no preço do petróleo Brent.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.subheader("Falência do Lehman Brothers")
    st.write("""
        Em 15 de setembro de 2008, o Lehman Brothers, um dos maiores bancos de investimento dos Estados Unidos, declarou falência. 
        Este evento é frequentemente visto como o auge da crise financeira global de 2008. A falência do Lehman Brothers teve um impacto significativo 
        nos mercados financeiros globais, incluindo o mercado de petróleo.
    """)

    dados_lehman = dados[(dados['Data'] >= '2007-01-01') & (dados['Data'] <= '2009-12-31')]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados_lehman['Data'], y=dados_lehman['Preco_petroleo_bruto_Brent_FOB'],
                             mode='lines', name='Preço do Brent (FOB)',
                             line=dict(color='blue')))

    fig.add_shape(type="line",
                  x0='2008-09-15', y0=dados_lehman['Preco_petroleo_bruto_Brent_FOB'].min(),
                  x1='2008-09-15', y1=dados_lehman['Preco_petroleo_bruto_Brent_FOB'].max(),
                  line=dict(color="red", width=2, dash="dash"))

    fig.add_annotation(x='2008-09-15', y=dados_lehman['Preco_petroleo_bruto_Brent_FOB'].max(),
                       text="Falência do Lehman Brothers",
                       showarrow=True, arrowhead=1,
                       yshift=10)

    fig.update_layout(
        title='Impacto da Falência do Lehman Brothers no Preço do Petróleo Brent (2007-2009)',
        xaxis_title='Data',
        yaxis_title='Preço (USD)'
    )

    st.plotly_chart(fig)

    csv = dados_lehman.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados da Falência do Lehman Brothers como CSV",
        data=csv,
        file_name='falencia_lehman_brothers_preco_petroleo_brent.csv',
        mime='text/csv',
    )


def plotar_aprovacao_tarp(dados):
    """
    Plota o impacto da aprovação do TARP no preço do petróleo Brent.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.subheader("Aprovação do TARP")
    st.write("""
        Em 3 de outubro de 2008, o governo dos Estados Unidos aprovou o Programa de Alívio de Ativos Problemáticos (TARP) para estabilizar o sistema financeiro. 
        O TARP autorizou o Departamento do Tesouro a gastar até 700 bilhões de dólares para comprar ativos tóxicos e fornecer capital a instituições financeiras. 
        Esta medida teve um impacto significativo nos mercados financeiros, incluindo o mercado de petróleo.
    """)

    dados_tarp = dados[(dados['Data'] >= '2007-01-01') & (dados['Data'] <= '2009-12-31')]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados_tarp['Data'], y=dados_tarp['Preco_petroleo_bruto_Brent_FOB'],
                             mode='lines', name='Preço do Brent (FOB)',
                             line=dict(color='blue')))

    fig.add_shape(type="line",
                  x0='2008-10-03', y0=dados_tarp['Preco_petroleo_bruto_Brent_FOB'].min(),
                  x1='2008-10-03', y1=dados_tarp['Preco_petroleo_bruto_Brent_FOB'].max(),
                  line=dict(color="green", width=2, dash="dash"))

    fig.add_annotation(x='2008-10-03', y=dados_tarp['Preco_petroleo_bruto_Brent_FOB'].max(),
                       text="Aprovação do TARP",
                       showarrow=True, arrowhead=1,
                       yshift=-10)

    fig.update_layout(
        title='Impacto da Aprovação do TARP no Preço do Petróleo Brent (2007-2009)',
        xaxis_title='Data',
        yaxis_title='Preço (USD)'
    )
    st.plotly_chart(fig)

    csv = dados_tarp.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados da Aprovação do TARP como CSV",
        data=csv,
        file_name='aprovacao_tarp_preco_petroleo_brent.csv',
        mime='text/csv',
    )

def plotar_volatilidade(dados):
    """
    Plota a volatilidade dos preços do petróleo Brent durante a Crise Financeira de 2008.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.subheader("Volatilidade dos Preços do Petróleo")
    st.write("""
        A volatilidade dos preços do petróleo aumentou significativamente durante a Crise Financeira de 2008.
        Isso reflete a incerteza e o pânico no mercado à medida que os preços do petróleo flutuavam drasticamente.
    """)

    dados_volatilidade = dados[(dados['Data'] >= '2007-01-01') & (dados['Data'] <= '2009-12-31')]
    dados_volatilidade['Retornos Diários'] = dados_volatilidade['Preco_petroleo_bruto_Brent_FOB'].pct_change()
    dados_volatilidade['Volatilidade'] = dados_volatilidade['Retornos Diários'].rolling(window=30).std()

    fig = px.line(dados_volatilidade, x='Data', y='Volatilidade', title='Volatilidade dos Preços do Petróleo Brent (2007-2009)')
    fig.update_xaxes(title_text='Data')
    fig.update_yaxes(title_text='Volatilidade (30 dias)')
    st.plotly_chart(fig)

    csv = dados_volatilidade[['Data', 'Volatilidade']].dropna().to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados de Volatilidade como CSV",
        data=csv,
        file_name='volatilidade_preco_petroleo_brent.csv',
        mime='text/csv',
    )
#FIM DOS PLOTS
#------------------------------------------------------FIM PLOTS--------------------------------------------------------------------------

#------------------------------------------------------INICIO QUEDAS--------------------------------------------------------------------------
def quedas(dados):
    """
    Exibe a análise das quedas no preço do petróleo Brent, incluindo os impactos da COVID-19, Crise dos Tigres Asiáticos e Crise Financeira de 2008.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.title("Análise do Preço do Petróleo Brent")
    submenu = option_menu(
        menu_title="",  
        options=["Covid-19", "Crise Financeira 2008"],
        icons=["virus", "dropbox"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Covid-19":
        plotar_impacto_covid(dados)
        plotar_eventos_vacina(dados)
        plotar_comparacao_pre_pandemia(dados)
        
        
    elif submenu == "Crise Financeira 2008":
        st.title("Crise Financeira 2008")
        plotar_falencia_lehman_brothers(dados)
        plotar_aprovacao_tarp(dados)
        plotar_volatilidade(dados)
#------------------------------------------------------INICIO FIM--------------------------------------------------------------------------

#------------------------------------------------------INICIO AUMENTOS--------------------------------------------------------------------------
def aumentos(dados):
    """
    Exibe a análise dos aumentos no preço do petróleo Brent, incluindo a Primavera Árabe, Revolução Iraniana e Guerra do Golfo.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.title("Análise do Preço do Petróleo Brent")
    submenu = option_menu(
        menu_title="",  
        options=["Primavera Árabe","Guerra do Golfo"],
        icons=["globe", "peace"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Primavera Árabe":
        st.title("Primavera Árabe")
        st.write("""
            A Primavera Árabe, que começou em 2010, teve impactos significativos em diversas economias, 
            especialmente em países exportadores de petróleo no Oriente Médio e Norte da África. 
            Vamos analisar como esses eventos afetaram os preços do petróleo Brent durante esse período.
        """)
        # Adicione análises e gráficos específicos para a Primavera Árabe aqui

    elif submenu == "Guerra do Golfo":
        st.title("Guerra do Golfo")
        st.write("""
            A Guerra do Golfo de 1990-1991 causou um choque no mercado de petróleo devido à incerteza e à interrupção na produção. 
            Vamos analisar como esses eventos afetaram os preços do petróleo Brent durante e após o conflito.
        """)
        # Adicione análises e gráficos específicos para a Guerra do Golfo aqui
#------------------------------------------------------FIO AUMENTOS--------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Análise do Preço do Petróleo Brent", layout="wide")
    caminho_arquivo = 'petroleo.xlsx'
    dados = carregar_dados(caminho_arquivo)

    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu Principal",  
            options=["Introdução", "Dados Brutos", "Quedas", "Aumentos", "Notícias", "Conclusão"],  
            icons=["info-circle", "database", "arrow-down", "arrow-up", "newspaper", "check"],  
            menu_icon="cast",  
            default_index=0,  
        )

    if selecionado == "Introdução":
        introducao(dados)
    elif selecionado == "Dados Brutos":
        exibir(dados)
    elif selecionado == "Quedas":
        quedas(dados)
    elif selecionado == "Aumentos":
        aumentos(dados)
    elif selecionado == "Notícias":
        st.subheader("Notícias Relacionadas ao Petróleo")
        noticias = buscar_noticias(NEWS_API_KEY)
        if noticias:
            for noticia in noticias:
                st.write(f"### {noticia['title']}")
                st.write(f"**Fonte**: {noticia['source']['name']}")
                st.write(noticia['description'])
                st.write(f"[Leia mais]({noticia['url']})")
        else:
            st.error("Não foi possível buscar as notícias. Verifique sua chave de API.")
    elif selecionado == "Conclusão":
        conclusao()
   

if __name__ == "__main__":
    main()

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
        margin=dict(b=100) 
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
        Obrigado por usar nossa aplicação para analisar os preços do petróleo Brent, esperamos que tenha encontrado as informações úteis.\b
        Se tiver alguma dúvida ou sugestão, por favor, entre em contato.\n
        O petróleo é um recurso natural de extrema importância, tanto histórica quanto economicamente, mas que também apresenta grandes desafios ambientais.\b 
        O futuro da energia deve equilibrar a demanda por combustíveis com a necessidade de práticas sustentáveis.\n
        Fatores como geopolítica, crises econômicas, demanda global por energia e outras situações influenciam no preço do barril do petróleo. Com dados histórico é possível criar uma análise e ter insights, afim de poder avaliar e escolher a melhor resolução para deliberação financeiras dentro de uma empresa.\n 
        A Guerra do Golfo de 1990-1991 não só alterou drasticamente o cenário político e econômico do Oriente Médio, mas também teve implicações globais significativas, desde o impacto sobre os preços do petróleo até mudanças nas políticas de segurança internacional. O conflito exemplificou as complexidades das relações internacionais e a volatilidade das questões de energia e soberania no mundo contemporâneo.\n        
        A Revolução Iraniana de 1979 não apenas transformou o Irã, mas também teve um impacto profundo e duradouro no mercado global de petróleo, nas relações internacionais e na geopolítica do Oriente Médio. A crise resultante sublinhou a importância da estabilidade regional e a vulnerabilidade das economias globais às flutuações nos mercados de energia, destacando a interconexão entre política, economia e recursos naturais no mundo contemporâneo.\n
        A Primavera Árabe teve um impacto profundo e duradouro no mercado de petróleo e na geopolítica do Oriente Médio e do Norte da África. As interrupções na produção e os aumentos nos preços do petróleo destacaram a vulnerabilidade da economia global às crises regionais em áreas ricas em recursos energéticos. Esse período tumultuado sublinhou a necessidade de diversificação energética e de investimentos em infraestrutura para mitigar os riscos associados à dependência do petróleo de regiões instáveis.\n
        
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
    st.subheader("Análise de Tendências")
    st.write("Explore as tendências nos preços do petróleo Brent.")

    dados['Media_Movel_30'] = dados['Preco_petroleo_bruto_Brent_FOB'].rolling(window=30).mean()
    dados['Media_Movel_90'] = dados['Preco_petroleo_bruto_Brent_FOB'].rolling(window=90).mean()
    dados['Media_Movel_365'] = dados['Preco_petroleo_bruto_Brent_FOB'].rolling(window=365).mean()
    dados['Media_Geral'] = dados['Preco_petroleo_bruto_Brent_FOB'].mean()

    st.write("Selecione um intervalo de datas para visualizar a análise de tendências.")
    data_min = dados['Data'].min().date()
    data_max = dados['Data'].max().date()

    data_inicio, data_fim = st.slider("Selecione o intervalo de datas", min_value=data_min, max_value=data_max, value=(data_min, data_max), format="DD/MM/YYYY")

    if data_inicio > data_fim:
        st.error("Data de início não pode ser maior que a data de fim.")
    else:
        dados_filtrados = dados[(dados['Data'] >= pd.to_datetime(data_inicio)) & (dados['Data'] <= pd.to_datetime(data_fim))]

        medias_moveis = st.multiselect('Selecione as médias móveis que deseja visualizar:',
                                       ['Média Móvel 30 Dias', 'Média Móvel 90 Dias', 'Média Móvel 365 Dias', 'Média Geral'],
                                       default=['Média Móvel 30 Dias', 'Média Móvel 90 Dias', 'Média Móvel 365 Dias', 'Média Geral'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Preco_petroleo_bruto_Brent_FOB'], mode='lines', name='Preço do Brent (FOB)'))
        
        if 'Média Móvel 30 Dias' in medias_moveis:
            fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Media_Movel_30'], mode='lines', name='Média Móvel 30 Dias'))
        
        if 'Média Móvel 90 Dias' in medias_moveis:
            fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Media_Movel_90'], mode='lines', name='Média Móvel 90 Dias'))
        
        if 'Média Móvel 365 Dias' in medias_moveis:
            fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Media_Movel_365'], mode='lines', name='Média Móvel 365 Dias'))
        
        if 'Média Geral' in medias_moveis:
            fig.add_trace(go.Scatter(x=dados_filtrados['Data'], y=dados_filtrados['Media_Geral'], mode='lines', name='Média Geral', line=dict(dash='dash')))

        fig.update_layout(title='Análise de Tendências nos Preços do Petróleo Brent',
                          xaxis_title='Data',
                          yaxis_title='Preço (USD)')

        st.plotly_chart(fig)

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


#------------------------------------------------------INICIO CRISE 2008--------------------------------------------------------------------------

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



def plotar_comparacao_prepos_primavera_arabe(dados):
    st.subheader("Comparação de Preços Antes e Depois da Primavera Árabe")
    st.write("""
        Este gráfico compara os preços do petróleo Brent antes, durante e depois da Primavera Árabe, destacando o impacto dos eventos nos preços.
    """)

    pre_arabe = dados[(dados['Data'] >= '2008-01-01') & (dados['Data'] < '2010-01-01')]
    durante_arabe = dados[(dados['Data'] >= '2010-01-01') & (dados['Data'] < '2012-01-01')]
    pos_arabe = dados[(dados['Data'] >= '2012-01-01') & (dados['Data'] <= '2014-12-31')]

    fig = go.Figure()

    fig.add_trace(go.Box(y=pre_arabe['Preco_petroleo_bruto_Brent_FOB'], name='Antes da Primavera Árabe', marker_color='blue'))
    fig.add_trace(go.Box(y=durante_arabe['Preco_petroleo_bruto_Brent_FOB'], name='Durante a Primavera Árabe', marker_color='red'))
    fig.add_trace(go.Box(y=pos_arabe['Preco_petroleo_bruto_Brent_FOB'], name='Após a Primavera Árabe', marker_color='green'))

    fig.update_layout(
        title='Comparação de Preços do Petróleo Brent Antes, Durante e Após a Primavera Árabe',
        yaxis_title='Preço (USD)',
        boxmode='group'
    )

    st.plotly_chart(fig)

    dados_comparacao = pd.concat([pre_arabe, durante_arabe, pos_arabe])
    csv = dados_comparacao.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='comparacao_prepos_primavera_arabe.csv',
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

#------------------------------------------------------FIM CRISE 2008--------------------------------------------------------------------------

#------------------------------------------------------INICIO PRIMAVERA ARÁBE--------------------------------------------------------------------------


def plotar_primavera_arabe(dados):
    st.subheader("Impacto da Primavera Árabe no Preço do Petróleo Brent")
    st.write("""
        A Primavera Árabe foi uma série de protestos e levantes que ocorreram no Oriente Médio e no Norte da África a partir de 2010.
        Esses eventos tiveram um impacto significativo no mercado global de petróleo, causando aumentos nos preços devido à instabilidade política.
    """)

    dados_arabe = dados[(dados['Data'] >= '2010-01-01') & (dados['Data'] <= '2013-12-31')]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados_arabe['Data'], y=dados_arabe['Preco_petroleo_bruto_Brent_FOB'],
                             mode='lines', name='Preço do Brent (FOB)', line=dict(color='blue')))

    eventos = [
        {'data': '2010-12-17', 'evento': 'Início dos Protestos na Tunísia', 'cor': 'red'},
        {'data': '2011-02-11', 'evento': 'Queda do Governo no Egito', 'cor': 'green'},
        {'data': '2011-10-20', 'evento': 'Queda do Governo na Líbia', 'cor': 'purple'}
    ]

    for evento in eventos:
        fig.add_shape(
            type="line",
            x0=evento['data'], y0=dados_arabe['Preco_petroleo_bruto_Brent_FOB'].min(),
            x1=evento['data'], y1=dados_arabe['Preco_petroleo_bruto_Brent_FOB'].max(),
            line=dict(color=evento['cor'], width=2, dash="dash")
        )
        fig.add_annotation(
            x=evento['data'], y=dados_arabe['Preco_petroleo_bruto_Brent_FOB'].max(),
            ax=0, ay=-30,
            text=evento['evento'], showarrow=True, arrowhead=2,
            arrowcolor=evento['cor'], arrowsize=1, arrowwidth=2,
            font=dict(color=evento['cor'], size=12),
            textangle=-45
        )

    for evento in eventos:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            line=dict(color=evento['cor'], dash='dash'),
            showlegend=True,
            name=evento['evento']
        ))

    fig.update_layout(
        title='Impacto da Primavera Árabe no Preço do Petróleo Brent',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5,
            itemwidth=50,  
            font=dict(size=10)
        ),
        margin=dict(b=100)  
    )

    st.plotly_chart(fig)

    csv = dados_arabe.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='impacto_primavera_arabe_preco_petroleo_brent.csv',
        mime='text/csv',
    )

def plotar_comparacao_prepos_primavera_arabe(dados):
    st.subheader("Comparação de Preços Antes e Depois da Primavera Árabe")
    st.write("""
        Este gráfico compara os preços do petróleo Brent antes, durante e depois da Primavera Árabe, destacando o impacto dos eventos nos preços.
    """)

    
    pre_arabe = dados[(dados['Data'] >= '2008-01-01') & (dados['Data'] < '2010-01-01')]
    durante_arabe = dados[(dados['Data'] >= '2010-01-01') & (dados['Data'] < '2012-01-01')]
    pos_arabe = dados[(dados['Data'] >= '2012-01-01') & (dados['Data'] <= '2014-12-31')]

    fig = go.Figure()

    fig.add_trace(go.Box(y=pre_arabe['Preco_petroleo_bruto_Brent_FOB'], name='Antes da Primavera Árabe (2008-2009)', marker_color='blue'))
    fig.add_trace(go.Box(y=durante_arabe['Preco_petroleo_bruto_Brent_FOB'], name='Durante a Primavera Árabe (2010-2011)', marker_color='red'))
    fig.add_trace(go.Box(y=pos_arabe['Preco_petroleo_bruto_Brent_FOB'], name='Após a Primavera Árabe (2012-2014)', marker_color='green'))

    fig.update_layout(
        title='Comparação de Preços do Petróleo Brent Antes, Durante e Após a Primavera Árabe',
        yaxis_title='Preço (USD)',
        boxmode='group'
    )

    st.plotly_chart(fig)

    dados_comparacao = pd.concat([pre_arabe, durante_arabe, pos_arabe])
    csv = dados_comparacao.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='comparacao_prepos_primavera_arabe.csv',
        mime='text/csv',
    )

def plotar_dispersao_retornos(dados):
    st.subheader("Dispersão dos Retornos Diários do Preço do Petróleo Brent (2009-2014)")
    st.write("""
        Este gráfico mostra a dispersão dos retornos diários do preço do petróleo Brent, destacando a volatilidade durante o período de 2009 a 2014.
    """)

    
    dados_filtrados = dados[(dados['Data'] >= '2009-01-01') & (dados['Data'] <= '2014-12-31')]
    dados_filtrados['Retornos_Diarios'] = dados_filtrados['Preco_petroleo_bruto_Brent_FOB'].pct_change()

    fig = px.scatter(dados_filtrados, x='Data', y='Retornos_Diarios', title='Dispersão dos Retornos Diários do Preço do Petróleo Brent (2009-2014)', color='Retornos_Diarios', labels={'Retornos_Diarios': 'Retornos Diários'})
    fig.update_layout(xaxis_title='Data', yaxis_title='Retornos Diários')
    st.plotly_chart(fig)

    
    csv = dados_filtrados[['Data', 'Retornos_Diarios']].dropna().to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='dispersao_retornos_2009_2014.csv',
        mime='text/csv',
    )


#------------------------------------------------------FIM PRIMAVERA ARÁBE--------------------------------------------------------------------------


#------------------------------------------------------INICIO GUERRA DO GOLFO--------------------------------------------------------------------------


def plotar_guerra_golfo(dados):
    st.subheader("Impacto da Guerra do Golfo no Preço do Petróleo Brent")
    st.write("""
        A Guerra do Golfo, ocorrida entre 1990 e 1991, foi um conflito de curta duração, mas de grande impacto global, especialmente no mercado de petróleo. Este gráfico ilustra a evolução dos preços do petróleo Brent durante a guerra, destacando eventos cruciais que influenciaram esses preços. Vamos explorar como esses eventos moldaram o mercado de petróleo e as economias globais.
    """)

    st.write("""
        **Contexto Histórico:**

        1. **Invasão do Kuwait (2 de agosto de 1990):**
        
        Em 2 de agosto de 1990, o Iraque, liderado por Saddam Hussein, invadiu o Kuwait, um dos maiores produtores de petróleo do mundo. Esta invasão não só provocou um aumento imediato nos preços do petróleo devido ao medo de uma interrupção significativa na oferta global, mas também gerou uma reação internacional que culminaria em um conflito militar.

        2. **Início da Operação Tempestade no Deserto (17 de janeiro de 1991):**
        
        A resposta internacional veio na forma de uma coalizão liderada pelos Estados Unidos, que iniciou a Operação Tempestade no Deserto em 17 de janeiro de 1991. Esta operação tinha como objetivo liberar o Kuwait e proteger os interesses petrolíferos na região. Durante este período, a incerteza continuou a manter os preços do petróleo elevados.

        3. **Fim da Guerra do Golfo (28 de fevereiro de 1991):**
        
        A guerra terminou oficialmente em 28 de fevereiro de 1991, quando as forças da coalizão declararam a libertação do Kuwait. Com o fim do conflito, houve uma expectativa de estabilização na produção e fornecimento de petróleo, o que levou a uma diminuição gradual nos preços.
    """)

    
    dados_golfo = dados[(dados['Data'] >= '1990-01-01') & (dados['Data'] <= '1991-12-31')]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dados_golfo['Data'], y=dados_golfo['Preco_petroleo_bruto_Brent_FOB'],
                             mode='lines', name='Preço do Brent (FOB)', line=dict(color='blue')))

    
    eventos = [
        {'data': '1990-08-02', 'evento': 'Invasão do Kuwait', 'cor': 'red'},
        {'data': '1991-01-17', 'evento': 'Início da Operação Tempestade no Deserto', 'cor': 'green'},
        {'data': '1991-02-28', 'evento': 'Fim da Guerra do Golfo', 'cor': 'purple'}
    ]

    for evento in eventos:
        fig.add_shape(
            type="line",
            x0=evento['data'], y0=dados_golfo['Preco_petroleo_bruto_Brent_FOB'].min(),
            x1=evento['data'], y1=dados_golfo['Preco_petroleo_bruto_Brent_FOB'].max(),
            line=dict(color=evento['cor'], width=2, dash="dash")
        )
        fig.add_annotation(
            x=evento['data'], y=dados_golfo['Preco_petroleo_bruto_Brent_FOB'].max(),
            ax=0, ay=-30,
            text=evento['evento'], showarrow=True, arrowhead=2,
            arrowcolor=evento['cor'], arrowsize=1, arrowwidth=2,
            font=dict(color=evento['cor'], size=12),
            textangle=-45
        )

   
    for evento in eventos:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            line=dict(color=evento['cor'], dash='dash'),
            showlegend=True,
            name=evento['evento']
        ))

    fig.update_layout(
        title='Impacto da Guerra do Golfo no Preço do Petróleo Brent',
        xaxis_title='Data',
        yaxis_title='Preço (USD)',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5,
            itemwidth=50, 
            font=dict(size=10)
        ),
        margin=dict(b=100)  
    )

    st.plotly_chart(fig)

    csv = dados_golfo.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='impacto_guerra_golfo_preco_petroleo_brent.csv',
        mime='text/csv',
    )

def plotar_volatilidade_guerra_golfo(dados):
    st.subheader("Volatilidade dos Preços do Petróleo Durante a Guerra do Golfo")
    st.write("""
        Este gráfico mostra a volatilidade dos preços do petróleo Brent durante a Guerra do Golfo.
    """)

    dados_golfo = dados[(dados['Data'] >= '1990-01-01') & (dados['Data'] <= '1991-12-31')]
    dados_golfo['Retornos_Diarios'] = dados_golfo['Preco_petroleo_bruto_Brent_FOB'].pct_change()
    dados_golfo['Volatilidade'] = dados_golfo['Retornos_Diarios'].rolling(window=30).std()

    fig = px.line(dados_golfo, x='Data', y='Volatilidade', title='Volatilidade dos Preços do Petróleo Brent Durante a Guerra do Golfo')
    fig.update_xaxes(title_text='Data')
    fig.update_yaxes(title_text='Volatilidade (30 dias)')
    st.plotly_chart(fig)

    csv = dados_golfo[['Data', 'Volatilidade']].dropna().to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name='volatilidade_guerra_golfo.csv',
        mime='text/csv',
    )

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
            Teve início na Tunísia em dezembro de 2010 e rapidamente se espalhou para países como Egito, Líbia, Síria, Iémen e Bahrein. Os protestos eram, em sua maioria, contra regimes autoritários e a favor de reformas políticas, econômicas e sociais.                    
            Muitos desses países são grandes produtores e exportadores de petróleo, e as tensões políticas e sociais ameaçaram interromper a produção e a exportação desse recurso vital.
            
            Preço do Petróleo:
            Os levantes e a instabilidade política resultante provocaram um aumento na incerteza global em relação à oferta de petróleo, o que fez os preços subirem significativamente. Em 2011, por exemplo, o preço do barril de petróleo Brent subiu de aproximadamente 90 dollars para 125 dollars.
            Os mercados temeram que a instabilidade pudesse afetar os principais pontos de produção e transporte de petróleo, levando a uma possível escassez no fornecimento global.
            
            Interrupção da produção:
            Na Líbia, um dos países mais afetados, a guerra civil que seguiu a queda do líder Muammar Gaddafi em 2011 reduziu drasticamente a produção de petróleo. A produção, que estava em cerca de 1,6 milhão de barris por dia antes da revolução, caiu para quase zero durante o conflito.
            No Iémen, os combates e a instabilidade também afetaram a produção de petróleo e gás, reduzindo a capacidade do país de exportar esses recursos.
            
            Reajuste nas políticas energéticas:
            A instabilidade gerada pela Primavera Árabe levou muitos países consumidores de petróleo a reavaliar suas políticas energéticas e a buscar maior segurança energética por meio da diversificação de fontes e fornecedores .
            Países como os Estados Unidos aumentaram o foco na produção doméstica de petróleo e gás, contribuindo para a expansão do fracking e da produção de petróleo de xisto.
            
            Mudança no Poder Geopolítico:
            A Primavera Árabe alterou significativamente o equilíbrio de poder no Oriente Médio e no Norte da África. Novos governos emergiram em alguns países, enquanto outros entraram em prolongados períodos de conflito civil e instabilidade política.
            Essas mudanças políticas afetaram a OPEP (Organização dos Países Exportadores de Petróleo) e sua capacidade de coordenar políticas de produção e preços entre seus membros, dada a instabilidade em países como Líbia e Iémen .
            
            Oportunidade para novos produtores:
            A instabilidade nos países da Primavera Árabe permitiu que outros grandes produtores de petróleo, como Arábia Saudita e Rússia, aumentassem sua influência nos mercados globais de energia.
            A Arábia Saudita, por exemplo, aumentou sua produção de petróleo para compensar as perdas de produção em países afetados pela Primavera Árabe, solidificando sua posição como líder de facto da OPEP. Alguns países começaram a investir mais em infraestrutura energética e em medidas de segurança para proteger suas instalações de petróleo e gás .
            
            Energias renováveis:
            A volatilidade nos preços do petróleo durante e após a Primavera Árabe incentivou um maior interesse e investimento em energias renováveis e tecnologias de eficiência energética como uma forma de reduzir a dependência do petróleo importado.
            A União Europeia e outros grandes consumidores de energia intensificaram seus esforços para aumentar a proporção de fontes de energia renovável em suas matrizes energéticas .
            
            Impacto Social e Econômico:
            Os aumentos nos preços do petróleo devido à Primavera Árabe tiveram efeitos significativos nas economias globais, contribuindo para a inflação e aumentando os custos de transporte e produção de bens e serviços.
            Nos países produtores afetados, a perda de receita do petróleo durante os conflitos teve graves consequências econômicas e sociais, exacerbando as crises humanitárias e as dificuldades econômicas .                        
            Vamos analisar como esses eventos afetaram os preços do petróleo Brent durante esse período.
        """)
        plotar_primavera_arabe(dados)
        plotar_comparacao_prepos_primavera_arabe(dados)
        plotar_dispersao_retornos(dados)
        
        
        

    elif submenu == "Guerra do Golfo":
        st.title("Guerra do Golfo")
        plotar_guerra_golfo(dados)
        plotar_volatilidade_guerra_golfo(dados)
        
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

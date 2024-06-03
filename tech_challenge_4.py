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
def introducao():
    """
    Exibe a introdução da aplicação.
    """
    st.title("Introdução")
    st.write("""
        Bem-vindo à análise do preço do petróleo Brent. 
        Esta aplicação permite visualizar e analisar a evolução do preço do petróleo Brent ao longo do tempo.
        Utilize o menu para navegar entre as páginas e explorar diferentes análises.
    """)

    plotar_mapa_producao()
#------------------------------------------------------FIM INTRODUÇÃO--------------------------------------------------------------------------


#------------------------------------------------------CONCLUSÃO--------------------------------------------------------------------------
def conclusao():
    """
    Exibe a conclusão da aplicação.
    """
    st.title("Conclusão")
    st.write("""
        Obrigado por usar nossa aplicação para analisar os preços do petróleo Brent.
        Esperamos que tenha encontrado as informações úteis.
        Se tiver alguma dúvida ou sugestão, por favor, entre em contato.
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
        options=["Dados Brutos", "Preço ao Longo do Tempo", "Estatísticas Descritivas", "Análise de Tendências", "Notícias"],
        icons=["table", "line-chart", "bar-chart", "trend-up", "newspaper"],
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

    elif submenu == "Notícias":
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
    Plota a análise de tendências nos preços do petróleo Brent utilizando médias móveis gerais.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
    st.subheader("Análise de Tendências")
    st.write("Explore as tendências nos preços do petróleo Brent.")

    dados['Media_Movel_Geral'] = dados['Preco_petroleo_bruto_Brent_FOB'].expanding().mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados['Data'], y=dados['Preco_petroleo_bruto_Brent_FOB'], mode='lines', name='Preço do Brent (FOB)'))
    fig.add_trace(go.Scatter(x=dados['Data'], y=dados['Media_Movel_Geral'], mode='lines', name='Média Móvel Geral'))
    fig.update_layout(title='Tendências nos Preços do Petróleo Brent', xaxis_title='Data', yaxis_title='Preço (USD)')
    st.plotly_chart(fig)
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
def plotar_comparacao_pre_pandemia_pandemia(dados):
    """
    Plota a comparação de preços do petróleo Brent antes, durante e após a pandemia de COVID-19.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
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

def plotar_eventos_especificos(dados):
    """
    Plota os impactos de eventos específicos durante a pandemia no preço do petróleo Brent.

    Parâmetros:
    dados (DataFrame): O DataFrame contendo os dados do preço do petróleo.
    """
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

    fig.update_layout(title='Impacto de Eventos Específicos Durante a Pandemia no Preço do Petróleo Brent (2020-2021)',
                      xaxis_title='Data',
                      yaxis_title='Preço (USD)')
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', dash='dash'), showlegend=True, name='Início da Pandemia'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='green', dash='dash'), showlegend=True, name='Início da Vacinação'))
    st.plotly_chart(fig)


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
    for i in range(len(produtores)):
        st.write(f"**{produtores['País'][i]}**: {produtores['Produção (milhões de barris/dia)'][i]:,} milhões de barris/dia")

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
        options=["Covid-19", "Crise dos Tigres Asiáticos", "Crise Financeira 2008"],
        icons=["virus", "chart-line", "money-bill-wave"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Covid-19":
        plotar_impacto_covid(dados)
        plotar_eventos_especificos(dados)
        plotar_comparacao_pre_pandemia_pandemia(dados)
        
        
  
    elif submenu == "Crise dos Tigres Asiáticos":
        st.title("Crise dos Tigres Asiáticos")
        st.write("""
            A Crise dos Tigres Asiáticos em 1997-1998 foi uma grande crise financeira que afetou muitos países do Sudeste Asiático. 
            Vamos analisar como esses eventos afetaram os preços do petróleo Brent durante esse período.
        """)
        # Adicione análises e gráficos específicos para a Crise dos Tigres Asiáticos aqui
        
    elif submenu == "Crise Financeira 2008":
        st.title("Crise Financeira 2008")
        st.write("""
            A Crise Financeira de 2008 foi uma das maiores crises econômicas globais desde a Grande Depressão. 
            Vamos analisar como esses eventos afetaram os preços do petróleo Brent durante esse período.
        """)
        # Adicione análises e gráficos específicos para a Crise Financeira de 2008 aqui
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
        options=["Primavera Árabe", "Revolução Iraniana", "Guerra do Golfo"],
        icons=["globe", "flag", "fighter-jet"],
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

    elif submenu == "Revolução Iraniana":
        st.title("Revolução Iraniana")
        st.write("""
            A Revolução Iraniana de 1979 levou a uma grande interrupção na produção de petróleo, causando um aumento acentuado nos preços globais do petróleo. 
            Esta seção examina as flutuações de preço durante e após a revolução.
        """)
        # Adicione análises e gráficos específicos para a Revolução Iraniana aqui

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
            options=["Introdução", "Dados Brutos", "Quedas", "Aumentos", "Conclusão"],  
            icons=["info-circle", "database", "arrow-down", "arrow-up", "check"],  
            menu_icon="cast",  
            default_index=0,  
        )

    if selecionado == "Introdução":
        introducao()
    elif selecionado == "Dados Brutos":
        exibir(dados)
    elif selecionado == "Quedas":
        quedas(dados)
    elif selecionado == "Aumentos":
        aumentos(dados)
    elif selecionado == "Conclusão":
        conclusao()

if __name__ == "__main__":
    main()

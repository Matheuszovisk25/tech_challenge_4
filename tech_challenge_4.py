import streamlit as st
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt

def carregar_data(file_path):
    return pd.read_excel(file_path, sheet_name='Planilha1')

def plot_evolucao_preco(data, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_data = data[(data['Data'] >= start_date) & (data['Data'] <= end_date)]
    fig, ax = plt.subplots(figsize = (8,4))
    ax.plot(filtered_data['Data'], filtered_data['Preço - petróleo bruto - Brent (FOB)'], marker='o')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço (USD)')
    ax.set_title('Evolução do Preço do Petróleo Brent')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)



def introducao():
    st.title("Introdução")
    st.write("""
        Bem-vindo à análise do preço do petróleo Brent. 
        Esta aplicação permite visualizar e analisar a evolução do preço do petróleo Brent ao longo do tempo.
        Utilize o menu para navegar entre as páginas.
    """)

def conclusao():
    st.title("Conclusao")
    st.write("Texto conclusão")

def display(data):
    st.title("Análise do Preço do Petróleo Brent")

    submenu = option_menu(
        menu_title="",  
        options=["Dados Brutos", "Preço ao Longo do Tempo", "Estatísticas Descritivas", "Análise de Tendências"],
        icons=["table", "line-chart", "bar-chart", "trend-up"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Dados Brutos":
        st.subheader("Dados Brutos")
        st.write(data)

    elif submenu == "Preço ao Longo do Tempo":
        st.subheader("Preço do Petróleo Brent ao Longo do Tempo")
        min_date = data['Data'].min().date()
        max_date = data['Data'].max().date()

        start_date = st.date_input("Data de Início", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("Data de Fim", max_date, min_value=min_date, max_value=max_date)

        if start_date > end_date:
            st.error("Data de início não pode ser maior que a data de fim.")
        else:
            plot_evolucao_preco(data, start_date, end_date)

    elif submenu == "Estatísticas Descritivas":
        st.subheader("Estatísticas Descritivas")
        st.write(data.describe())

    elif submenu == "Análise de Tendências":
        st.subheader("Análise de Tendências")
        

def quedas():
    st.title("Análise do Preço do Petróleo Brent")
    submenu = option_menu(
        menu_title="",  
        options=["Covid_19", "Crise dos tigres asiaticos", "Crise financeira 2008"],
        icons=["table", "line-chart", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Covid_19":
        st.title("Covid-19")
        
    elif submenu == "Crise dos tigres asiaticos":
        st.title("Crise dos tigres asiaticos")
        
    elif submenu == "Crise financeira 2008":
        st.title("Crise financeira 2008")

def aumentos():
    st.title("Análise do Preço do Petróleo Brent")
    submenu = option_menu(
        menu_title="",  
        options=["Primavera arabe", "Revolução iraniana", "Guerra do golfo"],
        icons=["table", "line-chart", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if submenu == "Primavera arabe":
         st.title("Primavera arabe")
         st.write("2011")
        
    elif submenu == "Revolução iraniana":
        st.title("Revolução iraniana")
        st.write("1979")
        
    elif submenu == "Guerra do golfo":
        st.title("Guerra do golfo")
        st.write("1990")

def main():
    st.set_page_config(page_title="Análise do Preço do Petróleo Brent", layout="wide")
    file_path = 'petroleo.xlsx'  
    data = carregar_data(file_path)

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu Principal",  
            options=["Introdução", "Dados brutos", "Quedas", "Aumentos", "conclusao"],  
            icons=["info-circle", "database", "graph-up", "graph-down", "end", "calendar-xmark"],  
            menu_icon="cast",  
            default_index=0,  
        )

    if selected == "Introdução":
        introducao()
    elif selected == "Dados brutos":
        display(data)
    elif selected == "Quedas":
        quedas()
    elif selected == "Aumentos":
        aumentos()
    elif selected == "Conclusão":
        conclusao()

if __name__ == "__main__":
    main()

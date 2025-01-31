import streamlit as st
import pandas as pd

# Carregar os dados do Excel
@st.cache
def load_data(file_path):
    data = pd.read_excel(file_path)
    data['VALOR_CLEAN'] = data['VALOR'].replace('[R$\s.]', '', regex=True).replace(',', '.', regex=True)
    data['VALOR_CLEAN'] = pd.to_numeric(data['VALOR_CLEAN'], errors='coerce')
    return data

# Carregue o arquivo analisado
file_path = 'IA_Emendas2025.xlsx'  # Atualize para o caminho correto
data = load_data(file_path)

# Título do painel
st.title("Painel de Controle de Emendas")

# Filtros principais
area_options = data['ÁREA'].dropna().unique()
gnd_options = data['GND_IA'].dropna().unique()

selected_area = st.selectbox("Selecione a Área", options=["Todas"] + list(area_options))
selected_gnd = st.selectbox("Selecione o GND", options=["Todos"] + list(gnd_options))

# Aplicação de filtros
filtered_data = data.copy()
if selected_area != "Todas":
    filtered_data = filtered_data[filtered_data['ÁREA'] == selected_area]
if selected_gnd != "Todos":
    filtered_data = filtered_data[filtered_data['GND_IA'] == selected_gnd]

# Mostrar resumo
total_value = filtered_data['VALOR_CLEAN'].sum()
st.metric("Valor Total Filtrado (R$)", f"{total_value:,.2f}")

# Drilldown por autor
authors = filtered_data['AUTOR'].dropna().unique()
selected_author = st.selectbox("Selecione o Autor", options=["Todos"] + list(authors))

if selected_author != "Todos":
    filtered_data = filtered_data[filtered_data['AUTOR'] == selected_author]

# Mostrar tabela
st.write("Tabela de Emendas Filtradas:")
st.dataframe(filtered_data[['AUTOR', 'ÁREA', 'OBJETO', 'GND_IA', 'VALOR_CLEAN']])

# Gráficos (opcional)
if not filtered_data.empty:
    st.bar_chart(filtered_data.groupby('ÁREA')['VALOR_CLEAN'].sum())
    st.bar_chart(filtered_data.groupby('GND_IA')['VALOR_CLEAN'].sum())

# Observação
st.info("Use os filtros acima para explorar as emendas de forma detalhada.")


import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")

# Título e descrição
st.title("Dashboard de Ordens de Serviços Encerradas")
st.markdown("### Vizualize os principais indicadores!")

# URL do dashboard (substitua pelo link do seu Streamlit)
dashboard_url = "https://dashboards-os-encerradas.streamlit.app/"  # Insira o link da sua aplicação aqui

# Gerar QR Code
qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(dashboard_url)
qr.make(fit=True)

# Converter QR Code em imagem
qr_img = qr.make_image(fill="black", back_color="white")
buffer = BytesIO()
qr_img.save(buffer, format="PNG")
buffer.seek(0)
qr_image = Image.open(buffer)

# Exibir QR Code no Streamlit
st.sidebar.image(qr_image, caption="Acesse pelo QR Code", use_container_width=True)

# Carregar os dados ignorando os cabeçalhos
try:
    df = pd.read_csv("os_encerradas.csv", sep=";", decimal=",", encoding="latin1",skiprows=1)
except UnicodeDecodeError:
    st.error("Erro ao carregar o arquivo. Verifique a codificação do arquivo CSV.")
    st.stop()

# Renomear as colunas manualmente
df.columns = [
    "Protocolo", "ID Cliente", "ID Contrato", "Cliente", "Tipo", "Classificações", "Metodo",
    "Status", "Criada", "Agendamento", "Encerrada", "Responsável", "Usuário", "Bairro",
    "POP", "OS", "Protocolo Externo", "Finalizado Por", "Telefones"
]

# Verifica se a coluna 'Criada' existe
if "Criada" not in df.columns:
    st.error("A coluna 'Criada' não foi encontrada no arquivo")
    st.stop

# Garantir que a coluna 'Criada' seja datetime
df["Criada"] = pd.to_datetime(df["Criada"], errors="coerce")

# Filtrar dados inválidos
df = df.dropna(subset=["Criada"])
df = df.sort_values("Criada")

# Criar coluna de agrupamento mensal
df["Month"] = df["Criada"].dt.to_period("M").astype(str)

# Sidebar para selecionar o mês
month = st.sidebar.selectbox("Selecione o Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

# Layout de gráficos
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8 = st.columns(2)

# Gráfico 1: Clientes com chamados encerrados
client_counts = df_filtered["Cliente"].value_counts().reset_index()
client_counts.columns = ["Cliente", "Chamados"]
fig_clients = px.bar(client_counts, x="Cliente", y="Chamados",
                     title="Clientes que mais encerraram chamados",
                     text="Chamados")
col1.plotly_chart(fig_clients, use_container_width=True)

# Gráfico 2: Tipos de problemas que mais encerraram chamados
tipo_counts = df_filtered["Tipo"].value_counts().reset_index()
tipo_counts.columns = ["Tipo", "Chamados"]
fig_tipos = px.bar(tipo_counts, x="Tipo", y="Chamados", color="Chamados",
                     title="Tipos de problemas que mais encerraram chamados",
                     text="Chamados")
col2.plotly_chart(fig_tipos, use_container_width=True)

# Gráfico 3: Metodo de encerramento de chamados
metodo_counts = df_filtered["Metodo"].value_counts().reset_index()
metodo_counts.columns = ["Metodo", "Chamados"]
fig_metodos = px.pie(metodo_counts, names="Metodo", values="Chamados",
                     title="Metodo de encerramento de chamados")
col3.plotly_chart(fig_metodos, use_container_width=True)

# Gráfico 4: Status de encerramento de chamados
status_counts = df_filtered["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Chamados"]
fig_status = px.bar(status_counts, x="Status", y="Chamados", color="Chamados",
                     title="Status da encerramento de chamados",
                     text="Chamados")
col4.plotly_chart(fig_status, use_container_width=True)

# Gráfico 5: Data de encerramento dos chamados
encerrada_counts = df_filtered["Encerrada"].value_counts().reset_index()
encerrada_counts.columns = ["Encerrada", "Chamados"]
fig_encerradas = px.bar(encerrada_counts, x="Encerrada", y="Chamados", color="Chamados",
                   title="Data de encerramento dos chamados",
                   text="Chamados")
col5.plotly_chart(fig_encerradas, use_container_width=True)

# Gráfico 6: Técnicos que mais encerram chamados
final_counts = df_filtered["Finalizado Por"].value_counts().reset_index()
final_counts.columns = ["Finalizado Por", "Chamados"]
fig_finals = px.area(final_counts, x="Finalizado Por", y="Chamados", color="Chamados",
                   title="Usuários que mais encerraram chamados",
                   text="Chamados")
col6.plotly_chart(fig_finals, use_container_width=True)

# Gráfico 7: Bairros que mais encerraram chamados
bairro_counts = df_filtered["Bairro"].value_counts().reset_index()
bairro_counts.columns = ["Bairro", "Chamados"]
fig_bairros = px.pie(bairro_counts, names="Bairro", values="Chamados",
                     title="Bairros que mais abriram chamados")
col7.plotly_chart(fig_bairros, use_container_width=True)

# Gráfico 8: POPs que mais encerraram chamados
pop_counts = df_filtered["POP"].value_counts().reset_index()
pop_counts.columns = ["POP", "Chamados"]
fig_pops = px.bar(pop_counts, x="POP", y="Chamados", color="Chamados",
                   title="POPs que mais encerraram chamados",
                   text="Chamados")
col8.plotly_chart(fig_pops, use_container_width=True)
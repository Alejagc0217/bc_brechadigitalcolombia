import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title= "Super Store Dashboard",
    page_icon= ":)"
)

def cargar_datos():
    url = "https://raw.githubusercontent.com/WuCandice/Superstore-Sales-Analysis/refs/heads/main/dataset/Superstore%20Dataset.csv"
    data = pd.read_csv(url, encoding='latin1')
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    return data

df = cargar_datos()

st.sidebar.header("Filtros del Dashboard")
min_date = df['Order Date'].min()
max_date= df['Order Date'].max()


fecha_inicial, fecha_final = st.sidebar.date_input(
    "selecciona un rango de fechas", 
    value= [min_date, max_date],
    min_value= min_date,
    max_value= max_date
)

df_filtrado = df[df['Order Date'].between(pd.to_datetime(fecha_inicial), pd.to_datetime(fecha_final))]

st.title("Super Store Dashboard")
st.markdown("##")

ventas_totales = df['Sales'].sum()
utilidades_totales = df["Profit"]
ordenes_totales = df['Order ID'].nunique()
clientes_totales = df['Customer ID'].nunique()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label = "Ventas Totales", value=f"{ventas_totales}")
with col2:
    st.metric(label = "Utilidad Totales", value=f"{utilidades_totales}")
with col3:
    st.metric(label = "Ordenes Totales", value=f"{ordenes_totales}")
with col4:
    st.metric(label = "Clientes Totales", value=f"{clientes_totales}")


st.header("Ventas y Utilidades a lo largo del tiempo")
ventas_por_utilidad = df_filtrado.set_index("Order Date").resample('M').agg({'Sales':'sum', 'Profit':'sum'}).reset_index()

fig_area = px.area(
    ventas_por_utilidad,
    x ='Order Date',
    y=['Sales', 'Profit'],
    title="Evolución de entas y utilidades en el tiempo"
)

st.plotly_chart(fig_area, use_container_width=True)
st.markdown('---')

colpie, coldona = st.columns(2)

with colpie:
    ventas_by_region = df_filtrado.groupby('Region')['Sales'].sum().reset_index()
    fig_pie_region = px.pie(
        ventas_by_region,
        names = 'Region',
        values = 'Sales',
        title="Ventas por Region"
    )

    st.plotly_chart(fig_pie_region, use_container_width=True)

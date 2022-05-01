# Librerias para Streamlit, Pandas y Altair
import streamlit as st
import pandas as pd 
import altair as alt

# Librerias para importar imagenes
from PIL import Image
from pandas import read_excel

#Cargar bases
precios_productos = pd.read_excel('InformationRefinery.xlsx',sheet_name='PreciosProductos')

# Convertir base en tablas con pandas 

base_precios_productos= pd.melt(precios_productos, id_vars=['Fecha'], var_name='Producto', value_name='Precio U$D/barril')


#Cargar Imagenes
image1 = Image.open('Image1.jpg')
image2 = Image.open('Image2.jpg')
image3 = Image.open('Image3.jpg')
image4 = Image.open('Tarjetadepresntacion.PNG')

# Inicio de la aplicación
st.sidebar.title('Demo de Aplicación')
selectbox=st.sidebar.selectbox(
    "Seleccione el proceso",
    ("Bienvenida","Inicio de Aplicación", "Análisis", "Machine-Learning"), index=0)


# Primera selección "Bienvenida"  en la caja de opciones 
if 	selectbox== 'Bienvenida':

	st.title("Bienvenido")

	html_temp = """
	<div style="background-color:teal ;padding:10px">
	<h2 style="color:white;text-align:center;">Indicadores con Machine Learning Python</h2>
	</div>
	"""

	st.markdown(html_temp, unsafe_allow_html=True)

	st.image(image1, caption='Python-Streamlit-Altair',
	          use_column_width=True)

# Segunda selección "Inicio de Aplicación" en la caja de opciones

if 	selectbox== 'Inicio de Aplicación':

	st.title("Indicadores en Refinerias Python App")

	html_temp = """
	<div style="background-color:teal ;padding:10px">
	<h2 style="color:white;text-align:center;">Margen de Refinación</h2>
	</div>
	"""

	st.markdown(html_temp, unsafe_allow_html=True)

	st.image(image2, caption='Version 0.2 by Ing. Carlos Carrillo Villavicencio',
	          use_column_width=True)

	st.title('Margen de refinación App')

	st.write("""
		El margen de refinación es un **indicador económico** que diferencia los ingresos de 
		los productos refinados y los costos de todo el  petróleo crudo y otros insumos que
		intervienen en el proceso de refinación.
		### **Variables del Margen de refinación** 
		|Margen Neto|=|Ventas por productos|-|Costos por materia prima|-|Costos operativos|
		|-----------|-|----------------------|-|--------------|-|-----------------|
		|Margen de refinación|=|Gasolinas Diesel GLP Jet Fuel Oíl Residuo|-|Crudo NAO Cutter Stock|-|Personal Materiales Gastos financieros Administrativos|
	""")

	st.write("""
	### **Matemáticamente la expresión:**
		+ ∑[Producto]i * [Precio Producto]i
		- ∑[Crudo]j *[Costo del Crudo]j
		-  Costos varibales
		____________________________________
		= Margen de refinacion 
	""")

# Tercera selección "Análisis" en la caja de opciones

if 	selectbox== 'Análisis':

	st.sidebar.subheader('Parámetros ingresos-refinería')

	# Tercera selección  tipo de refineria en slidebar


	def configuracion_refinerias():
		tipo = st.sidebar.selectbox('Configuracion de Refineria',('Baja-conversión','Mediana-conversión','Alta-conversión','Profunda-conversión'))
		configuracion_refineria =	{'Configuración':tipo}

		configuracion = pd.DataFrame(configuracion_refineria, index=['Tipo'] ) 
		return configuracion

	df_configuracion=configuracion_refinerias()
	st.subheader('Configuracion de la refinería')
	st.write(df_configuracion.T)

	
	# Tercera selección carga a refineria e ingreso de materias primas

	def ingreso_de_carga():
		carga = st.sidebar.slider('Carga a refineria', 10000,300000,100000, step=10000)
		carga_a_refinerias = {'Ingreso de crudo':carga}
		carga_refineria = pd.DataFrame(carga_a_refinerias, index=['BPD'])
		return carga_refineria
	df_carga=ingreso_de_carga()	
	st.subheader('Carga a refinería')		
	st.write(df_carga.T)


	previo_configuracion = df_configuracion.loc['Tipo' ,'Configuración']

	def ingreso_importaciones():
	
		if previo_configuracion == 'Baja-conversión':	
			ingreso_importados = st.sidebar.slider('porcentaje de importados respecto a la carga', 0.0, 0.5, 0.3)
		if previo_configuracion == 'Mediana-conversión':
			ingreso_importados = st.sidebar.slider('porcentaje de importados respecto a la carga', 0.0, 0.30, 0.1)
		if previo_configuracion == 'Alta-conversión':
			ingreso_importados = st.sidebar.slider('porcentaje de importados respecto a la carga', 0.0, 0.15, 0.05)
		if previo_configuracion == 'Profunda-conversión':
			ingreso_importados = st.sidebar.slider('porcentaje de importados respecto a la carga', 0.0, 0.10, 0.05)
		ingreso_importados=round(ingreso_importados,2)
		
		importacion_a_refinerias = {'Importacion a refinerías':ingreso_importados}
		ingreso_importacion = pd.DataFrame(importacion_a_refinerias, index=['BPD'])	
		return ingreso_importacion	

	df_importaciones=ingreso_importaciones()
	
	dato_carga = df_carga.loc['BPD' ,'Ingreso de crudo']
	dato_importacion = df_importaciones.loc['BPD' ,'Importacion a refinerías']
	volumen_importacion = dato_carga*dato_importacion
	volumen_importado = {'Importacion de otras materias prima':volumen_importacion }
	df_volulmen_de_importacion =pd.DataFrame(volumen_importado, index=['BPD'])
	st.write(df_volulmen_de_importacion.T)
		


	# Tercera selección  porcentajes de produccion en slidebar

	st.sidebar.subheader('Parámetros producción-derivados')

	def porcentaje_de_produccion():
		porcentaje_residuo = st.sidebar.slider('Porcentaje de Residuo', 0.0, 1.0, 0.45)
		lim1=1-porcentaje_residuo
		porcentaje_gasolina = st.sidebar.slider('Porcentaje de gasolina', 0.0, lim1, 0.0)
		lim2=1-porcentaje_residuo-porcentaje_gasolina
		porcentaje_diesel =st.sidebar.slider('Porcentaje de diesel',0.0,lim2,0.0)
		lim3=1-porcentaje_residuo-porcentaje_gasolina-porcentaje_diesel
		porcentaje_glp =st.sidebar.slider('Porcentaje de GLP', 0.0,lim3, 0.00)
		lim4=1-porcentaje_residuo-porcentaje_gasolina-porcentaje_diesel-porcentaje_glp
		porcentaje_jet =st.sidebar.slider('Porcentaje de Jet', 0.0,lim4, 0.00)
		porcentaje_otros=round(1-porcentaje_residuo-porcentaje_gasolina-porcentaje_diesel-porcentaje_glp-porcentaje_jet,2)
		porcentaje_total=round(porcentaje_residuo+porcentaje_gasolina+porcentaje_diesel+porcentaje_glp+porcentaje_jet+porcentaje_otros,2)
		data_porcentajes = {'1-Porcentaje de residuo :':porcentaje_residuo,
				'2-Porcentaje de gasolina:':porcentaje_gasolina,
				'3-Porcentaje de diesel  :':porcentaje_diesel,
				'4-Porcentaje de GLP     :':porcentaje_glp,
				'5-Porcentaje de Jet     :':porcentaje_jet,
				'6-Porcentaje de otros   :':porcentaje_otros,
				'Total':porcentaje_total}
		

		porcentajes = pd.DataFrame(data_porcentajes, index=['%'])
		return porcentajes

	df_porcentajes = porcentaje_de_produccion()
	st.subheader('Porcentajes de Producción')
	st.write(df_porcentajes.T)	


	#tercera seleccion operaciones de base con parametros
	#**************************************************************************

	dato_carga = df_carga.loc['BPD' ,'Ingreso de crudo']
	


	dato_residuo = df_porcentajes.loc['%' ,'1-Porcentaje de residuo :']
	dato_gasolina = df_porcentajes.loc['%' ,'2-Porcentaje de gasolina:']
	dato_diesel =df_porcentajes.loc['%','3-Porcentaje de diesel  :']
	dato_GLP =df_porcentajes.loc['%','4-Porcentaje de GLP     :']
	dato_jet = df_porcentajes.loc['%','5-Porcentaje de Jet     :']
	dato_otros = df_porcentajes.loc['%','6-Porcentaje de otros   :']

	volumen_residuo =dato_carga*dato_residuo
	volumen_gasolina= dato_carga*dato_gasolina
	volumen_diesel =dato_carga*dato_diesel
	volumen_GLP=dato_carga*dato_GLP
	volumen_jet =dato_carga*dato_jet
	volumen_otros = dato_carga*dato_otros
	volumen_Total= volumen_residuo+volumen_gasolina+volumen_diesel+volumen_GLP+volumen_jet+volumen_otros

	volumen_residuo=round(volumen_residuo,0)
	volumen_gasolina=round(volumen_gasolina,0)
	volumen_diesel=round(volumen_diesel,0)
	volumen_GLP=round(volumen_GLP,0)
	volumen_jet=round(volumen_jet,0)
	volumen_otros=round(volumen_otros,0)
	volumen_Total=round(volumen_Total,0)


	data_volumen = {'Volumen de residuo':volumen_residuo,
			 		'Volumen de gasolina':volumen_gasolina,
			 		'Volumen de diesel':volumen_diesel,
			 		'Volumen de GLP': volumen_GLP,
			 		'Volumen de jet': volumen_jet,
			 		'Volumen de otros': volumen_otros,
			 		'Volumen Total': volumen_Total}				 

	df_volumenes = pd.DataFrame(data_volumen, index=['BBL'])

	date = precios_productos['Fecha']
	ingreso_gasolina = precios_productos['Precio Gasolinas']*volumen_gasolina
	ingreso_diesel = precios_productos['Precio Diesel']*volumen_diesel
	ingreso_GLP = precios_productos['Precio GLP']*volumen_GLP
	ingreso_jet = precios_productos['Precio Jet']*volumen_jet
	ingreso_otros = precios_productos['Precio Otros']*volumen_otros
	ingreso_residuo = precios_productos['Precio Residuo']*volumen_residuo

	ingreso_gasolina = round(ingreso_gasolina,2)
	ingreso_diesel = round(ingreso_diesel,2)
	ingreso_GLP = round(ingreso_GLP,2)
	ingreso_jet = round(ingreso_jet,2)
	ingreso_otros = round(ingreso_otros,2)
	ingreso_residuo = round(ingreso_residuo,2)

	data_ingresos ={'Fecha':date,
					'Ingresos por Gasolinas':ingreso_gasolina,
					'Ingresos por Diesel':ingreso_diesel,
					'Ingresos por GLP':ingreso_GLP,
					'Ingresos por Jet':ingreso_jet,
					'Ingresos por Otros':ingreso_otros,
					'Ingresos por Residuo':ingreso_residuo}
	df_ingresos = pd.DataFrame(data_ingresos)

	base_df_ingresos= pd.melt(df_ingresos, id_vars=['Fecha'], var_name='Producto', value_name='U$D')

	importacion_materias_primas = precios_productos['Precio Gasolinas']*volumen_importacion
	importacion_materias_primas = round(importacion_materias_primas,2)

	ingresos_magen = ingreso_gasolina+ingreso_diesel+ingreso_GLP+ingreso_jet+ingreso_otros+ingreso_residuo
	costos_materia_prima =(precios_productos['Precio WTI']*dato_carga)+importacion_materias_primas
	margen_de_refinacion=(ingresos_magen-costos_materia_prima)
	margen_unitario=(margen_de_refinacion/dato_carga)

	ingresos_magen = round(ingresos_magen,2)
	costos_materia_prima=round(costos_materia_prima,2)
	margen_de_refinacion=round(margen_de_refinacion,2)
	margen_unitario=round(margen_unitario,2)

	importacion_materias_primas = precios_productos['Precio Gasolinas']*volumen_importacion
	importacion_materias_primas = round(importacion_materias_primas,2)

	data_margen ={'Fecha':date,
			      'Ingresos por ventas':ingresos_magen,
				  'Costos por materia prima':costos_materia_prima,
				  'Margen de refinación': margen_de_refinacion,
				  'Margen bruto de refinación':margen_unitario}
	df_margen_de_refinacion =pd.DataFrame(data_margen)


	#**************************************************************************
	# Tercera selección checklist 1 mercado de precios

	check_precios= st.checkbox('Mercado de precios', value=False, key=None)
	if check_precios==True:

		# Tabla precios de productos 

		st.write(precios_productos)
		
		# Gráfico del precios de productos 

		grafico_precios = alt.Chart(base_precios_productos).mark_line(point = True).encode(
		alt.X('Fecha'),
		alt.Y('Precio U$D/barril'),
		color='Producto',
		tooltip=['Fecha', 'Precio U$D/barril', 'Producto']
		).interactive().properties( title = 'Precios internacionales de productos derivados de petróleo 2018-2019', width=700, height=400)
		st.altair_chart(grafico_precios)

		# Gráfico del precios de productos  con linea indicadora

		nearest = alt.selection(type='single', nearest=True, on='mouseover',
		                        fields=['Fecha'], empty='none')
		
		grafico_lineas = alt.Chart(base_precios_productos).mark_line().encode(
		    x='Fecha',
		    y='Precio U$D/barril',
		    color='Producto',
		    tooltip=['Fecha','Precio U$D/barril']
		    
		)

		selectors = alt.Chart(base_precios_productos).mark_point().encode(
		    x='Fecha',
		    opacity=alt.value(0),
		).add_selection(
		    nearest
		)
		points = grafico_lineas.mark_point().encode(
		    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
		)

		text = grafico_lineas.mark_text(align='left', dx=5, dy=-5).encode(
		    text=alt.condition(nearest, 'Precio U$D/barril', alt.value(' '))
		)

		rules = alt.Chart(base_precios_productos).mark_rule(color='gray').encode(
		    x='Fecha',
		).transform_filter(
		    nearest
		)

		grafico_capas = alt.layer( grafico_lineas, selectors, points,  rules , text).properties( width=600, height=300).interactive()

		st.altair_chart(grafico_capas)

	# Tercera selección checklist 2 cálculos básicos 

	check_calculos= st.checkbox('Cálculos preliminares', value=False, key=None)
	
	if check_calculos==True:
		st.subheader('Volumen de derivados producidos')
		st.write(df_volumenes.T)

		st.subheader('Ingresos por derivados producidos')
		st.write(df_ingresos)

		grafico_ingresos_area = alt.Chart(base_df_ingresos).mark_area(opacity=0.7).encode(
		    x='Fecha',
		    y='U$D',
		    color='Producto',
		    tooltip=['Fecha','U$D']
		    
		).interactive().properties( title = 'Ingresos por venta derivados de petróleo 2018-2019', width=700, height=400)
		st.altair_chart(grafico_ingresos_area)

		st.subheader('Análisis de ventas por derivados producidos')
		filtro_base_df_ingreso = st.multiselect('Selecione el producto', base_df_ingresos['Producto'].unique())
		base_df_ingresos_filtrada =base_df_ingresos[base_df_ingresos['Producto'].isin(filtro_base_df_ingreso)]
		st.write(base_df_ingresos_filtrada)
		grafico_ingresos = alt.Chart(base_df_ingresos_filtrada).mark_bar().encode(
		    x='Fecha',
		    y='U$D',
		    color='Producto',
		    tooltip=['Fecha','U$D']
		    
		).interactive().properties( title = 'Ingresos por venta derivados de petróleo 2018-2019', width=700, height=400)
		st.altair_chart(grafico_ingresos)

	# Tercera selección checklist 3 margen de refinación 

	check_margen = st.checkbox('Cálculo del magen de refinación', value=False, key=None)
	
	if check_margen == True:
			
		st.write(df_margen_de_refinacion)
			
		grafico_margen_ingresos = alt.Chart(df_margen_de_refinacion).mark_area(color='yellow',opacity=0.3).encode(
		    x='Fecha',
		    y='Ingresos por ventas',
		    tooltip=['Fecha','Ingresos por ventas']  
		).interactive().properties(  width=700, height=300)
		grafico_margen_costos = alt.Chart(df_margen_de_refinacion).mark_area(color='red',opacity=0.5).encode(
		    x='Fecha',
		    y='Costos por materia prima',
		    tooltip=['Fecha','Costos por materia prima']  
		).interactive()
			
		grafico_margen = alt.Chart(df_margen_de_refinacion).mark_line(color='red').encode(
		    x='Fecha',
		    y='Margen bruto de refinación',
		    tooltip=['Fecha','Margen bruto de refinación']  
		).interactive().properties( width=700, height=200)
			
		st.subheader('Balance de costos y ventas')
		st.altair_chart(grafico_margen_ingresos+grafico_margen_costos)
		st.subheader('Margen bruto de refinación')
		st.altair_chart(grafico_margen)

		st.subheader('Análisis de resultados')	
		histograma_margen =	alt.Chart(df_margen_de_refinacion).mark_bar(color='red').encode(
    		alt.X("Margen bruto de refinación", bin=True),
   			y='count()',
		).interactive().properties(  width=250, height=200)

		media = alt.Chart(df_margen_de_refinacion).mark_rule(color='black').encode(
		    x='mean(Margen bruto de refinación)',
		    size=alt.value(5),
		)
		

		orden_margen = alt.Chart(df_margen_de_refinacion).mark_bar(color='gold').encode(
		    x='Margen bruto de refinación',
		    y=alt.Y('Fecha', sort='-x')
		).interactive().properties(  width=250, height=200)


		st.altair_chart(histograma_margen+media|orden_margen)

# Cuarta Seleccion "Machine-Learning"  en la caja de opciones 
if selectbox== 'Machine-Learning':

	st.title("Keras-Tensorflow-Scikit learn")

	html_temp = """
	<div style="background-color:teal ;padding:10px">
	<h2 style="color:white;text-align:center;">Python</h2>
	</div>
	"""

	st.markdown(html_temp, unsafe_allow_html=True)

	st.image(image3, caption='Version Premium',
	          use_column_width=True)
	st.sidebar.image(image4, caption='Contacto',
	          use_column_width=True)
	st.markdown('https://www.linkedin.com/in/carloscarrillovillavicencio/')	
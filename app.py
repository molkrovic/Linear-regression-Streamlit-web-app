import streamlit as st
import numpy as np
import pickle

modelo_no_fumador = pickle.load(open('models/modelo_no_fumador.sav', 'rb'))
modelo_fumador_bmi_alto = pickle.load(open('models/modelo_fumador_bmi_alto.sav', 'rb'))
modelo_fumador_bmi_bajo = pickle.load(open('models/modelo_fumador_bmi_bajo.sav', 'rb'))

st.markdown('#### Insurance Cost Prediction')

age = st.selectbox("Age:", np.arange(18, 100, 1))
sex = st.selectbox("Sex:", ['male', 'female'])
bmi = st.number_input(label='BMI:', step=0.01, format='%.2f')
children = st.number_input(label='Number of children:', step=1., format='%.0f')
smoker = st.selectbox("Smoker:", ['yes', 'no'])
region = st.selectbox("Region:", ['northeast', 'northwest', 'southeast', 'southwest'])

if sex == 'male':
    sex = 1
else:
    sex = 0

if smoker == 'yes':
    smoker = 1
else:
    smoker = 0

region_northeast = 0
region_northwest = 0
region_southeast = 0
region_southwest = 0

if region == 'northeast':
    region_northeast = 1
elif region == 'northwest':
    region_northwest = 1
elif region == 'southeast':
    region_southeast = 1
elif region == 'southwest':
    region_southwest = 1

cols = ['age', 'sex', 'bmi', 'children', 'smoker', 'region_northeast', 'region_northwest', 'region_southeast', 'region_southwest'] 
data = [age, sex, bmi, children, smoker, region_northeast, region_northwest, region_southeast, region_southwest]
posted = np.asarray(data).reshape(1,9)

if smoker == 0:
    modelo = modelo_no_fumador
else:
    if bmi<30:
        modelo = modelo_fumador_bmi_bajo
    else:
        modelo = modelo_fumador_bmi_alto

try:
    result = modelo.predict(posted)
    text_result = result.tolist()[0]
except:
    text_result = 'Invalid values'

if text_result == 'Invalid values':
    message = 'Invalid values'
else:
    message = 'Estimated charges: ' + str(round(text_result))

st.code(message)
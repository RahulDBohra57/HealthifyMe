import os
import pandas as pd
import streamlit as st 
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the environment
gemini_api_key = os.getenv('GOOGLE_API_KEY1')

# Lets configure the model
model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash-lite",
    api_key = gemini_api_key,
    temperature = 0.7)

# Designe the UI of application
st.title(':orange[HealthifyMe:] :green[Your Personal Health Assistant]')
st.markdown('''
            This application will assist you to get better and customized health advice. You can ask your health realted issues and
            get the personalized guidance.
            ''')
st.write (''' 
**Follow These Steps:**
* Enter your details in sidebar.
* Rate your activity and fitnesss on the scale of 0-5.
* Submit your details.
* Ask your question on main page.
* Click generate and relax.
''')

# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name = st.sidebar.text_input('Enter Your Name:')
gender = st.sidebar.selectbox('Select Your Gender:',['Male','Female'])
age = st.sidebar.text_input('Enter Your Age:')
weight = st.sidebar.text_input('Enter your Weight in Kgs:')
height = st.sidebar.text_input('Enter your Height in cm:')
bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
active = st.sidebar.slider('Rate your daily activity (0-5):',0,5,step=1)
fitness = st.sidebar.slider('Rate your fitness (0-5):',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, your BMI is: {round(bmi,2)} Kg/m^2")
    
# Lets use the gemini model to generate the report
user_input = st.text_input('Ask me your question: ')
prompt = f'''
<Role> You are an expert in health and wellness and has 10+ years experience in guiding people.

<Goal> Generate a customized report addressing the problem the user has asked. Here is the question that user has aksed: {user_input}

<Context> Here are the details that the user has provided:
name={name}
gender={gender}
age={age}
height = {height}
weight = {weight}
bmi={bmi}
activity rating (0-5) = {active}
fitness rating (0-5) = {fitness}

<Format> Following should be outline of the report, in the sequence provided:
* Start with a 2-3 line comment on the details that user has provided.
* Explain what the real problem could be on the basis of input the user has provided.
* Suggest the possible reasons for the problem.
* What are the possible solutions.
* Mention the doctor from which specialization can be visited (if required)
* Mention any change in the diet which is required.
* In last create a final summary of all the things that has been discussed in the report.

<Instructions> 
* Use bullet points where ever possible.
* Create tables to represent any data where ever possible.
* Strictly do not advise any medicine.

<Style>
* Strictly use positive tone of voice.
'''

if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)
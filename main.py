import streamlit as st
import random
import string
import pandas as pd
import os
import base64

def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'

def generate_password(length, upper, lower, numeric, special_chars):
    password = []

    for _ in range(upper):
        password.append(random.choice(string.ascii_uppercase))

    for _ in range(lower):
        password.append(random.choice(string.ascii_lowercase))

    for _ in range(numeric):
        password.append(random.choice(string.digits))
        
    password += list(special_chars)

    while len(password) < length:
        char_type = random.choice([0, 1, 2])  # 0 for uppercase, 1 for lowercase, 2 for numeric

        if char_type == 0:
            password.append(random.choice(string.ascii_uppercase))
        elif char_type == 1:
            password.append(random.choice(string.ascii_lowercase))
        else:
            password.append(random.choice(string.digits))

    random.shuffle(password)

    return ''.join(password)

st.title("Bulk Password Generator")



num_passwords = st.number_input('Enter the number of passwords you want to generate', min_value=1, max_value=10, value=1)

data = []

for i in range(num_passwords):
    st.subheader(f'Password {i+1}')
    name = st.text_input(f'Enter a name/identifier for password {i+1}')
    length = st.number_input(f'Enter the maximum length of password {i+1}', min_value=1, max_value=100, value=8)
    upper = st.number_input(f'Enter the number of uppercase letters for password {i+1}', min_value=0, max_value=100, value=2)
    lower = st.number_input(f'Enter the number of lowercase letters for password {i+1}', min_value=0, max_value=100, value=2)
    numeric = st.number_input(f'Enter the number of numeric characters for password {i+1}', min_value=0, max_value=100, value=2)
    special_chars = st.text_input(f'Enter the special characters you want to include in password {i+1}')
    
    password = generate_password(length, upper, lower, numeric, special_chars)
    data.append([name, password])

df = pd.DataFrame(data, columns=['Name', 'Password'])

if st.button('Generate Passwords'):
    st.dataframe(df)

    if not os.path.isfile('passwords.csv'):
        df.to_csv('passwords.csv', index=False)
    else:
        df.to_csv('passwords.csv', mode='a', header=False, index=False)

    st.markdown(get_csv_download_link(df, 'passwords.csv'), unsafe_allow_html=True)


st.text('''Note: 
1. You can generate up to 10 passwords at a time.
2. Each password can be customised according to your preference.
3. Passwords can be downloaded as a CSV file.''')

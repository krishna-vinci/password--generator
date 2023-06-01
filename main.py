import streamlit as st
import random
import string
import pandas as pd
import os
import base64

# Function to download data as csv
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'

def generate_password(length, upper, lower, numeric, special_chars):
    password = []

    # Add uppercase letters
    for _ in range(upper):
        password.append(random.choice(string.ascii_uppercase))

    # Add lowercase letters
    for _ in range(lower):
        password.append(random.choice(string.ascii_lowercase))

    # Add numeric characters
    for _ in range(numeric):
        password.append(random.choice(string.digits))

    # Add special characters
    password += list(special_chars)

    # If the password is shorter than the desired length, add random characters
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


st.title("Password Generator")
st.text('''Note: 
1. You can download CSV at the end
2. It will add random upper, lower or numeric characters to reach the maximum password length''')

website = st.text_input('Enter the name of the website/service')
length = st.number_input('Enter the maximum length of the password', min_value=1, max_value=100, value=8)
upper = st.number_input('Enter the number of uppercase letters', min_value=0, max_value=100, value=2)
lower = st.number_input('Enter the number of lowercase letters', min_value=0, max_value=100, value=2)
numeric = st.number_input('Enter the number of numeric characters', min_value=0, max_value=100, value=2)
special_chars = st.text_input('Enter the special characters you want to include')

if st.button('Generate Password'):
    password = generate_password(length, upper, lower, numeric, special_chars)
    st.text_area("Your password is:", value=password)  # User can manually copy from here
    st.text("manual copy")

    # Save password to CSV
    df = pd.DataFrame({'Website': [website], 'Password': [password]})
    if not os.path.isfile('passwords.csv'):
        df.to_csv('passwords.csv', index=False)
    else:  # else it exists so append without writing the header
        df.to_csv('passwords.csv', mode='a', header=False, index=False)

    # Download link
    st.markdown(get_csv_download_link(df, 'password.csv'), unsafe_allow_html=True)

    st.success("Done")


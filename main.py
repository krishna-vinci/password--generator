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

def generate_password(length, upper, lower, special_chars, digits):
    password = []

    # Add uppercase letters
    for _ in range(upper):
        password.append(random.choice(string.ascii_uppercase))

    # Add lowercase letters
    for _ in range(lower):
        password.append(random.choice(string.ascii_lowercase))

    # Add special characters
    password += list(special_chars)

    # Add digits
    for _ in range(digits):
        password.append(random.choice(string.digits))

    # If the password is shorter than the desired length, add random characters
    while len(password) < length:
        char_type = random.choice([0, 1, 2])  # 0 for uppercase, 1 for lowercase, 2 for digits

        if char_type == 0:
            password.append(random.choice(string.ascii_uppercase))
        elif char_type == 1:
            password.append(random.choice(string.ascii_lowercase))
        else:
            password.append(random.choice(string.digits))

    random.shuffle(password)

    return ''.join(password)

number_of_passwords = st.sidebar.slider("How many passwords do you want to generate?", 1, 10)
auto_generate = st.sidebar.checkbox("Auto generate all passwords with first input parameters?")
default_auto_generate = st.sidebar.checkbox("Default mode for auto-generation?")
auto_name = st.sidebar.text_input("Enter prefix for auto name generation (leave blank for no auto naming):")

# Default parameters for auto-generation
default_length = 8
default_upper = 2
default_lower = 2
default_special_chars = '@'
default_digits = 2

length = default_length if default_auto_generate else None
upper = default_upper if default_auto_generate else None
lower = default_lower if default_auto_generate else None
special_chars = default_special_chars if default_auto_generate else None
digits = default_digits if default_auto_generate else None

all_passwords = []

for i in range(number_of_passwords):
    with st.expander(f"Generate Password {i + 1}", expanded=i == 0):
        website = auto_name + str(i + 1) if auto_name else st.text_input(f'Enter the name of the website/service for Password {i + 1}')

        if i == 0 or not auto_generate:
            length = st.number_input(f'Enter the maximum length of the password for Password {i + 1}', min_value=1, max_value=100, value=length)
            upper = st.number_input(f'Enter the number of uppercase letters for Password {i + 1}', min_value=0, max_value=100, value=upper)
            lower = st.number_input(f'Enter the number of lowercase letters for Password {i + 1}', min_value=0, max_value=100, value=lower)
            special_chars = st.text_input(f'Enter the special characters you want to include in Password {i + 1}', value=special_chars)
            digits = st.number_input(f'Enter the number of digits for Password {i + 1}', min_value=0, max_value=100, value=digits)

        password = generate_password(length, upper, lower, special_chars, digits)
        all_passwords.append({'Website': website, 'Password': password})

if st.button('Generate Passwords'):
    # Create DataFrame and save to csv
    df = pd.DataFrame(all_passwords)
    df.to_csv('passwords.csv', index=False)

    # Download link
    st.markdown(get_csv_download_link(df, 'passwords.csv'), unsafe_allow_html=True)

    # Show passwords
    for i in range(number_of_passwords):
        st.text_input(f"Your password {i + 1} is:", value=all_passwords[i]['Password'], type="password")

note = """
    ### Note:
    1. You can generate a single password or bulk passwords up to 10 at a time.
    2. Each password can be customised according to your preference.
    3. You can opt to automatically generate all 10 passwords based on the criteria of the first password.
    4. All generated passwords can be downloaded as a single CSV file for your reference.
"""
st.sidebar.markdown(note)

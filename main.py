import streamlit as st
import random
import string
import pandas as pd
import os
import base64
import pyperclip

# Function to download data as csv
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'

def generate_password(length, upper, lower, special_chars):
    password = []

    # Add uppercase letters
    for _ in range(upper):
        password.append(random.choice(string.ascii_uppercase))

    # Add lowercase letters
    for _ in range(lower):
        password.append(random.choice(string.ascii_lowercase))

    # Add special characters
    password += list(special_chars)

    # If the password is shorter than the desired length, add random characters
    while len(password) < length:
        char_type = random.choice([0, 1])  # 0 for uppercase, 1 for lowercase

        if char_type == 0:
            password.append(random.choice(string.ascii_uppercase))
        else:
            password.append(random.choice(string.ascii_lowercase))

    random.shuffle(password)

    return ''.join(password)


st.text('''  

                                                                                                                                                       
,------.                                                          ,--.    ,----.                                                ,--.                   
|  .--. '  ,--,--.  ,---.   ,---.  ,--.   ,--.  ,---.  ,--.--.  ,-|  |   '  .-./     ,---.  ,--,--,   ,---.  ,--.--.  ,--,--. ,-'  '-.  ,---.  ,--.--. 
|  '--' | ' ,-.  | (  .-'  (  .-'  |  |.'.|  | | .-. | |  .--' ' .-. |   |  | .---. | .-. : |      \ | .-. : |  .--' ' ,-.  | '-.  .-' | .-. | |  .--' 
|  | --'  \ '-'  | .-'  `) .-'  `) |   .'.   | ' '-' ' |  |    \ `-' |   '  '--'  | \   --. |  ||  | \   --. |  |    \ '-'  |   |  |   ' '-' ' |  |    
`--'       `--`--' `----'  `----'  '--'   '--'  `---'  `--'     `---'     `------'   `----' `--''--'  `----' `--'     `--`--'   `--'    `---'  `--'    
                                                                                                                                                       

''')
st.title("Password Generator")
st.text('''Note: 
1. It Will auto save to clipboard
2. You can download CSV at the end
3. It will add random upper or lowercase letters to reach the maximum password length''')

website = st.text_input('Enter the name of the website/service')
length = st.number_input('Enter the maximum length of the password', min_value=1, max_value=100, value=8)
upper = st.number_input('Enter the number of uppercase letters', min_value=0, max_value=100, value=2)
lower = st.number_input('Enter the number of lowercase letters', min_value=0, max_value=100, value=2)
special_chars = st.text_input('Enter the special characters you want to include')

if st.button('Generate Password'):
    password = generate_password(length, upper, lower, special_chars)
    st.text_input("Your password is:", value=password, type="password")
    st.text("Auto saved to clipboard")

    # Save password to CSV
    df = pd.DataFrame({'Website': [website], 'Password': [password]})
    if not os.path.isfile('passwords.csv'):
        df.to_csv('passwords.csv', index=False)
    else:  # else it exists so append without writing the header
        df.to_csv('passwords.csv', mode='a', header=False, index=False)

    # Download link
    st.markdown(get_csv_download_link(df, 'password.csv'), unsafe_allow_html=True)

    # Copy to clipboard
    pyperclip.copy(password)

    st.success("Password has been copied to clipboard")
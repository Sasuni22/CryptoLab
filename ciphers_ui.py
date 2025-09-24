import streamlit as st

# ====== Page Config ======
st.set_page_config(
    page_title="CryptoLab",
    page_icon="🔐",
    layout="centered",
)

# ====== Dark Theme + Fonts ======
st.markdown("""
<style>
/* Dark background */
.stApp {
    background-color: #1e1e2f; /* dark blue/purple */
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Headers styling */
h1, h2, h3 {
    color: #f0f0f0; /* white */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Buttons */
.stButton>button {
    background-color: #4CAF50;  /* green */
    color: white;
    height: 3em;
    width: 10em;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #45a049;
}

/* Text input fields */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #2e2e3e;  /* dark input */
    color: white;
    border-radius: 5px;
}

/* Selectbox & Radio buttons */
.stSelectbox>div>div>div>span, .stRadio>div>label {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ====== Title ======
st.title("🔐 CryptoLab")
st.subheader("Encrypt & Decrypt Classical Ciphers")

# ====== Cipher Functions ======
def caesar_encrypt(text, shift):
    text = text.upper().replace(" ", "")
    return ''.join([chr((ord(c)-65 + shift)%26 + 65) if c.isalpha() else c for c in text])

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, 26-shift)

def vigenere_encrypt(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    res = ""
    key_index = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            res += chr((ord(c)-65 + shift)%26 + 65)
            key_index += 1
    return res

def vigenere_decrypt(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    res = ""
    key_index = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            res += chr((ord(c)-65 - shift + 26)%26 + 65)
            key_index += 1
    return res

# ====== Playfair Cipher ======
class Playfair:
    def __init__(self, key):
        self.key = ''.join(dict.fromkeys(key.upper().replace('J','I')))
        self.matrix = self.generate_matrix()

    def generate_matrix(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        used = set(self.key)
        matrix = list(self.key) + [c for c in alphabet if c not in used]
        return [matrix[i*5:(i+1)*5] for i in range(5)]

    def find_pos(self, char):
        if char == 'J': char = 'I'
        for r, row in enumerate(self.matrix):
            if char in row:
                return r, row.index(char)
        return None

    def process_text(self, text):
        text = text.upper().replace('J','I').replace(' ','')
        res = ''
        i = 0
        while i < len(text):
            a = text[i]
            b = ''
            if i+1 < len(text):
                b = text[i+1]
                if a == b:
                    b = 'X'
                    i -= 1
            else:
                b = 'X'
            res += a+b
            i += 2
        return res

    def encrypt(self, text):
        text = self.process_text(text)
        result = ''
        for i in range(0,len(text),2):
            a,b = text[i], text[i+1]
            r1,c1 = self.find_pos(a)
            r2,c2 = self.find_pos(b)
            if r1==r2:
                result += self.matrix[r1][(c1+1)%5]+self.matrix[r2][(c2+1)%5]
            elif c1==c2:
                result += self.matrix[(r1+1)%5][c1]+self.matrix[(r2+1)%5][c2]
            else:
                result += self.matrix[r1][c2]+self.matrix[r2][c1]
        return result

    def decrypt(self, text):
        result = ''
        for i in range(0,len(text),2):
            a,b = text[i], text[i+1]
            r1,c1 = self.find_pos(a)
            r2,c2 = self.find_pos(b)
            if r1==r2:
                result += self.matrix[r1][(c1-1)%5]+self.matrix[r2][(c2-1)%5]
            elif c1==c2:
                result += self.matrix[(r1-1)%5][c1]+self.matrix[(r2-1)%5][c2]
            else:
                result += self.matrix[r1][c2]+self.matrix[r2][c1]
        return result

# ====== Interactive UI ======
cipher = st.selectbox("Select Cipher", ["Caesar", "Vigenère", "Playfair"])
mode = st.radio("Mode", ["Encrypt", "Decrypt"])
text = st.text_area("Enter Text")
key = st.text_input("Enter Key / Shift")

if st.button("Run"):
    if cipher == "Caesar":
        try:
            shift = int(key)
            result = caesar_encrypt(text, shift) if mode=="Encrypt" else caesar_decrypt(text, shift)
        except:
            result = "Shift must be an integer!"
    elif cipher == "Vigenère":
        result = vigenere_encrypt(text, key) if mode=="Encrypt" else vigenere_decrypt(text, key)
    elif cipher == "Playfair":
        if key.strip()=="":
            result = "Key cannot be empty!"
        else:
            pf = Playfair(key)
            result = pf.encrypt(text) if mode=="Encrypt" else pf.decrypt(text)

    st.subheader("Result")
    st.text(result)

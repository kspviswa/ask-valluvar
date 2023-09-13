import streamlit as st
from prompt import fireGPTQuery
from talkvv import saveAudioFromTxt
import time
import base64



def getAvatar(role):
    if role == 'assistant':
        return './resources/vv.png'
    else:
        return None

def flatten(msges):
    if len(msges) > 1:
      s = ""
      for m in msges:
          s += str(m) + "\n"
      return s
    else:
        return ""

def glow(raw):
    s = f"""
      <p class="glow"> {raw}</p>
    """
    return s

def glow2(raw):
    s = f"""
      <p class="neonText"> {raw}</p>
    """
    return s

def decideGlow(raw, role):
    if role == 'assistant':
        return doGreen(raw)
    else:
        return doOrange(raw)

def doGreen(raw):
    s = f"""
      <p class="doGreen"> {raw}</p>
    """
    return s

def doOrange(raw):
    s = f"""
      <p class="doOrange"> {raw}</p>
    """
    return s

st.set_page_config(
    page_title="Ask Valluvar",
    page_icon="💭",
)

def embedAudio():
    with open('./test.wav', "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/wav">
            </audio>
            """
        return md

if 'listenEnabled' not in st.session_state :
    st.session_state.listenEnabled = True

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.image('./resources/vv.png', use_column_width='always')
    st.session_state.listenEnabled = st.toggle(label=':orange[Also hear 🎧 from Valluvar]')
    sw = '''
Ask Valluvar is powered by a large language model, along with some finetuning.
Ask Valluvar may produce inaccurate information about people, places, or facts
'''
    st.warning(body=f'`{sw}`', icon="⚠️")
    st.warning(body='Please refrain from providing any sensitive information', icon="🚨")
    if len(st.session_state.messages) > 1:
        st.download_button('Download Transcript 📖⬇️', str(st.session_state.messages),type='primary', use_container_width=True)




st.markdown("<center><h1>Ask Valluvar</h1></center>", unsafe_allow_html=True)

st.markdown("""
<style>
.chat-font {
    font-size:100px !important;
    
    color:green;
}

.doGreen {
  font-family:monospace;
  font-size:14px;
  color: green;   
}

.doOrange {
  font-family:monospace;
  font-size:14px;
  color: orange;   
}              

.neonText {
  color: #fff;
  font-family:monospace;
  font-size:20px;
  text-shadow:
      0 0 7px #fff,
      0 0 10px #fff,
      0 0 21px #fff,
      0 0 42px #0fa,
      0 0 82px #0fa,
      0 0 92px #0fa,
      0 0 102px #0fa,
      0 0 151px #0fa;
}
            
.glow {
  font-size: 18px;
  color: #fff;
  font-family:monospace;
  animation: glow 1s ease-in-out infinite alternate;
}

@-webkit-keyframes glow {
  from {
    text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #0fa, 0 0 40px #0fa, 0 0 50px #0fa, 0 0 60px #0fa, 0 0 70px #0fa;
  }
  
  to {
    text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6, 0 0 50px #ff4da6, 0 0 60px #ff4da6, 0 0 70px #ff4da6, 0 0 80px #ff4da6;
  }
}
            
</style>
""", unsafe_allow_html=True)

with st.chat_message(name='assistant', avatar='./resources/vv.png'):
    st.markdown('<p class="glow"> Speak you mind 🧠, Dear Friend 🤗!</p>',unsafe_allow_html=True)
    st.success('`Tip: Toggle listening 🎧 capability from 👈🏻 side bar, if you like to hear 👂 from Valluvar 😎`', icon="💡")

for message in st.session_state.messages:
    with st.chat_message(name=message["role"], avatar=getAvatar(message["role"])):
        st.markdown(decideGlow(message["content"], message["role"]), unsafe_allow_html=True)

if prompt := st.chat_input("Speak your mind... 🧠"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message(name='assistant', avatar='./resources/vv.png'):
        message_placeholder = st.empty()
        talk_placeholder = st.empty()
        full_response = ""
        with st.spinner(text="Thinking... 💭💭💭"):
          history = len(st.session_state.messages) - 1
          vv_response = fireGPTQuery(str(st.session_state.messages), "")
          if st.session_state.listenEnabled:
            saveAudioFromTxt(vv_response)

          # Simulate stream of response with milliseconds delay
          for chunk in vv_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(glow2(full_response + "▌"), unsafe_allow_html=True)
          message_placeholder.markdown(glow2(full_response), unsafe_allow_html=True)
          if st.session_state.listenEnabled:
            with talk_placeholder.expander(label="Hear 🎧 from Valluvar"):
                st.markdown(embedAudio(), unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
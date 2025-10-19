
# ------------

# 0.0 IMPORTS

# ------------

import streamlit as st
from langchain_groq                import ChatGroq
from langchain_core.prompts        import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv                        import load_dotenv
load_dotenv()

# ------------

# 1.0 LLM CONECTION

# ------------

id_model = "llama-3.3-70b-versatile" #@param {type: 'string'}
llm = ChatGroq(
    model=id_model,
    temperature=0.7,
    max_tokens = None,
    timeout = None,
    max_retries = 2
    )

# ------------

# 2.0 GENERATE FUNCTION

# ------------

def llm_generate(llm, prompt):
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing specialist with a focus on SEO and persuasive writing."),
        ("human", '{prompt}')
    ])

    chain = template | llm | StrOutputParser()

    res = chain.invoke({'prompt': prompt})
    return res

# ------------

# 3.0 STREAMLIT APPLICATION

# ------------

st.set_page_config(page_title = "CONTENT GENERATOR 🤖", page_icon ="🤖")
st.title("CONTENT GENERATOR - ESSENCIAL SAUDE CLINIC ❤️💊")

# ------------

# 4.0 FORM INPUTS

# ------------

topic = st.text_input("Theme:", placeholder="e.g. Mental Health, Healthy Food, Prevention of Diseases")
platform = st.selectbox("Platform:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tone:", ['Normal', 'Informative', 'Inspire', 'Urgent', 'Informal'])
length = st.selectbox("Length:", ['Short', 'Medium', 'Long'])
audience = st.selectbox("Audience:", ['General Public', 'Adults', 'Family', 'Old Public', 'Teenagers'])
cta = st.checkbox("Include Call to Action")
hashtag = st.checkbox("Return Hashtags")
keywords = st.text_area("Keywords SEO:", placeholder="e.g. mental health, well-being, stress management")

if st.button("Generate Post"):
    prompt = f"""
    Whrite a text with SEO optimization about the following theme: {topic}.
    Return in yours response only the final text, without any additional information.

    - Platform: {platform}
    - Tone: {tone}
    - Length: {length}
    - {'- Include Call to Action' if cta else 'Not Include Call to Action'}
    - {'- Include final Hashtags relevant to the topic' if hashtag else 'Not Include Hashtags'}
    - {'- Keywords to be included in the SEO text:' + keywords if keywords else ''}
    """
    try:
        res = llm_generate(llm, prompt)
        st.markdown(f"**Response:** {res}")
    except Exception as e:
        st.error(f'Error: {e}')
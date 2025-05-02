import streamlit as st
import pandas as pd
import google.generativeai as genai

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "info" not in st.session_state:
    st.session_state.info = {}
if "main_info" not in st.session_state:
    st.session_state.main_info = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Tab 1"
if "checkbox" not in st.session_state:
    st.session_state.checkbox = False
if "txt" not in st.session_state:
    st.session_state.txt = None
if "tab4text" not in st.session_state:
    st.session_state.tab4text = ""
if "tab5text" not in st.session_state:
    st.session_state.tab5text = ""
if "Tab4TextBoxView" not in st.session_state:
    st.session_state.Tab4TextBoxView = False
if "ChatBotCalled" not in st.session_state:
    st.session_state.ChatBotCalled = False
if "chatbotHistory" not in st.session_state:
    st.session_state.chatbotHistory = ""

st.sidebar.title("This is a simple app to demonstrate Streamlit features.")
st.sidebar.write("## DataFrame Example")
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)
st.sidebar.dataframe(df)
# Navigation function
def switch_tab(tab_name):
    st.session_state.active_tab = tab_name

# Step transition
def toggle_input():
    st.session_state.checkbox = not st.session_state.checkbox
def getToStep2(name, age):
    if name and age:
        st.session_state.info = {"name": name, "age": age}
        st.session_state.main_info.append(st.session_state.info)
        st.session_state.step = 2
        switch_tab("Tab 2")

def getToStep1():
    st.session_state.step = 1
    st.session_state.info = {}
    switch_tab("Tab 1")

def Tab4TextBoxView():
    st.session_state.Tab4TextBoxView = True


# def ChatBotHistoryShower():

def apiai(prompt):
    api_key = "AIzaSyBUOfYKrZWcjme8mDlcFU3GTgJt97Bl2os"
    genai.configure(api_key=api_key)
    model_name = "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)
    if prompt =="summarize data":
        prompt = "summarize the data in the file"+"'Name': ['Alice', 'Bob', 'Charlie'],'Age': [25, 30, 35],'City': ['New York', 'Los Angeles', 'Chicago']"
    try:
        response = model.generate_content(prompt)
        print(response.text)
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
# Simulated tabs with buttons or a selectbox
tab = st.selectbox("Choose Tab", ["Tab 1", "Tab 2", "Tab 3","Tab 4","Tab 5"], index=["Tab 1", "Tab 2", "Tab 3","Tab 4","Tab 5"].index(st.session_state.active_tab))
st.session_state.active_tab = tab

# TAB 1: Form Input
if st.session_state.active_tab == "Tab 1":
    st.markdown("## Step 1 - Enter Info")
    name = st.text_input("Enter your name", value=st.session_state.info.get("name", ""))
    age = st.text_input("Enter your age", value=st.session_state.info.get("age", ""))
    st.button("Next", on_click=getToStep2, args=(name, age))

# TAB 2: Display Info
elif st.session_state.active_tab == "Tab 2":
    with st.container(border=True):
        st.markdown("## Step 2 - Display Info")
        if st.session_state.main_info:
            st.write("Latest submission:")
            st.write(st.session_state.info)
            df = pd.DataFrame(st.session_state.main_info)
            st.data_editor(df)
            st.button("Reset Info", on_click=st.session_state.main_info.clear)
        else:
            st.warning("No data submitted yet.")
        st.button("Go back to Step 1", on_click=getToStep1)

# TAB 3: Extras
elif st.session_state.active_tab == "Tab 3":
    with st.container(border=True):
        st.markdown("## Extra UI - Tab 3")
        col1, col2 = st.columns(2)
        with col1:
            st.info("This is Column 1 content.")
            with st.expander("Expand to see more"):
                st.write("Here are some more details inside the expander.")
                code = """
                    def greet(name):
                         print(f"Hello, {name}!")
                """
                st.code(code, language='python')
        with col2:
            st.success("This is Column 2 content.")
        with st.expander("Expand to see more"):
            st.write("Here are some more details inside the expander.")
        min = st.slider("Select a minimum value", 0, 50,25)
        max = st.slider("Select a maximum value", min, 100, min)
        st.checkbox("Check me!", value=st.session_state.checkbox, on_change=toggle_input)
        if st.session_state.checkbox:
            txt = st.text_input("Enter your text here", value=st.session_state.txt)
            st.session_state.txt = txt
        else:
            st.session_state.txt = ""
        if st.session_state.checkbox and st.session_state.txt!=None:
            st.write("User: ",st.session_state.txt)

# TAB 4: File handing
elif st.session_state.active_tab == "Tab 4":
    st.markdown("## File Handling - Tab 4")
    with st.container(border=True):
        st.write("write the content of the file here")
        try:
            file = open("writeChecker.txt","a+")
        except Exception as e:
            file = open("writeChecker.txt","w+")
        input1 = st.text_input("Enter your text here", value="")
        col1,col2,col3 = st.columns(3)
        if st.session_state.Tab4TextBoxView == False:
            if input1==None or input1 == "":
                st.warning("Please enter some text.")
        with col1:
            if st.button("Write to file"):
                st.session_state.Tab4TextBoxView = False
                # if input1!=None or input1 != "":
                st.success("Text written to file successfully!")
                file.write(input1 + "\n")
                file.close()

        with col2:
            if st.button("Read from file",on_click=Tab4TextBoxView):
                file = open("writeChecker.txt","r")
                content = file.read()
                st.session_state.tab4text = content
                file.close()
                st.success("File read successfully!")
        with col3:
            if st.button("clear file"):
                st.session_state.Tab4TextBoxView = False
                file = open("writeChecker.txt","w")
                file.write("")
                file.close()
                st.success("File cleared successfully!")
        with st.expander("File Content here"):
            if st.session_state.Tab4TextBoxView:
                if st.session_state.tab4text == "":
                    st.text_area("File Content", st.session_state.tab4text, height=68)
                else:
                    st.text_area("File Content", st.session_state.tab4text, height=300)

if st.session_state.active_tab == "Tab 5":
    maincontent = ""
    st.markdown("## Tab 5 - Placeholder")
    st.write("This is a placeholder for future content.")
    st.button("Go back to Step 1", on_click=getToStep1)
    prompt = st.text_input("Enter your prompt here", value="")
    col = st.columns(2)
    with col[0]:
        if st.button("Submit") and prompt != "" and prompt != None:
            content  = apiai(prompt)
            maincontent = content
            st.session_state.ChatBotCalled = True
            try:
                file = open("AiResponse.txt","a+")
                file.write("[split]"+"USER: "+prompt+"[split]"+"AI: "+content+"[split]")
                file.close()
            except Exception as e:
                file = open("AiResponse.txt","w")
                file.write("\n\n"+"USER: "+prompt+"\n\n"+"AI: "+content)
                file.close()
        else:
            st.warning("Please enter a prompt.")
    if st.session_state.ChatBotCalled:
        st.chat_message("user").markdown(prompt)
        response = maincontent
        st.chat_message("assistant").markdown(response)

    # with col[0]:
    with col[1]:
        if st.button("History"):
            st.write("History of API calls:")
            try:
                file = open("AiResponse.txt","r")
                content = file.read()
                st.chat_message("assistant").markdown(content)
                file.close()
            except Exception as e:
                st.warning("No history available.")
    if st.button("clear history"):
        st.success("History cleared successfully!")
        file = open("AiResponse.txt","w")
        file.write("")
        file.close()
    with open("AiResponse.txt", "rb") as file:
        st.download_button(label="Download", data=file, file_name="AiResponse.txt", mime="text/plain")



        # Call your API function here with the prompt
        # apiai(prompt)  # Uncomment this line to call the API function

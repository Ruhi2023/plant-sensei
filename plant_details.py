import streamlit as st 
import os
import google.generativeai as genai
import json
import pandas as pd
single_p_pr = """give details in json format about the plant image below 
1. name of this plant scientific and common 
2.its growth requirements 
3. its uses (explain well) 
4.diseases pests and common preventive and remidial actions 
5. care methods
6. places it is commonly grown 
7. profitable places to grow it at"""
multiple_p_pr = """give details (separate by image name) in json format about each of the plant images below 
1. name of this plant scientific and common 
2.its growth requirements 
3. its uses (explain well) 
4.diseases pests and common preventive and remidial actions 
5. care methods
6. places it is commonly grown 
7. profitable places to grow it at
"""
# single_r_prompt = "Scan this reciept and give the name of the store, receipt date time, reciept number, order total, payment method and the list of products purchased, their barcode if available, quantity and price in json format"
# multiple_r_prompt = "Analyze the receipt images and provide a JSON list of receipts, each containing store name, receipt date/time, number, total, payment method, and a list of products with barcode (if available),product name, quantity, and price."
def upload_to_genai(path, mime_type):
   file = genai.upload_file(path, mime_type=mime_type)
   print(f"file has been uploaded to genai: {file.name}")
   return file
st.session_state["should_i_disable"] = True
def take_images(uplo):
  """
  Take images from file upload then makes a folder (if not aleredy present), uploads to gemini using upload to genai
  """
  par = os.getcwd()
  if not os.path.exists(os.path.join(par, "file upload")):
    os.mkdir(os.path.join(par, "file upload"))
  with open(os.path.join(par, "file upload", uplo.name), "wb") as file:
    file.write(uplo.getvalue())
  f_nam =upload_to_genai(os.path.join(par, "file upload",uplo.name), mime_type="image/png")
  return f_nam.name
def make_img_inp(names):
  """
  Makes a list of images from the uploaded files
  """
  lis =list(map(genai.get_file, names))
  return lis

def gen_exist(a_name_key):
   if a_name_key not in st.session_state:
      return False
   else:
      return st.session_state[a_name_key]


st.header("Plant Expert")

use_img = st.checkbox("Work with images")
if use_img:
    st.session_state.should_i_disable = not use_img

with st.form("Input Prompt"):
    gak = st.text_input(label="Enter your google API key",type="password")
    genai.configure(api_key=gak)
    pr = st.text_input("Something else you want to ask? (you can leave it blank)")


    if not gen_exist("should_i_disable"):
        uplad_files = st.file_uploader("Upload files", type=["png"], accept_multiple_files=True, disabled=st.session_state.should_i_disable) 
        names = list(map(take_images, uplad_files))
        #Done: make a function map that will use upload files and return a file object appended to list
    genb = st.form_submit_button("Generate Text")
if genb:
    if "gen" not in st.session_state:
      st.session_state.gen = True
    #st.write(genai.get_file(a[0]))
if gen_exist("gen"):
      generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": int(1024*8),
    "response_mime_type": "text/plain",  }
      model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config)
      if len(uplad_files)>1:
        model_input = [multiple_p_pr+pr]
      else:
        model_input = [single_p_pr+pr]
      if use_img:
        model_input.extend(make_img_inp(names))
        
        #Done: make a model input function that will make append a model input
      res = model.generate_content(model_input)
      try:
         jo = json.loads(res.text)
         st.json(jo)
         df = pd.read_json(jo)
      except:
        st.write(f"{res.text}")
      if "should_i_disable" not in st.session_state:  
        st.session_state["should_i_disable"] = True
      else:
       st.session_state["should_i_disable"] = True



delb = st.button("Delete cached files",key = "Del_tru")
if delb:
    if "chk_del" not in st.session_state:
        st.session_state.chk_del = True
    else:
        st.session_state.chk_del = True 
    


if gen_exist("chk_del"):  
  st.write("""Files in cache being deleted.....
            These are the files both in ***previous session(s) and current session***""")
  if genai.list_files() is not None:
      for f in genai.list_files():
        st.write(f"Deleting {f}")
        genai.delete_file(f)
  st.write("Done deleting from cloud")
  par = os.getcwd()
  path_files = os.listdir(os.path.join(par, "file upload"))
  if len(path_files) != 0:
      for f in path_files:
        try:
          os.remove(os.path.join(par, "file upload",f))
        except:
            st.write(f"Could not delete {f}") 
  st.write("Done deleting from local")

if gen_exist("gen"):
  del st.session_state.gen 
if gen_exist("chk_del"):
  del st.session_state.chk_del


import streamlit as st 
import os
import google.generativeai as genai
import json
import pandas as pd


no_img_pr ="""
give details in json format about the plant disease named above 
1. name of the plants scientific and common which this disease effects
2. its accumulation causes 
3. its recovery stages (explain well with time) 
4. preventive and remidial actions 
5. care methods 
6. places it is commonly found in and symptoms 
7. some diseases are profitable is this one of them?
8. Is full recovery possible if possible how difficult, if not till which stage can the plant recover
9. Is it contagious, cronic, or seasonal"""
single_p_pr = """give details in json format about the plant image below 
1. name of this plant scientific and common, which disease effects it?
2. its accumulation causes 
3. its recovery stages (explain well with time) 
4. preventive and remidial actions 
5. care methods 
6. places it is commonly found in and symptoms 
7. some diseases are profitable is this one of them?
8. Is full recovery possible if possible how difficult, if not till which stage can the plant recover
9. Is it contagious, cronic, or seasonal and natural"""
multiple_p_pr = """give details (separate by image name) in json format about each of the plant images below 
1. name of this plant scientific and common, which disease effects it?
2. its accumulation causes 
3. its recovery stages (explain well with time) 
4. preventive and remidial actions 
5. care methods 
6. places it is commonly found in and symptoms 
7. some diseases are profitable is this one of them?
8. Is full recovery possible if possible how difficult, if not till which stage can the plant recover
9. Is it contagious, cronic, or seasonal and natural
"""
def gen_exist(a_name_key):
   if a_name_key not in st.session_state:
      return False
   else:
      return st.session_state[a_name_key]
def upload_to_genai(path, mime_type):
   file = genai.upload_file(path, mime_type=mime_type)
   print(f"file has been uploaded to genai: {file.name}")
   return file
def take_images(uplo):
  """
  Take images from file upload then makes a folder (if not aleredy present), 
  uploads to gemini using upload to genai
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


st.header("Plant Disease Identification")
st.subheader("Use Image of a diseased plant or name of the disease to learn about. ")
st.write("Can be used to check for disease as well")

use_img = st.toggle("I have the image of plant", value=False)
if (use_img and not(gen_exist("generate_dis"))):
   print("true after toggle -need upload")
   st.session_state["need_upload_dis"] = True
with st.form("GAk and Inp"):
  gak = st.text_input("Enter your gemini api key", type="password")
  if gak !="" or gak is not None:
        genai.configure(api_key=gak)
  if use_img:
    pr = st.text_input("Do you want to ask something else?")
    hdd= not(st.session_state.need_upload_dis) 
    has_dis = st.checkbox("I am not sure if the plant has disease")
    print(hdd)
    uplo = st.file_uploader("Upload an image", type=["png"], disabled= hdd, accept_multiple_files=True)
    names = list(map(take_images, uplo))
  else:
    inp = st.text_input("Enter the name of the plant disease")
    pr = st.text_input("Do you want to ask something else?")
  generate = st.form_submit_button("Get Details")
# code snippt of generation
if gak =="":
        st.write("Please provide your google API key to get details")
if generate:
  print("true after click get details -generate")
  st.session_state.generate_dis = True

if gen_exist("generate_dis") and gak != "":
    # take model input
    if use_img:
      
        if len(uplo)==1:
            model_input = make_img_inp(names)
            model_input.extend([single_p_pr + ". "+ pr])
        else:
            model_input =make_img_inp(names)
            model_input.extend([multiple_p_pr + ". "+ pr])
        if has_dis:
          model_input.extend(["I am not sure if the plant has disease if it has disease give me the above setails about disease, if it doesn't tell me some care methods specifying no disease in json format"])
    else:
        model_input = inp + no_img_pr + ". "+ pr
    
    # configure and generate
    if gak =="":
        st.write("Please provide your google API key ")
    else:
        genai.configure(api_key=gak)
        generation_config = {
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 20,
        "max_output_tokens": int(1024*8),
        "response_mime_type": "text/plain",  }
        model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config)
        res = model.generate_content(model_input)
        try:
            jo = json.loads(res.text)
            st.json(jo)
            df = pd.read_json(jo)
        except:
            st.write(f"{res.text}")
    
    if st.button("Generate another"):
       print("False after generate another -need uplaoad")
       del st.session_state["generate_dis"]
       st.session_state.need_upload_dis = False
       del uplo
       del names
       st.rerun()


# delete cache
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
if gen_exist("chk_del"):
  print("del after all -chk_del")
  del st.session_state.chk_del
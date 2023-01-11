import pandas as pd
import xlrd,openpyxl
from pandasql import sqldf
import streamlit as st
import os

test_file = st.file_uploader("Select File", type=None, accept_multiple_files=False, key=None, help=None, label_visibility="visible")
st.write(test_file)
getFileType = ""
def file_selector(folder_path='./sample-files'):
    FileType = ['Text','CSV','Excel']
    DeMil = ['Tab','Comma','Pipe']
    selecttype = st.sidebar.selectbox('Select a File Type', FileType)
    if selecttype == 'Text':
        demili = st.sidebar.selectbox('Select a File Delimiter If Text or CSV', DeMil)
    elif selecttype == 'CSV':
        demili = 'Comma'
    else:
        demili = 'Excel'
        
    getFileType = selecttype
    print('FilePath'+getFileType)
    filenames = []
    file_type = {
        'Text': ['.txt','.txt'],
        'CSV' : ['.csv','.csv'],
        'Excel' : ['xls','xlsx']
        }
    filename = os.listdir(folder_path)
    for x in filename:
        if x.endswith(file_type[selecttype][0]) or x.endswith(file_type[selecttype][1]):
            filenames.append(x)
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    
    return os.path.join(folder_path, selected_filename),selecttype,demili

filename,getFileType,dl = file_selector()
st.write('You selected `%s`' % filename)

#select delimiter
delimiter = {
    'Tab': '\t',
    'Comma': ',',
    'Pipe' : '|'
    }
filePath = filename
def readxl(path,sheetnum):
    try:
        data = pd.read_excel(path,engine='openpyxl',sheet_name = sheetnum, index_col=0)
        return data
    except:
        data = pd.read_excel(path,sheet_name = 0, index_col=0)
        return data

def readcsv(path,dlimit):
    data = pd.read_csv(path,sep=dlimit)
    return data


if getFileType == 'Text':
    dataset = readcsv(filePath,delimiter[dl])
elif getFileType == 'CSV':
    dataset = readcsv(filePath,delimiter['Comma'])
else:
    dataset = readxl(filePath,0)


st.title('Data Query Visualizer')
default = 'SELECT * FROM dataset'
query = st.text_area("Enter Your SQL Query", default)
output = sqldf(query)
print(output)
st.write(output)

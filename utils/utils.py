import streamlit as st
import pandas as pd

def get_excel_sheet_names(file):
    xls = pd.ExcelFile(file)  # Open the Excel file
    sheet_names = xls.sheet_names
    return sheet_names
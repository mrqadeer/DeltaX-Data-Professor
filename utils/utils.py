import streamlit as st
import pandas as pd
from typing import List
def get_excel_sheet_names(file)-> List[str]:
    """
    Opens an Excel file and returns a list of its sheet names.

    Parameters
    ----------
    file : str
        The path to the Excel file.

    Returns
    -------
    list of str
        A list of sheet names in the file.
    """
    xls = pd.ExcelFile(file)  # Open the Excel file
    sheet_names = xls.sheet_names
    return sheet_names
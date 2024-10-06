# src/handlers/file_handlers.py
import streamlit as st
import pandas as pd
from abc import ABC, abstractmethod
from typing import Any,List,Union

class BaseFileHandler(ABC):
    """Base class for handling different file types."""

    def __init__(self, files) -> None:
        self.files = files

    @abstractmethod
    def read(self) -> pd.DataFrame:
        """Read the file and return a DataFrame."""
        pass
class CSVFileHandler(BaseFileHandler):
    """Class for handling CSV files."""

    def read(self) -> List[pd.DataFrame]:
        """Read the CSV file(s) and return a list of DataFrames."""
        all_dfs = []
        for file in self.files:
            if file is None or file.size == 0:
                st.warning(f"File {file.name} is empty. Skipping.")
                continue
            try:
                df = pd.read_csv(file)
                all_dfs.append(df)
                st.session_state['data_frames'] = all_dfs  # Store DataFrames in session state
            except ValueError as e:
                st.error(f"Error reading CSV file '{file.name}': {e}")
            except Exception as e:
                st.error(f"Unexpected error reading file '{file.name}': {e}")
        return all_dfs

class TSVFileHandler(BaseFileHandler):
    """Class for handling TSV files."""

    def read(self) -> List[pd.DataFrame]:
        """Read the CSV file(s) and return a list of DataFrames."""
        all_dfs = []
        for file in self.files:
            if file is None or file.size == 0:
                st.warning(f"File {file.name} is empty. Skipping.")
                continue
            try:
                df = pd.read_csv(file, sep='\t')
                all_dfs.append(df)
                st.session_state['data_frames'] = all_dfs # Store DataFrames in session state
            except ValueError as e:
                st.error(f"Error reading CSV file '{file.name}': {e}")
            except Exception as e:
                st.error(f"Unexpected error reading file '{file.name}': {e}")
        return all_dfs

class ExcelFileHandler(BaseFileHandler):
    """Class for handling Excel files."""

    def read(self) -> List[pd.DataFrame]:
        """Read selected sheets from the Excel file and return a list of DataFrames."""
        all_dfs = []
        file = self.files[0]

        if file is None or file.size == 0:
            st.warning(f"File {file.name} is empty. Skipping.")
            return all_dfs  # Return empty if no valid file

        try:
            # Open the Excel file
            xls = pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            # Get selected sheets from session state or default to all sheets
            selected_sheets = st.session_state.get('selected_sheets', [])

            # Check if sheets have been selected
            if not selected_sheets:
                selected_sheets = st.multiselect("Select Sheets to Read", sheet_names, default=sheet_names)
                st.session_state['selected_sheets'] = selected_sheets  # Store the selected sheets in session state

            st.write(f"Selected Sheets: {selected_sheets}")

            # Read the selected sheets and append to all_dfs
            for sheet_name in selected_sheets:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                all_dfs.append(df)

            # Store the DataFrames in session state
            st.session_state['data_frames'] = all_dfs

        except Exception as e:
            st.error(f"Error reading Excel file '{file.name}': {e}")
        
        return all_dfs

def handle_uploaded_files(uploaded_files: Union[List[Any], Any]) -> List[pd.DataFrame]:
    """
    Process the uploaded files and return a list of DataFrames.
    
    Handles both single and multiple file uploads, determining file type
    and passing each file to the appropriate handler.

    Parameters:
        uploaded_files (Union[List[Any], Any]): List of uploaded files or a single file object.

    Returns:
        List[pd.DataFrame]: A list of DataFrames generated from the uploaded files.
    """
    dfs = []

    try:
        # If multiple files are uploaded
        if isinstance(uploaded_files, list):
            for file in uploaded_files:
                st.write(f"Uploaded file: {file.name}")
                # Process each file based on its type
                dfs.extend(handle_file(file))
        
        # If a single file is uploaded
        elif uploaded_files is not None:
            # Process the single file
            dfs = handle_file(uploaded_files)
    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
    
    return dfs


def handle_file(file: Any) -> List[pd.DataFrame]:
    """
    Handle an individual file by determining its type and reading it using the appropriate handler.

    Parameters:
        file (Any): A single file object to be processed.

    Returns:
        List[pd.DataFrame]: A list of DataFrames containing the file data.
    """
    try:
        # Handle CSV file
        if file.name.endswith('.csv'):
            handler = CSVFileHandler([file])
            dfs = handler.read()

        # Handle TSV file
        elif file.name.endswith('.tsv'):
            handler = TSVFileHandler([file])
            dfs = handler.read()

        # Handle Excel file (XLSX)
        elif file.name.endswith(('.xlsx', '.xls')):
            handler = ExcelFileHandler([file])
            dfs = handler.read()

        else:
            st.error("Unsupported file type. Please upload a CSV, TSV, or XLSX file.")
            dfs = []

    except ValueError as ve:
        st.error(f"Error processing file '{file.name}': {ve}")
        dfs = []
    
    return dfs
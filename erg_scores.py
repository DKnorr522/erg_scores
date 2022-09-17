import streamlit as st
import openpyxl
import os
import re
from rowing_functions import *


def main():
    # code_to_use = st.secrets["code_word"]  # Defined with streamlit

    st.set_page_config(page_title="Erg Scores",
                       layout="wide")

    # code = st.sidebar.text_input(
    #     "Enter code:"
    # )

    code_to_use = "code"
    code = code_to_use

    # Only move on if the correct code has been entered
    if code == code_to_use:

        # Get all the files in the "pieces" folder. Should only be Excel files, but it doesn't actually matter
        files = os.listdir("pieces")

        # Regular expression patterns for the files and to pull out the distances
        dist_pattern = r"\d+"
        file_pattern = rf"{dist_pattern}m Tests.xlsx"

        # List comprehension to get all Excel files with proper titles
        distances = [re.match(dist_pattern, file).group() for file in files if re.fullmatch(file_pattern, file)]
        distances.sort()

        with st.expander("", expanded=True):
            col_dist, col_piece = st.columns(2)

            with col_dist:  # Choose the distance of the piece
                distance = st.selectbox(
                    "Choose a distance:",
                    options=distances
                )
            distance = int(distance)  # selectbox returns a string, so need to typecast

            with col_piece:  # Open the Excel file then choose the piece
                wb = openpyxl.load_workbook(f"pieces/{distance}m Tests.xlsx")
                piece = st.selectbox(
                    "Choose a piece:",
                    options=wb.sheetnames
                )

        sheet = wb[piece]
        scores_weight_yes = scores_to_dict(sheet, weight_adj=True)
        scores_weight_no = scores_to_dict(sheet, weight_adj=False)

        # Get names for the plot. Plot can show up to 6 people
        st.header("Please select rowers (no more than 6): ")

        rowers = st.multiselect(
            "Select the rowers:",
            options=scores_weight_yes.keys()
        )

        col_weight, col_splits = st.columns(2)

        with col_weight:
            weight_adjust = st.checkbox(
                "Weight Adjust",
                value=False
            )
        with col_splits:
            show_splits = st.checkbox(
                "Show Splits",
                value=True
            )

        scores = scores_weight_yes if weight_adjust else scores_weight_no  # select the relevant dictionary
        fig = plot_splits(rowers, scores, dist=distance, weight_adjusted=weight_adjust, show_splits=show_splits)

        if fig:  # Without this a blank plot is shown until a name is selected
            st.pyplot(fig)


if __name__ == '__main__':
    main()


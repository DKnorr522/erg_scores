import streamlit as st
import openpyxl
import os
import re
from rowing import *


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
        pattern = rf"{dist_pattern}m Tests.xlsx"

        # List comprehension to get all Excel files with proper titles
        distances = [re.match(dist_pattern, file).group() for file in files if re.fullmatch(pattern, file)]
        distances.sort()

        # Choose the distance of the piece
        distance = st.selectbox(
            "Choose a distance:",
            options=distances
        )
        distance = int(distance)  # selectbox returns a string, so need to typecast

        # Open the Excel file then choose the piece
        wb = openpyxl.load_workbook(f"pieces/{distance}m Tests.xlsx")
        piece = st.selectbox(
            "Choose a piece:",
            options=wb.sheetnames
        )

        sheet = wb[piece]
        scores_weight_yes = scores_to_dict(sheet, True)
        scores_weight_no = scores_to_dict(sheet, False)

        # Get names for the plot. Plot can show up to 6 people
        st.header("Please select rowers (no more than 6): ")

        rowers = st.multiselect(
            "Select the rowers:",
            options=scores_weight_yes.keys()
        )

        col1, col2 = st.columns(2)

        with col1:
            weight_adjust = st.checkbox(
                "Weight Adjust",
                value=False
            )
        with col2:
            show_splits = st.checkbox(
                "Show Splits",
                value=True
            )

        scores = scores_weight_yes if weight_adjust else scores_weight_no  # select the relevant dictionary
        fig = plot_splits(rowers, scores, dist=distance, weightAdjusted=weight_adjust, showSplits=show_splits)

        st.write(len(fig))

        if fig:  # Without this a blank plot is shown until a name is selected
            st.pyplot(fig)
            # st.download_button("Save plot", fig, file_name=saveName)


if __name__ == '__main__':
    main()

import streamlit as st
import openpyxl
import os
import re
from rowing import *


def main():
    # Defined with streamlit
    code_to_use = st.secrets["code_word"]

    st.set_page_config(page_title="Erg Scores",
                       layout="wide")

    code = st.sidebar.text_input(
        "Enter code:"
    )

    # Only move on and show names if the correct code has been entered
    if code == code_to_use:

        files = os.listdir("pieces")

        distances = []

        # Regular expression patterns for the files and to pull out the distances
        pattern = r"\d+m Tests.xlsx"
        dist_pattern = r"\d+"

        # for file in files:
        #     # Only cares about Excel files that are properly named
        #     if re.fullmatch(pattern, file):
        #         dist = re.match(dist_pattern, file).group()
        #         distances.append(dist)

        distances = [re.match(dist_pattern, file).group() for file in files if re.fullmatch(pattern, file)]
        distances.sort()

        distance = st.sidebar.selectbox(
            "Choose a distance:",
            options=distances
        )
        distance = int(distance)

        wb = openpyxl.load_workbook(f"pieces/{distance}m Tests.xlsx")
        piece = st.sidebar.selectbox(
            "Choose a piece:",
            options=wb.sheetnames
        )

        sheet = wb[piece]
        scores_weight_yes = scores_to_dict(sheet, True)
        scores_weight_no = scores_to_dict(sheet, False)

        st.sidebar.header("Please select rowers (no more than 6): ")

        # Allow multiple rowers to be selected
        rowers = st.sidebar.multiselect(
            "Select the rowers:",
            options=scores_weight_yes.keys()
        )
        weight_adjust = st.sidebar.checkbox(
            "Weight Adjust",
            value=False
        )
        show_splits = st.sidebar.checkbox(
            "Show Splits",
            value=True
        )

        scores = scores_weight_yes if weight_adjust else scores_weight_no  # select the relevant dictionary
        fig = plot_splits(rowers, scores, dist=distance, weightAdjusted=weight_adjust, showSplits=show_splits)
        if fig:
            st.pyplot(fig)


if __name__ == '__main__':
    main()

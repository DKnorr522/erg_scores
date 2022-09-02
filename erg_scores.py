import streamlit as st
import openpyxl
import os
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
        pieces = os.listdir("pieces")

        piece = st.sidebar.selectbox(
            "Choose a piece:",
            options=pieces
        )

        if piece:
            wb = openpyxl.load_workbook(f"pieces/{piece}")
            sheet = wb[wb.sheetnames[0]]
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
            distance = wb[wb.sheetnames[1]].cell(row=1, column=1).value  # piece's distance is stored on sheet 2 cell A1
            fig = plot_splits(rowers, scores, dist=distance, weightAdjusted=weight_adjust, showSplits=show_splits)
            if fig:
                st.pyplot(fig)


if __name__ == '__main__':
    main()

import streamlit as st
import openpyxl
import os
from rowing import *


# Turns a yes/no string into a bool
# Does not check for proper input
def yn2bool(option):
    return True if option == "Yes" else False


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
        st.set_page_config(page_title=f"piece",
                           layout="wide")
        # wb = openpyxl.load_workbook(f"pieces/{piece}")

        if piece:
            # wb = openpyxl.load_workbook("pieces/2022-07-17 Henley Erg Test.xlsx")
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
            # Yes or no on whether to weight adjust
            weight = st.sidebar.selectbox(
                "Weight Adjust?",
                options=["No", "Yes"]
            )
            # Yes or no on whether to show splits or just average split
            splits = st.sidebar.selectbox(
                "Show Splits?",
                options=["Yes", "No"]
            )

            weight_adjust = yn2bool(weight)  # turn Yes/No menu option into bool
            show_splits = yn2bool(splits)
            scores = scores_weight_yes if weight_adjust else scores_weight_no  # select the relevant dictionary
            distance = wb[wb.sheetnames[1]].cell(row=1, column=1).value  # piece's distance is stored on sheet 2 cell A1
            fig = plot_splits(rowers, scores, dist=distance, weightAdjusted=weight_adjust, showSplits=show_splits)
            if fig:
                st.pyplot(fig)


if __name__ == '__main__':
    main()

import pandas as pd
import streamlit as st
import openpyxl
import matplotlib.pyplot as plt
from math import floor, ceil
from rowing import *


if __name__ == '__main__':

    code_to_use = st.secrets["code_word"]

    st.set_page_config(page_title="Erg Scores",
                       layout="wide")

    code = st.sidebar.text_input(
        "Enter code:"
    )

    if code == code_to_use:
        wb = openpyxl.load_workbook("2022-07-17 Henley Erg Test.xlsx")
        sheet = wb[wb.sheetnames[0]]
        scores_weight_yes = scores_to_dict(sheet, True)
        scores_weight_no = scores_to_dict(sheet, False)
        
        st.sidebar.header("Please select rowers (no more than 6): ")
        
        rowers = st.sidebar.multiselect(
            "Select the rowers:",
            options=scores_weight_yes.keys()
#             options=scores_pd["Name"]
        )
        weight = st.sidebar.selectbox(
            "Weight Adjust?",
            options=["No", "Yes"]
        )

        weight_adjust = False if weight == "No" else True
        scores = scores_weight_yes if weight_adjust else scores_weight_no
        distance = wb[wb.sheetnames[1]].cell(row=1, column=1).value
        fig = plot_splits(rowers, scores, dist=distance, weightAdjusted=weight_adjust)
        if fig:
            st.pyplot(fig)

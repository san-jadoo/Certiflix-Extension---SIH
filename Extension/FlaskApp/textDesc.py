import pandas as pd
from fuzzywuzzy import fuzz
def desc_match(desc,pname):
    df = pd.read_excel('Description.xlsx')
    df_cleaned = df.dropna(how='all')
    if pname in df_cleaned.iloc[:, 0]:
        similarity_ratio = fuzz.ratio(desc.lower(),df_cleaned.iloc[:,1].lower())
    return similarity_ratio
def imgtxt_match(desc,imgtxt):
    print("Image")
    print(desc)
    print(imgtxt)
    return fuzz.ratio(desc.lower(),imgtxt.lower())

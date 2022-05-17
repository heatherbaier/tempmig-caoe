import pandas as pd

# Mexico 2000 data
df2000 = pd.read_stata("./data/mx2000a_migration.dta", convert_categoricals = False)
df2000["serial"] = df2000["serial"].astype(int)
sps2000 = pd.read_spss("./data/mx2000a_migration.sav")#[[]]
df2000 = pd.concat([df2000, sps2000], axis=1)
df2000 = df2000[df2000["COUNTRYM"] == "United States of America"]
df2000 = df2000[df2000["MONTHM"] != "Unknown"]
df2000 = df2000.drop(["hhwtm", "SERIAL", "HHWTM", "SAMPLE", "seqm", "sexm", "agem", "SEQM", "COUNTRYM", "COUNTRYR", "MONTHRET", "YEARRET", "countryr", "monthret", "yearret", "countrym"], axis = 1)
print(df2000.shape)

# Mexico 2010 data
df2010 = pd.read_stata("./data/mx2010a_migration.dta", convert_categoricals = False)
df2010["serial"] = df2010["serial"].astype(int)
sps2010 = pd.read_spss("./data/mx2010a_migration.sav")#[[]]
df2010 = pd.concat([df2010, sps2010], axis=1)
df2010 = df2010[df2010["COUNTRYM"] == "United States of America"]
df2010 = df2010[df2010["MONTHM"] != "Unknown"]
df2010 = df2010.drop(["wtmig", 'RESIDM', 'MIGID', 'WTMIG', "SERIAL", "migid", "seqm", "SAMPLE", 'sizeplm', 'residm', 'longfm', 'hdim', "psum", "sexm", "agem", "SEQM", "COUNTRYM", "COUNTRYR", "MONTHRET", "YEARRET", "countryr", "monthret", "yearret", "countrym", "stratam", "STRATAM", "PSUM", "SIZEPLM", "LONGFM", "HDIM"], axis = 1)
df2010 = df2010[[i for i in df2000.columns]]
print(df2010.shape)

# Combine 2000 and 2010
df = df2000.append(df2010)

# Group by count of migrants per municipality, month and year
grouped = pd.DataFrame(df.groupby(["sample", "serial"])["monthm", "yearm"].count()).reset_index()
grouped.head()

# Read in person level data and get ADM2 column
pers_data = pd.read_csv("../../heather_data/temporal_mex/ipumsi_00009.csv")
subset_pers = pers_data[pers_data['SERIAL'].isin(grouped["serial"])][["SAMPLE", "SERIAL", "GEO2_MX2000", "GEO2_MX2010"]].fillna(0)
subset_pers["munim"] = subset_pers["GEO2_MX2000"] + subset_pers["GEO2_MX2010"]
subset_pers = subset_pers.drop(["GEO2_MX2000", "GEO2_MX2010"], axis = 1)
subset_pers.columns = subset_pers.columns.str.lower()
subset_pers

# Merge
merged = pd.merge(df, subset_pers, on = ["sample", "serial"])
merged = pd.DataFrame(merged.groupby(['munim', 'yearm', 'monthm'])['serial'].count()).reset_index()
merged = merged[merged["yearm"] != 9999]
merged.head()

# Save
merged.to_csv("./data/migrants_per_month_year.csv", index = False)
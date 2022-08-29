import pandas as pd

happy_df = pd.read_csv("data/dis_happy.csv")

stat_colours = {
    "grp1": "#d10373",
    "grp2": "#9eab05",
    "mean": "#f49103",
    "median": "#006338",
    "std": "#0085a1",
    "quartile": "#c70540"
}


def get_df(value):
    df = happy_df[["Total happiness", value]].dropna().reset_index(drop=True)
    categories = df[value].unique()
    df1 = df["Total happiness"][(df[value] == categories[0])]
    df2 = df["Total happiness"][(df[value] == categories[1])]
    return categories, df1, df2


def get_stats(df):
    n = df.size
    mean = round(df.mean(), 3)
    std = round(df.std(), 3)
    q1 = df.quantile(0.25)
    median = df.median()
    q3 = df.quantile(0.75)
    iqr = q3 - q1
    return n, mean, std, q1, median, q3, iqr


# categories, hist_df1, hist_df2 = get_df("Sex")
# def hist_hovertext(df):
#     counts = df.value_counts()
#     print(f"Counts: {counts}")
#     total = counts.sum()
#     print(f"Total: {total}")
#     df_sorted = counts.sort_index()
#     print(f"Sorted: {df_sorted}")
#     proportions = []
#     for value in df_sorted.values:
#         proportions.append(round((value/total)*100, 2))
#     print(proportions)
#     return proportions

# hist_hovertext(hist_df1)
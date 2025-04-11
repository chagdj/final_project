import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="GitHunt Sourcing App", layout="wide")

# 🔍 Style bleu + compact + texte Not available + message d'erreur bleu clair
st.markdown("""
<style>
.compact-table table {
    font-size: 13px;
    width: 100%;
}
.compact-table td, .compact-table th {
    padding: 6px 10px;
    text-align: center !important;
}
.compact-table thead th {
    color: #007BFF;
    text-transform: capitalize;
}
.stMultiSelect [data-baseweb="tag"] {
    background-color: #007BFF !important;
    color: white !important;
}
.stMultiSelect [data-baseweb="tag"] span[role="button"] {
    color: white !important;
}
[data-baseweb="radio"] svg,
[data-baseweb="radio"] svg path,
[data-baseweb="checkbox"] svg {
    color: #007BFF !important;
    fill: #007BFF !important;
}
.custom-warning {
    background-color: #eaf4ff;
    color: #007BFF;
    padding: 1rem;
    border-radius: 8px;
    font-size: 15px;
}
img.avatar {
    vertical-align: middle;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    margin-right: 5px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("df_merged.csv")
    df["repo_month_count"] = df["repo_activity_by_month"].fillna("").apply(lambda x: len(x.split(",")))
    df["Position Reliability"] = df["position_from_bio"].apply(lambda x: "High" if pd.notna(x) and str(x).strip() != "" else "Low")
    if "raw_score" not in df.columns:
        df["raw_score"] = 0
    return df

df = load_data()

st.title("🔍 GitHunt – Tech Talent Sourcing on GitHub")

# Filters
st.sidebar.header("📊 Filters")
cities = st.sidebar.multiselect("Select City", df["city"].dropna().unique())
position_col = "position_final" if "position_final" in df.columns else "position_from_bio"
positions = st.sidebar.multiselect("Select Position", df[position_col].dropna().unique(), default=df[position_col].dropna().unique())

all_techs = set()
df["top_languages"].dropna().apply(lambda x: all_techs.update([t.strip() for t in str(x).split(",")]))
selected_tech = st.sidebar.multiselect("Select Technologies", sorted(all_techs))

st.sidebar.markdown('<p style="color:#007BFF; font-weight:600;">Position Reliability</p>', unsafe_allow_html=True)
reliability_levels = st.sidebar.multiselect("Select Reliability", df["Position Reliability"].dropna().unique(), default=df["Position Reliability"].dropna().unique())

st.sidebar.markdown('<p style="color:#007BFF; font-weight:600;">Sort by Matching Score</p>', unsafe_allow_html=True)
score_order = st.sidebar.radio("Sort Order", ["Highest to Lowest", "Lowest to Highest"], index=0)

st.sidebar.markdown('<p style="color:#007BFF; font-weight:600;">Include Only Profiles With Email?</p>', unsafe_allow_html=True)
with_email = st.sidebar.checkbox("Yes", value=False)

# Apply filters
filtered = df.copy()
if cities:
    filtered = filtered[filtered["city"].isin(cities)]
if not positions:
    positions = df[position_col].dropna().unique()
if not reliability_levels:
    reliability_levels = df["Position Reliability"].dropna().unique()
filtered = filtered[filtered[position_col].isin(positions) & filtered["Position Reliability"].isin(reliability_levels)]

if selected_tech:
    filtered = filtered[filtered["top_languages"].apply(lambda x: any(t in str(x) for t in selected_tech))]

if with_email and "email" in filtered.columns:
    filtered = filtered[filtered["email"].notna() & (filtered["email"] != "")]

ascending = score_order == "Lowest to Highest"
if not filtered.empty and "raw_score" in filtered.columns:
    filtered = filtered.sort_values(by="raw_score", ascending=ascending)

# Display Table

def format_na(val):
    return '<span style="color:#999;font-style:italic;">Not available</span>' if pd.isna(val) or val in ["", "N/A"] else val

def make_link(url, label):
    if pd.isna(url) or url == "":
        return format_na(None)
    return f'<a href="{url}" target="_blank">{label}</a>'

if filtered.empty:
    st.markdown('<div class="custom-warning">🔍 No matching profiles found for the selected filters. Try adjusting your filters.</div>', unsafe_allow_html=True)
else:
    table_display = filtered.copy()
    table_display = table_display.rename(columns={
        "name": "Name",
        position_col: "Position",
        "city": "City",
        "top_languages": "Technologies",
        "bio": "Bio"
    })

    table_display["GitHub"] = table_display.apply(lambda row: f'<img src="{row.get("avatar_url", "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")}" class="avatar"> <a href="{row["profile_url"]}" target="_blank">{row["username"]}</a>' if pd.notna(row.get("username")) else format_na(None), axis=1)
    if "email" in table_display.columns:
        table_display["Email"] = table_display["email"].apply(lambda x: f'<a href="mailto:{x}">{x}</a>' if pd.notna(x) and x != "" else format_na(None))
    table_display["LinkedIn"] = table_display["linkedin_search"].apply(lambda x: make_link(x, "LinkedIn"))
    table_display["Twitter"] = table_display["twitter"].apply(lambda x: make_link(x, "Twitter"))
    table_display["Website"] = table_display["blog_or_website"].apply(lambda x: make_link(x, "Website"))

    for col in ["Name", "Position", "City", "Technologies", "Bio"]:
        table_display[col] = table_display[col].apply(format_na)

    st.subheader(f"🎯 Number of Profiles Found: {len(table_display)}")
    st.markdown('<div class="compact-table">' +
        table_display[["GitHub", "City", "Name", "Position", "Position Reliability", "Technologies", "LinkedIn", "Twitter", "Email", "Bio"]]
        .to_html(escape=False, index=False) + '</div>', unsafe_allow_html=True)

    st.subheader("👤 Explore a GitHub User")
    usernames = filtered["username"].unique()

    if len(usernames) == 0:
        st.markdown('<div class="custom-warning">🔍 No matching profiles found for your selected filters. Please adjust the filters and try again.</div>', unsafe_allow_html=True)
    else:
        selected_user = st.selectbox("Choose a username:", usernames)
        user_row = filtered[filtered["username"] == selected_user].iloc[0]

        email_value = user_row['email'] if "email" in user_row else ""
        email_display = f"[{email_value}](mailto:{email_value})" if pd.notna(email_value) and email_value else "*Not available*"

        match_score = user_row.get("raw_score", "Not available")

        st.markdown(f"""
        - **City**: {user_row.get('city', 'Not available')}  
        - **Position**: {user_row.get(position_col, 'Not available')}  
        - **Position Reliability**: {user_row.get('Position Reliability', 'Not available')}  
        - **Technologies**: {user_row.get('top_languages', 'Not available')}  
        - **GitHub**: <a href="{user_row['profile_url']}" target="_blank">{user_row['username']}</a>  
        - **LinkedIn**: {make_link(user_row['linkedin_search'], user_row['linkedin_search'])}  
        - **Twitter**: {make_link(user_row['twitter'], user_row['twitter'])}  
        - **Website**: {make_link(user_row['blog_or_website'], user_row['blog_or_website'])}  
        - **Email**: {email_display}  
        - **Matching Score**: {match_score}  
          → This score is based on repository count, stars, recent activity, and tech match to help recruiters find top talent.
        """, unsafe_allow_html=True)

        st.write("**Bio:**", user_row.get("bio", "Not available"))

        def extract_repo_counts(repo_str):
            monthly_counts = {}
            if isinstance(repo_str, str):
                entries = repo_str.split(",")
                for entry in entries:
                    if ":" in entry:
                        month, count = entry.strip().split(":")
                        monthly_counts[month.strip()] = int(count.strip())
            return monthly_counts

        repo_counts = extract_repo_counts(user_row.get("repo_activity_by_month", ""))

        if repo_counts:
            df_counts = pd.Series(repo_counts)
            df_counts.index = pd.to_datetime(df_counts.index, errors="coerce")
            df_counts = df_counts.dropna()
            df_counts = df_counts.sort_index()

            if not df_counts.empty:
                st.subheader("📈 Monthly Repo Activity for Selected User")
                st.line_chart(df_counts)
        else:
            st.info("This user has no repo activity data available for plotting.")

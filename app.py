import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📈 YouTube Trending Dashboard", layout="wide")

# Load credentials directly (paste from your credentials.json)
credentials = {
  "type": "service_account",
  "project_id": "youtube-data-api-v3-457023",
  "private_key_id": "YOUR_KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nYOUR_KEY\\n-----END PRIVATE KEY-----\\n",
  "client_email": "sheets-writer@youtube-data-api-v3-457023.iam.gserviceaccount.com",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "YOUR_CERT_URL"
}

# Google Sheets access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(credentials, scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("YouTube Trending Tracker").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Show dashboard
st.title("📺 Real-Time YouTube Trending Dashboard")
st.markdown("This dashboard displays real-time trending videos scraped using YouTube Data API.")

# Show data
st.dataframe(df)

# Show Top Video
st.subheader("🔥 Most Viewed Right Now")
df["Views"] = pd.to_numeric(df["Views"], errors='coerce')
top = df.sort_values("Views", ascending=False).head(1).iloc[0]
st.success(f"**{top['Title']}** by **{top['Channel']}** with **{top['Views']:,}** views")

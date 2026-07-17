import base64
from datetime import datetime

def get_table_download_link(df, filename_prefix, file_type="csv"):
    if file_type == "csv":
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename_prefix}_{datetime.now().strftime("%Y%m%d")}.csv">📥 Download CSV File</a>'
    else:
        data = df.to_json(orient="records")
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/json;base64,{b64}" download="{filename_prefix}_{datetime.now().strftime("%Y%m%d")}.json">📥 Download JSON File</a>'
    return href

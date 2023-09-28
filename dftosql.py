import base64
import streamlit as st
import pandas as pd


# Function to clean the value for SQL insertion
def clean_value(value):
    if pd.isna(value):
        return "NULL"
    elif isinstance(value, str):
        value = value.replace("'", "''")
        return f"'{value}'"
    else:
        return str(value)


# Function to convert DataFrame to SQL file content
def df_to_sql(df):
    # Write the CREATE TABLE statement
    sql_content = """
CREATE TABLE transcriptions (
    id INT PRIMARY KEY,
    study_id INT,
    transcription_data TEXT,
    created_by VARCHAR(255),
    created_dt DATETIME,
    is_updated BOOLEAN,
    updated_dt DATETIME NULL,
    state CHAR(2),
    addendum_no INT DEFAULT 0,
    linked_studies TEXT NULL,
    approving_provider_id INT NULL,
    has_locked BOOLEAN,
    locked_dt DATETIME NULL,
    unlocked_dt DATETIME NULL,
    transcription_text TEXT,
    approved_dt DATETIME,
    transcribing_user VARCHAR(255) NULL,
    pre_approved_provider_contact_id INT NULL,
    pre_approved_dt DATETIME NULL
);
    """
    # Write the INSERT INTO statements
    for index, row in df.iterrows():
        values = ", ".join(clean_value(value) for value in row)
        sql_content += f"INSERT INTO transcriptions VALUES ({values});\n"
    return sql_content


st.title("Excel to SQL Converter")

# Upload the Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
if uploaded_file is not None:
    # Read the uploaded Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    # Convert the DataFrame to SQL
    sql_content = df_to_sql(df)

    # Limit the display to a reasonable length to avoid performance issues
    display_content = sql_content
    if len(sql_content) > 5000:
        display_content = sql_content[:5000] + "\n\n-- ... Content is truncated ... --"

    # Display the SQL content as a code block with syntax highlighting
    st.code(display_content, language="sql")

    # Encode the SQL content to bytes and create a download button
    b64 = base64.b64encode(sql_content.encode()).decode()
    href = (
        f'<a href="data:file/sql;base64,{b64}" download="output.sql" '
        f'style="display:inline-block;background-color:#FF2E88;color:white;padding:10px 20px;'
        f'border-radius:3px;text-decoration:none;font-weight:bold;">Download SQL File</a>'
    )
    st.markdown(href, unsafe_allow_html=True)

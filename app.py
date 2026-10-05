import streamlit as st
import pandas as pd
import plotly.express as px


# Page Settings
st.set_page_config(
    page_title="Student Dashboard",
    page_icon="📊",
    layout="wide"
)


#-------Visual Changes--------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: gray;
}

h1 {
    color: yellow !important;
    text-align: center;
    margin-bottom: 30px;
}

h2, h3 {
    color: #1F3A5F !important;
}

[data-testid="stMetric"] {
    background-color: white !important;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #E1E5EA;
}
[data-testid="stMetricValue"] {
    color: #1F3A5F !important;
    font-size: 28px;
    font-weight: bold;
}
[data-testid="stMetricLabel"] {
    color: #555555 !important;
}
/* جدول‌های داشبورد */

[data-testid="stDataFrame"] {
    background-color: white !important;
    border-radius: 10px;
}

[data-testid="stDataFrame"] [role="columnheader"] {
    background-color: #1F3A5F!important;
    color: white !important;
}

[data-testid="stDataFrame"] [role="gridcell"] {
    background-color: white !important;
    color: #333333 !important;
}
</style>
""", unsafe_allow_html=True)

# --------Title-----------
st.title("📊 Student Performance Dashboard")
uploaded_file = st.file_uploader(
    "📁 Upload Students Excel File",
    type=["xlsx"]
)

# ---------Reading an Excel file----------
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_excel("students.xlsx")
if uploaded_file is None:
    st.info("Please upload an Excel file to analyze.")

#------------GPA calculation------------
df["Average"] = df[["Math", "Physics", "English"]].mean(axis=1)
#------Make a function to describe students status and show in a box

def get_status(average):
    if average >= 18:
        return "Excellent"
    elif average >= 15:
        return "Good"
    else:
        return "Needs Attention"

df["Status"] = df["Average"].apply(get_status)# apply the get_status function on all of student's average and put the result in the new column

#--------------------Student Filter by sidebar --------------------
st.sidebar.title("🎛️ Dashboard")

st.sidebar.subheader("🔍 Filter Students")

filter_option = st.sidebar.selectbox(
    "Show:",
    [
        "All Students",
        "Average below 15",
        "Attendance below 75%",
        "Excellent Students"

    ]
)
#-----------------Creating a slider-----------------------
slider_value = st.sidebar.slider(
    "Minimum Average",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.5
)
min_average = slider_value

#--------------Display project information-------------
st.sidebar.divider()

st.sidebar.write("📌 Project Information")

st.sidebar.write("Student Performance Dashboard")

st.sidebar.write("Python + Pandas + Streamlit")



#------------Filters--------------------

if filter_option == "All Students":
    filtered_df = df

elif filter_option == "Average below 15":
    filtered_df = df[df["Average"] < 15]

elif filter_option == "Attendance below 75%":
    filtered_df = df[df["Attendance"] < 75]

elif filter_option == "Excellent Students":
    filtered_df = df[df["Average"] >= 18]
filtered_df = filtered_df[filtered_df["Average"] >= min_average]

#-------------Creating a sidebar for selective sorting---------
st.sidebar.divider()
sort_option = st.sidebar.selectbox(
    "Sort Students By:",
    [
        "Average: High to Low",
        "Average: Low to High",
        "Name: A to Z"
    ]
)

if sort_option == "Average: High to Low":
    filtered_df = filtered_df.sort_values(
        by="Average",
        ascending=False
    )

elif sort_option == "Average: Low to High":
    filtered_df = filtered_df.sort_values(
        by="Average",
        ascending=True
    )

elif sort_option == "Name: A to Z":
    filtered_df = filtered_df.sort_values(
        by="Name",
        ascending=True
    )

#--------Selecting a Name and displaying information---------
st.subheader("👩‍🎓 Student Details")
selected_student = st.selectbox("Select a student:", df["Name"])
student = df[df["Name"] == selected_student].iloc[0]
col1, col2, col3 = st.columns(3)
col1.metric("📊 Average",f"{student['Average']:.2f}")
col2.metric("📅 Attendance",f"{student['Attendance']}%")
col3.metric( "📐 Math", student["Math"])

#-------Display grades for the selected student-----

st.write("### Subject Grades")
subject_data = pd.DataFrame({ "Subject": ["Math", "Physics", "English"],"Grade": [student["Math"],student["Physics"],student["English"]]})
#st.dataframe( subject_data,use_container_width=True, hide_index=True)
#I replaced the style section below with the line above so that the background and text color changes for the table would be applied.
styled_subject = subject_data.style \
    .set_properties(**{
        "background-color": "#FFFFFF",
        "color": "#333333"
    }) \
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#1F3A5F"),
                ("color", "white"),
                ("font-weight", "bold")
            ]
        }
    ])

st.dataframe(
    styled_subject,
    use_container_width=True,
    hide_index=True
)
# محاسبات
number_of_students = len(df)
class_average = df["Average"].mean()
best_average = df["Average"].max()

students_need_attention = df[
    (df["Average"] < 15) &
    (df["Attendance"] < 75)
]

number_need_attention = len(students_need_attention)

# ------------Show basic information-----
col1, col2, col3, col4 = st.columns(4)

col1.metric("👩‍🎓 Students", number_of_students)

col2.metric(
    "📊 Class Average",
    f"{class_average:.2f}"
)

col3.metric(
    "🏆 Best Average",
    f"{best_average:.2f}"
)

col4.metric(
    "⚠️ Need Attention",
    number_need_attention
)


st.divider()

#-------show the status of selected student------


st.write("### Student Status")

status = student["Status"]

if status == "Excellent":
    st.success("🟢 Excellent")

elif status == "Good":
    st.info("🟡 Good")

else:
    st.warning("🔴 Needs Attention")

#----------------Show the table-----------
st.subheader("📋 Student Grades")

#st.dataframe( filtered_df , use_container_width=True )
#I replaced the style section below with the line above so that the background and text color changes for the table would be applied.
styled_df = filtered_df.style \
    .set_properties(**{
        "background-color": "#FFFFFF",
        "color": "#333333",
        "text-align": "center"
    }) \
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#1F3A5F"),
                ("color", "white"),
                ("font-weight", "bold"),
                ("text-align", "center")
            ]
        }
    ])

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)

# -------------------------
# Student Grade Point Average Chart
# -------------------------

st.subheader("📊 Students Average")

fig = px.bar(
    filtered_df,
    x="Name",
    y="Average",
    title="Students Average",
    text="Average",
    color="Average",
     color_continuous_scale="RdYlGn"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
    marker_line_width=3
)

fig.update_layout(
    xaxis_title="Student",
    yaxis_title="Average",
    yaxis_range=[0, 20]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------
# Attendance chart
# -------------------------

st.subheader("📅 Students Attendance")

fig_attendance = px.bar(
    filtered_df,
    x="Name",
    y="Attendance",
    title="Students Attendance",
    text="Attendance",
    color="Attendance",
    color_continuous_scale="RdYlGn"
)

fig_attendance.update_traces(
    texttemplate="%{text}%",
    textposition="outside",
    marker_line_width=3
)

fig_attendance.update_layout(
    xaxis_title="Student",
    yaxis_title="Attendance (%)",
    yaxis_range=[0, 100]
)

st.plotly_chart(
    fig_attendance,
    use_container_width=True
)

#-----------Make a pie chart from status of student---------
status_counts = df["Status"].value_counts()
st.subheader("🎯 Student Status")

fig_status = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    title="Student Status Distribution",
    color=status_counts.index,
    color_discrete_map={
        "Excellent": "cyan",
        "Good": "white",
        "Needs Attention": "pink"
    }
)

st.plotly_chart( fig_status,    use_container_width=True)



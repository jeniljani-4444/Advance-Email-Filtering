import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd 
from streamlit_lottie import st_lottie
import requests
import sweetviz as sv
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk

nltk.download('stopwords')

df = pd.read_excel('mail.xlsx')
df.columns = df.columns.str.lower()
df['time'] = pd.to_datetime(df['time'])

primary_mails = ['jobalerts-noreply@linkedin.com', 'messages-noreply@linkedin.com',
                 'no-reply@accounts.google.com', 'hr@finanvo.in', 'hr@pranshtech.com',
                 'drive-shares-dm-noreply@google.com','ravidholariya700@gmail.com',
                 'noreply@github.com','anomalydetection@costalerts.amazonaws.com','freetier@costalerts.amazonaws.com','no-reply@signup.aws']

promotion_mails = ['invitations@linkedin.com', 'info@meetup.com','chitchat@jollyhires.com',
                   'newsletters-noreply@linkedin.com']

df['mail_category'] = df['senderemail'].apply(lambda x: 'primary' if x in primary_mails else ('promotion' if x in promotion_mails else 'uncategorized'))


st.set_page_config(
    page_title="Email Filtering App",
    page_icon="📧",
    layout="wide"
)

st.markdown(
    """<style>
            footer {
            visibility: hidden;
      }
    </style>""",
    unsafe_allow_html=True
)

def lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def generate_sweetviz_report(dataframe):
    report = sv.analyze(dataframe)
    return report.show_html()

with st.sidebar:
    selected = option_menu(
        menu_title='Menu',
        menu_icon='menu-button-wide',
        default_index=0,
        options=['Description', 'Email Filtering', 'Dashboard','Automated EDA'],
        icons=['book', 'envelope', 'bar-chart','gear'],
        orientation='vertical'
    )

if selected == 'Description':
    st.title("Welcome to our Advanced Email Filtering System 📧")
    st.write("Ensure a clutter-free inbox with our cutting-edge email filtering solution.")
    left_col, right_col = st.columns(2)

    with left_col:
        st.header("Key Features:")
        st.markdown("- Intelligent Spam Filtering")
        st.markdown("- Customizable Filtering Rules")
        st.markdown("- Machine Learning-powered Classification")
        st.markdown("- Real-time Threat Analysis")
        st.markdown("- User-friendly Dashboard")
        
        st.header("Get Started:")
        st.write("1. Sign up for our service.")
        st.write("2. Configure your filtering preferences.")
        st.write("3. Enjoy a cleaner and safer email experience!")

    with right_col:
        lottie = lottieurl(
            "https://lottie.host/df753460-9980-4b74-bf63-b100002a291d/1or8xrdwVA.json")
        st_lottie(lottie, height=500, width=600, key="mail_image")

    st.header("Contact Us:")
    st.write("Have questions or need assistance? Contact our support team.")

    st.text_input("Your Name", key="name")
    st.text_input("Your Email", key="email")
    st.text_area("Your Message", key="message")

    if st.button("Send Message"):
        st.success("Message sent successfully!")

if selected == 'Email Filtering':
    st.title("Email Filtering 📧")

    df['time'] = pd.to_datetime(df['time'])

    email_input = st.text_input("Enter Keywords:", "")
    entered_emails = [email.strip() for email in email_input.split(',')]

    include_attachments = st.checkbox("Include emails with attachments")
    sender_domain = st.text_input("Filter by Sender Domain (e.g., example.com):")

    start_date = st.date_input("Start Date", min_value=df['time'].min(), max_value=df['time'].max())
    end_date = st.date_input("End Date", min_value=df['time'].min(), max_value=df['time'].max())
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")

    if st.button("Filter Emails"):
        pattern = '|'.join(entered_emails)
        filtered_rows = df[df['payload'].str.contains(pattern, case=False, regex=True)]

        if include_attachments:
            filtered_rows = filtered_rows[filtered_rows['Attachments'].notnull()]

        if sender_domain:
            df['payload'] = df['senderemail'].astype(str)
            filtered_rows = df[df['senderemail'].apply(lambda x: sender_domain.lower() in x.split('@')[1].lower() if '@' in x else False)]

        if not filtered_rows.empty:
            st.success("Emails filtered successfully!")
            st.dataframe(filtered_rows)
        else:
            st.warning("No matching emails found.")

if selected == "Automated EDA":
    st.title("Automated EDA Report :gear:")
    st.write("Automated Exploratory Data Analysis (EDA) reports are powerful tools in the field of data science that streamline the initial stages of data exploration.")
    generate_btn = st.button("Generate EDA Report")

    if generate_btn:
        with st.spinner("Generating EDA Report....."):
            report_html = generate_sweetviz_report(df)
            st.components.v1.html(report_html, height=800)

def remove_stopwords_and_tokenize(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return ' '.join(filtered_words)



if selected == 'Dashboard':
    st.title('Email Analysis Dashboard 📊')

    first_col, sec_col, third_col, fourth_col, fifth_col = st.columns(5)

    total_mails = len(df['senderemail'])
    unique_senders = df['senderemail'].unique()
    avg_time_rate = df['time'].mean()
    prom_mails = df['mail_category'].value_counts()['promotion']
    prim_mails = df['mail_category'].value_counts()['primary']

    with first_col:
        st.subheader("Total Emails")
        st.subheader(total_mails)
    with sec_col:
        st.subheader("Unique Senders")
        st.subheader(len(unique_senders))
        st.selectbox("List of unique senders",unique_senders)
    with third_col:
        st.subheader("Promotion Mails")
        st.subheader(prom_mails)
        st.selectbox("List of Promotion Mails",df[df['mail_category'] == 'promotion']['senderemail'])
    with fourth_col:
        st.subheader("Primary Mails")
        st.subheader(prim_mails)
        st.selectbox("List of Promotion Mails",df[df['mail_category'] == 'primary']['senderemail'])
    with fifth_col:
        pass

    st.markdown('---')
    one_col, second_col = st.columns(2)

    with one_col:
        df.columns = df.columns.str.lower()
        mail_counts = df['senderemail'].value_counts().reset_index().head(10)
        fig = px.bar(mail_counts, x='senderemail', y='count')
        fig.update_layout(xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True)

    with second_col:
        df.columns = df.columns.str.lower()
        mail_name_counts = df['sendername'].value_counts().reset_index().head(10)
        fig = px.bar(mail_name_counts, x='sendername', y='count')
        fig.update_layout(xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('---')

    time_counts = df['time'].value_counts().reset_index()
    fig_3 = px.histogram(time_counts, x='time', y='count')
    st.plotly_chart(fig_3, use_container_width=True)

    st.markdown('---')
   
    st.title('Email Payload Word Cloud')

    df['cleaned_payload'] = df['payload'].apply(remove_stopwords_and_tokenize)
    all_text = ' '.join(df['cleaned_payload'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_text)
    st.image(wordcloud.to_array(), caption='Word Cloud', use_column_width=True)
    
    st.markdown('---')
    
    st.title("Mail Category Pie Chart")
    
    cat_counts = df.groupby('mail_category')[['mail_category']].sum()
    
    mail_pie_chart = px.pie(cat_counts,names=cat_counts.index)
    st.plotly_chart(mail_pie_chart, use_container_width=True)





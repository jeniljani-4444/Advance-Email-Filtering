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



import pandas as pd


df = pd.read_excel('mail.xlsx')
df.columns = df.columns.str.lower()
df['time'] = pd.to_datetime(df['time'])


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
            # Features section
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
            st_lottie(lottie, height=500,width=600, key="mail_image")

        

        # Contact us section
         st.header("Contact Us:")
         st.write("Have questions or need assistance? Contact our support team.")

        # Contact form (you can replace this with your contact form or link)
         st.text_input("Your Name", key="name")
         st.text_input("Your Email", key="email")
         st.text_area("Your Message", key="message")

         if st.button("Send Message"):
                st.success("Message sent successfully!")




if selected == 'Email Filtering':
        st.title("Email Filtering 📧")
        
        df['time'] = pd.to_datetime(df['time'])

        # st.title("Email Filtering 📧")

        email_input = st.text_input("Enter Keywords:", "")
        entered_emails = [email.strip() for email in email_input.split(',')]

            # Additional advanced filters
        include_attachments = st.checkbox("Include emails with attachments")
        sender_domain = st.text_input("Filter by Sender Domain (e.g., example.com):")

            # Date and time filters
        start_date = st.date_input("Start Date", min_value=df['time'].min(), max_value=df['time'].max())
        end_date = st.date_input("End Date", min_value=df['time'].min(), max_value=df['time'].max())
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")

        if st.button("Filter Emails"):
        
            pattern = '|'.join(entered_emails)
            filtered_rows = df[df['payload'].str.contains(pattern, case=False, regex=True)]
            
            # Apply advanced filters
            if include_attachments:
                filtered_rows = filtered_rows[filtered_rows['Attachments'].notnull()]  # Assuming 'Attachments' is a column in your DataFrame

            if sender_domain:
                # Ensure 'payload' is of string type and then filter by sender domain
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
            generate_btn = st.button("Genreate EDA Report")
           

            if generate_btn:
                 with st.spinner("Generating EDA Report....."):
                    report_html = generate_sweetviz_report(df)
                    st.components.v1.html(report_html, height=800)

                 


if selected == 'Dashboard':
     st.title('Email Analysis Dashboard 📊')
     
     first_col, sec_col, third_col, fourth_col, fifth_col = st.columns(5)

     total_mails = len(df['senderemail'])
     unique_senders = len(df['senderemail'].unique())
     avg_time_rate = df['time'].mean()

     with first_col:
          st.subheader("Total Emails")
          st.subheader(total_mails)
     with sec_col:
          st.subheader("Unique Senders")
          st.subheader(unique_senders)
     with third_col:
          pass
          
          
     with fourth_col:
          pass
     with fifth_col:
          pass

     st.markdown('---')
     one_col,second_col = st.columns(2)
     
     with one_col:
       
        df.columns = df.columns.str.lower()
        mail_counts = df['senderemail'].value_counts().reset_index().head(10) 
        fig = px.bar(mail_counts,x='senderemail',y='count')
        fig.update_layout(xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True)
        
     with second_col:
        df.columns = df.columns.str.lower()
        mail_name_counts = df['sendername'].value_counts().reset_index().head(10) 
        fig = px.bar(mail_name_counts,x='sendername',y='count')
        fig.update_layout(xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True)
        
        
    #  st.markdown('---')

    #  df['days'] = df.date.dt.day_name()
    #  days_counts = df['days'].value_counts().reset_index() 
    #  fig_2 = px.bar(days_counts,x='days',y='count',color='count',color_continuous_scale='viridis', height=400,width=1500)
    
    #  st.plotly_chart(fig_2, use_container_width=True)
    
    #  st.markdown('---')
     
     time_counts = df['time'].value_counts().reset_index()
     fig_3 = px.histogram(time_counts,x='time',y='count')
     st.plotly_chart(fig_3, use_container_width=True)


     st.markdown('---')
     

    # Download NLTK stopwords
     import nltk
     nltk.download('stopwords')

    # Function to remove stopwords and tokenize the text
     def remove_stopwords_and_tokenize(text):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
        return ' '.join(filtered_words)

    # Streamlit app
     def main():
        st.title('Email Payload Word Cloud')

            # Apply the function to the 'payload' column
        df['cleaned_payload'] = df['payload'].apply(remove_stopwords_and_tokenize)

            # Combine all cleaned payloads into a single string
        all_text = ' '.join(df['cleaned_payload'].astype(str))

            # Generate a WordCloud
        wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_text)

            # Plot the WordCloud using Streamlit
        st.image(wordcloud.to_array(), caption='Word Cloud', use_column_width=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()




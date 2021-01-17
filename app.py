import pandas as pd
import streamlit as st
import plotly.express as px


DATA_URL = "tweets.csv"

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard used to analyze sentiments of tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard used to analyze sentiments of tweets 🐦")


# Load Data
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()


# Random Tweet
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])


# Number of tweets by sentiment
st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


# When and where are users tweeting from?
st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour to look at", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown("### Tweet locations based on time of day")
    st.markdown(f"{len(modified_data)} tweets between {hour}:00 and {(hour + 1) % 24}:00")
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)
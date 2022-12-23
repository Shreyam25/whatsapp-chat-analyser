import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image



img=Image.open("img.png")
st.set_page_config(page_title="Whatsapp Chat Analyser",page_icon=img)
st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a text file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    for i  in user_list:
        if i == 'group_notification':
            user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Group Analysis")
    selected_user = st.sidebar.selectbox("Show analysis by", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area


        messages, words, media, links,emojis,users = helper.fetch_stats(selected_user, df)
        st.markdown("""
        <style>
        .big-font {
            font-size:50px; color: #0B5345  ;
            text-align: center;
        }
        .header {
            font-size:30px; color: #075E54;
            
        }
         .title {
            font-size:35px; color: "red";
            background-color:#075E54 ;
            padding:2px 5px 5px 10px;
            
        }
        
         .container {
            font-size:35px; 
            border-color:#H3672P
            background-color:#1E8449 ;
            
        }
       
        
        
        
        
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<h1 class="big-font">Chat Analysis</h1>', unsafe_allow_html=True)
        st.markdown('<h1 class="title">Chat summary</h1>', unsafe_allow_html=True)
        col1, col2, col3= st.columns(3)

        with col1:
            st.markdown('<h1 class="header">Messages</h1>', unsafe_allow_html=True)
            st.subheader(messages)
        with col2:
            st.markdown('<h1 class="header">Users</h1>', unsafe_allow_html=True)
            st.subheader(users)
        with col3:
            st.markdown('<h1 class="header">Words</h1>', unsafe_allow_html=True)
            st.subheader(words)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown('<h1 class="header">Emoji</h1>', unsafe_allow_html=True)
            st.subheader(emojis)
        with col2:
            st.markdown('<h1 class="header">Media</h1>', unsafe_allow_html=True)
            st.subheader(media)
        with col3:
            st.markdown('<h1 class="header">Link</h1>', unsafe_allow_html=True)
            st.subheader(links)
#awards
        active_days= helper.Top_5_chatdays(selected_user, df)
        m=len(active_days)-1
        talkative,a = helper.most_active_users(df)
        n=len(talkative)-1
        emoji_fan=helper.emoji_fan(selected_user,df)
        media_admirer=helper.top5_media(selected_user,df)

        st.markdown('<h1 class="title">Awards </h1>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<h1 class="header">Active day</h1>', unsafe_allow_html=True)
            st.subheader(active_days.index[0])
        with col2:
            st.markdown('<h1 class="header">Talkative </h1>', unsafe_allow_html=True)
            st.subheader(talkative.index[0])
        with col3:
            st.markdown('<h1 class="header">Silent reader</h1>', unsafe_allow_html=True)
            st.subheader(talkative.index[n])

        col1, col2,col3= st.columns(3)

        with col1:
            st.markdown('<h1 class="header">Emoji Fan</h1>', unsafe_allow_html=True)
            st.subheader(emoji_fan[0])
        with col2:
            st.markdown('<h1 class="header">Media admirer</h1>', unsafe_allow_html=True)
            st.subheader(media_admirer.index[0])
        with col3:
            st.markdown('<h1 class="header">Lazy day</h1>', unsafe_allow_html=True)
            st.subheader(active_days.index[m])








        # activity map
        st.markdown('<h1 class="title">Activity Map</h1>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Active Day")
            busy_day = helper.week_activity_map(selected_user, df)
            plt.figure(figsize=(5, 10))
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            plt.xlabel("Date")
            plt.ylabel("Count of messages")
            st.pyplot(fig)

        with col2:
            st.header("Most Active Month")
            busy_month = helper.month_activity_map(selected_user, df)
            plt.figure(figsize=(5, 10))
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="#075E54")
            plt.xticks(rotation='vertical')
            plt.xlabel("Month")
            plt.ylabel("Count of messages")
            st.pyplot(fig)

            # activity map

        col1, col2 = st.columns(2)
        with col1:

            st.header("Weekly activity analysis")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
        with col2:
            st.header("Monthly chat analysis")
            timeline = helper.monthly_timeline(selected_user, df)
            plt.figure(figsize=(5, 10))
            fig, ax = plt.subplots()

            ax.plot(timeline['time'], timeline['message'], color="#145A32")
            plt.xticks(rotation='vertical')
            plt.xlabel("Yearwise Months")
            plt.ylabel("Count of messages")
            st.pyplot(fig)


        if selected_user == 'Group Analysis':
            st.markdown('<h1 class="title">Activity Map</h1>', unsafe_allow_html=True)
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.header("Top 5 Active users")
                x=x.head(5)

                ax.bar(x.index, x.values, color="#5499C7")
                plt.xticks(rotation='vertical')
                plt.xlabel("User Name")
                plt.ylabel("Count of messages")
                st.pyplot(fig)
            with col2:
                new_df.index =new_df.index + 1
                st.header("Users based on screen time")
                st.dataframe(new_df,width=500,height=300)





         # WordCloud
        st.markdown('<h1 class="title">Wordcloud:Most Used words</h1>', unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        plt.figure(figsize=(10,10))
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.markdown('<h1 class="title">Analysis based on emojis</h1>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most used emojis with count")

            st.dataframe(emoji_df,width=400,height=300)
        with col2:
            df.index=df.index+1
            st.header("Top 5 emojis")
            plt.figure(figsize=(5, 5))
            fig, ax = plt.subplots()
            ax.pie(emoji_df["Count"].head(), labels=emoji_df["Emojis"].head(), autopct="%0.3f")
            st.pyplot(fig)


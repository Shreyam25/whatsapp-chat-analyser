from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user,df):


    extract = URLExtract()
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    n = df[df['user'] != "group_notification"]
    users = n.user.unique()
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    return num_messages, len(words), num_media_messages, len(links),len(emojis),len(users)

def most_active_users(df):
    df=df[df['user'] != "group_notification"]
    x = df['user'].value_counts()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):


    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']



    wc = WordCloud(width=300,height=300,min_font_size=10,background_color='#25D366')

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def emoji_helper(selected_user,df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df = emoji_df.rename(columns={0: "Emojis", 1: "Count"})

    return emoji_df

def emoji_fan(selected_user,df):
    emojis = pd.DataFrame(columns=['sender', 'emoji'])
    df = df[df['user'] != "group_notification"]
    # Loop through all messages in the DataFrame
    for sender, message in zip(df.user, df.message):


        message_split = list(message)


        for character in message_split:


            if character in emoji.UNICODE_EMOJI['en']:
                # Add each emoji to the DataFrame
                emojis = emojis.append({'sender': sender, 'emoji': character}, ignore_index=True)
    return emojis.value_counts().index[0]
def monthly_timeline(selected_user,df):

    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline



def week_activity_map(selected_user,df):

    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def Top_5_chatdays(selected_user,df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    return df['only_date'].value_counts().head(3)

def top5_media(selected_user,df):
    if selected_user != 'Group Analysis':
        df = df[df['user'] == selected_user]

    return df[df['message']=="<Media omitted>\n"].groupby('user')['message'].count().sort_values(ascending=False).head(5)


import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2}\,\s\d{1,2}\:\d{2}\s[A-Z]{2}\s'
    pattern2 = '\d{1,2}\/\d{1,2}\/\d{2}\,\s\d{1,2}\:\d{2}\s[A-Z]{2}\s\-\s'



    messages = re.split(pattern2, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'Message': messages, 'Date': dates})
    # convert message_date type
    df['Date'] = pd.to_datetime(df['Date'])

    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)

    df['only_date'] = df['Date'].dt.date
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

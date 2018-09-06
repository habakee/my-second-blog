from sqlalchemy import create_engine
import pandas as pd
from pandas.io import sql
import time
from datetime import date, datetime, timedelta

start_date = '2018-08-10'
end_date = '2018-08-10'


def calculate_num_of_days(start_date, end_date):
    day_1 = datetime.strptime(start_date, "%Y-%m-%d")
    day_2 = datetime.strptime(end_date, "%Y-%m-%d")

    delta = day_2 - day_1

    return delta.days


def day_increment(date, increment_num):
    date_to_datetime = datetime.strptime(date, "%Y-%m-%d")
    incremented_date = date_to_datetime + timedelta(days=increment_num)

    return datetime.strftime(incremented_date, "%Y-%m-%d")


def visitor_info_analysis(start_date, end_date):
    engine_string = 'mysql+pymysql://root:team21sangha@smartvisitorpass.cwbrhvpulmkd.ap-northeast-2.rds.amazonaws.com:3306/smart_visitor_pass?charset=utf8'

    conn = create_engine(engine_string)

    end_date = day_increment(end_date, 1)

    try:
        query = "SELECT * FROM visitor_info_sample WHERE timestamp BETWEEN '"+start_date+"' and '"+end_date + "'"

        selected_df = sql.read_sql(query, conn)
        statistics_people_count_per_hour(selected_df, start_date, end_date)
        statistics_gender_age_ratio(selected_df)

    except Exception as e:
        print(e)
        pass


def statistics_people_count_per_hour(selected_df, start_date, end_date):
    # prepare dataframe for analysis result
    columns = ['time', 'count']
    result_df = pd.DataFrame(columns=columns)

    time_list = []
    count_list = []

    for i in range(calculate_num_of_days(start_date, end_date)):
        date = day_increment(start_date, i)
        for j in range(0, 24):
            time_list.append(date + ' ' + str(j).rjust(2, '0'))
            count_list.append(0)

    time_se = pd.Series(time_list)
    count_se = pd.Series(count_list)

    result_df['count'] = count_se
    result_df['time'] = time_se.values

    # sorting dataframe with timestamp
    selected_df = selected_df.sort_values(["timestamp"])
    selected_df = selected_df.reset_index(drop=True)
    print(selected_df)

    # start analysis
    for i in range(len(selected_df)):
        try:
            matching_time = selected_df.loc[i, 'timestamp'].split(':')[0]
            matching_index = result_df.index[result_df['time'] == matching_time].tolist()[0]

            result_df.loc[matching_index, 'count'] = result_df.loc[matching_index, 'count'] + 1
        except IndexError as e:
            print(e)

    for i in range(len(result_df)):
        result_df.loc[i, 'time'] = result_df.loc[i, 'time']+":00:00"

    result_df.to_csv('./blog/static/data/people_count_per_hour.csv', index=False)


def statistics_gender_age_ratio(selected_df):
    # prepare dataframe for analysis
    columns = ['gender', 'age_scope', 'count', 'ratio']
    result_df = pd.DataFrame(columns=columns)

    columns_total = ['gender', 'count', 'ratio']

    gender_list = ['F', 'F', 'F', 'F', 'F', 'F',
                   'M', 'M', 'M', 'M', 'M', 'M']
    age_scope_list = ['under_10s', '20s', '30s', '40s', '50s', 'over_60s',
                      'under_10s', '20s', '30s', '40s', '50s', 'over_60s']

    count_list = []
    for i in range(len(gender_list)):
        count_list.append(0)

    gender_se = pd.Series(gender_list)
    age_scope_se = pd.Series(age_scope_list)
    count_se = pd.Series(count_list)

    result_df['gender'] = gender_se
    result_df['age_scope'] = age_scope_se
    result_df['count'] = count_se

    # start analysis
    for i in range(len(selected_df)):
        current_gender = str(selected_df['gender'][i])
        current_age = int(selected_df['age'][i])
        if current_gender is "F":
            if current_age < 20:
                matching_index = 0
            elif current_age < 30:
                matching_index = 1
            elif current_age < 40:
                matching_index = 2
            elif current_age < 50:
                matching_index = 3
            elif current_age < 60:
                matching_index = 4
            else:
                matching_index = 5

        elif current_gender is "M":
            if current_age < 20:
                matching_index = 6
            elif current_age < 30:
                matching_index = 7
            elif current_age < 40:
                matching_index = 8
            elif current_age < 50:
                matching_index = 9
            elif current_age < 60:
                matching_index = 10
            else:
                matching_index = 11

        result_df.loc[matching_index, 'count'] = result_df.loc[matching_index, 'count'] + 1

    total_count = len(selected_df)

    # calculate ratio
    for i in range(len(result_df)):
        current_ratio = result_df.loc[i, 'count'] / total_count * 100
        result_df.loc[i, 'ratio'] = float("{0:.2f}".format(current_ratio))

    total_count_female = 0
    total_count_male = 0

    total_ratio_female = 0
    total_ratio_male = 0

    for i in range(0, 6):
        total_count_female += result_df.loc[i, 'count']
    for i in range(6, 12):
        total_count_male += result_df.loc[i, 'count']

    total_ratio_female = float("{0:.2f}".format(total_count_female / total_count * 100))
    total_ratio_male = float("{0:.2f}".format(total_count_male / total_count * 100))

    total_dict = {'gender': ['F', 'M'],
                  'count': [total_count_female, total_count_male],
                  'ratio': [total_ratio_female, total_ratio_male]}

    result_df_total = pd.DataFrame(total_dict, columns=columns_total)

    result_df.to_csv('./blog/static/data/gender_age_count_ratio.csv', index=False)
    result_df_total.to_csv('./blog/static/data/total_gender_count_ratio.csv', index=False)


if __name__ == '__main__':
    start_time = time.time()
    visitor_info_analysis(start_date, end_date)
    print("--- %s seconds ---" % (time.time() - start_time))
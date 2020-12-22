import time
import pandas as pd
import os


# Classes to handle exception
class IncorrectName(Exception):
    """Base class for other exceptions"""
    pass


class IncorrectTimeFilter(Exception):
    pass


# ********************************


# Dictionaries used for conversion integer -> Date or Date -> integer
day = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

month = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'Jully': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}


# *************************************


def find_key(dictio, val):
    """
    Function search the first key of a value

    Args:
        (dict) dictio - the dictionary that contain the value that you search for
        (*)     val - the value that you are searching
    Returns:
        (str)   k - the key of the value
    """
    for k, v in dictio.items():
        if val == v:
            return k
    return 'Error the is no such key'


# ***************************************************************************


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    pass
    while True:
        try:
            nb_city = input('How many city do you want to consult the information about the bikes :\n')
            nb_city = int(nb_city)
            if nb_city < 0 or nb_city > 3:
                raise Exception()
        except:
            print('Please enter a number between 1 and 3')
        else:
            break

    while True:
        try:
            if nb_city == 1:
                name_city1 = input(
                    'which city are you interested about :\n * chicago\n * new york city\n * washington\n> ').lower()
                if not (name_city1 in CITY_DATA.keys()):
                    raise IncorrectName()
                filter_parameter = {
                    'city': name_city1
                }
            elif nb_city == 2:
                name_city1, name_city2 = input(
                    'which cities are you interested about don\'t forget to separate them with / :\n * chicago\n * new '
                    'york city\n * washington\n> ').lower().split(
                    '/')
                if not (name_city1 in CITY_DATA.keys() or name_city2 in CITY_DATA.keys()):
                    raise IncorrectName()
                filter_parameter = {
                    'city': [name_city1, name_city2]
                }
            elif nb_city == 3:
                filter_parameter = {
                    'city': list(CITY_DATA.keys())
                }
        except (IncorrectName, ValueError):
            print('Please enter the correct name')
        else:
            break

    while True:
        try:
            filter_time = input(
                'Would you like to explore data by :\n * month\n * day\n * both\n * not at all Type "none" for no '
                'time filter \n> ').lower()
            if filter_time == 'month':
                filter_month_value = input('Enter the month (January, february, MARCH, ...):\n> ').capitalize()
                filter_day_value = 'all'
                if not filter_month_value in month:
                    raise IncorrectTimeFilter()
            elif filter_time == 'day':
                filter_day_value = input('Enter the day (Monday, tuesday, THURSDAY, ...)  :\n> ').capitalize()
                filter_month_value = 'all'
                if not (filter_day_value in day):
                    raise IncorrectTimeFilter()
            elif filter_time == 'both':
                filter_month_value = input('Enter the month (January, february, MARCH, ...):\n> ').capitalize()
                if not filter_month_value in month:
                    raise IncorrectTimeFilter()
                filter_day_value = input('Enter the day (Monday, tuesday, THURSDAY, ...)  :\n> ').capitalize()
                if not (filter_day_value in day):
                    raise IncorrectTimeFilter()
            elif filter_time == 'none':
                filter_month_value = 'all'
                filter_day_value = 'all'
            else:
                raise IncorrectTimeFilter()
        except (IncorrectTimeFilter, ValueError):
            print('Please enter the correct data to get the filtered results')
        else:
            break
    filter_parameter['month'] = filter_month_value
    filter_parameter['day'] = filter_day_value
    print('-' * 40)
    return filter_parameter


def load_data(filter_parameter):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    cities = filter_parameter['city']
    os.chdir(os.path.dirname(__file__)) # for some users doesn't require this line like my computer
    if type(cities) == str:
        name_file = CITY_DATA[cities]
        path = os.getcwd() + '\\' + name_file
        df = pd.read_csv(path)
    elif len(cities) > 1:
        name_file = [CITY_DATA[elt] for elt in cities]  # rajouter une question en prenant compte du type
        df = []
        for elt in name_file:
            path = os.getcwd() + '\\' + elt
            df.append(pd.read_csv(path))
        df = pd.concat(df)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if filter_parameter['month'] == 'all' and filter_parameter['day'] == 'all':
        print('filter none')
    elif not filter_parameter['month'] == 'all' and filter_parameter['day'] == 'all':
        print('filter month')
        df = df[df['Start Time'].dt.month == month[filter_parameter['month']]]
    elif filter_parameter['month'] == 'all' and not filter_parameter['day'] == 'all':
        print('filter day')
        df = df[df['Start Time'].dt.weekday == day[filter_parameter['day']]]
    elif not (filter_parameter['month'] == 'all' and filter_parameter['day'] == 'all'):
        print('filter day and month')
        df = df[df['Start Time'].dt.month == month[filter_parameter['month']]]
        df = df[df['Start Time'].dt.weekday == day[filter_parameter['day']]]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Start Time'].groupby(df['Start Time'].dt.month).count().idxmax()
    common_month = find_key(month, common_month)
    print("common_month : " + str(common_month))
    # TO DO: display the most common day of week
    common_day = df['Start Time'].groupby(df['Start Time'].dt.weekday).count().idxmax()
    common_day = find_key(day, common_day)
    print("common_day : " + str(common_day))
    # TO DO: display the most common start hour
    common_hour = df['Start Time'].groupby(df['Start Time'].dt.hour).count().idxmax()
    print("common_hour : " + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].groupby(df['Start Station']).count().idxmax()
    print('The most common start station : ' + str(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].groupby(df['End Station']).count().idxmax()
    print('The most common end station : ' + str(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    common_traject = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(
        name="The count").head(1)
    print('The most frequent station : ' + str(common_traject['Start Station'][0]) + ' ==> ' + str(
        common_traject['End Station'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (pd.to_timedelta(df['Trip Duration'], unit='S')).sum()
    print('Total travel time : ' + str(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = (pd.to_timedelta(df['Trip Duration'], unit='S')).mean()
    print('Mean travel time : ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):  # need some verification
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_type = df.groupby('User Type').size().sort_values(ascending=False).reset_index(
        name="Count User Type").to_string(index=False)
    print('The count of user types :\n' + str(count_user_type))
    # TO DO: Display counts of gender
    try:
        count_user_gender = df.groupby('Gender').size().sort_values(ascending=False).reset_index(
        name="Count User Gender").to_string(index=False)
        print('The count of user Gender :\n' + str(count_user_gender))
    except KeyError:
        print('there is no gender in the data')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year_birth = df['Birth Year'].dropna().sort_values().iloc[0]
        print('The earliest year birth : ' + str(earliest_year_birth))
        recent_year_birth = df['Birth Year'].dropna().sort_values().iloc[-1]
        print('The most recent year birth : ' + str(recent_year_birth))
        common_year_birth = df['Birth Year'].dropna().value_counts().idxmax()
        print('The most common year birth : ' + str(common_year_birth))
    except KeyError:
        print('there is no birth year in the data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def handle_input_raw_data():
    avaliable_input = ['yes','no']
    while(True):
        consult_data = input('Would you like to see some data answer by "yes" or "no"\n').lower()
        if consult_data in avaliable_input:
            break
        else:
            print('Your input is wrong please answer "yes" or "no" ')
    return consult_data == 'yes'


def raw_data(df):
    """Displays some data on bikeshare users."""
    start_data = 0
    end_data = 5
    consult_data = handle_input_raw_data()
    while(consult_data):
        print(df.iloc[start_data:end_data].to_string(index=False))
        consult_data = handle_input_raw_data()
        start_data += 5
        end_data += 5


def main():
    print("-------------------- Bikeshare Programm --------------------\n")
    while True:
        filter_parameter = get_filters()
        df = load_data(filter_parameter)
        #load_data(filter_parameter)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

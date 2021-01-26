import time
import pandas as pd
import numpy as np

chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'
rows_to_see = 5

def get_city():
    """
    Asks user to specify a city.
    Args:
        None.
    Returns:
        (str) Filename containing the correponding city data.
    """

    city = input('Would you like to see data for [C]hicago, [N]ew York, or [W]ashington? ').strip().casefold()
    while True:
        if city == 'c':
            print('\nYou chose Chicago.')
            return 'chicago.csv'
            break
        elif city == 'n':
            print('\nYou chose New York City.')
            return 'new_york_city.csv'
            break
        elif city == 'w':
            print('\nYou chose Washington.')
            return 'washington.csv'
        else:
            city = input('Please type \'c\' for Chicago, \'n\' for New York or \'w\' for Washington ')


def get_time_period():
    """
    Asks user to specify a time period to filter.
    Args:
        none.
    Returns:
        month - string containing the month to filter by, or "all" to apply no month filter
        day   - string containing the day of week to filter by, or "all" to apply no day filter
    """

    f = input('Would you like to filter the data by [m]onth, [d]ay, or [n]ot at all? ').strip().casefold()
    while True:
        if f == 'm':
            day = 'all'
            # Get user input for month (all, january, february, ... , june)
            month = input('Which month - January, February, March, April, May or June? ').strip().casefold()
            while True:
                if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                    month = input('Please, enter a valid month from January to June: ').strip().casefold()
                else:
                    break
            break
        elif f == 'd':
            month = 'all'
            # Get user input for day of week (all, monday, tuesday, ... sunday)
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ').strip().casefold()
            while True:
                if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    day = input('Please, enter a valid day: ').strip().casefold()
                else:
                    break
            break
        elif f == 'n':
            month = 'all'
            day = 'all'
            break
        else:
            f = input('Please type \'m\' to filter by month, \'d\' to filter by day or \'n\' for no filter: ').strip().casefold()

    return month, day


def load_data(city):
    """
    Reads the city file name and loads it to a dataframe
    Args:
        city - string containing the path to the city file
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Loading data from file ' + city + '...\n')
    df = pd.read_csv(city)

    # Provide datetime format to allow easier filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month

    return df

def apply_time_filters(df, month, day_of_week):
    """
    Filters the data according to the criteria specified by the user.
    Args:
        df          - Pandas DataFrame
        month       - string indicating the month to filter by, or "all" to apply no month filter
        day_of_week - string indicating the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - DataFrame to be used to calculate all aggregates that is filtered according to
             the specified time period
    """

    print('Data loaded. Computing stats...')
    # Filter by Month if required
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of week if required
    if day_of_week != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            if day_of_week.capitalize() in d:
                day = d
        df = df[df['day_of_week'] == day]

    return df


def popular_month(df):
    """
    What is the most popular month for start time?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        most_popular_month - string of most frequent month
    """

    print('\n * What is the most popular month for bike traveling?')
    mnth = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_popular_month = months[mnth - 1].capitalize()
    return most_popular_month


def popular_day(df):
    """
    What is the most popular day of week for start time?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        popular_day - string with name of day with most rides
    """

    print('\n * What is the most popular day of the week (Monday to Sunday) for bike traveling?')
    return df['day_of_week'].value_counts().reset_index()['index'][0]


def popular_hour(df):
    """
    What is the most popular hour of day for start time?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        popular_hour - int of the most popular hour
    """

    print('\n * What is the most popular hour of the day for bike traveling?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]


def trip_duration(df):
    """
    What is the total trip duration and average trip duration?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        tuple = total trip duration, average trip durations
        each one is a pandas._libs.tslib.Timedelta object
    """

    print('\n * What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    # Sum for total trip time, Mean for average trip time

    total_travel_time = np.sum(df['Travel Time'])
    totalDays = str(total_travel_time).split()[0]
    print ("\nThe total travel time on 2017 through June was " + totalDays + " days \n")
    average_travel_time = np.mean(df['Travel Time'])
    averageDays = str(average_travel_time).split()[0]
    print("The average travel time on 2017 through June was " + averageDays + " days \n")
    return total_travel_time, average_travel_time


def popular_stations(df):
    """
    What is the most popular start station and most popular end station?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        tuple - indicating most popular start and end stations
    """

    print("\n* What is the most popular start station?")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n* What is the most popular end station?")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station + "\n")
    return start_station, end_station


def popular_trip(df):
    """
    What is the most popular trip?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        result - pandas.core.frame.DataFrame - with start, end, and number of trips for most popular trip
    """

    print('\n* What was the most popular trip from start to end?')
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    return result


def users(df):
    """
    What are the counts of each user type?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        users - pandas series with counts for each user type
    """

    print('\n* Are users subscribers, customers, or dependents?\n')
    return df['User Type'].value_counts()


def gender(df):
    """
    What are the counts of gender?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        gender - pandas.core.series.Series counts for each gender
    """

    try:
        print('\n* What is the breakdown of gender among users?\n')
        return df['Gender'].value_counts()
    except:
        print('There is no gender data in the source.')


def birth_years(df):
    """
    What is the earliest, latest, and most frequent birth year?
    Args:
        df - DataFrame from apply_time_filters
    Returns:
        tuple of earliest, latest, and most frequent year of birth
    """

    try:
        print('\n* What is the earliest, latest, and most frequent year of birth, respectively?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest))
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest))
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent))
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this period.')

def compute_stat(f, df):
    """
    Calculates the time it takes to commpute a stat
    Args:
        f  - Applied stats function
        df - DataFrame with all the data
    Returns:
        None. Only prints information to console
    """

    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print(" >>> Computing this stat took %s seconds." % (time.time() - start_time))


def display_raw_data(df):
    """
    Displays the data used to compute the stats
    Args:
        df - DataFrame with all the data
    Returns:
       None.
    """

    rowIndex = 0
    more = input("Would you like to see rows of the data used to compute the stats? Type 'y' or 'n' ").strip().casefold()

    while True:
        if more == 'n':
            return
        if more == 'y':
            print(df[rowIndex: rowIndex + rows_to_see])
            rowIndex = rowIndex + rows_to_see

        more = input("\nWould you like to see " + str(rows_to_see) + " more rows of the data? Type 'y' or 'n' ").strip().casefold()

def stats():
    """
    Calculates and prints out the descriptive statistics about a city
    and time period specified by the user via raw input.
    Args:
        None.
    Returns:
        None.
    """

    city = get_city()
    df = load_data(city)
    month, day = get_time_period()

    df = apply_time_filters(df, month, day)

    display_raw_data(df)

    stat_function_list = [popular_month,
        popular_day, popular_hour,
        trip_duration, popular_trip,
        popular_stations, users, birth_years, gender]

    for fun in stat_function_list:
        compute_stat(fun, df)

    restart = input("\n * Would you like to restart and perform another analysis? Type \'y\' or \'n\' ").strip().casefold()
    if restart == "y":
        stats()

if __name__ == '__main__':
    stats()

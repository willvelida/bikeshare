import time
import pandas as pd
import numpy as np
import datetime
import calendar

chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = ''
    month = ''
    day = ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York or Washington? ')
    city = city.lower()
    if city == 'chicago':
        city = chicago
    elif city == 'new york city':
        city = new_york_city
    elif city == 'washington':
        city = washington
    else:
        print("That's not a listed city! Please try again")
        get_filters()
    # get user input for month (all, january, february, ... , june)
    month = input('Please select a month from january to june, or "all" for no filter: ')
    month = month.lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a day of the week, or "all" for no filter: ')
    day = day.lower()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract the month and day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create new dataframe
        df = df[df['month'] == month]

    # filter day
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['Month'] = df['Start Time'].dt.month
    common_month = df['Month'].mode()[0]
    # return common month as the name of the month
    # month = datetime.date(common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day
    common_day = df['day_of_week'].mode()[0]
    # return comman day as the name of the day
    # common_day = calendar.day_name[common_day]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print('Most common month: ', calendar.month_name[common_month])
    print('Most common day: ', common_day)
    print('Most popular hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df['common_start'] = df['Start Station']

    common_Start = df['common_start'].mode()[0]
    print ('The most common start station is: ', common_Start)

    # display most commonly used end station
    df['common_end'] = df['End Station']
    common_end = df['common_end'].mode()[0]
    print('The most common end station is: ', common_end)

    # display most frequent combination of start station and end station trip
    common_trip = df['common_start'] + ' to ' + df['common_end']
    print('The most common trip is: ', common_trip.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    start_time = time.time()
    # display total travel time
    # Get the start of the trip time
    trip_start = pd.to_datetime(df['Start Time'])
    # Get the end of the trip time
    trip_end = pd.to_datetime(df['End Time'])
    # Set the trip total time to a new column
    df['Trip Total Time'] = trip_start - trip_end
    # Get the sum of trip total time column
    total_time =  df['Trip Total Time'].sum()
    print("The total amount of time for a trip is: " + str(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The average time of a trip is: " + str(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    # Display counts of gender
    # count it for washington
    gender = df['Gender'].value_counts()

    # Display earliest, most recent, and most common year of birth
    earliest_year = df.sort_values('Birth Year').iloc[0]
    # recent_year =  df.sort_values(by=['Birth Year'])
    common_year = df['Birth Year'].mode()[0]

    print('Count of user types: ', user_type)
    print('Count of gender: ', gender)
    print('Oldest person to rent: ', earliest_year['Birth Year'])
    # print('Youngest person to rent: ', recent_year)
    print('Most common birth year: ', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    # Ask the user if they want to see the next 5 rows of data
        view_data = input('Would you like to see the next five rows of data? Yes or No: ')
        view_data = view_data.lower()

        while view_data == 'yes':
            print(df.head(5))
            display_data(df)
        
       
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to interact with.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data to help identify trends!')
# get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ["chicago","new york city", "washington"]
        city = input("Enter City (chicago, new york city, washington): ").lower()
        if city not in cities:
            print("Please enter chicago, new york city or washington with correct spelling.")
            continue
        else:
            break

# get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter month or all: ").lower()
        if month not in ["all", "january", "february", "march", "april", "may", "june"]:
            print("Please enter all, january, february, march, april, may, or june with correct spelling.")
            continue
        else:
            break
# get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day of week or all: ").lower()
        if day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            print("Please enter all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday with correct spelling.")
            continue
        else:
            break

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
# display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Start Month:', popular_month)

# display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most Frequent Start Week Day:', popular_weekday)

# display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

# display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start_station)
# display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end_station)
# display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Frequent Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# display total travel time
    total_trips_time = int(df['Trip Duration'].sum() / 60)
    print('Total Trips Duration in Minutes:', total_trips_time)

# display mean travel time
    average_trip = int(df['Trip Duration'].mean() / 60)
    print('Average Trip Duration in Minutes:', average_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

# Display counts of gender
    while True:
        if 'Gender' not in df.columns:
            print('Gender Count: Gender Data Not Collected')
            break
        elif 'Gender' in df.columns:
            user_gender = df['Gender'].value_counts(dropna=False)
            print(user_gender)
            break


# Display earliest, most recent, and most common year of birth
    while True:
        if 'Birth Year' not in df.columns:
            print('Youngest Customer Birth Year: Birth Data Not Collected')
            break
        elif 'Birth Year' in df.columns:
            youngest_customer = int(df['Birth Year'].max())
            print('Youngest Customer Birth Year:', youngest_customer)
            break

    while True:
        if 'Birth Year' not in df.columns:
            print('Most Recent Customer Birth Year: Birth Data Not Collected')
            break
        elif 'Birth Year' in df.columns:
            recent_birthyear = int(df.groupby('Start Time')['Birth Year'].max()[0])
            print('Most Recent Customer Birth Year:', recent_birthyear)
            break

    while True:
        if 'Birth Year' not in df.columns:
            print('Most Recent Customer Birth Year: Birth Data Not Collected')
            break
        elif 'Birth Year' in df.columns:
            common_birth = int(df['Birth Year'].mode()[0])
            print('Most Common Birth Year:', common_birth)
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    print_count = 0
    while True:
        raw_data_request = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        if raw_data_request.lower() == 'yes':
                print(df[print_count:print_count + 5].to_string(index=False))
                print_count += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

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

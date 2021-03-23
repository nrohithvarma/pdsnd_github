import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Get user input for city (chicago, new york city, washington).
    cities = ['chicago', 'new york city', 'washington']
    city = []
    
    while city not in cities:
        print('Please enter the city for which you would like to see the data: \n 1. Chicago, \n 2. New York City, \n 3. Washington')
        city = input().lower()
        
        if city not in cities:
            print('\nInvalid input. Please provide a valid city name')

    print('\nData will be shown for:', city.capitalize())
    
    #Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = []
          
    while month not in months:
        print('\n\nPlease enter the month for which you would like to see the data: January, February,....,June')
        print('\nEnter "all" if you want to see data for all months')
          
        month = input().lower()
          
        if month not in months:
            print('\nInvalid input. Please provide a valid month')
        
    print('\nData will be shown for {} month(s)'.format(month.capitalize()))
          
    #Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = []
    
    while day not in days:
        print('\nPlease enter the day of week for which you would like to see the data: Monday, Tuesday,....,Sunday')
        print('\nEnter "all" if you want to see data for all days of week')
        
        day = input().lower()
        
        if day not in days:
            print('\nInvalid input. Please provide a valid day')
    
    print('\nData will be shown for {}'.format(day))

    print('-'*100)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df,month):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - the dataframe to analyze
        (str) month - name of the month to print out exceptions   
    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displaying the most common month
    common_month = str(df['month'].mode()[0])
    
    # converting month number to month name
    month_num = datetime.datetime.strptime(common_month, "%m")
    month_name = month_num.strftime("%B")
    
    print('\nThe most frequent month of travel is {}'.format(month_name)) 

    # displaying the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most frequent day of travel is {}'.format(common_day))

    # displaying the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nThe most frequent hour of travel is {}:00'.format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        df - The dataframe to analyze
        
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displaying most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\n{} is the most common start station'.format(start_station))

    # displaying most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\n{} is the most common end station'.format(end_station))

    # displaying most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + ' to ' + df['End Station']
    common_statcombo = df['Station Combo'].mode()[0]
    print('\nThe most frequent trips happen from {}'.format(common_statcombo))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        df - The dataframe to analyze
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displaying total travel time
    total_traveltime = df['Trip Duration'].sum()
    
    # converting total travel time to hours, minutes and seconds
    (minutes, seconds) = divmod(total_traveltime, 60)
    (hours, minutes) = divmod(minutes, 60)
    
    print(f'\nThe total travel time is {round(hours)} hrs, {round(minutes)} mins, {round(seconds)} secs .')
    

    # displaying mean travel time
    mean_traveltime = round(df['Trip Duration'].mean())
    
    # converting mean travel time to hours, minutes and seconds
    (minute, second) = divmod(mean_traveltime, 60)
    (hour, minute) = divmod(minute, 60)
    
    print(f'\nThe mean travel time is {hour} hrs, {minute} mins, {second} secs .')
 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df,city):
    """
    Displays statistics on bikeshare users.
    
    Args:
        df - The dataframe to analyze
        (str) city - The name of the city to print out exceptions
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    count_user = df['User Type'].value_counts()
    print('\nThe counts of different users by user types are: \n{}'.format(count_user))

    # Displaying counts of gender (calling try and except because gender data is not available for all datasets)
    try:
        count_gender = df['Gender'].value_counts()
        print('\nThe counts of different users by gender are: \n{}'.format(count_gender))
    except:
        print('\nGender data unavailable for {}.'.format(city.capitalize()))
        
        
    # Displaying earliest, most recent, and most common year of birth (calling try and except because birth year data is not available for all datasets)
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f'\nThe earliest year of birth: {earliest}\nThe most recent year of birth: {recent}\nThe most common year of birth: {common_year}')
    except:
        print('\nBirth year data unavailable for {}.'.format(city.capitalize()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def raw_data(df):
    """ 
    Function to ask user if they want to view 5 lines of raw data 
    
    Args:
        df - The dataframe to view
        
    """
    
    responses = ['yes', 'no']
    user_response = []
    
    i = 5   # counter variable for displaying rows of dataset
    
    
    # loop to accept user response and show data
    while user_response not in responses:
        print('\nDo you want to view first 5 lines of raw data?  (Yes/No)')
        
        user_response = input().lower()
        
        if user_response == 'yes':
            print(df[0:i])
        elif user_response not in responses:
            print('\nPlease provide a valid response: (Yes/No)')
            
            
    # loop to ask users if they want to continue viewing data
    while user_response == 'yes':
        print('\nDo you want to continue viewing more raw data?')
        user_response = input().lower()
        
        if user_response == 'yes':
            print('\nHow many more lines of data do you wish to see?   (Please enter a valid number)')
            
            user_number = int(input())
            print(df[i:i+user_number])
            i += user_number
        elif user_response == 'no':
            break
        else:
            print('\nPlease provide a valid response: (Yes/No)')
            
    print('-'*100)            
              
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            

if __name__ == "__main__":
	main()

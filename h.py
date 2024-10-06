import os

import curses
import calendar
from datetime import datetime, timedelta

def run_time_selector():
    # Store the returned tuple in a variable
    selected_time = curses.wrapper(interactive_time_selector)  # Run the interactive time selector in a curses wrapper

    if selected_time:
        hour, minute = selected_time  # Unpack the returned tuple
        print(f"Selected time: {hour:02}:{minute:02}")  # Output the selected time
    else:
        print("No time selected.")  # Handle case where no time was selected


def draw_calendar(stdscr, year, month, selected_day):
    stdscr.clear()

    # Create a Calendar object
    cal = calendar.monthcalendar(year, month)  # Returns a list of weeks (each week is a list of days)

    # Display the calendar header (Month Year)
    stdscr.addstr(0, 0, f"{calendar.month_name[month]} {year}".center(20))
    stdscr.addstr(1, 0, "Su Mo Tu We Th Fr Sa")  # Day names

    today = datetime.today()

    # Loop over the weeks of the month
    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            # Determine the position to print each day
            x_pos = day_idx * 3  # Calculate the x position based on the day of the week
            y_pos = week_idx + 2  # Calculate the y position (week number)

            # Handle the case where day is 0 (empty day)
            if day == 0:
                stdscr.addstr(y_pos, x_pos, "  ")
            else:
                if day == selected_day:  # Highlight the selected day
                    stdscr.addstr(y_pos, x_pos, f"[{day:2}]", curses.A_REVERSE)
                elif year == today.year and month == today.month and day == today.day:
                    # Highlight today's date with brackets
                    stdscr.addstr(y_pos, x_pos, f"[{day:2}]")
                else:
                    stdscr.addstr(y_pos, x_pos, f"{day:2}")

    stdscr.addstr(9, 0, "Use arrow keys to navigate. Press Enter to select the day. 'q' to quit.")
    stdscr.refresh()

def interactive_calendar(stdscr):
    # Get the current month and year
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year
    selected_day = current_date.day if current_date.month == month and current_date.year == year else 1  # Start with today's day or the 1st

    while True:
        draw_calendar(stdscr, year, month, selected_day)
        key = stdscr.getch()

        # Handle key input
        if key == curses.KEY_RIGHT:
            # Move selection to the next day
            max_day = calendar.monthrange(year, month)[1]
            if selected_day < max_day:
                selected_day += 1
            else:
                # Move to the next month
                selected_day = 1
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1

        elif key == curses.KEY_LEFT:
            # Move selection to the previous day
            if selected_day > 1:
                selected_day -= 1
            else:
                # Move to the previous month
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
                selected_day = calendar.monthrange(year, month)[1]  # Last day of the previous month

        elif key == curses.KEY_UP:
            # Move up a week (7 days)
            if selected_day > 7:
                selected_day -= 7
            else:
                # Move to the previous month
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
                selected_day = max(calendar.monthrange(year, month)[1] - (7 - selected_day), 1)

        elif key == curses.KEY_DOWN:
            # Move down a week (7 days)
            max_day = calendar.monthrange(year, month)[1]
            if selected_day + 7 <= max_day:
                selected_day += 7
            else:
                # Move to the next month
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                selected_day = min(7 - (max_day - selected_day), calendar.monthrange(year, month)[1])

        elif key == ord('q'):
            # Quit the program
            return None

        elif key == 10:  # Enter key
            # Return the selected day when the user presses Enter
            return year, month, selected_day  # Return the full date (year, month, day)

class User:
    def __init__(self, email, name, description, grade, gender, instagram):
        self.email = email
        self.name = name
        self.description = description
        self.grade = grade
        self.gender = gender
        self.instagram = instagram

users = {}  # Initialize an empty dictionary for users

class FileBasedEventRegistration:
    def __init__(self, filename='hinfo.txt'):
        self.filename = filename

    def addtofile(self, user):
        """Registers a participant by appending to the file."""
        with open(self.filename, 'a') as file:
            file.write(f"{user.email},{user.name},{user.description},{user.grade},{user.gender},{user.instagram},{users[user][0]},{users[user][1]},{users[user][2]},{users[user][3]}\n")

    def addtoUsers(self, users):
        """Populates the users dictionary from the file."""
        if not os.path.exists(self.filename):
            print(f"File '{self.filename}' does not exist.")
            return  # Exit if the file does not exist

        with open(self.filename, mode='r') as file:
            for line in file:
                # Split the line into columns and check the correct number of fields
                columns = line.strip().split(',')
                if len(columns) != 10:  # Ensure there are exactly 10 columns
                    print(f"Skipping invalid line: {line}")
                    continue

                try:
                    email, name, description, grade, gender, instagram, time, date, location, realdate = columns
                    # Create a User object and add to the users dictionary
                    user = User(email, name, description, grade, gender, instagram)
                    users[user] = [time, date, location, realdate]
                except Exception as e:
                    print(f"Error processing line: {line}. Error: {e}")

"""
    def addtoUsers(self, users):
        Populates the users dictionary from the file.
        if not os.path.exists(self.filename):
            return  # Return if the file does not exist

        with open(self.filename, mode='r') as file:
            for line in file:
                columns = line.strip().split(',')
                email, name, description, grade, gender, instagram, time, date, location, realdate = columns
                users[User(email, name, description, grade, gender, instagram)] = [time, date, location, realdate]
"""

# Instantiate the event registration system
registration_system = FileBasedEventRegistration()
registration_system.addtoUsers(users)  # Populate users from the file

def area():
    area1 = int(input("Type the associated number: ").strip())
    if (area1 == 1):
        return "Helen Newman"
    elif (area1 == 2):
        return "Noyes"
    elif (area1 == 3):
        return "Teagle Downstairs"
    elif (area1 == 4):
        return "Teagle Upstairs"
    elif (area1 == 5):
        return "Toni Morrison"
    elif (area1 == 6):
        return "Sand Volleyball - CKB Quad"
    elif (area1 == 7):
        return "Pickleball - Jessup"
    elif (area1 == 8):
        return "Pickleball - Noyes"
    elif (area1 == 9):
        return "Basketball - Jessup"
    elif (area1 == 10):
        return "Basketball - Noyes"
    elif (area1 == 11):
        return "Tennis - McClintok"
    elif (area1 == 12):
        return "Tennis - Jessup"
    elif (area1 == 13):
        return "Tennis - Jessup"
    elif (area1 == 14):
        return "Turf field - North Campus"
    else:
        print("Please enter a valid number.")
        area()

def adduser(user, time, date, location, actual_date):
    """Adds a user to the in-memory dictionary and file."""
    users[user] = [time, date, location, actual_date]
    registration_system.addtofile(user)  # Add the user to the file

def login_or_signUp():
    """Handles user login or sign-up."""
    response = input("Do you have an account? You must answer with 'Yes' or 'No': ").strip().lower()

    if response == "yes":
        email = input("Please enter your email: ").strip()

        for key in users:
            if (key.email == email):
                print("You have successfully logged in!")
                return key
        else:
            print("You don't have an account. You will be redirected to sign-up.")
            return login_or_signUp()

    elif response == "no":
        email = input("Sign up for TogetherCornell! Please enter your email to create a new account: ").strip()

        if email in users:
            print("You already seem to have an account. Redirecting you to the login page.")
            return login_or_signUp()

        print("The following are optional questions. Please enter nothing if you do not wish to respond.")
        name = input("What is your name/username?: ").strip()
        description = input("Write a short description about yourself: ").strip()
        grade = input("What grade are you in?: ").strip()
        gender = input("What are your preferred pronouns?: ").strip()
        instagram = input("What is your Instagram?: ").strip()

        user = User(email, name, description, grade, gender, instagram)
        adduser(user, "", "", "", "")

        print("You have successfully signed up and logged in!")
        return user

    else:
        print("Invalid response. Please answer with 'Yes' or 'No'.")
        return login_or_signUp()

def partner_matching(current_user):
    print("Select a day you want to excercise!")
    selected_date = curses.wrapper(interactive_calendar)
    selected_time = (str(input("What time do you want to excercise? Please include AM or PM: "))).upper()
    while (("AM" not in selected_time) and ("PM" not in selected_time)):
        selected_time = input("Your response did not inlcude AM or PM. Please include AM or PM: ")
    time = ""
    if "AM" in selected_time:
        time = "AM"
    else:
        time = "PM"
    print("Cornell University offers a number of facilities to excercise and have fun with friends!")
    print("1. Helen Newman")
    print("2. Noyes")
    print("3. Teagle Downstairs")
    print("4. Teagle Upstairs")
    print("5. Toni Morrison")
    print("6. Sand Volleyball - CKB Quad")
    print("7. Pickleball - Jessup")
    print("8. Pickleball - Noyes")
    print("9. Basketball - Jessup")
    print("10. Basketball - Noyes")
    print("11. Tennis - McClintok")
    print("12. Tennis - Jessup")
    print("13. Tennis - Risley")
    print("14. Turf field - North Campus")
    print("Above is a list of places you can meet with others. Which place do you want to explore?")
    date = str(selected_date[1]) + "/" + str(selected_date[2]) + "/" + str(selected_date[0])
    x = area()
    users[current_user] = [time, date, str(x), selected_time]
    print("You are planning on going to " + str(x) + " at " + selected_time + " on " + date)
    print("The following are people who are going at a similar time as you!")
    y = 0
    list = []
    for key in users:
        if (users[key][0] == users[current_user][0] and
            users[key][1] == users[current_user][1] and
            users[key][2] == users[current_user][2]):
            if (key.email != current_user.email):
                print(f"{key.name} is going to {str(x)} at {users[key][3]} on {date}")
                y = 1
                list.append(key.name)
    adduser(current_user, time, date, str(x), selected_time)
    if (y == 1):
        print("It looks like a few people are going at a similar time as you.")
        usernamec = input("Type the username of a person you want to go with: ")
        for x in list:
            if (usernamec == x):
                print("We will notify " + usernamec)
                return True
        return False
    else:
        return False

def grade_partner():
    while True:
        try:
            score = int(input("Please rate your partner's timeliness on a scale from 1 to 10: "))
            if 1 <= score <= 10:
                print(f"You rated your partner: {score}/10")
                break
            else:
                print("Invalid input. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


# Start the login or sign-up process
print("Welcome to TogetherCornell!")
current_user = login_or_signUp()
print(f"Welcome, {current_user.name}!")
if(partner_matching(current_user)):
    grade_partner()

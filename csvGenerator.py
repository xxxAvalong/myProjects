# Import Required Library
from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from datetime import datetime, timedelta, date
import os


def zero_remove(original_date):
    """
    function to remove the zero num in date, for example:
    09 -> 9
    :param original_date: is date part like this: 08 or 07
    :return: int number 8 or 7
    """
    original_date = str(original_date)

    if original_date[0] == '0':
        new_date = original_date.replace('0', '')
    else:
        new_date = original_date

    return int(new_date)


def get_today():
    """
    function to get today date: in this format: 14.2.2022, not in: 2022-02-14
    or original date if you call getToday()['today']
    :return: dictionary to get the part of this day date or all this day date
    """

    today = str(datetime.today()).split(' ')[0]

    day = int(zero_remove(today.split('-')[-1]))
    month = int(zero_remove(today.split('-')[1]))
    year = int(today.split('-')[0])

    return {'day': day, 'month': month, 'year': year, 'today': f'{today}'}
################


def main():
    # create the window
    window = Tk()
    window.title('Filling helper :)')

    # Set geometry
    window.geometry("250x350")

    date_container = {}  # base dictionary with data for timeline(start,stop) and mode of interval of timeline

    # Add Calendar
    calendar = Calendar(window, selectmode='day',
                        day=get_today().get('day'),
                        month=get_today().get('month'),
                        year=get_today().get('year'))

    # show the calendar
    calendar.pack()
    # create and show the comboBox, that have modes of interval of timeline
    combo_box = combobox(window)

    user_interface(window, calendar, container=date_container, combo__box=combo_box)

    window.mainloop()
###############


def combobox(window):
    """
    function to create comboBox (in the window),
    that save a mod of time Interval
    dqy month of year
    :return: actual value from comboBox
    """
    combo_label = Label(text='Interval :', font='9')
    combo_label.place(y=240, x=5)

    combo = Combobox(window)
    combo['values'] = ('Day', 'Month', 'Year')  # comboBox values(modes of interval of )
    combo.current(0)
    combo.place(x=80, y=240)

    return combo
###############


def show_and_save_calendar_date(window, calendar, mode, date_container):
    """
    function to get date from Calendar and pass it to the base dictionary
    with timeline data. Depending on the mode parameter this function write the value
    to the base dictionary, where key == 'date{mode}'
    :return:
    """
    #  get actual date from Calendar
    get_date = calendar.get_date()
    #  clear the space, where date will be written. Just in case there's already something written down
    clear_window_space(window, mode)

    date_ = converter_to_d_m_yyyy(get_date)

    day = date_['day']
    month = date_['month']
    year = date_['year']
    date_lbl = Label(window, text=f'{day}.{month}.{year}', font=12)

    date_container[mode] = date_
    if mode == 'From':
        date_lbl.place(y=190, x=40)
    elif mode == 'To':
        date_lbl.place(y=190, x=155)

    return date_
###############


def user_interface(window, calendar, container, combo__box):
    """
    function that calls all backend functions
    :param combo__box:
    :param window: app window
    :param calendar: app Calendar
    :param container: dictionary that collect data to create date interval(timeline)
        and save the mod_value from comboBox
    :return:
    """
    def show_start_date_and_pass_to_dict():
        """
        wrap function to get date from Calendar(start of timeline) and pass it to the dictionary with timeline data
        :return:
        """
        show_and_save_calendar_date(window, calendar, mode='From', date_container=container)

    def show_finish_date_and_pass_to_dict():
        """
        wrap function to get date from Calendar(finish of timeline) and pass it to the dictionary with timeline data
        :return:
        """
        show_and_save_calendar_date(window, calendar, mode='To', date_container=container)

    def confirm_button():
        """
        function to pass the date from comboBox(interval mode) to the dictionary with timeline date
        :return:
        """
        time_slot = combo__box.get()
        container['timeSlot'] = time_slot

        backend(container)
        # return container

    # Button "OD" - definition
    Button(window, text="OD", command=show_start_date_and_pass_to_dict).place(y=190, x=5)
    # Button "OD" - definition
    Button(window, text='DO', command=show_finish_date_and_pass_to_dict).place(y=190, x=120)

    # Button "CONFIRM" - definition
    Button(window, text='Confirm', command=confirm_button, padx=90, pady=20).place(y=270, x=10)
###############


def backend(date_set):
    """
    Backend funktion
    """
    #  get dictionary with first and last date, get mode of interval from comboBox
    timeline_and_mode = create_timeline(date_set)
    first_date = timeline_and_mode['firstDate']  # first date of timeline
    last_date = timeline_and_mode['lastDate']  # last date of timeline
    time_slot = timeline_and_mode['mode']  # time-slot split mod

    # function fo create the corrects dates, depending on the mod. It will be saved in base dictionary
    date_set = get_date_set(time_slot, first_date, last_date)
    # function for writing the values from base dictionary to the CSV file
    write_csv(date_set)

    # start the created file
    os.startfile(f"{get_today()['today']}_Temp.csv")
###############


def create_timeline(date_container):
    """
    Transform the input data and return the date in DateTime-format, mode of interval of timeline
    :param date_container: base dictionary with timeline data
    :return: transformed data
    """
    return {"mode": date_container['timeSlot'], 'firstDate': date_container['From']['date_date'],
            'lastDate': date_container['To']['date_date']}
###############


def get_date_set(time_slot, first_date, last_date):
    """
    Create a list with the dates to be recorded,
    depending on the mode
    :param time_slot: mode of interval of timeline
    :param first_date: start date
    :param last_date: finish data
    :return: list with all needed dates
    """
    if last_date > first_date:
        # create list with spread between first and last days. (There are count of Days)
        days_delta = (last_date - first_date).days
    else:
        # if the original date is larger than the final date (which is an error) then simply reverse them
        days_delta = (first_date - last_date).days

    date_set = []  # a list to which the dates required will be added
    first_iter = True  # The first iteration

    for i in range(days_delta + 1):
        date_ = False  # day date uin this iteration, not suitable yet, because we don't know what is the date
        day_date = first_date + timedelta(i)  # date of one of the days between first and last date

        if time_slot.lower().startswith('d'):  # if "day" interval selected (in comboBox)
            date_ = day_date  # all days from timeline will be added to the date_set

        elif time_slot.lower().startswith('m'):  # if "month" interval selected (in comboBox)
            if first_iter:  # if the first iteration is
                date_set.append(first_date.replace(day=1))  # add the first day of month from start date

            date_ = day_date if day_date.day == 1 else False  # date will be added if is the first day of month

        elif time_slot.lower().startswith('y'):  # if "year" interval selected (in comboBox)
            if first_iter:  # if the first iteration is
                date_set.append(first_date.replace(day=1, month=1))  # add the first day of year from start date

            # date will be added if is the first day of year
            date_ = day_date if day_date.day == 1 and day_date.month == 1 else False

            # if date_ = False  # nothing will be added

        first_iter = False  # this is no more the first iteration

        if date_:  # if the day has the right date, it won't be "false"
            date_set.append(date_)  # add right day to the data_set
        else:
            continue

    return date_set  # return list with all right dates
###############


def write_csv(dates_set):
    """
    function that write csv file
    :param dates_set:
    :return:
    """
    today = get_today()  # get today date

    if configured_headers():  # check availability of setting file
        headers = configured_headers()  # configured headers
    else:
        headers = 'Date;\n'  # the standard header, if there is non configuration file

    """if os.path.exists(f"{today['today']}_Temp.csv"):
        
        try:
            os.remove(f"{today['today']}_Temp.csv")   # if csv file with today exits
        except:
            pass"""

    with open(f"{today['today']}_Temp.csv", 'w+', newline='') as file:  # create or rewrite the csv file
        firs_iter = True  # if there is first iteration write the headers

        for day in dates_set:

            if firs_iter:
                file.write(f'{headers}')
                firs_iter = False

            file.write(str(day) + '\n')  # write the date from date-det
###############


def configured_headers():
    """
    function to search for a configuration file to create columns in the output file

    As configuration file I use the file that has already been created ...
                                          ...by this script in this folder
    :return: False if there is no configuration file or columns from configuration file
    """
    # get all files from Python.file directory
    files_in_directory = os.listdir()

    for fileName in files_in_directory:  # go by the name of each file in the folder

        file_parts = fileName.split('.')
        file_format = file_parts[-1]  # format of file
        file_name = ''.join(file_parts[:-1])  # name of file

        # find the .csv format file that have 'Temp' in the name - it will be the configure file
        if file_format == 'csv' and 'Temp' in file_name:

            with open(f'{fileName}', 'r') as file:
                headers = file.readline()  # read the firs line from configure file

                return headers  # the first line from the configure file is the previously used columns

    return False  # if there is no correct file to configure the file
###############


def converter_to_d_m_yyyy(date_):  # 07/23/2022 or 2022-01-14  to 23.3.2022(datetime type)
    date_ = str(date_)

    # If date like: 03/17/2022 - mm/dd/yyyy
    if '/' in date_:
        changed_date = [int(i) for i in date_.split('/')]
        changed_date[-1] = changed_date[-1] + 2000

        year = changed_date[-1]
        month = zero_remove(changed_date[0])
        day = zero_remove(changed_date[1])

    # If date like: 2022-01-14 = yyyy-mm-dd
    elif '-' in date_:
        date_ = str(date_).split('-')

        year = int(date_[0])
        month = int(date_[1])
        day = int(date_[-1])

    else:
        return False
    # date_date: is the date in  date format (it wil be used to adding or subtraction the date)
    date_date = date(year, month, day)

    date_dict = {'year': year, 'month': month, 'day': day, 'date_date': date_date}

    return date_dict
###############


def clear_window_space(window, mode):
    """
    clear the date from date spase in main window
    :param window:
    :param mode: place(location) of date space
    """

    if mode == 'From':
        Label(window, width=12).place(y=190, x=35)    # clear_LbL_from

    elif mode == 'To':
        Label(window, width=12).place(y=190, x=150)   # clear_LbL_To

    """else:
         Label(window, width=12).place(y=190, x=35)   # clear_LbL_from
         Label(window, width=12).place(y=190, x=150)  # clear_LbL_To"""
###############


if __name__ == '__main__':
    main()

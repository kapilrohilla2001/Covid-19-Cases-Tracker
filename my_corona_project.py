from tkinter import *
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import plyer
import pandas as pd

def display_notification(title, message):
    plyer.notification.notify(
        title=title,
        message=message,
        app_icon=r"C:\Users\kapil\OneDrive\Desktop\Python Project\virus_corona_coronavirus_icon_140473.ico",
        timeout=10
    )

def fetch_data_and_notify():
    global selected_formats, save_path

    url = "https://www.worldometers.info/coronavirus/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')

    country_name = country_entry.get().lower() if country_entry.get() else "world"

    # Initialize lists to store data
    serial_numbers, countries, total_cases, new_cases, total_deaths = [], [], [], [], []

    for row in rows:
        columns = row.find_all('td')
        country = columns[1].text.strip().lower()

        if country == country_name:
            total_cases_value = int(columns[2].text.strip().replace(',', ""))
            total_deaths_value = columns[4].text.strip()
            new_cases_value = columns[3].text.strip()
            display_notification(f"COVID-19 Updates: {country.title()}",
                                 f"Total Cases: {total_cases_value}\nTotal Deaths: {total_deaths_value}\nNew Cases: {new_cases_value}")
        
        # Store data in lists
        serial_numbers.append(columns[0].text.strip())
        countries.append(columns[1].text.strip())
        total_cases.append(columns[2].text.strip().replace(',', ""))
        new_cases.append(columns[3].text.strip())
        total_deaths.append(columns[4].text.strip())

    # Create DataFrame
    df = pd.DataFrame({
        'Serial Number': serial_numbers,
        'Country': countries,
        'Total Cases': total_cases,
        'New Cases': new_cases,
        'Total Deaths': total_deaths
    })

    # Sort data by total cases
    sorted_df = df.sort_values(by='Total Cases', ascending=False)

    # Save data to selected formats
    for file_format in selected_formats:
        if file_format == 'html':
            file_path = f'{save_path}/coronadata.html'
            sorted_df.to_html(file_path, index=False)
        elif file_format == 'json':
            file_path = f'{save_path}/coronadata.json'
            sorted_df.to_json(file_path, orient='records', lines=True)
        elif file_format == 'csv':
            file_path = f'{save_path}/coronadata.csv'
            sorted_df.to_csv(file_path, index=False)

    # Show confirmation message
    if selected_formats:
        messagebox.showinfo("Notification", f"COVID-19 data saved at: {file_path}", parent=main_window)

# Initialize variables
selected_formats = []
save_path = ''

# Function to select HTML format
def select_html_format():
    selected_formats.append('html')
    html_button.configure(state='disabled')

# Function to select JSON format
def select_json_format():
    selected_formats.append('json')
    json_button.configure(state='disabled')

# Function to select CSV format
def select_csv_format():
    selected_formats.append('csv')
    csv_button.configure(state='disabled')

# Function to download data
def download_data():
    global save_path

    if selected_formats:
        save_path = filedialog.askdirectory()
        fetch_data_and_notify()
        selected_formats.clear()
        html_button.configure(state='normal')
        json_button.configure(state='normal')
        csv_button.configure(state='normal')
    else:
        messagebox.showwarning("Warning", "Please select a format to download.")

# Initialize main window
main_window = Tk()
main_window.title("COVID-19 Information")
main_window.geometry('800x500+200+100')
main_window.configure(bg='#E8F1F2')  # Light blue-green background

# Labels
title_label = Label(main_window, text="COVID-19 Cases Tracker", font=("Arial", 30, "bold italic"), bg="#4E878C", fg="#FFFFFF", width=33, bd=5)
title_label.place(x=0, y=0)

country_label = Label(main_window, text="Country", font=("Arial", 20, "bold italic"), bg="#E8F1F2")
country_label.place(x=5, y=100)

format_label = Label(main_window, text="Download file in", font=("Arial", 20, "bold italic"), bg="#E8F1F2")
format_label.place(x=5, y=200)

# Entry
country_entry = Entry(main_window, font=("Arial", 20), relief=RIDGE, bd=2, width=32)
country_entry.place(x=280, y=100)

# Buttons
html_button = Button(main_window, text="HTML", bg="#3498DB", font=("Arial", 15, "bold italic"), relief=RIDGE, activebackground="#2980B9", activeforeground="white", bd=5, width=5, command=select_html_format)
html_button.place(x=300, y=200)

json_button = Button(main_window, text="JSON", bg="#3498DB", font=("Arial", 15, "bold italic"), relief=RIDGE, activebackground="#2980B9", activeforeground="white", bd=5, width=5, command=select_json_format)
json_button.place(x=300, y=260)

csv_button = Button(main_window, text="CSV", bg="#3498DB", font=("Arial", 15, "bold italic"), relief=RIDGE, activebackground="#2980B9", activeforeground="white", bd=5, width=5, command=select_csv_format)
csv_button.place(x=300, y=320)

submit_button = Button(main_window, text="SUBMIT", bg="#E74C3C", font=("Arial", 15, "bold italic"), relief=RIDGE, activebackground="#C0392B", activeforeground="white", bd=5, width=25, command=download_data)
submit_button.place(x=450, y=260)

# Start main loop
main_window.mainloop()

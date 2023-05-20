# Code README
#### This code is designed to scrape data from the University of Illinois at Chicago (UIC) Mathematics, Statistics, and Computer Science (MSC) faculty profile pages. It extracts relevant information such as the name, email, and teaching schedule of each faculty member and saves the data to a JSON file. The code also includes a Flask web application that allows users to search for faculty members based on their names or teaching schedules.

### Dependencies
#### The code requires the following dependencies:

1. json
2. urllib3
3. BeautifulSoup
4. re
5. Flask
####These dependencies can be installed using the appropriate package manager for your Python environment (e.g., pip).

### Code Structure
#### The code consists of the following main functions:

### extract(site): This function takes a UIC faculty profile URL as input and extracts the relevant data such as the name, email, and teaching schedule using web scraping techniques.

### write(writeList): This function creates a dictionary from the extracted data and writes it to a JSON file.

### scrape(): This function initiates the scraping process by fetching the faculty profile pages, extracting the data for each faculty member, and calling the write() function to save the data to a JSON file.

### Details(text): This function reads the JSON file and retrieves the details (name, email, teaching schedule, and profile link) for a specific faculty member based on the provided email address.

### partialTeacher(text): This function searches for faculty members whose email addresses match a partial text input and returns the list of matching faculty members.

### searchTeacher(text): This function uses the partialTeacher() function to find faculty members whose names match a partial text input and returns the details (name, email, teaching schedule, and profile link) for all matching faculty members.

### schedSplit(text): This function searches for faculty members who have a specific class time in their teaching schedule and returns their details (name, email, teaching schedule, and profile link).

### home(): This is the main Flask route for the homepage ("/"). It handles both GET and POST requests, allowing users to search for faculty members by name or class time. The search results are saved to a temporary file ("teacher.txt" or "sched.txt") and then redirected to the appropriate page ("/teacher" or "/class") for display.

### index(): This Flask route is a clone of the homepage ("/index.html") and handles the same functionality as the home() function.

### about(): This Flask route is for the about page ("/about.html") and simply renders the "about.html" template.

### teacher(f): This Flask route displays the search results for faculty members based on name ("/teacher"). It handles both GET and POST requests, allowing users to search within the search results. The search results are read from the "teacher.txt" file and displayed on the page.

### sched(f): This Flask route displays the search results for faculty members based on class time ("/class"). It handles both GET and POST requests, allowing users to search within the search results. The search results are read from the "sched.txt" file and displayed on the page.

## Running the Code
### To run the code, ensure that you have installed the required dependencies mentioned above. Then, execute the code, and it will initiate the scraping process and start the Flask web application. The web application will be accessible at http://localhost:81/.

1. The homepage ("/" or "/index.html") allows users to search for faculty members by name or class time.
2. The search results for faculty members by name are displayed on the "/teacher" page.
3. The search results for faculty members
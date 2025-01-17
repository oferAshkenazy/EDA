EDA Tutorial
1. Using the following URL "https://f2xtjiotkmwsbxjqoasgfk.streamlit.app/" to load the app or view DEMO at EDA.mp4
2. On the main homepage choose a seaborn dataset OR Drag/Upload CSV file with DATA
3. The first 5 rows from the file will be shown
4. The "OVERVIEW" section is next
    4.1 Dataset statistics tab shows general stats like : number of cols/rows,missing data ,duplicates rows and etc.
    4.2 Alerts tab shows data on columns : Correlation,Uniformly ,Unique ,Zeros ,Duplicates and Missing .
5. Variables where data and graph on selected column is displayed.
6. Correlations shows Heat Map/Table and graph
7. Interactions shows scatter plot graph by picking : x/y columns and hue.
8. Category shows catplot graphs by picking :x/y columns
9. Missing values : histogram of missing values (if any) per column.

# How to Use the EDA Streamlit App

## Step 1: Clone the Repository
1. Open a terminal (Git Bash, Command Prompt, or PowerShell).
2. Navigate to the folder where you want to download the app:
   cd path\to\desired\directory
3. Clone the repository:
   git clone https://github.com/oferAshkenazy/EDA.git
4. Navigate into the project folder:
   cd EDA

## Step 2: Install Poetry
1. Install Poetry if it’s not already installed:
   pip install poetry
   Alternatively, follow the instructions on the Poetry website: https://python-poetry.org/docs/#installation
2. Confirm Poetry is installed:
   poetry --version

## Step 3: Install Dependencies
1. Use Poetry to set up the environment and install dependencies:
   poetry install
2. Activate the Poetry shell:
   poetry shell

## Step 4: Run the Streamlit App
1. Identify the main Streamlit file (usually main.py).
2. Start the app using Streamlit:
   streamlit run main.py
3. Open the URL shown in the terminal (e.g., http://localhost:8501) in your browser to interact with the app.

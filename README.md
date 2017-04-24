### Typeform API 

python script to interact with Typeform api and gets the response in csv format ( Execute : `python get_data.py`)

- Uses requests library
- Takes only completed responses(which can include missing response on some questions)
- Dumps the output in a csv file named `<form-id>.csv` with the header(first row) as the questions and 
respective columns as answers

### How to use? 

- Open `keys.ini` file and enter your API key
- Execute the program with python : `python get_data.py`
- Check current folder for the csv file

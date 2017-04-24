import sys
import requests

# sys.path.append("/Keboola/")

from Typeform import *
import logging, configparser

config = configparser.ConfigParser()
config.read("keys.ini")
api_key = config['DEFAULT']['API_KEY']
form_key = config['DEFAULT']['UID']

def main():

    # Sample request : https://api.typeform.com/v1/form/[typeform_UID]?key=[your_API_key]
    # Sample request : https://api.typeform.com/v1/forms?key=[your_API_key]
    url = "https://api.typeform.com/v1/forms?key={0}&completed=true".format(api_key)
    select_form = True

    #make a request
    response = requests.get(url)
    status_code = response.status_code

    # if 200 response
    if status_code == 200 and select_form:
        out_json = response.json()
        for form in out_json:
            form_id = form.get("id")
            if form_id:
                form_obj = Typeform(api_key, form_id)
                form_obj.get_data_from_form_write_to_csv()

            else:
                raise ValueError("No forms found on account!")

    else:
        raise ValueError("404 Page not found. Check your keys")




if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("keys.ini")
    print(config['DEFAULT']['API_KEY'])
    main()

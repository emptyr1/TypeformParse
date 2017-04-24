# encoding=utf8

import os
import requests
import sys
import collections
import logging
sys.path.append("/Keboola/")
import csv
import unicodedata
"""
Extracting data from typeform in CSV format using its API: https://www.typeform.com/help/data-api/
"""


class Typeform:
    """
    :Represents each typeform form and data functionality
    """
    def __init__(self, API_KEY, form_key):
        self.api_key = API_KEY
        self.form_key = form_key


    def get_data_from_form_write_to_csv(self):
        """
        :return: dictionary of {questions: answers}
        """
        # make a request
        url = "https://api.typeform.com/v1/form/{0}?key={1}&completed=true".format(self.form_key, self.api_key)

        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            out_json = response.json()

            get_formatted_questions_dict = self.questions_from_form_text(out_json.get('questions'))
            get_formatted_answers_dict = self.answers_from_form_text(out_json.get('responses'), get_formatted_questions_dict)
            self.write_to_csv(get_formatted_questions_dict, get_formatted_answers_dict)

        else:
            raise ValueError("404 Page not found. Check your keys")


    def questions_from_form_text(self, questions):
        """
        :param:
        :return: a dictionary unique {question_id: Question Text}
        """
        q_dict = {}

        for question in questions:
            q_dict[question["id"]] = question['question']
        return q_dict

    def answers_from_form_text(self, responses, q_dict):
        """
        :param responses:
        :return: Answers to every question in a deque
        """
        answers = collections.defaultdict()
        out = collections.deque()
        for resp in responses:
            d = collections.defaultdict()
            for question_id in q_dict.keys():
                d[question_id] = 'NaN'
            d.update(resp['answers'])
            out.append(d)
        return out


    def write_to_csv(self, get_formatted_questions_dict, get_formatted_answers_queue):

        filename = str(self.form_key) + ".csv"
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            try:
                # Check for unicode characters
                questions_out = list(map(lambda x : unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'),
                                         get_formatted_questions_dict.values()))

                csv_writer.writerow(questions_out)
                for resp in get_formatted_answers_queue:  # loop thru the queue
                    csv_writer.writerow(resp.values()) # write to file

            except Exception as err:
                print(err)



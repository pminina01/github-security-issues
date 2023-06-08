import os
import requests
import json
import time
import csv
import pycld2 as cld2
import regex

RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")


def remove_bad_chars(text):
    return RE_BAD_CHARS.sub("", text)

# Remove non-english
langs = {}
c_total = 0
with open(PATH + "3_issues_langs.csv", "a", newline='', encoding='utf-8') as fp:
    with open(PATH + '2_issues_sized.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            c_total += 1
            row[3] = row[3].replace('\x08', '') \
                .replace('\xad','') \
                .replace('\x19','') \
                .replace('\x1b', '') \
                .replace('\x07', '') \
                .replace('\x7f', ' ') \
                .replace('\x02', ' ') \
                .replace('\x1d', '') \
                .replace('\x10', '') \
                .replace('\x10', '') \
                .replace('\ufde8', '') \
                .replace('\uffff', '') \
                .replace('\ufdd3', '') \
                .strip()
            row[3] = remove_bad_chars(row[3])
            title = row[3]
            isReliable, _, details = cld2.detect(title)
            language = details[0][1]
            row.append(language)
            row.append(isReliable)
            writer = csv.writer(fp, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
            if language not in langs:
                langs[language] = 0
            langs[language] += 1
            # print(c_total, language,'---', title)
print(langs)

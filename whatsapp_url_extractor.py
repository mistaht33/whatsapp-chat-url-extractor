import re
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def convert_messages_to_list(f):
    """
    Convert WhatsApp Messages from File to List

    :param f: FileBuffer, FileBuffer with the opened file in read mode
    :return lines: List of WhatsApp Messages in 2 dimensional list
    """
    lines = []
    for line in f.readlines():
        line_list = line.replace("\n", "").split(",")
        if is_date(line_list[0]):
            lines.append([line_list[0], ("".join(line_list[1:]))])
        else:
            lines[-1][-1] = lines[-1][-1] + ' ' + line.replace("\n", "")
    return lines


def extract_url(message):
    """
    Regex to Extract URLs from Messages (Stackoverflow Help :smiley:)
    """
    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", message)
    return url[0] if url else None


def date_to_webkit(date_time):
    epoch_start = datetime(1601, 1, 1)
    date_ = date_time
    diff = date_ - epoch_start
    seconds_in_day = 60 * 60 * 24
    return '{:<017d}'.format(
        diff.days * seconds_in_day + diff.seconds + diff.microseconds)


def extract_page_name(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = urllib.request.Request(url=url, headers=headers)
    soup = BeautifulSoup(urllib.request.urlopen(request), features="lxml")
    if soup.title:
        if soup.title.string:
            return soup.title.string.replace("\n","")
        else:
            return "No Title"
    else:
        return "No Title"


if __name__ == '__main__':
    """
    Read in WhatsApp Conversation and Store As Text With Date, Name, URL in URLs.txt
    """
    # Open File Containing WhatsApp Chats
    cwd = '/Users/aibakitembo/Desktop/Private/WhatsApp Hackathon' #Put your directory which has the export file
    file_name = cwd + '/WhatsApp Chat with The Devs from Z.txt'
    f = open(file_name, "r")
    messages = convert_messages_to_list(f)
    whatsapp_df = pd.DataFrame(messages, columns=['date', 'message'])

    # Extract the Time and the Message from the DataFrame
    time_msg = whatsapp_df["message"].str.split("-", n=1, expand=True)
    whatsapp_df["time"] = time_msg[0]
    whatsapp_df["message"] = time_msg[1]

    # Extract the User Who Posted the Message and The Actual Message
    user_msg = whatsapp_df["message"].str.split(":", n=1, expand=True)
    whatsapp_df["user"] = user_msg[0]
    whatsapp_df["message"] = user_msg[1]

    # Drop Null Values i.e. for Messages which do not have a User e.g. "User Was Added To Group" e.t.c.
    whatsapp_df.dropna(inplace=True)

    # Create a New Column Called URL which has the Returned URL
    whatsapp_df["url"] = whatsapp_df["message"].apply(extract_url)

    # Create a New DataFrame with URLs Only
    whatsapp_grp_url = whatsapp_df.dropna()

    # Write URL's to File
    print("Writing Dataframe To Text File")
    whatsapp_grp_url.to_csv('URLs.txt', columns=["date", "user", "url"], index=None, mode='a')
    print("URL.txt created with Date, User and URL as Columns")

    # Convert URL Column to List
    list_of_urls = whatsapp_grp_url['url'].to_list()

    """
    Extract URL's as Chrome Bookmark
    """
    # Create HTML File for Bookmarks
    print("Building Chrome Bookmark HTML")
    standard_header = f"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!-- This is an automatically generated file. It will be read and overwritten. DO NOT EDIT! -->
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks</H1>
    <DL><p>
        <DT><H3 ADD_DATE="{date_to_webkit(datetime.now())}" LAST_MODIFIED="">Whatsapp Imports</H3>
        <DL><p>
    """

    bookmark_file = [standard_header]
    for url in list_of_urls:
        bookmark_file.append(
            f'\t\t<DT><A HREF="{url}" ADD_DATE="{date_to_webkit(datetime.now())}" '
            f'ICON="">{extract_page_name(url)}</A>\n')
    bookmark_file.append(f'''\t<DL><p>
    <DL><p>''')
    print("Chrome Bookmark HTML Creation Completed..")
    # Write to Bookmark File
    with open('chrome_bookmark.html', 'w') as bookmark_html:
        for line in bookmark_file:
            bookmark_html.write(line)
    print("HTML Bookmark File Written")

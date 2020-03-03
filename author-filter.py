import sys
import re

ENTRY_BREAKER = "\n==========\n"

def prepare_info(file, author):
     entries = [string for string in file.replace(u'\ufeff', '').split(ENTRY_BREAKER) if string != ""]
     return filter(None, [select_entry(entry, author) for entry in entries])

def select_entry(entry, author):
     info = entry.splitlines()
     if len(info) != 4: return # not including bookmarks
     book_author = re.search(r'\((.+)\)', info[0]).group(1)
     if book_author == author: return get_entry_info(info) 

def get_entry_info(info):
     entry = {}
     entry["title"] = re.search(r'(.+) \(', info[0]).group(1)
     useful_info = re.split("- Your (.*) at location (.*) \| Added on \w+, (.*) \d{2}\:\d{2}\:\d{2}", info[1])
     entry["type"], entry["location"], entry["date"] = [info for info in list(filter(None, useful_info))]
     entry["content"] = info[3].replace(u'\xa0', u'')
     return entry

def export(prepared_info, author):
     with open('Kindle - {}.txt'.format(author), 'w') as f:
          for info in prepared_info:
               f.write("{} ({}, {}, {}, location: {}) \r\n\n".format(info["content"], info["title"], info["type"], info["date"], info["location"]))

if __name__ == '__main__':
     try:
          file = open('My Clippings.txt', encoding='utf-8-sig').read() 
          if len(sys.argv) != 2:
               author = input("Enter author name: ").strip()
          else: 
               author = sys.argv[1]
          export(prepare_info(file, author), author)
     except: 
          print("Please put 'My Clippings.text' in the same directory as this program.")
          
#First run 'pip install pyshorteners' in terminal of pycharm then execute the below program
import pyshorteners

url = input('Enter Any Webpage address to Short: ')


def shortenurl(url):
    s = pyshorteners.Shortener()
    print('Your Shorted URL is: ',s.tinyurl.short(url))

shortenurl(url)

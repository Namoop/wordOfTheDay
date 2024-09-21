import os
import random
import re
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from wordfreq import zipf_frequency

# Allows the user to specify a game number to scrape
# archive = "/archive/game?num=" + sys.argv[1] if len(sys.argv) > 1 else ""
site= "https://wordgrid.clevergoat.com" # + archive

# Scrape the conditions from the site
def scrape_conditions():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(site)
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    conditions = []
    for div in soup.find('app-game').find_all('div'):
        for span in div.find_all('span'):
            conditions.append(span.text)

    # Conditions are inconsistently digits or words, so replace the words with digits
    conditions = [
        cond.replace("Four", "4")
            .replace("Five", "5")
            .replace("Six", "6")
            .replace("Seven", "7")
            .replace("Eight", "8")
        for cond in conditions]
    return conditions[:6] # The first six of these elements are the conditions


# Map the conditions to a regex pattern
def convert_to_regex(conditions):
    regex_patterns = []
    for condition in conditions:
        if re.search("\\d letter word", condition):
            regex_patterns.append("^\\w{" + re.search("\\d", condition).group() + "}$")
        if re.search("Starts with", condition):
            regex_patterns.append("^" + re.search("(?<=Starts with )\\w+", condition).group())
        if re.search("Ends with", condition):
            regex_patterns.append(re.search("(?<=Ends with )\\w+", condition).group() + "$")
        if re.search("Contains \\w, \\w, \\w", condition):
            letter1 = re.search("(?<=Contains )\\w", condition).group()
            letter2 = re.search("(?<=, )\\w", condition).group()
            letter3 = condition[-1]
            regex_patterns.append(
                ".*" + letter1 + ".*" + letter2 + ".*" + letter3 + "|" + ".*" + letter1 + ".*" + letter3 + ".*" + letter2 + "|" + ".*" + letter2 + ".*" + letter1 + ".*" + letter3 + "|" + ".*" + letter2 + ".*" + letter3 + ".*" + letter1 + "|" + ".*" + letter3 + ".*" + letter1 + ".*" + letter2 + "|" + ".*" + letter3 + ".*" + letter2 + ".*" + letter1)
            continue
        if re.search("Contains \\w, \\w", condition):  # should output x.*y|y.*x
            letter1 = re.search("(?<=Contains )\\w", condition).group()
            letter2 = re.search("(?<=, )\\w", condition).group()
            regex_patterns.append(".*" + letter1 + ".*" + letter2 + "|" + letter2 + ".*" + letter1)
            continue
        if re.search("Contains \\w", condition):
            regex_patterns.append(".*" + re.search("(?<=Contains )\\w+", condition).group() + ".*")
        if re.search("Multiple letter", condition):  # eg multiple letter x's
            regex_patterns.append(r"(.*" + re.search("(?<=Multiple letter )\\w+", condition).group() + r".*){2,}")
        if re.search("Double letter", condition):
            regex_patterns.append(r"(\w)\1")
        if re.search("Starts & ends with", condition):
            letter = re.search("(?<=Starts & ends with )\\w", condition).group()
            regex_patterns.append("^" + letter + ".*" + letter + "$")
    return regex_patterns

def select_word(pattern1, pattern2, max_freq = 1):
    # Read the wordlist.txt file
    words = open(os.path.dirname(os.path.realpath(__file__)) + '/wordlist.txt', 'r').read().splitlines()
    words = [line.split('\t') for line in words]  # Split it into two lists, one for words and one for definitions
    words = [[line[0].lower(), line[1]] for line in words]  # Make the words lowercase

    # Limit the wordlist to the words that match the patterns
    words = [line for line in words if re.match(pattern1, line[0]) and re.match(pattern2, line[0])]

    # Sort the words by frequency
    words = sorted(words, key=lambda x: zipf_frequency(x[0], 'en'))

    # Limit the wordlist to the first 10% of the words
    words = words[:len(words) // 10]

    # Get a random word from the wordlist
    word = random.choice(words)
    return word

def randword():
    conditions = scrape_conditions()
    conditions = conditions[:6]
    regex_patterns = convert_to_regex(conditions)

    # Select one of the first three and one of the second three patterns, ie, select a grid square
    row = random.randrange(0, 3)
    pattern1 = regex_patterns[row]
    condition1 = conditions[row]
    column = random.randrange(3, 6)
    pattern2 = regex_patterns[column]
    condition2 = conditions[column]

    word = select_word(pattern1, pattern2)
    return dict({
        'word': word[0],
        'definition': word[1],
        'condition 1': condition1,
        'condition 2': condition2
    })
import re
from pathlib import Path

inside_per = False
inside_loc = False

def extract_names_aba(element: object) -> str:
    """Takes a beautiful soup object and removes all tags except person and place names as they appear in the ABaCus dataset.

    Args:
        element (beautiful soup object): the object to extract names from

    Returns:
        str: The text without any tags, except for the name tags.
    """
    for tag in element.find_all(True):
        if (tag.name == 'persName' and not tag.parent.name == 'persName') or (tag.name == 'placeName' and not tag.parent.name == 'placeName'):
            continue  # Skip Named Entities
        else:
            tag.unwrap()  # Remove the tag, keeping its content

    # Get the processed HTML content
    processed_html = str(element)

    return processed_html

def extract_names(html: object) -> str:
    """Finds and unwraps all tags except <a> tags with href starting with "E01"

    Args:
        html (object): The beautifulsoup object

    Returns:
        str: the text stripped of all tags except <a href="E01">
    """

    # 
    for tag in html.find_all(True):
        if tag.name == 'a' and (tag['href'].startswith('E01') or tag['href'].startswith('E03')):
            continue  # Skip <a> tags with href starting with "E01"
        else:
            tag.unwrap()  # Remove the tag, keeping its content

    # Get the processed HTML content
    processed_html = str(html)

    return processed_html


def create_name_list(sermon: str) -> list:
    """creates a list of all names with markup tags

    Args:
        sermon (str): the string to be searched

    Returns:
        list: a matrix with the list of persons at index 0 and the list of places at index 1
    """
    
    pattern_1 = r'<PERSON>(.*?)</PERSON>'
    persons = re.findall(pattern_1, sermon)

    pattern_2 = r'<LOCATION>(.*?)</LOCATION>'
    locations = re.findall(pattern_2, sermon)

    matches = [persons, locations]
    return matches


def sermon_cleanup(sermon: str) -> str:
    """Takes a sermon and applies a range of cleaning jobs, mainly to get rid of superfluous dots

    Args:
        sermon (the sermon): The text to be cleaned up

    Returns:
        str: the cleaned up text
    """
    
    # load lists of abbreviations
    with open("bible_abbr.txt") as bible:
        bible_abbrs = [line.rstrip('\n') for line in bible]

    with open("latin_abbr.txt") as latin:
        latin_abbrs = [line.rstrip('\n') for line in latin]
    
    # add spaces around tags
    sermon = re.sub(r'</PERSON>(\S)', r'</PERSON> \1', sermon)
    sermon = re.sub(r'(\S)<PERSON>', r'\1 <PERSON>', sermon)
    sermon = re.sub(r'</LOCATION>(\S)', r'</LOCATION> \1', sermon)
    sermon = re.sub(r'(\S)<LOCATION>', r'\1 <LOCATION>', sermon)

    # replace all kinds of unnecessary characters
    sermon = re.sub(r'(?<!<)/', '', sermon)
    
    sermon = sermon.replace("|", "").replace("\n", " ").replace("\r", " ")
    sermon = sermon.replace("\xa0", "").replace("\u2002", "")
    sermon = sermon.replace("[vakat]", "")
    sermon = sermon.replace("[", "").replace("]", "")
    sermon = sermon.replace('<div class="edition">', '').replace("</div>", "")
    sermon = sermon.replace('Einzelanmerkungen', '').replace("<div>", "")
    sermon = sermon.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
    sermon = sermon.replace("»", "").replace("«", "").replace("‹", "").replace("›", "")
    
    # useless parentheses
    sermon = re.sub(r"\((\S){1,3}\)", "", sermon)
    sermon = re.sub(r" ([A-Za-z]|[0-9]|\*+)\)", " ", sermon)

    # add spaces after sentences
    sermon = re.sub(r"([\.\?!,;:])(\w)", r"\1 \2", sermon)

    # deal with hyphens
    sermon = re.sub(r'[=|-](\s*)und', '- und', sermon)
    sermon = re.sub(r'[=|-](\s*)(?!und)([a-zäöüß])', r'\2', sermon)
    sermon = re.sub(r'[=|-](\s*)([A-ZÄÖÜ])', r' \2', sermon)
    
    # remove pointlessly confusing punctuation
    sermon = sermon.replace('"', '').replace("'", "")
    sermon = sermon.replace('“', '').replace("", "")
    sermon = sermon.replace('”', '').replace("", "")
    sermon = sermon.replace('‘', '').replace("", "")
    sermon = sermon.replace('’', '').replace("", "")
    sermon = sermon.replace('{', '').replace("}", "")
    sermon = sermon.replace('´', '').replace("`", "")
    sermon = sermon.replace('§', '')
    sermon = sermon.replace('))', '')
    sermon = sermon.replace('☿', '')
    sermon = sermon.replace('*', '')
    sermon = sermon.replace('‚', '')
    sermon = sermon.replace('„', '')
    sermon = sermon.replace('–', '').replace('─', '').replace('-', '')
    
    # remove as many confusing dots as possible
    sermon = re.sub(r"(\S)\.([a-z])", r"\1\2", sermon)
    sermon = re.sub(r"St\.", "St", sermon)
    sermon = re.sub(r"Cap\.", "Cap", sermon)
    sermon = re.sub(r"cap\.", "Cap", sermon)
    sermon = re.sub(r"Hist\.", "Hist", sermon)
    sermon = re.sub(r"( \w)\.", r"\1", sermon)
    sermon = re.sub(r"([0-9])\.", r"\1", sermon)
    sermon = re.sub(r"([A-Z])\.", r"\1", sermon)

    # Abraham specific cleanup
    sermon = sermon.replace("Oe.", "Oe")
    sermon = sermon.replace("Maj.", "Maj").replace("Majest.", "Majest")
    sermon = sermon.replace("Röm.", "Röm")
    sermon = sermon.replace("Käyserl.", "Käyserl").replace("Kays.", "Kays")
    sermon = re.sub(r"([A-Z])\.", r"\1", sermon)

    sermon = sermon.replace("n̅", "nn")
    sermon = sermon.replace("m̅", "mm")
    sermon = sermon.replace("e̅", "en")

    # remove dots in tags
    sermon = re.sub(r"<(PERSON|LOCATION)>(\w+\.( \w+\.)*)</(PERSON|LOCATION)>", 
                    lambda match: f"<{match.group(1)}>{match.group(2).replace('.', ' ')}</{match.group(1)}>", 
                    sermon)
    sermon = re.sub(r"<(PERSON|LOCATION)>(\w+:( \w+:)*)</(PERSON|LOCATION)>", 
                    lambda match: f"<{match.group(1)}>{match.group(2).replace(':', ' ')}</{match.group(1)}>", 
                    sermon)
    sermon = re.sub(r"(\.|,|:|\?|!)</(PERSON|LOCATION)>", r"</\2>\1", sermon)
    #sermon = sermon.replace(".</PERSON>", "</PERSON>.")
    #sermon = sermon.replace(".</LOCATION>", "</LOCATION>.")
    
    # tighten tags
    sermon = sermon.replace("<PERSON> ", "<PERSON>")
    sermon = sermon.replace("<LOCATION> ", "<LOCATION>")
    sermon = sermon.replace(" </PERSON>", "</PERSON>")
    sermon = sermon.replace(" </LOCATION>", "</LOCATION>")

    # get rid of bible and latin abbreviation dots
    for x in bible_abbrs:
        sermon = sermon.replace(f" {x}.", f" {x}")
    for x in latin_abbrs:
        sermon = sermon.replace(f" {x}.", f" {x}")
    
    sermon = sermon.replace("&amp;", "und")
    sermon = sermon.replace("&gt;", "")
    sermon = sermon.replace("&lt;", "")
    sermon = sermon.replace("&quot;", "")
    sermon = sermon.replace("&apos;", "")
    
    return sermon


def word_to_row(word: str) -> list:
    """Takes a word and depending on present tags 
    and the GLOBAL VARIABLES inside_per and inside_loc assigns it a BIO-tag

    Args:
        word (str): The string to process

    Returns:
        list: A list with the word (cleaned of tag elements) and its assigned BIO-tag
    """
    
    global inside_per
    global inside_loc
    if word.startswith("<PERSON>"):
        if not word.endswith("</PERSON>"):
            inside_per = True
        return [word.replace("<PERSON>", "").replace("</PERSON>", ""), "B-PER"]
    elif word.endswith("</PERSON>"):
        inside_per = False
        return [word.replace("</PERSON>", ""), "I-PER"]
    elif inside_per:
        return [word, "I-PER"]
    
    if word.startswith("<L"):
        if not word.endswith("</LOCATION>"):
            inside_loc = True
        return [word.replace("<LOCATION>", "").replace("</LOCATION>", ""), "B-LOC"]
    elif word.endswith("</LOCATION>"):
        inside_loc = False
        return [word.replace("</LOCATION>", ""), "I-LOC"]
    elif inside_loc:
        return [word, "I-LOC"]
    
    else:
        return [word, "O"]
    

def get_long_names(sermon: str) -> list:
    """Creates a list of all "long names" in a given text which can then be filtered out

    Args:
        sermon (str): the text to be searched

    Returns:
        list: the list of long names
    """
    # names longer than 5 words ("Ernst Graff zu Schauenburg und Hollstein")
    tags1 = [x[0] for x in re.findall(r"(<PERSON>\w+\s\w+\s\w+\s\w+(\s\w+)+</PERSON>)", sermon)]

    # names longer than 3 words that contain no nobiliaries ("Landes Fürsten und Herrns")
    tags2 = [x[0] for x in re.findall(r"(<PERSON>\w+\s\w+\s\w+\s\w+\s\w+</PERSON>)", sermon)]
    tags2 = [x for x in tags2 if bool(re.search(r' zu | von | de ', x))]
    
    return tags1 + tags2

def make_sentences(list: list) -> list:
    """Takes a list of tokens and creates a list of sentences created from the tokens

    Args:
        list (The list of tokens): A list of tokens. Sentences are expected to be divided by NaN values

    Returns:
        list: A list of all generated sentences
    """
    return_list = []
    sentence = ''
    for x in list:
        if isinstance(x, str):
            if x in [".", "!", "?", ":", ",", ";"]:
                sentence += x
            else:
                sentence += (" " + x)
        else:
            return_list.append(sentence)
            sentence = ''
    return_list.append(sentence)
    return return_list

def bio_helper(prev, now):
    if now == "O":
        return now
    if prev == "B-" + str(now):
        return "I-" + str(now)
    else:
        return "B-" + str(now)
    
def transform_to_BIO(values: list) -> list:
    transformed_values = []
    previous_value = None

    for value in values:
        if isinstance(value, str) and (value != ""):
            if value == "O":
                transformed_values.append(value)
            elif value != previous_value:
                transformed_values.append("B-" + value)
            else:
                transformed_values.append("I-" + value)
            previous_value = value
        else:
            transformed_values.append(value)
    
    return transformed_values

def check_bio_validity(list: list, pattern: object = re.compile("(^\S+\t(B-PER|I-PER|B-LOC|I-LOC|O)$|^$)")) -> bool:
    """Checks if a list follows BIO annotation standard

    Args:
        list (list): The list to check
        pattern (re.compile object): The pattern to check for (word-tab-BIO format per default)

    Returns:
        bool: _description_
    """
    error_list = []
    for idx, line in enumerate(list):
        if not pattern.match(line):
            error_list.append(idx)
    if len(error_list) > 0:
        print(f"Errors in the list! Indices of problematic lines: {*error_list,}")
        return False
    else:
        return True
    
def read_conll_data(path: str) -> tuple:
    """ Takes a path to a data file and returns a tuple with the tokens and labels

    Args:
        path (str): the path to the file (requires imported Path from pathlib!)

    Returns:
        tuple: tuple[0] is a list of sentences, each with a list of tokens
               tuple[1] is a list of sentences, each with a list of labels
    """
    path = Path(path)

    raw_text = path.read_text().strip()
    raw_docs = re.split(r'\n\t?\n', raw_text)
    token_docs = []
    tag_docs = []
    for doc in raw_docs:
        tokens = []
        tags = []
        for line in doc.split('\n'):
            token, tag = line.split('\t')
            tokens.append(token)
            tags.append(tag)
        token_docs.append(tokens)
        tag_docs.append(tags)

    return token_docs, tag_docs

def find_good_split(list: list, index:int = 250) -> list:
    """ Takes a list of [token, label] lists and splits it 
    so that entities don't get separated,
    starting at the given index and going further down the list
    until the split is no longer within an entity.

    Args:
        list (list): The list to split
        index (int): The place to attempt the first split,
        defaults to 250

    Returns:
        list: a list with the splitted sentences
    """
    if list[index][1] not in ("I-PER", "I-LOC"):
        if len(list[:index]) < 300:
            return [list[:index], list[index:]]
        else:
            return [find_good_split(list[:index], int(index/2)),
                    find_good_split(list[index:], int(index/2))]
    else:
        return find_good_split(list, index + 1)

def list_transformer_results(sentence: str, predictions: list) -> tuple:
    words = sentence.split(" ")

    results = []

    running_char = 0
    for word in words:
        found_match = next((d for d in predictions if d.get("start") == running_char), None)
        if found_match:
          
            results.append(found_match.get("entity_group"))
        else:
            results.append("O")
        running_char += len(word) + 1

    return words, results

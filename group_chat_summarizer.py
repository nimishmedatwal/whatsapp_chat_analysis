import regex as re
import datetime
from dateutil.parser import parse
import google.generativeai as palm
import Constants
import nltk
from nltk.corpus import treebank
from nltk import Tree
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame

DATE_PATTERN = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
datepattern = '\d{1,2}/\d{1,2}/\d{2,4}'
SUMMARY_PROMPT = f""""Please summarize in 1000 words the following WhatsApp group chat based on topics that were discussed. For each topic, include its title and summary in bullet points. The bullets should include detailed information. If the topic includes recommendations about specific companies or services, please include them in the summary. Please include links that were shared. Ignore messages with null and <Media omitted> and joined using this group's invite link, requested to join."""
NEWSLETTER_PROMPT = f"""Please provide one paragraph to open a newsletter covering the following topics:"""
TIME_PER_MESSAGE = 0.015  # seconds
MAX_WORD_COUNT = 2500


palm.configure(api_key=Constants.API_KEY)

def read_file(file_path):
    bytes_data = file_path.getvalue()
    content = bytes_data.decode("utf-8")
    return content


def whatsapp_remove_sender(message, keep_date=False):
    start = message.find('] ')
    finish = message.find(': ')

    if keep_date:
        return message[:(start + 2)] + 'member: ' + message[(finish + 2):]
    else:
        return 'MESSAGE: ' + message[(finish + 2):]


def parse_whatsapp(text):
    message_splits = re.split(DATE_PATTERN, text)
    dates = re.findall(datepattern, text)

    parsed_messages = []
    for i in range(2, len(message_splits)):
        message = message_splits[i-1]
        date=dates[i-1]
        date = parse(date).date()
        message = whatsapp_remove_sender(message)
        parsed_messages.append((date, message))
    return parsed_messages


def filter_messages_by_dates(messages, start_day, end_day):
    filtered = []
    for message in messages:
        if message[0] < start_day:
            continue
        elif message[0] > end_day:
            break

        filtered.append(message)

    return filtered


def whatsapp_chunk_text(messages):
    current_word_count = 0
    current_chunk = ''
    chunks = []
    for _, message in messages:
        message_word_count = len(message.split())
        if current_word_count + message_word_count > MAX_WORD_COUNT:
            chunks.append(current_chunk.strip())
            current_chunk = ''
            current_word_count = 0

        current_chunk += message
        current_word_count += message_word_count

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def palm_api(prompt, model):
    completion = palm.generate_text(model=model, prompt=prompt, temperature=1, candidate_count=1)
    print(completion.result)
    return completion.result

def generate_and_draw_tree(text):
    tokens = nltk.word_tokenize(text)
    tagged_tokens = nltk.pos_tag(tokens)

    grammar = r"""
        NP: {<DT>?<JJ>*<NN>}   # noun phrase
        PP: {<IN><NP>}         # prepositional phrase
        VP: {<VB.*><NP|PP>*}   # verb phrase
    """
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(tagged_tokens)

    # Draw the tree
    tree.draw()

def draw_tree(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), tree)
    cf.add_widget(tc, 10, 10)
    cf.print_to_file('tree.png')
    cf.destroy()

def summarize_text(text, model):
    # generate_and_draw_tree(text)
    prompt = f""""{SUMMARY_PROMPT}\n\n {text}"""
    return palm_api(prompt, model)

    
def generate_newsletter_intro(text, model):
    prompt = f""""{NEWSLETTER_PROMPT}\n\n {text}"""
    return palm_api(prompt, model)


def summarize_messages(chunks, model):
    summary = ''
    calls_counter = 0
    for chunk in chunks:
        calls_counter += 1
        print(f"Sending prompt {calls_counter} out of {len(chunks)} Chunk size: {len(chunk)}")
        chunk_summary = summarize_text(chunk, model)
        summary += chunk_summary + '\n\n'

    return summary


def main( chat_export_file, summary_file, start_day_s, end_day_s, is_newsletter, model):
    start_day = datetime.datetime.strptime(start_day_s, '%m/%d/%Y').date()
    end_day = datetime.datetime.strptime(end_day_s, '%m/%d/%Y').date()

    content = read_file(chat_export_file)
    parsed_messages = parse_whatsapp(content)
    filtered_messages = filter_messages_by_dates(
        parsed_messages, start_day, end_day)
    chunks = whatsapp_chunk_text(filtered_messages)
    summary = summarize_messages(chunks, model)

    if is_newsletter:
        intro = generate_newsletter_intro(summary, model)
        summary = intro + '\n\n' + summary

    print(('*' * 10) + '\nSummary:\n' + ('*' * 10))
    print(summary)

    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)


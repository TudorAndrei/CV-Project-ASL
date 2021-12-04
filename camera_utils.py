import collections
import datetime

output_string = []
last_characters = collections.deque()
now = 0
timestamp = 0
string_to_process = []

letter = 0
confs = 0
ACC = 30


def get_one_letter(confs, letters):
    if confs:
        max_value_per_confs = max(confs)
        max_index = confs.index(max_value_per_confs)
        letters = letters[max_index]
        confs = confs[max_index]
    return confs, letters


def get_time(letter):
    global last_characters, timestamp
    now = datetime.datetime.now()
    timestamp = int(round(now.timestamp()))
    last_characters.append([timestamp, letter])
    # print(last_characters)
    return last_characters


def create_dic(the_list):
    dic = {x: the_list.count(x) for x in the_list}
    return dic


def get_necessary_letter(the_dic):
    max_key = max(the_dic, key=the_dic.get)
    return max_key


def process_time():
    global timestamp, last_characters, output_string
    # print(last_characters)
    # print(output_string)
    if (timestamp - last_characters[0][0]) >= 3:
        for i in range(len(last_characters)):
            if last_characters[i][1] is not []:
                string_to_process.append(last_characters[i][1])
        last_characters.clear()
        # print(string_to_process)
    if string_to_process:
        # print(last_characters)
        dic = create_dic(string_to_process)
        letter = get_necessary_letter(dic)
        string_to_process.clear()
        # print((dic[letter] * 100) / sum(dic.values()))
        if (dic[letter] * 100) / sum(dic.values()) >= ACC:
            # print(output_string)
            if output_string:
                if output_string[-1] != letter:
                    output_string.append(letter)
                    # print(output_string)
            else:
                output_string.append(letter)
    # print(output_string)


def process(confs, letters):
    global output_string
    # print(confs, letters)
    _, letters_ = get_one_letter(confs, letters)
    # print(letters_)
    get_time(letters_)
    process_time()

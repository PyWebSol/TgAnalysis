import json
from collections import Counter
from tabulate import tabulate
import re

class config:
    FILENAME = input("Введите имя файла JSON: ")
    tablefmt = "outline"

open("result.txt", "w").close()

def printAndWrite(text: str):
    with open("result.txt", "a", encoding="utf-8") as file:
        file.write(text)
        file.write("\n")
    print(text)

def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # Эмодзи эмоций
                           u"\U0001F300-\U0001F5FF"  # Эмодзи времени
                           u"\U0001F680-\U0001F6FF"  # Эмодзи транспорта
                           u"\U0001F700-\U0001F77F"  # Эмодзи символов
                           u"\U0001F780-\U0001F7FF"  # Эмодзи геометрии
                           u"\U0001F800-\U0001F8FF"  # Эмодзи знаков
                           u"\U0001F900-\U0001F9FF"  # Эмодзи дополнительных символов
                           u"\U0001FA00-\U0001FA6F"  # Эмодзи олимпиады
                           u"\U0001FA70-\U0001FAFF"  # Эмодзи еды
                           u"\U0001F004-\U0001F0CF"  # Эмодзи масти карт
                           u"\U0001F0D0-\U0001F0FF"  # Эмодзи игральных костей
                           u"\U0001F200-\U0001F251"  # Эмодзи символов
                           "]+", flags=re.UNICODE)

    text_without_emojis = emoji_pattern.sub(r'???', text)
    return text_without_emojis.strip()

def fixText(text: str):
    result = text.replace("ꠋ", "?")

    return result

with open(config.FILENAME, "r", encoding="utf-8") as dataFile:
    data = json.load(dataFile)

texts = []
dates = []
words = []
userMessagesCount = []
datesMessagesCount = []

for message in data["messages"]:
    if "text" in message:
        if len(message["text"]) != 0:
            if type(message["text"]) != str:
                text: str = "".join([(v["text"] if type(v) != str else str(v)) for v in message["text"]])
            else:
                text: str = message["text"][0]
            dateTime: str = " ".join(message["date"].split("T"))
            fromId: str = message["from_id"]
            fromName: str = fixText(message["from"].strip()) if message["from"] else "null"
            fromName = fromName[:25] + "..." if len(fromName) > 25 else fromName
            
            date: str = message["date"].split("T")[0]

            datesMessagesCount.append(date)

            if fromId.startswith("user"):
                fromId = fromId.replace("user", "")
            elif fromId.startswith("channel"):
                fromId = fromId.replace("channel", "")

            userMessagesCount.append(f"{fromId} \ {fromName}".replace('\n', '').strip())
            if text:
                texts.append(text.strip().lower())
                dates.append(dateTime)
                for wrd in text.replace("http://", "").replace("https://", "").replace("«", "").replace("»", "").replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ").replace(",", " ").replace(".", " ").replace(":", " ").replace(";", " ").strip().split(" "):
                    for word in wrd.split("\n") if "\n" in wrd else [wrd]:
                        if len(word.strip()) > 2:
                            words.append(word.replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ").strip().lower())

counterWords = Counter(words)

mostCommonWords = counterWords.most_common(15)

counterUsers = Counter(userMessagesCount)

mostCommonUsers = counterUsers.most_common(10)

counterDates = Counter(datesMessagesCount)

mostCommonDates = counterDates.most_common(10)

printAndWrite(f"Отчет по чату \"{data['name']}\"")

printAndWrite("\n")

printAndWrite(f"Дата создания: {' '.join(data['messages'][0]['date'].split('T'))}")

printAndWrite("")

printAndWrite(f"ID чата: {data['id']}")

printAndWrite("")

printAndWrite(f"Дата отправки первого сообщения: {dates[0]}")

printAndWrite("")

printAndWrite(f"Первое сообщение:")
printAndWrite(texts[0])

printAndWrite("")

printAndWrite(f"Количество текстовых сообщений в чате: {len(texts)}")

printAndWrite("")

printAndWrite("Самые популярные слова в чате:")

tableMostCommonWords = tabulate(mostCommonWords, tablefmt=config.tablefmt, headers=["Слово", "Повторения"])

printAndWrite(tableMostCommonWords)

printAndWrite("")

printAndWrite("Самые общительные пользователи:")

tableMostCommonUsers = tabulate(mostCommonUsers, tablefmt=config.tablefmt, headers=["ID / Имя", "Сообщения"])

printAndWrite(tableMostCommonUsers)

printAndWrite("")

printAndWrite("Дни, когда было отправлено больше всего сообщений:")

tableMostCommonDates = tabulate(mostCommonDates, tablefmt=config.tablefmt, headers=["Дата", "Сообщения"])

printAndWrite(tableMostCommonDates)
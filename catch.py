import stanza
stanza.download('ru')


def stanza_nlp_ru(text: str):
    nlp = stanza.Pipeline(lang='ru', processors='tokenize,ner')
    doc = nlp(text)
    with open('result.txt', 'a', encoding='utf-8') as file:

        [file.write(f'entity: {ent.text}\ttype: {ent.type}\n') for sent in doc.sentences for ent in sent.ents]

def main():
    with open('write.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    stanza_nlp_ru(text)

if __name__ == '__main__':
    main()

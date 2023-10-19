import PyPDF2
import enchant 

# I had to run these to get it to find enchant c lib on my m1...
# export DYLD_LIBRARY_PATH=/opt/homebrew/lib/
# export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib
def extract_text_from_pdf(pdf_path):
    word_dict = {}
    d = enchant.Dict("en_US")
    common_words = get_common('common.txt')

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                for word in text.split():
                    checkable = word.lower()
                    # if not d.check(word) or word in common_words:
                        # continue
                    if should_skip(checkable, common_words):
                        continue

                    if checkable in word_dict:
                        word_dict[word].append(page_num)
                    else:
                        word_dict[word] = [page_num]
    except Exception as e:
        print(e)

    # print(len(word_dict))
    return word_dict

def should_skip(word, common_words):
    return len(word) < 3 or word in common_words or not is_valid(word)

def is_valid(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz-'
    for letter in word:
        if letter not in alphabet:
            return False
    return True

def get_common(file_path):
    file = open(file_path, 'r')
    words = [] 
    for line in file.readlines():
        words.append(line.strip())
    return words

if __name__ == '__main__':
    d = extract_text_from_pdf('/Users/daghjelm/Downloads/DASAK_sammanfattning.pdf')
    d = dict(sorted(d.items()))
    # print(get_common('common.txt'))

    # for key in d:
    #    print(key, d[key])
    file = open('occurances.txt', 'w')
    for key in d:
        file.writelines(key + ' ' + str(d[key]) + '\\\\ \n')

    print(len(d))

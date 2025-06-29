def word_frequency_counter(file_path,top_n):
    words_dict=read_file_content_to_dictionary(file_path)#Turns the file into a dictionary with each word the number of times it appears.
    sorted_dict=dict(sorted(words_dict.items(),key=lambda item: item[1],reverse=True)[:top_n])
    for key, value in sorted_dict.items():
        print("Word: "+key+" Appears "+str(value)+" times")



def read_file_content_to_dictionary(file_path):
    d={}
    with open(file_path) as file:
        for line in file:
            words=line.split()
            for word in words:
                if word in d:
                    d[word]+=1
                else:
                    d[word]=1
    return d



file_path="test_words.txt"
top_n=2
word_frequency_counter(file_path,top_n)#print the N words that apears the max time in the file

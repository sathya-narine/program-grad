import re
import string

#function to clean the token 
def cleanToken(token):
    match = re.search(r'[a-zA-Z]+', token) #matches for letters - referenced from stack over flow
    if not match or len(token)==1:
        #discards non-word tokens, single letter cannot be token
        return ''
    low_case_token = token.lower()  #converting to lower case
    #clean_token = re.sub(r"(^[^\w]+)|([^\w]+$)", "",low_case_token) 
    clean_token = low_case_token.strip(string.punctuation)
    #strip removes leading and trailing punctuations leaving the in between punctuations untouched 
    #same is applied at begin and end,substitued by '' we get clean token.
    return clean_token 
    
#function process the file to create forward index
def readDocs(dbfile):
    fh = open(dbfile,"r", encoding="utf8") #opens the file in read mode           
    next_line = True 
    #initialising the urls and forward index
    cur_url = ''
    words_list= set() #initialising as set to avoid  repeated words
    forw_dict={}
    while next_line:
        line = fh.readline() #read line reads the content from handler line by line
        if not line:
            #it's the of the eof
            next_line = False
        if line.startswith('https'):
            #set the current url
            cur_url=line.strip('\n')
        elif line.startswith('<pageBody>'):
            #start appending values to the key
            forw_dict[cur_url]=words_list
        elif line.startswith('<endPageBody>'):
            #reset key value pair for next url processing
            cur_url=''
            words_list=set()
        else:
            #clean the tokens
            contents = line.split()
            for token in contents:
                clean_token = cleanToken(token)
                forw_dict[cur_url].add(clean_token)
                
    page_count = 0
    word_count = 0
    for k, v in forw_dict.items():
        page_count+=1
        word_count+=len(v)
    print(f'Indexed {page_count} web pages containing {word_count} unique terms.')   
    return forw_dict 
        
#this function takes the forward index and converts to inverted index
def buildInvertedIndex(forw_index):
    inverted_index={}
    #traverse the each values of forw_index to create inverted index
    for key,values in forw_index.items():
        for token in values:
            is_present = inverted_index.get(token,0) #first try to fetch
            if is_present: 
                #if present add it set
                inverted_index[token].add(key)
            else:
                #if not present add the token as key and url as value
                inverted_index[token]=set((key,))
    return inverted_index
 
#this function process the query string and searches in the index for results  
def findQueryMatches(index,query):
    process_query = query.split() #split the compound query into sub queries
    final_url_set = set()
    if len(process_query)==1:   #if it's a single query,it's a direct search
        clean_query = cleanToken(query) #calling clean token to have more accurate search in index
        final_url_set = index.get(clean_query,'')
    else:
        #for compound query
        for sub_query in process_query:
            if sub_query[0] == '-':
                #if it's '-' we need url that doesn't contain these word, so difference b/w sets
                srch_query = cleanToken(sub_query[1:])
                urls = index.get(srch_query,'')
                final_url_set = final_url_set.difference(urls)
            elif sub_query[0] == '+':
                #if it's '+' we need url that must and should contain both word, so intersection ie common b/w sets
                srch_query = cleanToken(sub_query[1:])
                urls = index.get(srch_query,'')
                final_url_set = final_url_set.intersection(urls)
            else:
                #if it doesn't have any prefixes then the results should be union ie added/combine both 
                srch_query = cleanToken(sub_query)
                urls = index.get(srch_query,'')
                final_url_set = final_url_set.union(urls) 
    print(f'Found {len(final_url_set)} matching pages')
    if final_url_set:
        print(final_url_set)
    else:
        print('{}')
  
'''This is the crucial function which invokes the above methods
 in orderly fashion, inorder to create a mini search engine'''
def mySearchEngine(dbfile):
    print('Stand by while building index...')
    #process file and create forward index
    forw_index = readDocs(dbfile)
    #create inverted index
    inverted_index = buildInvertedIndex(forw_index)
    
    while True:
        #user input for search query
        search_query = input('\nEnter query sentence (RETURN/ENTER to quit):')
        if search_query =='':
            break
        #search results
        findQueryMatches(inverted_index, search_query)

if __name__ == "__main__":
    mySearchEngine("sampleWebsiteData.txt")
    print('\nAll Done!')
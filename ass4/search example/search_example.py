# %% [markdown]
# ### As before, we import the libraries and code bases we need
# 
# ### This time, inverted_index and utils is mine... Note source files used in this context have to live within the context of where the jupyter notebook is being run...

# %%
# first install the required packages
import nltk
nltk.download('stopwords')


from inverted_index import InvertedIndex
from utils import read_data
inv_ind = InvertedIndex()

# %% [markdown]
# ### Add documents below, read_data scans directory passed for any files ending in ".txt" and reads them in as a single string.

# %%
documents = read_data("./data")
print(documents)

# %% [markdown]
# ### Print out number of documents and document titles

# %%
print(len(documents))
for d in documents:
    print(d[0])

# %% [markdown]
# ### Next, we will add all these documents to our Inverted Index...

# %%
for d in documents:
    print(d[0])
    inv_ind.add_document(d)

# %% [markdown]
# ### Print out some descriptives, total terms indexed and documents...

# %%
print(inv_ind.get_total_terms())
print(inv_ind.get_total_docs())

# %% [markdown]
# ### Print out the inverted index itself....

# %%
inv_ind.print()

# %% [markdown]
# ### Just for interest's sake, you can see nltk's built in stop word list

# %%
import nltk
print(nltk.corpus.stopwords.words('english'))

# %% [markdown]
# ### From this we can geneate a term by document matrix 

# %%
print(inv_ind.generate_term_by_doc_matrix())

# %% [markdown]
# #### We can compute the LogEntropy values for everything in the Inverted Index
# #### Display new values

# %%
inv_ind.calcLogEntropy()
inv_ind.generate_term_by_doc_matrix(log_entropy = True)

# %% [markdown]
# ### Let's do a search....

# %%
results = inv_ind.search("scotland kings and thanes", log_entropy = True)
for r in results:
    print (r)


# %% [markdown]
# ### We can deal with boolean queries too... let's get some data.

# %%
obama = inv_ind.get_document_set_from_term("Obama")
trump = inv_ind.get_document_set_from_term("Trump")
bernie = inv_ind.get_document_set_from_term("Bernie Sanders")
print(obama)
print(trump)
print(bernie)

# %% [markdown]
# ### We have sets containing the infor for Obama, Trump and Sanders
# ### Which documents discuss all 3?

# %%
print(obama & trump & bernie)

# %% [markdown]
# ### Let's use a larger dataset, we will use the complete works 
# ### of Shakespeare next... First, load it in.

# %%
documents = read_data("./shakespeare")
inv_ind = InvertedIndex()
for d in documents:
    print(d[0])

# %% [markdown]
# ### Next, add them to the Inverted Index...
# ### Note some of these documents are 25,000 - 35,000 words...

# %%
for d in documents:
    print(d[0])
    inv_ind.add_document(d)

# %% [markdown]
# ### We can reproduce our boolean search gave in the lecture slides...
# 
# ### Also see how many terms we have...

# %%
print(inv_ind.get_total_terms())
caes = inv_ind.get_document_set_from_term("Caesar")
brut = inv_ind.get_document_set_from_term("Brutus")
cap = inv_ind.get_document_set_from_term("Calpurnia")
print(caes)
print(brut)
print(cap)

# %% [markdown]
# ### Using simple set operations...
# ### Which are the plays that have Caesar AND Brutus but *NOT* Calpurnia

# %%
print((caes & brut) - cap)


# %% [markdown]
# ### Let's generate our TFIDF data for future work and generate a plain term by document matrix for queries.

# %%
#inv_ind.calcTFIDF()
inv_ind.generate_term_by_doc_matrix(tfidf = False)

# %% [markdown]
# ### Now, let's do a query about a Shakespeare play...

# %%
results = inv_ind.search("scotland kings and thanes", tfidf = False)
for r in results:
    print (r)

# %% [markdown]
# ### Is there anything weird going on here?

# %%
king_docs = inv_ind.get_document_set_from_term("Kings")
print(king_docs)

# %%
king_pl = inv_ind.get_postings_list_from_term("Kings")
print(king_pl)

# %%
scotland_pl = inv_ind.get_postings_list_from_term("Scotland")
print(scotland_pl)

# %%
thane_pl = inv_ind.get_postings_list_from_term("Thane")
print(thane_pl)



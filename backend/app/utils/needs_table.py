import nltk
from nltk.tokenize import word_tokenize

def needs_table(prompt):
  tokens = word_tokenize(prompt.lower())
  table_keywords = ['table', 'list', 'all', 'orders', 'summary']
  return any(keyword in tokens for keyword in table_keywords)
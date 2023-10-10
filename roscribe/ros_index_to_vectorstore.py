__import__('pysqlite3')
import sys, re
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer


# Load HTML
num_pages = 5
loader = AsyncChromiumLoader(["https://index.ros.org/repos/page/{i}/time/".format(i=page)
                              for page in range(1, num_pages + 1)])
html = loader.load()

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["a"])

# Find Matches
matches = []
for i in range(num_pages):
    matches.extend(re.findall(r'/r/[^\s]+', docs_transformed[i].page_content))

print("{} ROS repositories found!".format(len(matches)))

URLs = []
for match in matches:
    URLs.append('https://index.ros.org' + match[:-1])


# Retriever Declaration
link_limit = 100
loader = WebBaseLoader(URLs[:link_limit])
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
# vectorstore = Chroma.from_documents(documents=all_splits,
#                                     embedding=OpenAIEmbeddings(),
#                                     persist_directory="./ros_index_db2")
#
print("A ChromaDB object has been stored in \"ros_index_db\"!")

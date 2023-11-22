__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from datetime import date

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import AsyncChromiumLoader

from roscribe.ros_bs_transformer import ROSIndexTransformer, ROSRepoTransformer


num_pages = 5
ros_version = 'noetic'
URL_batch_size = 10

# Load ROS Index
loader = AsyncChromiumLoader(["https://index.ros.org/repos/page/{i}/time/".format(i=page)
                              for page in range(1, num_pages + 1)])
html_list = loader.load()

# Collect ROS Repositories
ros_index_transformer = ROSIndexTransformer(ros_version)
repo_URLs, repo_names = ros_index_transformer.get_distro_URLs(html_list)

# Initialize Database
db_name = "ros_index_db_{}_".format(ros_version) + str(date.today()).replace("-", "_")
vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="ROS_index_database/" + db_name)
print("A ChromaDB object has been initialized!")

# Load ROS Repositories
ros_repo_transformer = ROSRepoTransformer(ros_version)
for i in range(int(len(repo_URLs) / URL_batch_size)):
# for i in range(40, 45):
    loader = AsyncChromiumLoader(repo_URLs[i*URL_batch_size:(i+1)*URL_batch_size])
    html_list = loader.load()
    repo_struct_list = ros_repo_transformer.get_repo_struct(html_list,
                                                            repo_names[i*URL_batch_size:(i+1)*URL_batch_size])

    if len(repo_struct_list) > 0:
        repo_docs = []
        for repo_struct in repo_struct_list:
            repo_docs.extend(repo_struct.get_all_repo_info())

        # Database Update
        vectorstore.add_documents(documents=repo_docs)

    print("{}-th batch has been scraped!".format(i+1))

print("A ChromaDB object has been stored in \"{}\"!".format(db_name))

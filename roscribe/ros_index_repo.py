from langchain.text_splitter import RecursiveCharacterTextSplitter


class ROSIndexRepo:
    def __init__(self, repo_uri, repo_name, checkout_uri, vcs_type, vcs_version, last_updated,
                 dev_status, ci_status, released, tags, packages, readme, contrib):
        self.repo_name = repo_name
        self.checkout_uri = checkout_uri
        self.vcs_type = vcs_type
        self.vcs_version = vcs_version
        self.last_updated = last_updated
        self.dev_status = dev_status
        self.ci_status = ci_status
        self.released = released
        self.tags = tags
        self.packages = packages
        self.readme = readme
        self.contrib = contrib

        self.repo_metadata = {'source': repo_uri, 'language': 'en'}

    def get_repo_summary(self):
        ret_str = "Repository summary for {repo_name}:\nCheckout URI: {checkout_uri}\nVCS Type: {vcs_type}\n" \
                  "VCS Version: {vcs_version}\nLast Updated: {last_updated}\nDev Status: {dev_status}\n" \
                  "CI status: {ci_status}\nReleased: {released}\nTags: {tags}".format(repo_name=self.repo_name,
                                                                                      checkout_uri=self.checkout_uri,
                                                                                      vcs_type=self.vcs_type,
                                                                                      vcs_version=self.vcs_version,
                                                                                      last_updated=self.last_updated,
                                                                                      dev_status=self.dev_status,
                                                                                      ci_status=self.ci_status,
                                                                                      released=self.released,
                                                                                      tags=self.tags)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400000, chunk_overlap=0)
        summary_doc_list = text_splitter.create_documents(texts=[ret_str], metadatas=[self.repo_metadata])
        summary_doc_list[0].metadata['title'] = "Repository summary for {repo_name}".format(repo_name=self.repo_name)

        return summary_doc_list

    def get_repo_packages(self):
        ret_str = ""
        if len(self.packages) > 0:
            for package in self.packages:
                ret_str += "{package_name} (version: {package_ver})\n".format(package_name=package[0],
                                                                              package_ver=package[1])
        else:
            ret_str += "No packages available for {repo_name}.".format(repo_name=self.repo_name)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400000, chunk_overlap=0)
        package_doc_list = text_splitter.create_documents(texts=[ret_str], metadatas=[self.repo_metadata])
        package_doc_list[0].metadata['title'] = "ROS packages for {repo_name}".format(repo_name=self.repo_name)

        return package_doc_list

    def get_repo_readme(self, chunk_size=500, chunk_overlap=0):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        readme_doc_list = text_splitter.create_documents(texts=[self.readme], metadatas=[self.repo_metadata])
        if len(readme_doc_list) > 1:
            for i, split in enumerate(readme_doc_list):
                split.metadata['title'] = "README of {repo_name}, part {part_num}".format(repo_name=self.repo_name,
                                                                                          part_num=i+1)
        else:
            if len(readme_doc_list) == 0:
                readme_doc_list = text_splitter.create_documents(texts=["No README found."],
                                                                 metadatas=[self.repo_metadata])
            readme_doc_list[0].metadata['title'] = "README of {repo_name}".format(repo_name=self.repo_name)

        return readme_doc_list

    def get_repo_contrib(self, chunk_size=500, chunk_overlap=0):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        contrib_doc_list = text_splitter.create_documents(texts=[self.contrib], metadatas=[self.repo_metadata])
        if len(contrib_doc_list) > 1:
            for i, split in enumerate(contrib_doc_list):
                split.metadata['title'] = "Contributing information of {repo_name}, part {part_num}".\
                    format(repo_name=self.repo_name, part_num=i + 1)
        else:
            if len(contrib_doc_list) == 0:
                contrib_doc_list = text_splitter.create_documents(texts=["No Contributing found."],
                                                                  metadatas=[self.repo_metadata])
            contrib_doc_list[0].metadata['title'] = "Contributing information of {repo_name}".\
                format(repo_name=self.repo_name)

        return contrib_doc_list

    def get_all_repo_info(self, chunk_size=500, chunk_overlap=0):
        all_repo_docs = []
        all_repo_docs.extend(self.get_repo_summary())
        all_repo_docs.extend(self.get_repo_packages())
        all_repo_docs.extend(self.get_repo_readme(chunk_size=chunk_size, chunk_overlap=chunk_overlap))
        all_repo_docs.extend(self.get_repo_contrib(chunk_size=chunk_size, chunk_overlap=chunk_overlap))
        return all_repo_docs

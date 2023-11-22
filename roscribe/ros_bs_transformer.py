from bs4 import BeautifulSoup
from langchain.document_transformers import BeautifulSoupTransformer
from roscribe.ros_index_repo import ROSIndexRepo


class ROSRepoTransformer:
    def __init__(self, ros_distro):
        self.distro_key = "distro-" + ros_distro
        self.remove_unnecessary_lines = BeautifulSoupTransformer.remove_unnecessary_lines
        self.no_distro_msg = "No version for distro {}. Known supported distros are highlighted in the buttons above.".\
            format(ros_distro)

    def get_repo_struct(self, html_list, repo_names):
        repo_struct_list = []
        for i, html, repo_name in zip(range(len(html_list)), html_list, repo_names):
            soup = BeautifulSoup(html.page_content, "html.parser")
            elements = soup.find_all("div")
            for element in elements:
                if self.distro_key in element.get_attribute_list('class'):
                    if self.no_distro_msg not in element.get_text():
                        summary_div = element.contents[1].contents[1].contents[3].contents[1].contents[1]
                        checkout_uri = summary_div.contents[0].contents[3].get_text()
                        vcs_type = summary_div.contents[2].contents[3].get_text()
                        vcs_version = summary_div.contents[4].contents[3].get_text()
                        last_updated = self.remove_line_space(summary_div.contents[6].contents[2].get_text())
                        dev_status = self.remove_line_space(summary_div.contents[8].contents[3].get_text())
                        ci_status = self.remove_line_space(summary_div.contents[10].contents[3].get_text(), space=False)
                        released = self.remove_line_space(summary_div.contents[12].contents[3].get_text())
                        tags = self.remove_line_space(summary_div.contents[14].contents[3].get_text(), space=False)

                        packages = []
                        if element.contents[1].contents[3].contents[3].contents[1].get_text() != "No packages found.":
                            package_divs = element.contents[1].contents[3].contents[3].contents[1].contents[3].contents[
                                           1::2]

                            for package_div in package_divs:
                                packages.append((package_div.contents[1].get_text(), package_div.contents[3].get_text()))

                        readme = self.remove_unnecessary_lines(element.contents[1].contents[5].contents[3].get_text())
                        contrib = self.remove_unnecessary_lines(element.contents[1].contents[7].contents[3].get_text())

                        repo_struct_list.append(ROSIndexRepo(repo_uri=html.metadata['source'],
                                                             repo_name=repo_name,
                                                             checkout_uri=checkout_uri,
                                                             vcs_type=vcs_type,
                                                             vcs_version=vcs_version,
                                                             last_updated=last_updated,
                                                             dev_status=dev_status,
                                                             ci_status=ci_status,
                                                             released=released,
                                                             tags=tags,
                                                             packages=packages,
                                                             readme=readme,
                                                             contrib=contrib))

            print("{} out of {} repositories have been scraped!".format(i + 1, len(html_list)))

        return repo_struct_list

    @staticmethod
    def remove_line_space(input_text, line=True, space=True):
        if line:
            input_text = input_text.replace("\n", "")

        if space:
            input_text = input_text.replace(" ", "")

        return input_text


class ROSIndexTransformer:
    def __init__(self, ros_distro):
        self.distro_key = "distro-" + ros_distro

    def get_distro_URLs(self, html_list):
        distro_URLs = []
        distro_repo_names = []
        for i, html in enumerate(html_list):
            soup = BeautifulSoup(html.page_content, "html.parser")
            elements = soup.find_all("div")
            for element in elements:
                if self.distro_key in element.get_attribute_list('class'):
                    all_links = element.find_all("a")
                    for link in all_links:
                        if '/r/' in link.get_attribute_list('href')[0]:
                            distro_URLs.append('https://index.ros.org' + link.get_attribute_list('href')[0])
                            distro_repo_names.append(link.get_text())

        return distro_URLs, distro_repo_names

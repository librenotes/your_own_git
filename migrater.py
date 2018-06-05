from requests import post, get
from getpass import getpass

GH_API = "https://api.github.com/{}"


class Github:
    def __init__(self, login, password):
        self.headers = {}
        self.auth = None
        if password is '':
            self.headers['Authorization'] = "token {}".format(login)
        else:
            self.username = login
            self.auth = (login, password)

    def repos(self, visibility="all", affiliation="owner,collaborator,organization_member"):
        params = {
            "visibility": visibility,
            "affiliation": affiliation
        }
        r = get(GH_API.format("user/repos"), auth=self.auth, params=params, headers=self.headers)
        return r.json()


class Gittea:
    def __init__(self, api_url, login, password):
        self.API_URL = api_url
        self.headers = {}
        self.auth = None
        if password is '':
            self.headers['Authorization'] = "token {}".format(login)
        else:
            self.username = login
            self.auth = (login, password)
        r = get(api_url + "/user", auth=self.auth, headers=self.headers).json()
        self.uid = r['id']

    def __migrate(self, auth_password, auth_username, clone_addr, description, private, repo_name):
        data = {
            "auth_password": auth_password,
            "auth_username": auth_username,
            "clone_addr": clone_addr,
            "description": description,
            "mirror": False,
            "private": private,
            "repo_name": repo_name,
            "uid": str(self.uid)
        }
        r = post(self.API_URL + "/repos/migrate", data=data, auth=self.auth, headers=self.headers)

    def migrate(self, github_username, auth_password=None, affiliation="owner,collaborator,organization_member",
                visibility="all", new_visibility="inherit"):
        gh = Github(login=github_username, password=auth_password)
        repos = gh.repos(visibility=visibility, affiliation=affiliation)
        for repo in repos:
            clone_addr = repo['clone_url']
            print(clone_addr)
            description = repo['description']
            if new_visibility is "inherit":
                private = repo['private']
            elif new_visibility is "public":
                private = False
            else:
                private = True

            repo_name = repo['name']
            self.__migrate(auth_password, github_username, clone_addr, description, private, repo_name)


def main():
    api_url = input("Gitea Api Url (Ex: https://xxx.com/api/v1): ")
    gitea_username = input("Gitea Username or token: ")
    gitea_password = getpass("Gitea password (pass empty if token used): ")
    github_username = input("Github username or token: ")
    github_password = getpass("Github password (pass empty if token used): ")
    affiliation = input("Give affiliation for target repos \n"
                        "(Ex: 'owner,collaborator,organization_member' Default: 'owner' :")
    type = input("Type of repositories to migrate (Ex: 'private', Default: 'all' : ")
    if type is '':
        type = 'all'
    if affiliation is '':
        affiliation = 'owner'
    visibility = input("Give visibility for migrated repos (Ex: 'private', Default: 'inherit' :")
    if visibility is '':
        visibility = 'inherit'

    gt = Gittea(api_url=api_url, login=gitea_username, password=gitea_password)
    gt.migrate(github_username, github_password, affiliation=affiliation, new_visibility=visibility, visibility=type)


if __name__ == '__main__':
    main()

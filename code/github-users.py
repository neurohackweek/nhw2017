import sys
from github import Github
import pandas as pd
import getpass

user = input("Enter username: ")
password = getpass.getpass("Enter password: ")
org_name = input("Enter org name: ")
team_name = input("Enter team name: ")
csv_file = sys.argv[1]

g = Github(user, password)
org = g.get_organization(org_name)

user_names = [m.html_url.split('/')[-1] for m in list(org.get_members())]
print(user_names)

participants = pd.read_csv(csv_file)
for t in org.get_teams():
    if t.name == team_name:
        for member_name in participants['GitHub username']:
            if (not pd.isnull(member_name) and not
                    t.has_in_members(g.get_user(member_name))):
                print("Adding %s" % member_name)
                t.add_membership(g.get_user(member_name))

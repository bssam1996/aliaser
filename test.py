import gitlab
import base64

import gitlab.exceptions

gl = gitlab.Gitlab('http://localhost:80', private_token='glpat-TuzAGjfkzoqExLz_qycj')
gl.auth()


project = gl.projects.get(1) # Id of the project
# project_id = None
# for project in projects:
#     print(project.attributes['name'])

# get the file object
# try:
#     f = project.files.get(file_path='locations.json', ref='main')
#     with open('locations.json', 'w') as my_file:
#         content = base64.b64decode(f.content)
#         my_file.write(content.decode('utf-8'))
# except gitlab.exceptions.GitlabGetError as e:
#     if str(e).count('404') > 0:
#         print('Not Found')
#     print(str(e))

# # modify its contents

# f = project.files.get(file_path='locations.json', ref='main')
# f.content = base64.b64encode(b'new content').decode('utf-8')

# # save (commit) the new contents
# f.save(branch='main', commit_message='update file', encoding='base64')

# with open('locations.json', 'rb') as my_file:
#     contents = base64.b64encode(my_file.read()).decode('utf-8')
# # create new file in the repo
# f = project.files.create({'file_path': 'locations.json',
#                           'branch': 'main',
#                           'content': contents,
#                           'encoding': 'base64',
#                           'author_email': 'aliaser@cgg.com',
#                           'author_name': 'aliaser',
#                           'commit_message': 'Create locations'})
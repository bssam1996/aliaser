![Aliaser image](static/img/aliaser.png)

# Aliaser

Create aliases for long boring links with ease to use.

## API Endpoints

[GET] `/`: Main landpage for users to interact. 

[GET] `/<alias>`: Redirect to link with alias provided 

[GET] `/describe/<alias>`: Get full details of specific alias

[POST] `/add`: add new alias with the following provided details in the payload:-
```
alias: name of the alias
link: link to be redirected at
owner: owner of the alias <optional>
category: category of the alias <optional>
```
[POST] `/replace`: add or overwrite existing alias with the following provided details in the payload:-
```
alias: name of the alias
link: link to be redirected at
owner: owner of the alias <optional>
category: category of the alias <optional>
```
[DELETE] `/delete/<alias>`: Deletes provided alias


## Environment variables

- `HOST`: host of aliaser (default is `'0.0.0.0'`)
- `PORT`: port of aliaser (default is `5000`)
- `DEBUG`: run aliaser in debug mode or not (Expected values are `True` or `False` defaults to `True` and if `True`, it runs under [waitress](https://pypi.org/project/waitress/))
- `BACKUP_SCHEDULE`: how often backup thread should run in `seconds` (default is `3600`)
- `REDIS_HOST`: host of redis (default is `localhost`)
- `REDIS_PORT`:port of redis (default is `6379`)
- `GIT_MODE`: Whether thread is going to backup on github or gitlab (expected values are `GITHUB` or `GITLAB` defaults to `GITLAB`)
- `GITHUB_RAW_FILE_LOCATION`: locations.json file location in github to download it as a restore point (*mandatory field in case of `GIT_MODE` is `GITHUB`)
- `GITHUB_REPO`: Repo of aliaser (eg. `example/aliaser`) (*mandatory field in case of `GIT_MODE` is `GITHUB`)
- `GITHUB_BRANCH`: Branch of the project to push at (eg. `main`) (*mandatory field in case of `GIT_MODE` is `GITHUB`)
- `GITHUB_USER`: user to be used to push with (eg. `aliaser`) (*mandatory field in case of `GIT_MODE` is `GITHUB`)
- `GITHUB_TOKEN`: personal token to be used to push with (*mandatory field in case of `GIT_MODE` is `GITHUB`)
- `GITLAB_HOST`: host of gitlab (defaults to `http://localhost:80`)
- `GITLAB_PROJECT_TOKEN`: project token of aliaser in gitlab (*mandatory field in case of `GIT_MODE` is `GITLAB`)
- `GITLAB_PROJECT_ID`: project id of aliaser in gitlab (eg. `80`) (*mandatory field in case of `GIT_MODE` is `GITLAB`)
- `GITLAB_PROJECT_BRANCH`: Branch of the project to push at (eg. `main`) (*mandatory field in case of `GIT_MODE` is `GITLAB`)


## Components

Redis is used as caching

Flask for API

Jinja for frontend

Backup to Github or Gitlab with filename `locations.json`

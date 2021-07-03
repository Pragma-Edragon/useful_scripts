# RBRUTE
<img src="https://visitor-badge.laobi.icu/badge?page_id=Pragma-Edragon" /> <img src="https://img.shields.io/badge/-Python-333333?style=flat&logo=python" /> <img src="https://img.shields.io/badge/-Bash-333333?style=flat&logo=bash" />
### Useful information:
---
#### A fairly simple utility written entirely in bash. In order to start it, you need to start the tty session. This is done differently for each OS. You need your own virtual private server with web application that has `/success` endpoint to get script logs. Otherwise - script logging inside current machine.

##### For example, to spawn interactive shell (tty) you can use: `/usr/bin/script -qc /bin/bash /dev/null`

### Usage:
---
```bash
 Usage: /bin/bash main.sh [options]
  Options available to this script:
  -url  : Specify url from where password list could be downloaded;

  -host : Specify host to where all attempts could be logged;
  (host must have 2 endpoints: <host>:<port>/success and <host>:<port>/error,
  if no host specified - trying to log to dir available for current user);
```

### Screenshots of the script inside docker container and outside:
---
![inside-docker and outside](https://user-images.githubusercontent.com/45512613/124366666-068cf300-dc5a-11eb-9122-d0ce4826e64d.png)


### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-02-py/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | Никакое. Ошибка TypeError: unsupported operand type(s)|
| Как получить для переменной `c` значение 12?  | a=str(1)  |
| Как получить для переменной `c` значение 3?  | b=int('2')  |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
mypath = os.getcwd()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(mypath + '/' + prepare_result)


```

### Вывод скрипта при запуске при тестировании:
```
/home/kirill/netology/sysadm-homeworks/04-script-02-py/README.md
/home/kirill/netology/sysadm-homeworks/README.md

```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys
import subprocess

target_dir = sys.argv[1]
bash_command = ["git status; exit 0"]
try:
    os.chdir (target_dir)
except FileNotFoundError:
     print (f'Directory {target_dir} doesn\'t exist')
     exit (1)
except PermissionError:
     print (f'Permission denied. You don\'t have access rights to {target_dir}')
     exit (2)
result_os=subprocess.check_output(bash_command, stderr=subprocess.STDOUT, shell=True, text=True)
mypath = os.getcwd()
is_change = False
for result in result_os.split('\n'):
    if result.find(' not a git repository ') != -1:
        print (f'Directory {mypath} is not a git repository!')
        exit(3)
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(mypath + '/' + prepare_result)

```

### Вывод скрипта при запуске при тестировании:
```
kirill@ubuntu1:~/netology/sysadm-homeworks$ ./myscript.py ~/netology/sysadm-homeworks/
/home/kirill/netology/sysadm-homeworks/04-script-02-py/README.md
/home/kirill/netology/sysadm-homeworks/README.md

kirill@ubuntu1:~/netology/sysadm-homeworks$ ./myscript.py ~/netology/sysadm-homework/
Directory /home/kirill/netology/sysadm-homework/ doesn't exist

kirill@ubuntu1:~/netology/sysadm-homeworks$ ./myscript.py ~/netology/
Directory /home/kirill/netology is not a git repository!

kirill@ubuntu1:~/netology/sysadm-homeworks$ ./myscript.py /root
Permission denied. You don't have access rights to /root

```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3

#Script is used to track changes of hosts IPs
#It requires file with list of hosts to track to be created (hostfile.txt)

import socket
import os.path

hostlist={}
hostfile = 'hostlist.txt'
errcount = 0 #used to count DNS resolution errors
errlimit = 3 #after reaching this errors limit script is terminated
errmsg_done = False #used to track if error message was printed already

if not os.path.isfile(hostfile):
  print (f'Hostfile {hostfile} doesn\'t exist. Please create it and populate with hosts')
  print ('Each host must be on separate line')
  exit (1)

#Populating hosts dict from hostfile
with open(hostfile,'r') as f:
  for line in f:
    ls = line.split(' ')
    if len(ls) < 2:  #New host which IPs are not known yet
      hostlist[ls[0].rstrip('\n')] = ''
    else:
      hostlist[ls[0].rstrip('\n')] = ls[1].rstrip('\n')

for (host,ip) in hostlist.items():
  print (f'Checking {host}...')
  try:
    new_ip = socket.gethostbyname(host)
  except:
    new_ip = ip
    print (f'Unable to resolve {host} for some reason. There may be DNS or network issue or hostname is not correct')
    print ('Keeping old ip')
    errcount += 1
  if errcount == errlimit:  #IF there were too many errors we just write all hosts back to file and exit
    print ('Too many DNS resolution errors. Flushing host list and quitting...')
    break
  hostlist[host] = new_ip
  print (host, new_ip)
  if new_ip != ip and ip !='':
    print (f'IP for host {host} changed from {ip} to {new_ip}!')
#Flushing updated dict to file
with open(hostfile,'w') as f:
    for host,ip in hostlist.items():
      f.write (host + ' ' + ip + '\n')

```

### Вывод скрипта при запуске при тестировании:
```
kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ ./hostchecker.py
Hostfile hostlist.txt doesn't exist. Please create it and populate with hosts
Each host must be on separate line

kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ vi ./hostlist.txt
kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ cat ./hostlist.txt
mail.google.com
drive.google.com
google.com

kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ ./hostchecker.py
Checking mail.google.com...
mail.google.com 64.233.162.18
Checking drive.google.com...
drive.google.com 173.194.222.194
Checking google.com...
google.com 64.233.165.113
kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ cat ./hostlist.txt
mail.google.com 64.233.162.18
drive.google.com 173.194.222.194
google.com 64.233.165.113

kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ echo "rbc.ru" >> ./hostlist.txt
kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ ./hostchecker.py
Checking mail.google.com...
mail.google.com 64.233.162.18
Checking drive.google.com...
drive.google.com 173.194.222.194
Checking google.com...
google.com 64.233.165.113
Checking rbc.ru...
rbc.ru 178.248.236.77

#Добавил в файл fakehosts чтобы проверить обработку ошибок
kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ cat ./hostlist.txt
mail.google.com 64.233.162.17
drive.google.com 173.194.222.194
google.com 64.233.165.138
rbc.ru 178.248.236.77
fakehost1
fakehost2
fakehost3
fakehost4

kirill@ubuntu1:~/repos/devops-netology/lesson_4.2$ ./hostchecker.py
Checking mail.google.com...
mail.google.com 64.233.162.17
IP for host mail.google.com changed from 64.233.162.18 to 64.233.162.17!
Checking drive.google.com...
drive.google.com 173.194.222.194
Checking google.com...
google.com 64.233.165.138
IP for host google.com changed from 64.233.165.113 to 64.233.165.138!
Checking rbc.ru...
rbc.ru 178.248.236.77
Checking fakehost1...
Unable to resolve fakehost1 for some reason. There may be DNS or network issue or hostname is not correct
Keeping old ip
fakehost1
Checking fakehost2...
Unable to resolve fakehost2 for some reason. There may be DNS or network issue or hostname is not correct
Keeping old ip
fakehost2
Checking fakehost3...
Unable to resolve fakehost3 for some reason. There may be DNS or network issue or hostname is not correct
Keeping old ip
Too many DNS resolution errors. Flushing host list and quitting...




```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```
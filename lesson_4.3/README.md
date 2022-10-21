### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

Исправленный вариант. (ошибки - потеряна запятая между элементами, потеряны кавычки, лишние пробелы в IP
```json
 {
 	"info": "Sample JSON output from our service\t",
 	"elements": [{
 		"name": "first",
 		"type": "server",
 		"ip": 7175
 	}, 
 	{
 		"name": "second",
 		"type": "proxy",
 		"ip": "71.78.22.43"
 	}]
 }
```


## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
#!/usr/bin/env python3

#Script is used to track changes of hosts IPs
#It requires file with list of hosts to track to be created (hostfile.txt)

import socket
import os.path
import json
import yaml

hostlist={}
hostfile = 'hostlist.txt'
hostfile_json=hostfile.replace('txt','json')
hostfile_yaml=hostfile.replace('txt','yaml')
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

#Writing json
with open (hostfile_json,'w') as f:
    json.dump(hostlist,f)

#Writing yaml
with open (hostfile_yaml,'w') as f:
    yaml.dump(hostlist,f)

```

### Вывод скрипта при запуске при тестировании:
```
kirill@ubuntu1:~/repos/devops-netology/lesson_4.3$ ./hostchecker.py
Checking rbc.ru...
rbc.ru 178.248.236.77
Checking habr.ru...
habr.ru 178.248.233.33

```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"rbc.ru": "178.248.236.77", "habr.ru": "178.248.233.33"}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
habr.ru: 178.248.233.33
rbc.ru: 178.248.236.77

```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
???
```

### Пример работы скрипта:
???
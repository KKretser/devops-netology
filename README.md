# devops-netology

## Описание gitignore для terraform

- Во всех каталогах игнорируем все файлы  .terraform
- Игнорируем файлы, имеющие единственным или первым расширением .tfstate
- Игнорируем файлы с именем crash и последним (или единственным) расширением .log
- Игнорируем файлы c расширением .tfvars и .tfvasrs.json
- Игнорируем файлы override.tf, override.tf.json, либо заканчивающиеся на _override.tf, *_override.tf.json
- Игнорируем файлы с расширением .terraformrc и файлы terraform.rc


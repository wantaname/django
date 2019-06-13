import re
a='USD 23.40'
b=re.match(r'([a-zA-Z]*)',a)
print(b.group(1))
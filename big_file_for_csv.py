from collections import Counter
import sys
import time

file_name=sys.argv[1]
with open(file_name,'r') as file:
    all_line=file.readlines()
    all_number = [num.split(',')[0] for num in all_line]
    counter=dict(Counter(all_number))
    sorted_counter = sorted(counter.items(), key=lambda d: d[1], reverse=True)
    #sorted_counter 为list类型
new_file = time.strftime("%Y%m%d%H%M%S",time.localtime()) + '_' + file_name
with open(new_file,'w') as file:
    for l in sorted_counter:
        file.write(str(l[0]) + ','+ str(l[1]) + '\n')
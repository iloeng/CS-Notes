### 查找大文件

sudo find / \( -path /root/newrec -prune \) -o \( -type f -size +100M -exec ls -lh {} \; \) | awk '{ print $9 ": " $5 }'


### 文件传输

xxd -p myfile > tmp
xxd -r -p tmp > myfile


alias pull='rsync -aPv -e "ssh -p {port}" root@{ip_addr}:{src_dir} {dst_dir} --exclude "ckpts" --exclude "hstu_model" --exclude "dataio" --exclude ".idea" --exclude ".git"'
alias push='rsync -aPv -e "ssh -p {port}" {src_dir} root@{ip_addr}:{dst_dir} --exclude "ckpts" --exclude "hstu_model" --exclude "dataio" --exclude ".idea" --exclude ".git"'
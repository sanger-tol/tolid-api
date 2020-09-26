mv public_names.db public_names.db.old
mv final_merged.txt final_merged.txt.old
curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/final_merged.txt -o final_merged.txt
nohup start.sh &
echo $! > save_pid.txt
curl -X GET "http://localhost:8080/public-name?searchString=force_database_rebuild" -H  "accept: application/json"
kill -9 `cat save_pid.txt`
rm save_pid.txt

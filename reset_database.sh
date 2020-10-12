mv public_names.db public_names.db.old
mv final_merged.txt final_merged.txt.old
curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/final_merged.txt -o final_merged.txt
nohup start.sh &
echo $! > save_pid.txt
sleep 5
curl http://localhost:8080/verify-database  # Rebuild
echo "Server running. To stop the Python server use 'kill -9 `cat save_pid.txt`'"
echo "Testing the local database by searching for Homo sapiens, taxid 9606"
curl -X GET "http://localhost:8080/public-name?taxonomyId=9606" -H  "accept: application/json"
kill -9 `cat save_pid.txt`
rm save_pid.txt

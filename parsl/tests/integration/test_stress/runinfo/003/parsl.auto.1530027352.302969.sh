export CORES=$(getconf _NPROCESSORS_ONLN)
echo "Found cores : $CORES"
WORKERCOUNT=1

CMD ( ) {
cd .
cat <<EOF > ipengine.json
{
  "ssh": "",
  "interface": "tcp://*",
  "registration": 52784,
  "control": 52786,
  "mux": 52788,
  "hb_ping": 52789,
  "hb_pong": 52790,
  "task": 52792,
  "iopub": 52794,
  "key": "7ea16fea-ca5b6afc080f9f2b58910f55",
  "location": "sillygoose.local",
  "pack": "json",
  "unpack": "json",
  "signature_scheme": "hmac-sha256"
}
EOF

mkdir -p '.ipengine_logs'
ipengine --file=ipengine.json >> .ipengine_logs/$JOBNAME.log 2>&1

}

for COUNT in $(seq 1 1 $WORKERCOUNT)
do
    echo "Launching worker: $COUNT"
    CMD &
done
wait
echo "All workers done"

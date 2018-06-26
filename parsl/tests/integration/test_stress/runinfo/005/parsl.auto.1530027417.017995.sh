export CORES=$(getconf _NPROCESSORS_ONLN)
echo "Found cores : $CORES"
WORKERCOUNT=1

CMD ( ) {
cd .
cat <<EOF > ipengine.json
{
  "ssh": "",
  "interface": "tcp://*",
  "registration": 52882,
  "control": 52884,
  "mux": 52886,
  "hb_ping": 52887,
  "hb_pong": 52888,
  "task": 52890,
  "iopub": 52892,
  "key": "fc65ba85-cff62f4ed5ab08168ce4bcc1",
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
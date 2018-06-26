export CORES=$(getconf _NPROCESSORS_ONLN)
echo "Found cores : $CORES"
WORKERCOUNT=1

CMD ( ) {
cd .
cat <<EOF > ipengine.json
{
  "ssh": "",
  "interface": "tcp://*",
  "registration": 52740,
  "control": 52742,
  "mux": 52744,
  "hb_ping": 52745,
  "hb_pong": 52746,
  "task": 52748,
  "iopub": 52750,
  "key": "be3c120f-f6b507417d5069f9070f23dd",
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

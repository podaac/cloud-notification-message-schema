for f in samples/*.json
do
  echo "Testing $f"
	jsonschema -i $f cumulus_sns_schema.json
done

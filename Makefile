all:
	# make can't handle filenames with spaces, but bash can!
	for json in *.sublime-*; do jq . "$$json" > "$$json.tmp" && mv "$$json.tmp" "$$json"; echo Prettified $$json; done

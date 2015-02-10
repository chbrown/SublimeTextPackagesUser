all:
	# make can't handle filenames with spaces, but bash can!
	for json in *.sublime-*; do jq -i . "$$json"; echo Prettified $$json; done

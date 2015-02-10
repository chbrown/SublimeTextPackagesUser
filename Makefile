all:
	# make can't handle filenames with spaces, but bash can!
	for json in *.sublime-settings; do jq -i . "$$json"; echo Prettified $$json; done

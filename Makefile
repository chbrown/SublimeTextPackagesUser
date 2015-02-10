# Use like: make -B *.sublime-settings
%.sublime-settings:
	# prettifying in place
	jq -i . "$@"

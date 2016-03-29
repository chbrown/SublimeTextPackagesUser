all:
	# make can't handle filenames with spaces, but bash can!
	bash prettify.sh *.sublime-*

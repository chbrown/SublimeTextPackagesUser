all:
	# use jqi from github.com/chbrown/dotfiles to pretty print all the JSON files
	find . -name '*.sublime-*' -print0 | xargs -0 -n 1 jqi .

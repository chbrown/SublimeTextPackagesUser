## Installation

```bash
cd "~/Library/Application Support/Sublime Text 3/Packages"
rm -rf User/
git clone git@github.com:chbrown/SublimeTextPackagesUser.git User
```


## Changes

Some of Sublime Text's plugins (or Sublime Text itself) will make changes to the `.sublime-settings` files, ending up with a variety of JSON formatting flavors. Run `make` in this directory to standardize indentation.

This simply runs `jq -i . <file>` on each file matching the glob `*.sublime-*`.

It depends on [`jq`](http://stedolan.github.io/jq/) for JSON formatting, and uses the default output spacing.

If any of your `*.sublime-*` files are not valid JSON, `jq` will print out an error and exit without changing the file.
(It _will_ leave a temporary file with the same prefix as the file you were converting, which is kind of annoying.)


### Package control installation

1. Open up the Sublime Text 3 console: <code>ctrl + `</code>
2. Go to [sublime.wbond.net/installation](https://sublime.wbond.net/installation)
3. Copy and paste the install code into the ST3 console

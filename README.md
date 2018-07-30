## Installation

```bash
cd "$HOME/Library/Application Support/Sublime Text 3/Packages"
rm -rf User/
git clone https://github.com/chbrown/SublimeTextPackagesUser.git User
```


## Changes

Some of Sublime Text's plugins (or Sublime Text itself) will make changes to the `.sublime-settings` files,
ending up with a variety of JSON formatting flavors.

Run `./make.sh` to standardize indentation.

* `make.sh` calls <code>jq . <i>file</i> | sponge <i>file</i></code> for each file matching the glob `*.sublime-*`.
* It depends on [`jq`](http://stedolan.github.io/jq/) for JSON formatting, and uses the default output spacing.
* If any of your `*.sublime-*` files are not valid JSON, `jq` will display a parse error,
  and the script will not rewrite that file.


### Package control installation

1. Open up the Sublime Text 3 console: <code>ctrl + `</code>
2. Go to [sublime.wbond.net/installation](https://sublime.wbond.net/installation)
3. Copy and paste the install code into the ST3 console

Bugz v0.0.2
===========
Bugz is a simple command line bug tracking tool written in python. It uses
ascii text files (actually pickles at the moment) to keep a database of 
bugs so it can live in the source tree of the project and become part of 
the versioning system.

Installing
----------
Unfold the archive or checkout the source tree and type:

`$> sudo python setup.py install`

to install or

`$> chmod +x ./bgz`

and run it in place.

Now you can run `bgz --help` from the root of your source tree and 
possibly figure out the rest. Reading the source may help or hinder.

Config
------
~/.bugzrc

    # comment
    ; another comment
    user=your name
    email=me@someplace.com
    editor=vi


Running
-------
Bugz will walk up the directory tree to find its files so you can run it 
from anywhere in the tree.

Commands
--------
- `init`              - initialize a new db
- `add`               - add a new issue
- `status`            - get the db status
- `drop [ID]`         - drop an issue
- `edit [ID]`         - edit an issue
- `comment [ID]`      - comment on an issue
- `show [ID|FIELD]`   - show an issue. FIELD like s:open OR t:bug
- `open [ID]`         - open an issue
- `close [ID]`        - close an issue
- `time [add ID|DR]`  - add time or show by daterange (DR see below)


Dates
-----
Date ranges can be given to `show` and `time` commands. They look like

`STARTDATE[-ENDDATE]`

`ENDDATE` defaults to now().

understand english ranges like:

- lw | lastw[eek] - one week from a week ago monday
- t[oday] | n[ow] - from midnight to now
- y[esterday]     - midnight to midnight

understands dates like:

- YYYY.mm.dd | dd.mm.YYYY | mm.dd.YYYY
- delim between fields in a date can be ':' | '/' | '-' | '.'
  but if given a range '-' will conflict with delim between start and end dates


Changes
-------
- 2010-02-22 - basic handling of assoc time with an issue  		v0.0.2
- 2010-02-18 - pushed to http://github.com/mtvee/bgz       		v0.0.1

TODO
----
- [ ] easy ties/links to various VCSs?
- [-] some easy way to keep track of time spent and totals
- [ ] report output, templates??
- [-] need better search params for reports
- [ ] account for windows' path stuff
- [-] write some real unit tests once the commands are solidified

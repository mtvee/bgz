_\o/_   Bugz 
/(_)\   v0.0.3
==============
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
PROJECT/.bugz/_bugzrc

---[snip]---
    # comment
    ; another comment
    user=your name
    email=me@someplace.com
    editor=mate -w
---[snip]---

Running
-------
Bugz is very git like. Here's a quick sample sesh...

    cd my/cool/project
    bgz init
    >> Initialized .bugz
    bgz add task
    >> Title: Do something
    >> Author [me]: 
    >> Added:     ad6cfa42 - t/new    -  0:00 - Do something
    bgz status
    >> Status:  new/1  open/0  closed/0 
    >> Task
    >> ----
    >>    ad6cfa42 - t/new    -  0:00 - Do something

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
- `config [global]`   - set some configuration variables
- `purge`             - move closed issues to a purged directory

Changes
-------
- 2010-03-11 - better reporting, config system							  v0.0.3
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

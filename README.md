    _\o/_   Bugz 
    /(_)\   v0.2.3

Bgz is a simple command line issue tracking tool written in python. It uses
xml text files to keep a repository of issues so it can live in the source
tree of the project and become part of the source versioning system

Installing
----------
You can find the code at http://github.com/mtvee/bgz

Unfold the archive or checkout the source tree and:

`$> sudo python setup.py install`

to install or

`$> chmod +x ./bgz`

and run it in place.

Now you can run `bgz --help` from the root of your source tree and 
possibly figure out the rest. Reading the source may help or hinder.

Running
-------
Bugz is git like. Here's a quick sample sesh...

    $> cd my/cool/project
    $> bgz init
    >> Initialized .bugz
    $> bgz add task
    >> Adding new task
    >> Title: Do something
    >> Author [me]:
    -> runs editor to add a description 
    >> Added:     ad6cfa42 - t/new    -  0:00 - Do something
    $> bgz status
    >> Status:  new/1  open/0  closed/0 
    >> Task
    >> ----
    >>    ad6cfa42 - t/new    -  0:00 - Do something

Bugz will walk up the directory tree to find its files so you can run it 
from anywhere in the tree.

Commands
--------
Usage: 

    $> bgz [COMMAND] [ARG,...]

Commands are:

- `help`              - show help
- `init`              - initialize a new db
- `add`               - add a new issue or project
- `status`            - get the db status
- `drop [ID]`         - drop an issue or project
- `edit [ID]`         - edit an issue
- `comment [ID]`      - comment on an issue
- `show [ID|FIELD]`   - show an issue. FIELD like s:open OR ty:bug
- `open [ID]`         - open an issue
- `close [ID]`        - close an issue
- `time [add ID|DR]`  - add time or show by daterange (DR see `Dates` below)
- `config [--global]` - show/set some configuration variables
- `purge`             - move closed issues to a purged directory

Filtering
---------
You can filter the `show` command using `field:criteria`. Current the filterable
fields are [s]tatus, [ty]pe, [ti]tle, [a]uthor and [d]ate.

e.g.

    s:o
    status:o
    status:open
    type:task

Dates
-----
Dates can be input as a range. See `help time` for a list of date range syntax.
These work also for the `show` command.

    tw | [thisw]eek = this week (Monday - Sunday)
    lw | [lastw]eek = last week (Monday - Sunday)
    [y]esterday     = (midnight - midnight)
    [t]oday | [n]ow = (midnight - now)
    DD/MM/YYYY[:DD/MM/YYYY]


Projects
--------
Bugz can keep track of projects you are working on and report logged time 
across those projects. From the working area of a project you can `add` or 
`drop` the project. The `time` command will report across all currently
active projects.

Config
------
- (global) ~/.bugzrc
- (local)  PROJECT/.bugz/_bugzrc

    ---[snip]---
    # comment
    ; another comment
    user.name=your name
    user.email=me@someplace.com
    editor=vi
    ansi=on
    ---[snip]---

You can set key values with the 'config' command. For example, to set your
editor to textmate:

    $> bgz config editor "mate -w"

or to set your name, globally

    $> bgz config --global user.name "j. knight"

Recognized configuration items are:

    user.name   [string]
    user.email  [string]
    editor      [string]
    ansi        [bool]

Boolean items take [yes,on,1] or [no,off,0]

Changes
-------
- 2010-09-08 - fixed rc/conf issues                                     v0.2.2
- 2010-09-07 - better searching with 'show'                             v0.2.1
             - switched to XML format for issue storage
- 2010-03-23 - report time across projects                              v0.1.0
- 2010-03-11 - better reporting, config system, purge                   v0.0.3
- 2010-02-22 - basic handling of assoc time with an issue               v0.0.2
- 2010-02-18 - pushed to http://github.com/mtvee/bgz                    v0.0.1

TODO
----
- [ ] some DVCS integration (user info, etc)
- [ ] report output, templates, xml, json??
- [x] automatic conversion from pickle style repo to xml
- [x] save/load to xml
- [-] need better search params for reports
- [-] account for windows' path stuff
- [-] write some real unit tests once the commands are solidified

LINKS
-----
These might be of interest

- http://www.ericsink.com/entries/dbts_fossil.html
- http://nikolasco.livejournal.com/419924.html
- http://community.livejournal.com/evan_tech/248736.html
- http://oss.segetech.com/bugzilla-svn-wiki.html

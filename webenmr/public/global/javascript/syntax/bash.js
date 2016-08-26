/*
 *  Bash recipe for Chili syntax highlighter for jQuery
 *
 *  Copyright Raoul Snyman <raoul.snyman at saturnlaboratories.co.za>, 2009.
 */
{
      _name: 'bash'
    , _case: true
    , _main: {
          sl_comment: {
              _match: /#.*/
            , _style: 'color: green;'
        }
        , shebang: {
              _match: /#!.*/
            , _style: 'color: green; font-weight: bold;'
        }
        , string: {
              _match: /\b\"(.*)\"\b/
            , _style: 'color: teal;'
        }
        , num: {
              _match: /\b[+-]?(?:\d*\.?\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?\b/
            , _style: 'color: red;'
        }
        , keyword: {
              _match: /\b(if|fi|then|elif|else|for|do|done|until|while|break|continue|case|function|return|in|eq|ne|gt|lt|ge|le)\b/
            , _style: 'color: navy; font-weight: bold;'
        }
        , command: {
              _match: /\b(alias|apropos|awk|bash|bc|bg|builtin|bzip2|cal|cat|cd|cfdisk|chgrp|chmod|chown|chroot|cksum|clear|cmp|comm|command|cp|cron|crontab|csplit|cut|date|dc|dd|ddrescue|declare|df|diff|diff3|dig|dir|dircolors|dirname|dirs|du|echo|egrep|eject|enable|env|ethtool|eval|exec|exit|expand|export|expr|false|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|gawk|getopts|grep|groups|gzip|hash|head|history|hostname|id|ifconfig|import|install|join|kill|less|let|ln|local|locate|logname|logout|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|make|man|mkdir|mkfifo|mkisofs|mknod|more|mount|mtools|mv|netstat|nice|nl|nohup|nslookup|open|op|passwd|paste|pathchk|ping|popd|pr|printcap|printenv|printf|ps|pushd|pwd|quota|quotacheck|quotactl|ram|rcp|read|readonly|renice|remsync|rm|rmdir|rsync|screen|scp|sdiff|sed|select|seq|set|sftp|shift|shopt|shutdown|sleep|sort|source|split|ssh|strace|su|sudo|sum|symlink|sync|tail|tar|tee|test|time|times|touch|top|traceroute|trap|tr|true|tsort|tty|type|ulimit|umask|umount|unalias|uname|unexpand|uniq|units|unset|unshar|useradd|usermod|users|uuencode|uudecode|v|vdir|vi|watch|wc|whereis|which|who|whoami|wget|xargs|yes)\b/
            , _style: 'color: purple; font-weight: bold;'
        }
    }
}

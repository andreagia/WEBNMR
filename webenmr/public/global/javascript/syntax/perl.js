/*
 *  Perl recipe for Chili syntax highlighter for jQuery
 *
 *  Copyright Raoul Snyman <raoul.snyman at saturnlaboratories.co.za>, 2009.
 */
{
      _name: 'perl'
    , _case: true
    , _main: {
          sl_comment: {
              _match: /[^$]#[^!].*/
            , _style: 'color: green;'
        }
        , shebang: {
              _match: /#!.*/
            , _style: 'color: green; font-weight: bold;'
        }
        , string: {
              _match: /(?:\'[^\'\\\n]*(?:\\.[^\'\\\n]*)*\')|(?:\"[^\"\\\n]*(?:\\.[^\"\\\n]*)*\")/
            , _style: 'color: teal;'
        }
        , num: {
              _match: /\b(?:\d*\.?\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?\b/
            , _style: 'color: red;'
        }
        , variables: {
              _match: /(\\$|@|%)\\w+/
            , _style: 'color: orange;'
        }
        , keywords: {
              _match: /\b(bless|caller|continue|dbmclose|dbmopen|die|do|dump|else|elsif|eval|exit|for|foreach|goto|if|import|last|local|my|next|no|our|package|redo|ref|require|return|sub|tie|tied|unless|untie|until|use|wantarray|while)\b/
            , _style: 'color: navy; font-weight: bold;'
        }
        , functions: {
              _match: /\b(abs|accept|alarm|atan2|bind|binmode|chdir|chmod|chomp|chop|chown|chr|chroot|close|closedir|connect|cos|crypt|defined|delete|each|endgrent|endhostent|endnetent|endprotoent|endpwent|endservent|eof|exec|exists|exp|fcntl|fileno|flock|fork|format|formline|getc|getgrent|getgrgid|getgrnam|gethostbyaddr|gethostbyname|gethostent|getlogin|getnetbyaddr|getnetbyname|getnetent|getpeername|getpgrp|getppid|getpriority|getprotobyname|getprotobynumber|getprotoent|getpwent|getpwnam|getpwuid|getservbyname|getservbyport|getservent|getsockname|getsockopt|glob|gmtime|grep|hex|index|int|ioctl|join|keys|kill|lc|lcfirst|length|link|listen|localtime|lock|log|lstat|map|mkdir|msgctl|msgget|msgrcv|msgsnd|oct|open|opendir|ord|pack|pipe|pop|pos|print|printf|prototype|push|quotemeta|rand|read|readdir|readline|readlink|readpipe|recv|rename|reset|reverse|rewinddir|rindex|rmdir|scalar|seek|seekdir|select|semctl|semget|semop|send|setgrent|sethostent|setnetent|setpgrp|setpriority|setprotoent|setpwent|setservent|setsockopt|shift|shmctl|shmget|shmread|shmwrite|shutdown|sin|sleep|socket|socketpair|sort|splice|split|sprintf|sqrt|srand|stat|study|substr|symlink|syscall|sysopen|sysread|sysseek|system|syswrite|tell|telldir|time|times|tr|truncate|uc|ucfirst|umask|undef|unlink|unpack|unshift|utime|values|vec|wait|waitpid|warn|write)\b/
            , _style: 'color: navy;'
        }
    }
}

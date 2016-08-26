/*
 *  Ruby recipe for Chili syntax highlighter for jQuery
 *
 *  Copyright Raoul Snyman <raoul.snyman at saturnlaboratories.co.za>, 2009.
 */
{
      _name: 'ruby'
    , _case: true
    , _main: {
          sl_comment: {
              _match: /#[^\n]+/
            , _style: 'color: green;'
        }
        , string: {
              _match: /'[^']*'|"[^"]*"/
            , _style: 'color: teal;'
        }
        , num: {
              _match: /\b[+-]?(?:\d*\.?\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?\b/
            , _style: 'color: red;'
        }
        , statement: {
              _match: /\b(alias|and|BEGIN|begin|break|case|class|def|define_method|defined|do|each|else|elsif|END|end|ensure|false|for|if|in|module|new|next|nil|not|or|raise|redo|rescue|retry|return|self|super|then|throw|true|undef|unless|until|when|while|yield|Array|Bignum|Binding|Class|Continuation|Dir|Exception|FalseClass|File::Stat|File|Fixnum|Fload|Hash|Integer|IO|MatchData|Method|Module|NilClass|Numeric|Object|Proc|Range|Regexp|String|Struct::TMS|Symbol|ThreadGroup|Thread|Time|TrueClass)\b/
            , _style: 'color: navy; font-weight: bold;'
        }
    }
}

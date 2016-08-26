/*
 *  Diff recipe for Chili syntax highlighter for jQuery
 *
 *  Copyright Raoul Snyman <raoul.snyman at saturnlaboratories.co.za>, 2009.
 */
{
      _name: 'diff'
    , _case: false
    , _main: {
          added_lines: {
              _match: /\n\+\+\+.*/
            , _style: 'color: green;'
        }
        , removed_lines: {
              _match: /\n\-\-\-.*/
            , _style: 'color: red;'
        }
        , lines_affected: {
              _match: /\n@@.*@@/
            , _style: 'color: blue;'
        }
        , added_line: {
              _match: /\n\+[^\+]{1}.*/
            , _style: 'color: green;'
        }
        , removed_line: {
              _match: /\n\-[^\-]{1}.*/
            , _style: 'color: red;'
        }
        , index_line: {
              _match: /\n?Index\:.*/
            , _style: 'color: purple;'
        }
    }
}

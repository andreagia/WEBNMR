/*
 *  XML recipe for Chili syntax highlighter for jQuery
 *
 *  Copyright Raoul Snyman <raoul.snyman at saturnlaboratories.co.za>, 2009.
 */
{
      _name: 'xml'
    , _case: false
    , _main: {
          comment: {
              _match: /<!--[\w\W]*?-->/
            , _style: "color: #4040c2;"
        }
        // matches a starting tag of an element (with attrs)
        // like "<div ... >" or "<img ... />"
        , tag_start: {
              _match: /(<\w+)((?:[?%]>|[\w\W])*?)(\/>|>)/
            , _replace: function( all, open, content, close ) {
                  return "<span class='tag_start'>" + this.x( open ) + "</span>"
                      + this.x( content, '/tag_attrs' )
                      + "<span class='tag_start'>" + this.x( close ) + "</span>";
            }
            , _style: "color: navy; font-weight: bold;"
        }
        // matches an ending tag
        // like "</div>"
        , tag_end: {
              _match: /<\/\w+\s*>|\/>/
            , _style: "color: navy;"
        }
        , entity: {
              _match: /&\w+?;/
            , _style: "color: blue;"
        }
    }
    , tag_attrs: {
        // matches a name/value pair
        attr: {
            // before in $1, name in $2, between in $3, value in $4
              _match: /(\W*?)([\w-]+)(\s*=\s*)((?:\'[^\']*(?:\\.[^\']*)*\')|(?:\"[^\"]*(?:\\.[^\"]*)*\"))/
            , _replace: "$1<span class='attr_name'>$2</span>$3<span class='attr_value'>$4</span>"
            , _style: { attr_name:  "color: green;", attr_value: "color: maroon;" }
        }
    }
}

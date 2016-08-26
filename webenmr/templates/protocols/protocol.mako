<%inherit file="/base.mako"/>
<%def name="css()">
     <link rel="stylesheet" type="text/css" href="/global/javascript/contextmenu/jquery.contextmenu.css"></link>
     <link rel="stylesheet" type="text/css" href="/global/css/protocol.css"></link>
     <style type="text/css">
          #simplemodal-overlay {background-color:#000;}
          #simplemodal-container {background-color: #eee; border:4px solid #6495ED; padding:12px; font: 13px; text-align:left;}
          #simplemodal-container a.modalCloseImg {
              background:url('/global/images/x.png') no-repeat;
              width:25px;
              height:29px;
              display:inline;
              z-index:3200;
              position:absolute;
              top:-15px;
              right:-18px;
              cursor:pointer;
          }
          #infop{
               display: none;
          }
   </style>
</%def>
<%def name="js()">
     <script type="text/javascript" src="/global/javascript/contextmenu/jquery.contextmenu.js"></script>
     <script type="text/javascript" src="/global/javascript/protocols.js"></script>
     <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
     <!--<script type="text/javascript" src="/global/javascript/jquery.tools.min.js" ></script>-->
    
    <!--<script  type="text/javascript">-->
    <!--    -->
    <!--    -->
    <!--</script>-->
</%def>
<fieldset class="quickintro">
     <legend>Quick introduction to the taskbar</legend>
     <ul>
        <li>click on <img src="/global/images/p.png"> to create a new protocol</li>
        <!--<li>click on <img src="/global/images/amber.png"> to create a new Amber calculation for selected project</li>-->
        <!--<li>click on <img src="/global/images/jobs.gif"> to show jobs status for selected calculation</li>-->
        <!--<li>click on <img src="/global/images/floppy.png"> to download selected protocol(s)</li>-->
        <li>click on <img src="/global/images/edit.png"> to modify existing protocol</li>
        <li>click on <img src="/global/images/rem.png"> to completely remove selected protocol(s)</li>
        <li>click on <img src="/global/images/quicklook.png"> to a preview of protocol (step-by-step)</li>
     </ul>
</fieldset>



<div id="finder">
    
    <div id="toolbar" class="el-finder-toolbar">
        <ul>
            <!--<div title="Filemanager for your AMBER projects" class="el-finder-dock-button"> </div>-->
            <!--<li name="back" title="Back" class="back"></li>-->
            <!--<li name="reload" title="Reload" class="reload disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="open" title="Open" class="open disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="mkdir" title="New folder" class="mkdir disabled"></li>-->
            <!--<li name="mkfile" title="New text file" class="mkfile disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="cut" title="Cut file(s)" class="cut disabled"></li>-->
            <!--<li name="paste" title="Paste file(s)" class="paste disabled"></li>-->
            <!--<li class="delim"></li>-->
            <li name="edit" title="Edit protocol" class="edit disabled"></li>
            <li name="rename" title="Rename protocol" class="rename disabled"></li>    
            <li name="rm" title="Remove protocol(s)/step(s)" class="rm disabled"></li>
            <li class="delim"></li>
            <li name="protocol" title="Create new protocol" class="protocol"></li>
            <!--<li name="amber" title="Add new Amber calculation" class="amber disabled"></li>-->
            <li class="delim"></li>
            <!--<li name="jobs" title="Show jobs status for selected calculation" class="jobs disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="download" title="Download file(s)/directory" class="download disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="info" title="Get info" class="info disabled"></li>-->
            <li name="quicklook" title="Preview of content" class="quicklook disabled"></li>
            <li class="delim"></li>
            <!--<li name="icons" title="View as icons" class="icons disabled"></li>-->
            <!--<li name="list" title="View as list" class="list"></li>-->
            <!--<li class="delim"></li>-->
            <li name="help" title="Help" class="help"></li>
        </ul>
    </div>
    
     <div id="leftmenu">
          <ul id="menufinder">
               <li>
                    <a href="#" class="ui-selectee">
                        <div class="expanded"></div>
                        <p id="menuleft" class="dir_home open expanded"></p>
                        <i><b>Protocols</b></i>
                    </a>
                    <ul id="menulist">
                         <li>
                              <a>
                                   <div class="collapsed"></div>
                                   <p id="menuleft" class="dir_small close collapsed"></p>
                                   <i>Preset</i>
                              </a>
                         </li>
                         <li>
                              <a>
                                   <div class="collapsed" ></div>
                                   <p id="menuleft" class="dir_small close collapsed"></p>
                                   <i>Personal</i>
                              </a>
                         </li>
                    </ul> 
               </li>
          </ul>
     </div>
    <div id="rightmenu">
        <ul id="contentlist">
            
        </ul>
    </div>
    <div id="help">
        <b>Quick help to use Protocols Filemanager</b><br><br>
        This protocols manager work similar to file manager on your computer.<br>
        To make actions on file/folders use icons on top panel.
        If icon action it is not clear for you, hold mouse cursor
        over it to see the hint. Manipulations with existing file(s)/folder(s) can be
        done also through the context menu (mouse right-click). To Download/Delete
        a group of file(s)/folder(s), select them using Ctrl command + mouse
        left-click.<br>
        <!--Protocol Filemanager support following shortcuts:-->
        <!--<ul>-->
        <!--    <li>Ctrl+5 - Select all files</li>-->
        <!--    <li>Del/Backspace - Remove selected file(s)/folder(s)</li>-->
        <!--    <li>Ctrl+D - Download file(s)/folder(s)</li>-->
        <!--    <li>Ctrl+R - Remove file(s)/folder(s)</li>-->
        <!--</ul>-->
    </div>
</div>
     <div id="protocol">
          <div id="description">
               <p><b>Select a protocol</b> already defined,  
                <b>copy and paste</b> a protocol (use <b>CTRL+v</b> to paste clipboard contents, because right-click is disabled),
                or <b>build</b> a new protocol with help of lightweight Sander manual.  
               </p>
          </div>
          <div id="keyplushead">
               <div id="header-sander">
                    <span>Choose section view: </span>
                    <button id="bcontrol">control</button>
                    <button id="bewald">ewald</button>
                    <button id="bwt">wt</button>
                    <button id="bdebug">debug</button><br>
                    <span>Choose mode view: </span>
                    <input type="radio" id="bmode" name="mode" value="basic" checked> basic
                    <input type="radio" id="emode" name="mode" value="expert"> extended <br />
               </div>
               <div id="keyboard">
                    <h3><a href="#">Section 1</a></h3>
                    <div>
                         <p>
                         Mauris mauris ante, blandit et, ultrices a, suscipit eget, quam. Integer
                         ut neque. Vivamus nisi metus, molestie vel, gravida in, condimentum sit
                         amet, nunc. Nam a nibh. Donec suscipit eros. Nam mi. Proin viverra leo ut
                         odio. Curabitur malesuada. Vestibulum a velit eu ante scelerisque vulputate.
                         </p>
                    </div>
                    <h3><a href="#">Section 2</a></h3>
                    <div>
                         <p>
                         Sed non urna. Donec et ante. Phasellus eu ligula. Vestibulum sit amet
                         purus. Vivamus hendrerit, dolor at aliquet laoreet, mauris turpis porttitor
                         velit, faucibus interdum tellus libero ac justo. Vivamus non quam. In
                         suscipit faucibus urna.
                         </p>
                    </div>
                    <h3><a href="#">Section 3</a></h3>
                    <div>
                         <p>
                         Nam enim risus, molestie et, porta ac, aliquam ac, risus. Quisque lobortis.
                         Phasellus pellentesque purus in massa. Aenean in pede. Phasellus ac libero
                         ac tellus pellentesque semper. Sed ac felis. Sed commodo, magna quis
                         lacinia ornare, quam ante aliquam nisi, eu iaculis leo purus venenatis dui.
                         </p>
                         <ul>
                                 <li>List item one</li>
                                 <li>List item two</li>
                                 <li>List item three</li>
                         </ul>
                    </div>
                    <h3><a href="#">Section 4</a></h3>
                    <div>
                         <p>
                         Cras dictum. Pellentesque habitant morbi tristique senectus et netus
                         et malesuada fames ac turpis egestas. Vestibulum ante ipsum primis in
                         faucibus orci luctus et ultrices posuere cubilia Curae; Aenean lacinia
                         mauris vel est.
                         </p>
                         <p>
                         Suspendisse eu nisl. Nullam ut libero. Integer dignissim consequat lectus.
                         Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
                         inceptos himenaeos.
                         </p>
                    </div>
               </div>
          </div>
          <div id="rightside">
               <div id="protocol-manager">
                    <select name="protocol">
                        <option value="none">Select protocol</option>
                        <optgroup id="preset" label="Preset">
                         </optgroup>
                        <optgroup id="personal" label="Personal">
                         </optgroup>
                    </select>
                    <br />
               </div>
               <div id="parameters-sander">
                    <fieldset>
                         <legend>Sander parameters viewer</legend>
                         <p class="multistep_header nodisplay">Choose what step (also more than one) modify or include in the new protocol:</p>
                         <div id="textarea_sander">
                              <textarea id="param-list" name="param-list" class="txtsander" rows="15" cols="38"></textarea>
                         </div>
                         <div id="multistep" style="display: none;">
                              <!--deve uscire quando esce salva oppure quando c'è un multistep-->
                              <!--<a href="javascript:add_step()" title="Add new step">add new step</a>-->
                         </div>
                    </fieldset>
               </div>
          </div>
     </div>
     <div id="infop">
          <button class="retcp" type="button">back to create protocol</button>
     </div>
     <input type="button" value="pigiami" onclick="createProtocol()"/>

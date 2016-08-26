<%inherit file="/base.mako"/>
<%def name="css()">
   <link rel="stylesheet" type="text/css" href="/global/javascript/contextmenu/jquery.contextmenu.css"></link>
   <link rel="stylesheet" type="text/css" href="/global/css/filemanager.css"></link>
   <style type="text/css">
        #simplemodal-overlay {background-color:#000;}
        #simplemodal-container {background-color: #eee; border:4px solid #6495ED;  font: 13px; text-align:left;}
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
   </style>
</%def>
<%def name="js()">
    <script type="text/javascript" src="/global/javascript/contextmenu/jquery.contextmenu.js"></script>
    <script type="text/javascript" src="/global/javascript/filemanager.js"></script>
            <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <!--<script type="text/javascript" src="/global/javascript/topup1.7.2/javascripts/top_up-min.js"></script>-->
    <!--<script  type="text/javascript">-->
    <!--    -->
    <!--    -->
    <!--</script>-->
</%def>
    
<fieldset class="quickintro">
     <legend>Quick introduction to the taskbar</legend>
     <ul>
        <li>click on <img src="/global/images/project_add.png"> to create a new project</li>
        % if session['PORTAL'] == 'amps-nmr':
          <li>click on <img src="/global/images/amber.png"> to create a new AMBER calculation for selected project</li>
        % else:
          <li>click on <img src="/global/images/amber.png"> to create a new ${session['PORTAL'].capitalize()} calculation for selected project</li>
        % endif
        <li>click on <img src="/global/images/jobs.gif"> to show jobs status for selected calculation</li>
        <li>click on <img src="/global/images/floppy.png"> to download selected file(s), project or calculation(s)</li>
        % if session["PORTAL"] == 'amps-nmr':
          <li>click on <img src="/global/images/bundle.png"> to download only last pdb and sander output file, for each job in the calculation</li>
          <li>click on <img src="/global/images/chart-bar.jpg"> to download violations report for selected calculation</li>
         %endif
        <li>click on <img src="/global/images/edit.png"> to edit name of selected project or calculation</li>
        <li>click on <img src="/global/images/rem.png"> to completely remove selected project or calculation(s)</li>
     </ul>
</fieldset>

<div style="text-align: center">
     % if session['PORTAL'] == 'amps-nmr':
          <b>Note that Amber results (entire calculation folders) will be deleted permanently after two weeks. </b>
        % elif session['PORTAL'] == 'maxocc':
          <b>Note that MaxOcc results (entire calculation folders) will be deleted permanently after two weeks. </b>
        % elif session['PORTAL'] == 'xplor-nih':
          <b>Note that XPLOR-NIH results (entire calculation folders) will be deleted permanently after two weeks. </b>
        % endif
</div>

<div id="statusbar">
        <div class="el-finder-path">Projects</div>
        <!--<div class="el-finder-stat">items: , size: </div>-->
        <!--<div class="el-finder-sel"></div>-->
</div>
<div id="finder">
    
    <div id="toolbar" class="el-finder-toolbar">
        <ul>
            <!--<div title="Filemanager for your AMBER projects" class="el-finder-dock-button"> </div>-->
            <!--<li name="back" title="Back" class="back"></li>-->
            <!--<li name="reload" title="Reload" class="reload disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="open" title="Open" class="open disabled"></li>-->
            <!--<li class="delim"></li>-->
            <li name="mkdir" title="New folder" class="mkdir disabled"></li>
            <li name="mkfile" title="New text file" class="mkfile disabled"></li>
            <li class="delim"></li>
            <!--<li name="cut" title="Cut file(s)" class="cut disabled"></li>-->
            <!--<li name="paste" title="Paste file(s)" class="paste disabled"></li>-->
            <!--<li class="delim"></li>-->
            <li name="edit" title="Edit file" class="edit disabled"></li>
            <li name="rename" title="Rename project/calculation name" class="rename disabled"></li>    
            <li name="rm" title="Remove project(s)/calculation(s)" class="rm disabled"></li>
            <li class="delim"></li>
            <li name="project" title="Create new project" class="project"></li>
            % if session['PORTAL'] == 'amps-nmr':
               <li name="amber" title="Add new AMBER calculation" class="amber disabled"></li>
            % else:
               <li name="amber" title="Add new ${session['PORTAL'].capitalize()} calculation" class="amber disabled"></li>
            % endif
            <li class="delim"></li>
            <li name="jobs" title="Show jobs status for selected calculation" class="jobs disabled"></li>
            <li class="delim"></li>
            <li name="download" title="Download file(s)/directory" class="download disabled"></li>
             % if session["PORTAL"] == 'amps-nmr':
               <li name="downloadbundle" title="Download only last pdb and sander output file, for each job in the calculation" class="downloadbundle disabled"></li>
               <li name="downloadbundle" title="Download violations report for selected calculation" class="violations disabled"></li>
             %endif
             % if session["PORTAL"] == 'xplor-nih':
               <li name="downloadbundlexplor" title="Download all Xplor-NIH pdbs for each job in the selected calculation" class="downloadbundlexplor disabled"></li>
               <li name="analysisxplor" title="Analysis of results" class="analysisxplor disabled"></li>
             %endif
            <li class="delim"></li>
            <!--<li name="info" title="Get info" class="info disabled"></li>-->
            <!--<li name="quicklook" title="Preview with Quick Look" class="quicklook disabled"></li>-->
            <!--<li class="delim"></li>-->
            <!--<li name="icons" title="View as icons" class="icons disabled"></li>-->
            <!--<li name="list" title="View as list" class="list"></li>-->
            <!--<li class="delim"></li>-->
            <li name="help" title="Help" class="help"></li>
        </ul>
    </div>
    
    <div id="leftmenu">
        % if not c.dirlist == 'error':
            <ul id="menufinder">
                <li>
                    <a href="#" class="ui-selectee">
                        <div class="expanded"></div>
                        <p id="menuleft" class="dir_home open expanded"></p>
                        <i><b>Projects</b></i>
                    </a>
                    <ul  id="menulist">
                        % for item in c.dirlist:
                            <li>
                                <a>
                                    <div class="collapsed" ></div>
                                    <p id="menuleft" class="dir_small close collapsed"></p>
                                    <i>${item}</i>
                                </a>
                            </li>
                        % endfor
                    </ul>
                </li>
            </ul>
        % endif
    </div>
    <div id="rightmenu">
        <ul id="contentlist">
            
        </ul>
    </div>
    <div id="help">
        <b>Quick help to use ${session['PORTAL'].upper()} Web Portal Filemanager</b><br><br>
        This filemanager work similar to file manager on your computer.<br>
        To make actions on file/folders use icons on top panel.
        If icon action it is not clear for you, hold mouse cursor
        over it to see the hint. <!--Manipulations with existing file(s)/folder(s) can be
        done also through the context menu (mouse right-click).--> To Download/Delete
        a group of file(s)/folder(s), select them using Ctrl command + mouse
        left-click.<br>
        <!--Amber Web Portal Filemanager support following shortcuts:-->
        <!--<ul>-->
        <!--    <li>Ctrl+5 - Select all files</li>-->
        <!--    <li>Del/Backspace - Remove selected file(s)/folder(s)</li>-->
        <!--    <li>Ctrl+D - Download file(s)/folder(s)</li>-->
        <!--    <li>Ctrl+R - Remove file(s)/folder(s)</li>-->
        <!--</ul>-->
    </div>
</div>

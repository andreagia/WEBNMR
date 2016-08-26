<%inherit file="/base.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
   
</%def>

<%def name="js()">
<script type="text/javascript" src="/global/javascript/jquery.easing.js"></script>
<script type="text/javascript" src="/global/javascript/jqueryFileTree.js"></script>
<script  type="text/javascript">
$(document).ready( function() {
    
    
    
    (function() {
        // modify all calls to showTree
        var proxied = jQuery.fn.showTree;
        jQuery.fn.showTree = function(c, t) {
            alert("pippotto di un proxy");
            $(c).addClass('wait');
            $(".jqueryFileTree.start").remove();
            $.post(o.script, { dir: t }, function(data) {
                    $(c).find('.start').html('');
                    $(c).removeClass('wait').append(data);
                    if( o.root == t ){
                        $(c).find('UL:hidden').show();
                    }
                    else {
                        $(c).find('UL:hidden').slideDown({ duration: o.expandSpeed, easing: o.expandEasing });
                        $("#actions").find('UL:hidden').slideDown({ duration: o.expandSpeed, easing: o.expandEasing });
                    }
                    bindTree(c);
            });
        };
    })();

    
    $("#file_details").html("");
    $('#container_id').fileTree({
        root: '${c.pdir}/amber',
        script: '/filesystem/dirlist',
        expandSpeed: 750,
        collapseSpeed: 750,
        multiFolder: false
    }, function(file) {
        $.post("/filesystem/checkfile", { file: file },
                function(data){
                    $("#file_details").html(data);
                    $("#actions").children("a").remove();
                    var action = '<a href="/filesystem/download?requested_filename='+file+'"><img src="/global/images/download.png" border="0" title="Download file"></a>';
                    $("#actions").append(action);
                    var ext = file.split(".")[1];
                    if (ext == 'pdb'){
                        action = '<a href="javascript:open_jmolView(\''+file+'\');"><img src="/global/images/jmol.gif" border="0" title="View file in Jmol"></a>';
                        $("#actions").append(action);
                    }
                });       
    });
    //var ul_list = '<ul style="display: none;">';
    //$("#container_id").children('ul').children("li").each(function(){
    //    ul_list += "<li><a href='javascript:alert($(this).children('a').text())'>$(this).children('a').text()</a></li>";
    //});
    //ul_list += "<li>pippo</li></ul>"
    //
    //$("#actions").append(ul_list);
    
    
    
    
 });
</script>

<script type="text/javascript">
    function open_jmolView(filename){
                //alert(id)
                //var suffix = id.split('chain_')[1];
                //alert(suffix)
                
                //if(name == ""){
                //    var file_name = suffix+"_c.pdb";
                //}
                //else{
                //    var file_name = name;
                //}
                
                //var xhr = XMLHttpRequest();
                var name= "";
                var file_name = filename.split("/");
                var len = file_name.length;
                var namefile = file_name[len-1]; 
                $.ajax({
                    url: "/filesystem/jmol_file",
                    data: "file_name="+filename,
                    success: function(data){
                        
                        data = data.replace(/\n/g, "|");
                        
                        var obj = '<object name="jmolApplet0" id="jmolApplet0" classid="java:JmolApplet" type="application/x-java-applet" height="500" width="500">'+
                                        '<param name="syncId" value="216291259819275">'+
                                        '<param name="progressbar" value="true">'+
                                        '<param name="progresscolor" value="blue">'+
                                        '<param name="boxbgcolor" value="black">'+
                                        '<param name="boxfgcolor" value="white">'+
                                        '<param name="boxmessage" value="Downloading JmolApplet ...">'+
                                        '<param name="name" value="jmolApplet0">'+
                                        '<param name="archive" value="JmolApplet0.jar">'+
                                        '<param name="mayscript" value="true">'+
                                        '<param name="codebase" value="/global/jmol">'+
                                        '<param name="loadInline" value="'+data+'">';
                                        if (name == ''){
                                            obj += '<param name="script" value="select *">';
                                        }
                                        else{
                                            obj += '<param name="script" value="select atomname=MEX, atomname=AX; connect single;'+
                                            'select atomname=MEX, atomname=AY; connect single;'+
                                            'select atomname=MEX, atomname=AZ; connect single;'+
                                            'select atomname=MEX or atomname=AX or atomname=AY or atomname=AZ;'+
                                            'label %a; select protein; cartoons; color structure;'+
                                            'select protein; spacefill off; wireframe off;">';
                                        }
                                        
                                        obj += '<p style="background-color: yellow; color: black; width: 400px; height: 400px; text-align: center; vertical-align: middle;">'+
                                            'You do not have Java applets enabled in your web browser, or your browser is blocking this applet.<br>'+
                                            'Check the warning message from your browser and/or enable Java applets in<br>'+
                                            'your web browser preferences, or install the Java Runtime Environment from <a href="http://www.java.com">www.java.com</a><br></p>'+
                                            '</object>';
                                    
                         var $dialog = $('<div></div>');
                            $dialog.html(obj);
                            $dialog.dialog({
                                autoOpen: false,
                                title: "Jmol Chemical structure of "+namefile,
                                width: 540,
                                height: 570,
                                modal: false
                            });
                            
                            $dialog.dialog('open');
                            //if(name != ""){
                                //var script= 'select atomname=MEX, atomname=AX; connect single; select atomname=MEX, atomname=AY; connect single; select atomname=MEX, atomname=AZ; connect single; select atomname=MEX or atomname=AX or atomname=AY or atomname=AZ; label %a';
                                //jmolScript(script);
                            //}
                    }
                });

            }
</script>

</%def>
<h2></h2>
<div class="item-list">
    <div  class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Project: <b>${c.pname}</b></a>
                </legend>
                <div class="content">
                  
                    <table id="tableabssorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
                        <thead>
                            <tr>
                                <th>Directory</th><th>File Details</th><th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>
                               <div id="container_id"></div>
                            </td>
                     
                            <td>
                                <div id="file_details"></div>
                            </td>
                            <td><div id="actions"></div></td>
                        </tr>
                        </tbody>                      
                    </table>
                    <a href="${h.url('/projects/list')}">Return to project list</a>
                </div>
            </fieldset>
        </div>
    </div>
</div>

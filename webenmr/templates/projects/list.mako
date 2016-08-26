<%! import datetime %>
<%inherit file="/base.mako"/>
<%def name="js()">
 <script  type="text/javascript">

 $(document).ready(function() {
   // call the tablesorter plugin 
    $("table") 
    .tablesorter({widthFixed: true, widgets: ['zebra'], sortList: [[0,0]]}) 
    .tablesorterPager({container: $("#pager")}); 
 });

function check_download(id){  
  $.ajax({
         type: "POST",
         async: false,
         url: "/projects/check_download/"+id,
         success: function(data){
            if (data == "ok"){
              var str = '<acronym id="down" title="Download the project"><a href="/projects/project_download/'+id+'"><img src="/webenmr/images/b_save.png"></a></acronym>';
              $("a[href=javascript:project_tar("+id+")]").parent().after(str);
              $("a[href=javascript:project_tar("+id+")]").parent().remove();
            }
            else{
              var str = '<acronym id="comp" title="Compress the project">'+
                        '<a id="compress" href="javascript:project_tar('+id+')"><img src="/global/images/compress.png"></a>'+
                        '</acronym>'
              $("a[href=/projects/project_download/"+id+"]").parent().after(str);
              $("a[href=/projects/project_download/"+id+"]").parent().remove();
            }
         }
  });
}

function project_tar(id){
  var valid = true;
  var $dialog = $('<div></div>')
      .load("/compress.html")
      .dialog({
          autoOpen: false,
          modal: true,
          closeOnEscape: false,
          open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); },
          title: "Compressing project...",
          width: 230
      });
  $(document).bind('keypress', function(event){ 
    if ((event.which && event.which == 27) || (event.keyCode && event.keyCode == 27)) { // ESC
      $.jGrowl("Failed to compress project. Please, click again on <img src='/global/images/compress.png'> icon.", {header: 'INFORMATION', life: 8000, theme: 'iphone'});  
      var str = '<a id="compress" href="javascript:project_tar('+id+')"><img src="/global/images/compress.png"></a>';
      $("img[id=waiting]").after(str);
      $("img[id=waiting]").remove();
      valid = false;
      $dialog.dialog('close');
    }
  });
  $dialog.dialog('open');
  $.jGrowl("Please wait, system is compressing the project contents. Next message will advise you of possibility to download the project.", {header: 'INFORMATION', life: 7000, theme: 'iphone'});
  var str = '<img id="waiting" alt="Compressing project..." title="Compressing project..." src="/global/images/load.gif"></a>'
  $("a[href=javascript:project_tar("+id+")]").after(str);
  $("a[href=javascript:project_tar("+id+")]").remove();
  $.ajax({
         type: "POST",
         url: "/projects/project_compress/"+id,
         success: function(data){
            if(valid){
              $dialog.dialog('close');
              var str = '<acronym id="down" title="Download the project"><a href="/projects/project_download/'+id+'"><img src="/webenmr/images/b_save.png"></a></acronym>'
              $("img[id=waiting]").parent().after(str);
              $("img[id=waiting]").parent().remove();
              $.jGrowl("The project is compressed. Now, you can download it clicking on <img src='/webenmr/images/b_save.png'> icon.", {header: 'INFORMATION', life: 8000, theme: 'iphone'});
            }
         }
  });
}
</script>
</%def>

<h2></h2>
<div id="explanation">
   <span>Quick help about possible actions:</span>
   <ul>
      <li>click on <img src="/webenmr/images/b_newdb.png"> to create a new Amber calculation</li>
      <li>click on <img src="/webenmr/images/explore.gif"> to browse contents of project</li>
      <li>click on <img src="/global/images/compress.png"> to compress entire project</li>
      <!--<li>click on <img src="/webenmr/images/b_save.png"> to download and save entire project on your hard disk</li>-->
      <li>click on <img src="/webenmr/images/b_drop.png"> to completely remove entire project and it contents</li>
   </ul>
</div>
<div class="item-list">
    <div  class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Projects</a>
                </legend>
                <div class="content">
                    % if c.projects:
                        <table id="tableabssorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
                        <thead>
                        <tr>
                            <th>Project Name</th>
                            <th class="{sorter: false}">Creation Date</th>
                            <th class="{sorter: false}">Owner </th>
                            <th class="{sorter: false}">Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        % for p in c.projects:
                            <tr>
                                <td>${p.name}</td><td><% nt=datetime.datetime.ctime(p.creation_date)%> ${nt}</td><td>${p.owner.lastname}</td>
                                <td>
                                    <acronym title="Explore the project structure">
                                    ${h.image_to('/webenmr/images/explore.gif', '',
                                        h.url(controller=u'filesystem', 
                                        action='explore',
                                        id=unicode(p.id)
                                        ))}
                                    </acronym>
                                    &nbsp;&nbsp;
                                    <script type="text/javascript">
                                      check_download(${p.id});
                                    </script>
                                    <acronym id="comp" title="Compress the project">
                                      <a id="compress" href="javascript:project_tar(${p.id})"><img src="/global/images/compress.png"></a>
                                    </acronym>
                                     &nbsp;&nbsp;
                                    <acronym title="New calculations">
                                    ${h.image_to('/webenmr/images/b_newdb.png', '',
                                        h.url(controller=u'calculations', 
                                        action='amber',
                                        id=unicode(p.id)
                                        ))}
                                    </acronym>
                                    &nbsp;&nbsp;
                                    <acronym title="Remove the project">
                                    ${h.image_to('/webenmr/images/b_drop.png', '',
                                        h.url(controller=u'projects', 
                                        action='project_remove',
                                        id=unicode(p.id)
                                        ))}
                                    </acronym>
                                </td>
                            </tr>
                        % endfor
                        </tbody>
                        </table>
                        <div id="pager" class="tablesorterPager">
                              <form>
                                      <img src="/global/javascript/tablesorter/addons/pager/icons/first.png" class="first"/>
                                      <img src="/global/javascript/tablesorter/addons/pager/icons/prev.png" class="prev"/>
                                      <input type="text" class="pagedisplay"/>
                                      <img src="/global/javascript/tablesorter/addons/pager/icons/next.png" class="next"/>
                                      <img src="/global/javascript/tablesorter/addons/pager/icons/last.png" class="last"/>
                                      <select class="pagesize">
                                              <option selected="selected"  value="10">10</option>
                                              <option value="20">20</option>
                                              <option value="30">30</option>
                                              <option  value="40">40</option>
                                      </select>
                              </form>
                        </div>

                    %endif
                    <br />
                </div>
            </fieldset>
            
        </div>
    </div>
</div>

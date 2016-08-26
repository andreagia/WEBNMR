<%inherit file="/base.mako"/>
<%def name="js()">
<script  type="text/javascript">
	$(document).ready( function() {
	    if ($("input[type=checkbox]").length){
                $("#check").show();
            }
            else{
                $("#check").hide();
            }
	});
 </script>

 <script  type="text/javascript">
    function check(elem){
        var id = elem.val();
        $.ajax({
                type: "GET",
                url: "/jobs/job_status/"+id
        });
    }
    
    function checkAll(){
        $(":checkbox").attr('checked', true);
        $("input[type=checkbox]:checked").each(function(){
            check($(this));    
        });
        if($("input[type=checkbox]:checked").length){
            //window.location='/jobs/show/all';
            location.reload();            
        }
    }
    
    function checkSelected(){
        $("input[type=checkbox]:checked").each(function(){
            check($(this));        
        });
        if($("input[type=checkbox]:checked").length){
            //window.location='/jobs/show/all';
            location.reload();            
        }
        
    }
</script>
</%def>

<h2></h2>
<div class="item-list">
    <div  class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Job List</a>
                </legend>
                <div class="content">
                        <div id="check" style="background: none repeat scroll 0% 0% rgb(206, 227, 246);">
                            check <a style="text-decoration:underline;" href="javascript:checkAll();">all</a> or <a style="text-decoration:underline;" href="javascript:checkSelected();">selected</a> jobs status
                        </div>
                        <table id="tableabssorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
                        <thead>
                        <tr>
                            <th><img src="/global/images/checkbox_green.png"></th>
                            <th>Calculation Name</th>
                            <th>Job Guid</th>
                            <th>Start Date</th>
                            <th>Status</th>
                            <th>Log</th>
                            <th class="{sorter: false}">Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        % for j in c.jobs:
                            <tr>
                                <td>
                                    % if j.status == 'R' or j.status == 'S':
                                        <% id=unicode('%s_%s_%s' % (c.calc_id, c.prj_id, j.id))%>
                                        <input type="checkbox" name="checkStatus" value="${id}">
                                    %endif
                                </td>
                                <td>${j.calculation.name}</td>
                                <td>click <a href="javascript:open_dialog('GUID', '${j.guid}', 450, 180)">here</a> to view</td>
                                <td>${j.start_date}</td>
                                <td>${c.STATUS[j.status]}</td>
                                <td>${j.log}</td>
                                
                                <td>
                                    % if j.status == 'R' or j.status == 'S':
                                        <acronym title="Kill Job">
                                        ${h.image_to('/webenmr/images/b_drop.png', '',
                                            h.url(controller=u'jobs', 
                                            action='job_kill',
                                            id=unicode('%s_%s_%s' % (c.calc_id, c.prj_id, j.id))
                                            ))}
                                        </acronym>
                                    % endif
                                    % if j.status == 'F':
                                        &nbsp;&nbsp;
                                        <acronym title="Retrieve output">
                                        ${h.image_to('/webenmr/images/b_export.png', '',
                                            h.url(controller=u'jobs', 
                                            action='job_retrieve',
                                            id=unicode('%s_%s_%s' % (c.calc_id, c.prj_id, j.id))
                                            ))}
                                        </acronym>
                                    % endif
                                </td>
                            </tr>
                        % endfor
                        </tbody>
                        </table>
                    
                    <br />
                    
                    
                </div>
            </fieldset>
            
        </div>
    </div>
</div>

<%inherit file="/base.mako"/>
<%def name="js()">
 <script  type="text/javascript">

 $(document).ready(function() {
    $("#hidden").hide();
 });
function AddProject() {
 $("#hidden").show();
}

function checkProject() {
 if (! $("#project").val()) {
    jAlert("<br />You have to enter a Project name", "Warning");
    return false;
 }
 return true;
}
</script>
</%def>

<h2></h2>
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
                            <th>Creation Date</th>
                            <th>Owner</th>
                            <th class="{sorter: false}">Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        % for p in c.projects:
                            <tr>
                                <td>${p.name}</td><td>${p.creation_date}</td><td>${p.owner.lastname}</td>
                                <td>
                                    <acronym title="Explore the project structure">
                                    ${h.image_to('/webenmr/images/explore.gif', '',
                                        h.url(controller=u'filesystem', 
                                        action='explore',
                                        id=unicode(p.id)
                                        ))}
                                    </acronym>
                                    &nbsp;&nbsp;
                                    <acronym title="Download the project">
                                    ${h.image_to('/webenmr/images/b_save.png', '',
                                        h.url(controller=u'projects', 
                                        action='project_download',
                                        id=unicode(p.id)
                                        ))}
                                    </acronym>
                                     &nbsp;&nbsp;
                                    <acronym title="Check calculations">
                                    ${h.image_to('/webenmr/images/b_engine.png', '',
                                        h.url(controller=u'calculations', 
                                        action='calculation_list',
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
                    %endif
                    <br />
                    <a href="#" onclick="AddProject()">Create a new Project</a>
                    <div id="hidden">
                        <form id="NewProject" action="${h.url(controller='projects', action='project_create')}" onSubmit="return checkProject()" method="post" >
                         <div id="hidden">
                        <form id="signup" action="${h.url(controller='projects', action='project_create')}" onSubmit="return checkProject()" method="post" >
                        <table>
                            <tr>
                                <td class="labelcell">Project name:</td>
                                <td class="fieldcell"><input type="text" name="project" id="project" /></td>
                            </tr>
                            <tr>
                                <td class="labelcell">
                                    Select calculation tipology:
                                </td>
                                <td class="smallfieldcell">
                                    <select name="calc_type">
                                    %for t in c.calc_type:
                                        <option value="${t.id}">${t.tipology}</option>
                                    %endfor
                                    </select>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <center><input type="submit" name="submit" value="submit" class="button" /></center>
                                </td>
                            </tr>
                        </table>
                        </form>
                    </div>
                </div>
            </fieldset>
            
        </div>
    </div>
</div>

<%inherit file="/base.mako"/>
<%def name="js()">
 <script  type="text/javascript">

</script>
</%def>

<h2></h2>
<div class="item-list">
    <div  class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Calculation List</a>
                </legend>
                <div class="content">
                    % if c.project.calculation:
                        <table id="tableabssorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
                        <thead>
                        <tr>
                            <th>Project Name</th>
                            <th>Calculation Name</th>
                            <th>Calculation Type</th>
                            <th>Cration Date</th>
                            <th class="{sorter: false}">Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        % for p in c.project.calculation:
                            <tr>
                                <td>${c.project.name}</td><td>${p.name}</td>
                                <td>${p.calc_type.tipology}</td><td>${p.creation_date}</td>
                                
                                <td>
                                    <acronym title="Show Job list">
                                    ${h.image_to('/webenmr/images/b_browse.png', '',
                                        h.url(controller=u'jobs', 
                                        action='job_list',
                                        id=unicode('%s_%s_0' % (p.id, c.project.id))
                                        ))}
                                    </acronym>
                                    ##<%
                                    ##    job_running = False
                                    ##    for j in c.project.calculation[0].job:
                                    ##        if j.status == 'R' or j.status == 'S':
                                    ##            job_running = True
                                    ##%>
                                    ##% if not job_running:
                                    ##    &nbsp;&nbsp;
                                    ##    <acronym title="Submit Job">
                                    ##    ${h.image_to('/webenmr/images/s_process.png', '',
                                    ##        h.url(controller=u'jobs', 
                                    ##        action='job_submit',
                                    ##        id=unicode('%s_%s_0' % (p.id, c.project.id))
                                    ##        ))}
                                    ##    </acronym>
                                    ##% endif
                                    &nbsp;&nbsp;
                                    <acronym title="Kill all Job(s)">
                                        ${h.image_to('/webenmr/images/b_drop.png', '',
                                            h.url(controller=u'jobs', 
                                            action='job_killall',
                                            id=unicode('%s_%s_0' % (p.id, c.project.id))
                                            ))}
                                    </acronym>
                                </td>
                            </tr>
                        % endfor
                        </tbody>
                        </table>
                    %endif
                    <br />
                    
                    
                </div>
            </fieldset>
            
        </div>
    </div>
</div>

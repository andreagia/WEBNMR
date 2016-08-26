<%inherit file="/base.mako"/>
<%def name="js()">
 <script  type="text/javascript">

 $(document).ready(function() { 		
		$("#tablesorter").tablesorter({widgets: ['zebra']}).tablesorterPager({container: $("#pager")});
	});	

 </script>
</%def>

<h2>Users List</h2>
<div class="item-list">
    <div class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Users List:</a></legend>
                    <div class="content">
                        <center>
                        <table id="tablesorter" class="tablesorter" border="0" cellpadding="0" cellspacing="1">
                        <thead>
                            <tr>
                                <th class="{sorter: false}">ID</th><th>Firtname</th><th>Lastname</th>
								<th>Email</th><th>Home</th><th class="{sorter: false}">Removed</th>
								<th class="{sorter: false}">Action</th>
                            </tr>
                        </thead>
                        <tbody>
						%for user in c.users:
						  <tr>
							<td>
							  ${user.id}
							</td>
							<td>
								${user.firstname}
							</td>
							<td>
								${user.lastname}
							</td>
							<td>
								${user.email}
							</td>
							<td>
								${user.home}
							</td>
							<td>
								% if user.removed:
									Yes
								% else:
									No
								% endif
							</td>
							<td>
								<acronym title="Modify user">
								${h.image_to('/webenmr/images/edit_small.png', '',
								   h.url(controller=u'admin', 
								   action='edit_user',
								   id=unicode(user.id)
								   )
							   )}
							   </acronym>
								% if user.removed:
									&nbsp;&nbsp;
									<acronym title="Enable User">
									${h.image_to('/webenmr/images/success.png', '',
									   h.url(controller=u'admin', 
									   action='enable_user',
									   id=unicode(user.id)
									   )
								   )}
								   </acronym>
								% else:
									&nbsp;&nbsp;
									<acronym title="Remove User">
									${h.image_to('/webenmr/images/b_drop.png', '',
									   h.url(controller=u'admin', 
									   action='remove_user',
									   id=unicode(user.id)
									   )
								   )}
								   </acronym>
								% endif
							
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
                   
                    </div>
            </fieldset>
        </div>
    </div>
</div>

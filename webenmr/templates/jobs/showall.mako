<%inherit file="/base.mako"/>
<%def name="css()">
<style type="text/css"> 
	  #check {
			display: block;
			float: left;
			width: 50%;
			background: none repeat scroll 0 0 #CEE3F6;
			height: 24px;
	  }
	  #removejobs {
			display: block;
			float: right;
			width: 50%;
			text-align: right;
			background: none repeat scroll 0 0 #CEE3F6;
	  }
	  table {
			clear: both;
	  }
	  #simplemodal-overlay {background-color:#000;}
	  #simplemodal-container {background-color: #eee; border:4px solid #6495ED;  text-align:left;}
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
	  <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>

 <script  type="text/javascript">
       $(document).ready( function() {
	      if ($("input[type=checkbox]").length){
		     $("#check").show();
	      }
	      else{
		     $("#check").hide();
	      }
		  if ($("#tableabssorter").find("tr").length > 2){
			$("#removejobs").show();
		  }
		  else {
			$("#removejobs").hide();
		  }
		  
	      $("table") 
		     .tablesorter({
			    widthFixed: false,
			    widgets: ['zebra']
		     }) 
		     .tablesorterPager({container: $("#pager"), size: 30}); 
       });
 </script>
 
 <script  type="text/javascript">
    
    function open_dialog(titleDialog, message, w, h){
        var $dialog = $('<div></div>');
        $dialog.html(message);
       
        $dialog.dialog({
            autoOpen: false,
            title: titleDialog,
            width: w,
            height: h,
            modal: true,
            position: 'center',
            buttons: {
                "Ok": function() {
                    $(this).dialog("close");
                    }
            }
        });
        $dialog.dialog('open');
    }
    
    function check(elem){
        var id = elem.val();
        $.ajax({
                type: "GET",
                async: false,
                url: "/jobs/job_status/"+id
        });
    }
    
    function checkAll(){
			var myWidth = 320;
			var myHeight = 240;
			var option = {
				close: false,
				opacity:70,
				minWidth: myWidth,
				minHeight: myHeight,
				maxWidth: myWidth,
				maxHeight: myHeight
			};
			$.modal('<img src="/global/images/checkjobs.gif">', option);
			
			$.ajax({
				  type: 'POST',
				  url: '/jobs/checkalljobs',
				  success: function(data){
						//$.modal.close();
						window.location = window.location.href;
				  }
			  
			});
			////var externalPage =  $.get("/compress.html");
			//$("#loading").modal(option);

//      var $dialog = $('<div></div>')
//      .load("/compress.html")
//      .dialog({
//          autoOpen: false,
//          modal: true,
//          closeOnEscape: false,
//          open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); },
//          title: "Checking job(s)...",
//          width: 230,
//		  position: 'center'
//      });
//      $dialog.dialog('open');
//        
//        $(":checkbox").attr('checked', true);
//        $("input[type=checkbox]:checked").each(function(){
//            check($(this));    
//        });
//        
//        if($("input[type=checkbox]:checked").length){
//            /*var sURL = unescape(window.location.pathname);
//            $dialog.dialog('close');
//	    window.location = sURL;  */
//			//$.modal.close();
//			window.location = window.location.href;
//        }
    }
    
    function checkSelected(){
	  if($("input[type=checkbox]:checked").length){
			var myWidth = 320;
			var myHeight = 240;
			var option = {
				close: false,
				opacity:70,
				minWidth: myWidth,
				minHeight: myHeight,
				maxWidth: myWidth,
				maxHeight: myHeight
			};
			$.modal('<img src="/global/images/checkjobs.gif">', option);
			$("input[type=checkbox]:checked").each(function(){
				check($(this));        
			});
			//$("input[type=checkbox]:checked").attr("checked", false);
			
			//var sURL = unescape(window.location.pathname);
			//window.location = sURL;
				window.location = window.location.href;
	  }
        
    }
    
	function removeJobs(){
	  var status = $("#jobstatus :selected").val();
	  if (status != ""){
			$.ajax({
				  url: '/jobs/job_remove',
				  type: 'POST',
				  data: {'status': status},
				  success: function(data){
						window.location = window.location.href;
				  }
			});
	  }
	}
    
</script>
</%def>
<%def name="show_items(p, ca, j)">
<tr>
    <td>
        % if j.status == 'R' or j.status == 'S':
            <% id=unicode('%s_%s_%s' % (ca.id, p.id, j.id))%>
            <input type="checkbox" name="checkStatus" value="${id}" />
        %endif
    </td>
    <td>${p.name}</td>
    <td>${ca.name}</td>
    <td>click <a href="javascript:open_dialog('GUID', '${j.guid}', 450, 180)">here</a> to view</td>
    <td>${str(j.start_date)[:-7]}</td>
    <td><center><acronym title="${c.STATUS[j.status]}">${j.status}</acronym></center></td>
    <td>
		% if j.log:
		  <center><acronym title="${j.log}">Read</acronym></center>
		% endif
	</td>
    
    <td>
        % if j.status == 'R' or j.status == 'S':
            <acronym title="Kill Job">
            ${h.image_to('/webenmr/images/b_drop.png', '',
                h.url(controller=u'jobs', 
                action='job_kill',
                id=unicode('%s_%s_%s' % (ca.id, p.id, j.id))
                ))}
            </acronym>
        % endif
        % if j.status == 'F':
            &nbsp;&nbsp;
            <acronym title="Retrieve output">
            ${h.image_to('/webenmr/images/b_export.png', '',
                h.url(controller=u'jobs', 
                action='job_retrieve',
                id=unicode('%s_%s_%s' % (ca.id, p.id, j.id))
                ))}
            </acronym>
        % endif
    </td>
</tr>

</%def>
<div class="preamble">
	  <b>The job status does not update automatically (even if you log out and log in again).</b><br/>
	  To check if the job status has changed, please use the <b>Check all</b> or <b>selected jobs status</b> link above the Job List.<br/>
	  <br/>
	  A quick explanation about some <b>Status</b> column values:<br/>
			<ul>
				  <li><b>S</b> (Scheduled/Submitted) -- the job has been correctly submitted and is waiting to be processed;</li>
				  <li><b>R</b> (Running) -- the job is currently running;</li>
				  <li><b>E</b> (Completed/Retrieved) -- the job has been completed and automatically retrieved from the Grid.</li>
			</ul>
			If your job has spent more than 12 hours in the <b>S</b> status, we advise you to kill and re-submit it.<br><br>
</div>
<div class="item-list">
    <div  class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Job List</a>
                </legend>
                <div class="content">
				  <div id="jobActions">
                    <div id="check">
                        Check <a style="text-decoration:underline;" href="javascript:checkAll();">all</a> or <a style="text-decoration:underline;" href="javascript:checkSelected();">selected</a> jobs status
					</div>
					<div id="removejobs">
						remove all jobs
						<select id="jobstatus">
							  <option value="">Select status</option>
							  <optgroup label="Finished">
									<option value="E">E</option>
							  </optgroup>
							  <optgroup label="Cancelled">
									<option value="C">C</option>
							  </optgroup>
							  <optgroup label="Aborted">
									<option value="A">A</option>
							  </optgroup>
							  <optgroup label="Cleared">
									<option value="L">L</option>
							  </optgroup>
						</select>
						&nbsp;&nbsp;<a style="text-decoration:underline; cursor: pointer;" onclick="javascript:removeJobs()">remove</a>
					</div>
				  </div>
                        <table id="tableabssorter" class="tablesorter {sortlist: [[4,1],[5,1]]}" border="0" cellpadding="0" cellspacing="1">
							  <thead>
									<tr>
										<th class="{sorter: false}"><img src="/global/images/checkbox_green.png"></th>
										<th>Project Name</th>
										<th>Calculation Name</th>
										<th class="{sorter: false}">Job Guid</th>
										<th>Start Date</th>
										<th>Status</th>
										<th class="{sorter: false}">Log</th>
										<th class="{sorter: false}">Kill Job</th>
									</tr>
							  </thead>
							  <tbody>
									% for p in c.projects:
										% for ca in p.calculation:
										  %if ca.removed == False and (ca.calc_type_id == c.calctype_id or ca.calc_type_id == c.calctype2_id):
											% for j in ca.job:
											  %if j.removed == False:
												% if c.show == 'all':
													${show_items(p, ca, j)}
												% elif c.show == 'run':
													% if j.status == 'R':
														${show_items(p, ca, j)}
													% endif
												% elif c.show == 'canc':
													% if j.status == 'C':
														${show_items(p, ca, j)}
													% endif
												% elif c.show == 'term':
													% if j.status == 'E':
														${show_items(p, ca, j)}
													% endif
												% elif c.show == 'sched':
													% if j.status == 'S':
														${show_items(p, ca, j)}
													% endif
												% endif
											   % endif
											% endfor
										  %endif
										%endfor
									% endfor
								  <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
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
                                              <option value="10">10</option>
                                              <option value="20">20</option>
                                              <option selected="selected"  value="30">30</option>
                                              <option  value="40">40</option>
                                      </select>
                              </form>
                        </div>
                    <br />

                </div>
            </fieldset>
            
        </div>
    </div>
</div>
<div id="loading" style="display: none;">
	  <img src="/global/images/loading2.gif">
</div>

<%inherit file="/base.mako"/>
<%def name="css()">
    <link rel="stylesheet" type="text/css" href="/global/css/restart.css"  media="screen" charset="utf-8" />
</%def>
<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/restart.js" ></script>
</%def>

<div id="tabs_restart">
    <form id="restart_form" method="POST" action="${h.url('/calculations/restart_submit')}" enctype="multipart/form-data">
    <ul>
	    <li><a href="#tabs-input">Input</a></li>
	    <li><a href="#tabs-sander" onclick="next_tab();">Sander</a></li>
	    <li><a href="#tabs-run" onclick="fill_summary();">Run simulation</a></li>
    </ul>
    <div id="tabs-input">
	<p>Because molecular dynamics runs often require considerable amounts
	of computer time, this restart facility allows you to resume the calculation.</p>
	<fieldset>
	    <legend>Choose calculation to restart</legend>
	    Project: 
	    <select id="proj_list" name="proj_list" class="validate[required] select">
		<option value="none">Select project</option>
	    </select> &nbsp;&nbsp;&nbsp;
	    Calculation: 
	    <select id="calc_list" name="calc_list" class="validate[required] select">
		<option value="none">Select calculation</option>
	    </select>
	    <br />
	    <br />
	    <span class="note">After selected a project, if calculations list is empty it means not exist one, whereas if it is partially filled, it means some project's calculations are running or completed but not retrieved.</span>	
	</fieldset>
	<fieldset id="sel_inputs" style="display: none;">
	    <legend>Select input files</legend>
	    <p>
		<b>Default behaviour</b> - Will be used the outputs of a completed job, hence, if there is more than one job, please select what job restart.
		<!--and procede clicking <a href="javascript:next_tab();" style="text-decoration: underline; color: blue">here</a> to do the fine tuning of sander parameters.-->
		<br />
	    </p>
	    <fieldset id="job">
		<legend>Select completed job</legend>
		Job guid: 
		<select id="job_list" name="job_list" class="validate[required] select">
		    <option value="none">Select job</option>
		</select>
		<br />
		<br />
		<span class="note">If jobs list is empty or partially filled it means either not exist one or some Amber error occurred (check output files through <i>Project->Manage</i>).</span>
	    </fieldset>
	    <p>
		<br /><b>Advanced behaviour</b> - Will be used a manually modified version of a completed job outputs, hence, you must upload them. 
		Note that coordinates and topology files are required (marked with *) whereas constraints files are optional.
		You can switch to <i>advanced behaviour</i> clicking <a href="javascript:expert_mode();" style="text-decoration: underline; color: blue">here</a>.
	    </p>
	    <fieldset id="advanced" style="display: none;">
		<legend>Upload input files</legend>
		<span class="spantop">Topology file*: </span><input class="validate[required] file-input" type="file" id="top_input" name="top_input" />
		<span class="spancoord">Coordinates file*: </span><input class="validate[required] file-input" type="file" id="coord_input" name="coord_input" />
		<span class="spannoe">noe and/or dih. angles file(s): </span><input type="file" name="noe_input" />
		<span class="spanrdc">rdc file(s): </span><input type="file" name="rdc_input"/>
		<span class="spanpcs">pcs file(s): </span><input type="file" name="pcs_input"/>
		<br />
		<br />
		<input type="button" value="Back to default" onclick="javascript:normal_mode();"/>
		 or 
		<input type="button" value="Upload files" onclick="javascript:next_tab();"/> <span class="note">(and automatically go to sander parameters setting)</span>
	    </fieldset>
	</fieldset>
    </div>
    <div id="tabs-sander">
	<fieldset>
	    <legend>Molecular dynamics setting</legend>
	    <div id="header_sander">
		<p><b>Select group and protocol</b> already defined,<img class="infoimg" src="/global/images/icon_info.gif" onclick="javascript:show_info();"> 
		otherwise <b>copy and paste</b> a protocol (use <b>CTRL+v</b> to paste clipboard contents, because right-click is disabled).  
		You can see an MD production phase <a href="javascript:show_example()" style="text-decoration: underline; color: blue" >example</a>.
		</p>
		<select name="group">
		    <option value="none">Select group</option>
		    <option value="preset">Preset protocols</option>
		    <option value="personal">Personal protocols</option>
		</select>
		&nbsp;
		<select name="protocol">
		    <option value="none">Select protocol</option>
		</select>
		<br />
	    </div>
	    <div id="textarea_sander">
		<textarea name="sander" class="sander_param" cols="38" rows="15"></textarea>
	    </div>
	    <div id="multistep" style="display: none;">
		<fieldset>
		    <legend>Multistep protocol</legend>
		    <p class="multistep_header">Choose what step (also more than one) include in the restart:</p> <br />
		    <span>
			<img src="/global/images/megaphone.png" onclick="show_note()"><a href="javascript:show_note()">see advice</a>
		    </span>
		</fieldset>
	    </div>
	    <div id="example" class="simplemodal-wrap">
		<p><b>Example of production MD run</b></p>
		<p>You can <b>copy and paste</b> the example below, hence modify and use it in your simulation.</p>
		<fieldset>
		    <legend>Example of sander input</legend>
		    Production MD<br />
		    &cntrl<br /> 
		     imin=0, irest=1, ntx=5,<br /> 
		     nstlim=2500000,dt=0.002,<br /> 
		     ntc=1, ntf=2,<br />
		     ntt=1, tautp=0.5,<br />
		     tempi=325.0, temp0=325.0,<br /> 
		     ntpr=500, ntwx=500,<br /> 
		     ntb=0, igb=1,<br />
		     cut=999., rgbmax=999.<br /> 
		    /
		</fieldset>
		<br />
		<br />
		<p><b>Quick explanation about parameters used in the example above</b>.</p>
		<p>The simulation will consist of 2,500,000 steps (nstlim) with a 2 fs time step (dt) giving 5 ns per stage.<br />
		Note we have SHAKE on the whole time (ntc=2, ntf=2), and we use the Berendsen thermostat for temperature control (ntt=1). This example assumes 
		that we have heated our system up (300 K) and it appears to be stable, therefore we can use a much more closely coupled thermostat of 0.5 ps (tautp=0.5).
		This will serve to keep our system close to 325 K. We write to the output file and mdcrd file every 500 steps (ntpr=500, ntwx=500). 
		Writing more frequently that this would result in huge files.
		Every 500 steps should be frequent enough for our purposes.</p>
	    </div>
	    <div id="info">
		<p><b>Quick explanation about stored protocols</b></p>
		<p>Stored protocols are divided in two groups:
		<ul>
		    <li>Preset</li>
		    <li>Personal</li>
		</ul>
		The <b>Preset group</b> contains standard template multi-steps protocols useful for refinement of protein structures,
		in addition to some protocols for equilibration and production run of standard MD simulations.<br /><br />
		The <b>Personal group</b> contains all user-modified Preset group protocols and user-defined new protocols. Hence, if you want define new protocol
		<ul>
		    <li>can modify an existing one, easily loading + editing + saving it,</li>
		    <li>or you can click on &#60;Protocol&#62; menu item and build a new protocol.
			It is also possible to use the embedded smart facility for an "aided design" of your protocols.
		    </li>
		</ul>
		</p>
	    </div>
	    <div id="saveform">
		<fieldset>
		    <legend>Save new protocol</legend>
		    <p>You can store this new or modified protocol among your Personal group ones.
		    If you choose a filename already used, automatically will be added a suffix (e.g. <i>yourfilename</i> become <i>yourfilename(1)</i>, <i>or yourname(2)</i> and so on).</p>
		    <br />
		    <label for="protname">Choose name:*</label>
		    <input type="text" name="protname" id="protname" class="validate[required] text-input"/>
		    <br />
		    <label for="descrprot">Write protocol description</label>
		    <textarea class="descrprot" name="descrprot" id="descrprot" rows="6" cols="38"></textarea><br>
		    <button type="button" id="confirm">Confirm</button>
		    &nbsp;
		    <button type="button" id="close">Close</button><br><br>
		    <span class="note">* required</span>
		</fieldset>
	    </div>
	</fieldset>
    </div>
    <div id="tabs-run">
	<fieldset>
	    <legend>Summary</legend>
	    You are restarting job: <span id="summary_job"></span> <br />
	    that belong the calculation: <span id="summary_restart"></span> <br />
	    within the project: <span id="summary_project"></span> <br />
	    with inputs: <span id="summary_input"></span> <br />
	    and sander protocol: <span id="summary_sander"></span> <br />
	</fieldset>
	<fieldset id="fieldname">
	    <legend>Choose name of calculation</legend>
	    <label for="name_restart">Name: </label>
	    <input type="text" class="validate[required]" name="name-restart" id="name-restart" /> &nbsp; <button type="button" id="check" onclick="check_calc_name()">check availability</button>
	</fieldset>
	<br />
	<br />
	<input type="submit" value="Submit job" id="submit-button" disabled="disabled"/>
	<div id="sumsan"></div>
    </div>
</div>
</form>

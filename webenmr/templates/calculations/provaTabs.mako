# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
    <link href="/global/css/new_amberCalc.css" rel="stylesheet" type="text/css" />
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/new_amberCalc.js" ></script>
</%def>

    <div id="tabs">
        <ul>
                <li><a href="#tabs-1">structure upload</a></li>
                <li><a href="#tabs-2">constraint specification</a></li>
                <li><a href="#tabs-3">sander</a></li>
                <li><a href="#tabs-4">submit calculation</a></li>
        </ul>
        <div id="tabs-1">
        <form  id="structure" action="${h.url('/structureUpload/submitStructure')}" method="post"  enctype="multipart/form-data" >
            <fieldset>
                <legend>
                    Structure upload                     
                </legend>
                <p>Please complete the form below. Mandatory fields marked <em id="asterix">*</em></p>
                
                <div class="form-item">
                    <div id="column1">
                        <div id="proteinUpload">
                            <fieldset id="protein">
                                <legend>
                                    <!--<a     href="javascript:open_dialog('Info', 'Verba movent, exempla trahunt', 250, 150)"><img src="/global/images/info.png" border="0" title="click to obtain more info on it"></a>
                                    &nbsp;-->Chain upload
                                </legend>
        
                                <div id="chain_file">
                                        <label id="protein"  for="chain_file">Select chain file</label>
                                        <div id="chain_file_div">
                                        <input type="file" id="chain_file" name="chain_file" onChange="uploadFile(this.id, 'structure')" />
                                        <em id="asterix">*</em> 
                                        </div>
                                        
                                        <br />
                                        <span id="small">(Only .pdb files are accepted)</span>
                                </div>
                                <div id="chain-item">
                                    <!-- trovare un modo per far funzionare il validating -->
                                </div>
                                
                                <div id="advanced-setting" style="display: none;">
                                    <br />
                                    <br />
                                        
                                    <div id="bond">
                                        <a href="javascript:add_bond()"><img src="/global/images/plus.png" />add bond</a>
                                        <div id="bond-form" title="Add new bond">
                                            <p class="validateTips">All form fields are required.</p>
                                            
                                            <fieldset>
                                                <label for="atom1">Atom1</label>
                                                <input type="text" name="atom1" id="atom1" />
                                                <label for="residue1">Residue1</label>
                                                <input type="text" name="residue1" id="residue1" value=""/>
                                                <label for="atom2">Atom2</label>
                                                <input type="text" name="atom2" id="atom2" />
                                                <label for="residue2">Residue2</label>
                                                <input type="text" name="residue2" id="residue2" value=""/>
                                            </fieldset>
                                        </div>
                                        <div id="bond-item">
                                            <div id="items">
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div id="solv">
                                        <a href="javascript:add_solvent()"><img src="/global/images/plus.png" />add solvent</a>
                                        <div id="solvent-form" title="Add a solvent">
                                            <p class="validateTips">All form fields are required.</p>
                                            
                                            <fieldset>
                                                (Most people use solvent: "TIP3PBOX"; geometry: "box"; distance: "10")
                                                <br />
                                                <br />
                                                <label for="solvent">Solvent</label>
                                                <select name="solvent" id="solvent">
                                                    <option>Make a selection</option>
                                                    <option value="TIP3PBOX">TIP3PBOX</option>
                                                    <option value="TIP4PBOX">TIP4PBOX</option>
                                                    <option value="TIP5PBOX">TIP5PBOX</option>
                                                    <option value="POLBOX">POLBOX</option>
                                                    <option value="SPCBOX">SPCBOX</option>
                                                </select>
                                                <label for="geometry">Geometry</label>
                                                <select name="geometry" id="geometry" onChange="checkSolvate(this.id)">
                                                    <option>Make a selection</option>
                                                    <option value="box">box</option>
                                                    <option value="oct">oct</option>
                                                    <option value="boxDC">boxDC</option>
                                                    <option value="sshell">solvateShell</option>
                                                    <option value="scap">solvateCap</option>
                                                </select>
                                                <label id="ldistance" for="distance">Distance (&Aring;)</label>
                                                <input type="text" name="distance" id="distance" />
                                            </fieldset>
                                        </div>
                                        <div id="solvent-item">
                                            <div id="items">
                                            </div>
                                        </div>
                                    </div>
                                        
                                    <div id="ions">
                                        <a href="javascript:add_ion()"><img src="/global/images/plus.png" />add ion</a>
                                        <div id="ion-form" title="Add a ion">
                                            <p class="validateTips">All form fields are required.</p>
                                            <b>Note: max. two ions are permitted</b>
                                            
                                            <fieldset>
                                                <label for="type">Type</label>
                                                <select name="ion" id="ion">
                                                    <option>Make a selection</option>
                                                    <option value="Cl-">Cl-</option>
                                                    <option value="Na+">Na+</option>
                                                    <option value="K+">K+</option>
                                                    <option value="Li+">Li+</option>
                                                    <option value="MG2">MG2</option>
                                                </select>
                                                <label for="number">Number</label>
                                                <input type="text" name="number" id="number" />
                                            </fieldset>
                                        </div>
                                        <div id="ion-item">
                                            <div id="items">
                                            </div>
                                        </div>
                                    </div>
                                        
                                    <div id="born">
                                        <a href="javascript:add_born()"><img src="/global/images/plus.png" />Born radius</a>
                                        <div id="born-form" title="Born radius">
                                            <fieldset>
                                                <h4>Do you want use Born radius?</h4>
                                            </fieldset>
                                        </div>
                                        <div id="born-item">
                                            <div id="items">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </fieldset>
                            
                        </div>
                        
                        <div id="column2">
                        
                        </div><!-- column2 -->
                        
                        
                    </div><!-- column1 -->
                    
                    <div id="column3">
                        <div id="forceField">
                            <br />
                            
                            <div id="ffield-item">
                                <br />
                                <br />
                                <label id="forcefield" for="force_fields">Select chains force field: </label>
                                <select id="force_fields" name="forcefield" onchange="enableTabs()">
                                    <option></option>
                                    <option value="AMBER99SB">AMBER99SB</option>
                                    <option value="AMBER03">AMBER03</option>
                                </select>
                                <em id="asterix">*</em>
                                &nbsp;&nbsp;<input type="checkbox" name="antechamber" value="true" /> include antechamber force field
                            </div>
                        </div>
                    </div><!-- column3 -->
                    <div id="submit">
                        <input type="hidden" value="" id="field" name="field" />
                    </div>
                </div><!--div form-item-->
            </fieldset>
        </form>
            <div id="mstruct" style="display: none">
		<h4></h4>
		<div style="float: right">
		    <button type="button" id="mstructyes">Yes</button>
		    <button type="button" id="mstructno">No</button>
		</div>
	    </div>
        </div><!--div tabs-1-->
        <div id="tabs-2">
            <form id="constraint" action="${h.url('/structureUpload/submitConstraint')}" method="post"  enctype="multipart/form-data" >
                <fieldset>
                    <legend>Constraint upload</legend>
                    <div class="form-item">
                        <div id="chain_summary" class="table">
                            <fieldset id="chain_summary_fieldset">
                                <legend>Chain summary</legend>
                                 <div id="chain-row" class="row">
                                </div>
                            </fieldset>
                        </div>
                        
                            <div id="noeUpload"> 
                                <fieldset id="noe">
                                    <legend>Nuclear Overhauser Effect</legend>
                                    <div id="noe-fields">
                                            <label id="startResidue">First residue (number)</label>
                                            <input type="text" id="noe_number" name="noe_number" size=4 onkeyup="add_constraintEntry(this.id, 'constraint')"/>
                                            <label id="ltype" for="noe_cyanaXplor">Type </label>
                                            <select id="noe_cyanaXplor" name="noe_cyanaXplor" onchange="add_constraintEntry(this.name, 'constraint')">
                                                <option value="null"></option>
                                                <option value="dyana">DYANA</option>
                                                <option value="cyana">CYANA</option>
                                                <option value="xplor">XPLOR/CNS</option>
                                            </select>
                                            <input type="checkbox" id="noe_checkbox" name="noe_nocorr" value="True" /> no correction
                                            
                                            <div id="noe_file_div">
                                                <label id="noe"> Upper limit NOE file: </label>
                                                <input type="file" id="noe_file" name="noe_file" disabled="disabled" onChange="add_constraintEntry(this.id, 'constraint')"/>
                                                <label id="noe"> Lower limit NOE file: </label>
                                                <input type="file" id="noeLol_file" name="noeLol_file" disabled="disabled" onChange="add_constraintEntry(this.id, 'constraint')"/>
                                            </div>
                                    </div>
                                    
                                    <div id="noe-item">
                                        
                                    </div>
                                </fieldset>
                            </div>
            
                            <div id="dihedralUpload">
                                <fieldset id="dihedral">
                                    <legend>Dihedral angle</legend>
                            
                                    <div id="dihedral-fields">
                                            <label id="startResidue">First residue (number)</label>
                                            <input type="text" id="dihedral_number" name="dihedral_number" size=4 onkeyup="add_constraintEntry(this.id, 'constraint')" />
                                            <label id="ltype" for="dihedral_cyanaXplor">Type </label>
                                            <select id="dihedral_cyanaXplor" name="dihedral_cyanaXplor" onchange="add_constraintEntry(this.name, 'constraint')">
                                                <option value="null"></option>
                                                <option value="dyana">DYANA</option>
                                                <option value="cyana">CYANA</option>
                                                <option value="xplor">XPLOR/CNS</option>
                                            </select>
                                            <label id="dihedral"> Dihedral angle file: </label>
                                            <div id="dihedral_file_div">
                                            <input type="file" id="dihedral_file" name="dihedral_file" disabled="disabled" onChange="add_constraintEntry(this.id, 'constraint')"/>&nbsp;&nbsp;
                                            </div>
                                    </div>
                                    <div id="dihedral-item">
                                        
                                    </div>
                                </fieldset>
                            </div>
                        
                        
                        <div id="rdcUpload">
                            <fieldset id="rdc">
                                <legend>Residue Dipolar Coupling</legend>
                                <div id="rdc-fields">
                                    <label id="startResidue">First residue (number)</label>
                                    <input type="text" id="rdc_number" name="rdc_number" size=4 onkeyup="add_constraintEntry(this.id, 'constraint')"/>
                                    <label id="ltype" for="rdc_cyanaXplor">Type </label>
                                    <select id="rdc_cyanaXplor" name="rdc_cyanaXplor" onchange="add_constraintEntry(this.name, 'constraint')">
                                        <option value="null"></option>
                                        <option value="dyana">DYANA</option>
                                        <option value="cyana">CYANA</option>
                                        <option value="xplor">XPLOR/CNS</option>
                                    </select>
                                    &nbsp;&nbsp;
                                    
                                    <label id="rdc"> RDC file: </label>
                                    <div id="rdc_file_div">
                                    <input type="file" id="rdc_file" name="rdc_file" disabled="disabled" onChange="add_constraintEntry(this.id, 'constraint')"/>&nbsp;&nbsp;
                                    </div>
                                </div>
                                <div id="rdc-item">
                                    <div id="selectable">
                                    </div>
                                </div>
                                <div id="rdc_tensor">
                                </div>
                            </fieldset>
                        </div>
                        
                        <div id="pcsUpload">
                            <fieldset id="pcs">
                                <legend>Pseudocontact Chemical Shift</legend>
                                <div id="pcs-fields">
                                    <label id="startResidue">First residue (number)</label>
                                    <input type="text" id="pcs_number" name="pcs_number" size=4 onkeyup="add_constraintEntry(this.id, 'constraint')"/>
                                    <label id="ltype" for="pcs_cyanaXplor">Type </label>
                                    <select id="pcs_cyanaXplor" name="pcs_cyanaXplor"  onchange="add_constraintEntry(this.name, 'constraint')">
                                        <option value="null"></option>
                                        <option value="dyana">DYANA</option>
                                        <option value="cyana">CYANA</option>
                                        <option value="xplor">XPLOR/CNS</option>
                                    </select>
                                    &nbsp;&nbsp;
                                    
                                    <label id="pcs"> PCS file: </label>
                                    <div id="pcs_file_div">
                                    <input type="file" id="pcs_file" name="pcs_file"  disabled="disabled" onChange="add_constraintEntry(this.id, 'constraint')"/>&nbsp;&nbsp;
                                    </div>
                                </div>
                                <div id="pcs-item">
                                    <div id="selectable">
                                    </div>
                                </div>
                                <div id="pcs_tensor">
                                </div>
                            </fieldset>
                        </div>
                        <div id="submitConstr">
                            <br />
                            <input type="hidden" value="" id="field" name="field" />
                            <!--<input type="submit" value="submit constraint"/>-->
                        </div>
                    </div><!--div form-item-->
                </fieldset>
            </form>  
        </div><!-- div tab2-->
        <div id="tabs-3">
            
                <div id="sander_control">
                    <span>Choose mode view: </span>
                    <input type="radio" id="bmode" name="mode" value="basic" checked> basic
                    <input type="radio" id="emode" name="mode" value="expert"> extended <br />
                    <span>Choose section view: </span>
                    <button id="bcontrol">control</button>
                    <button id="bewald">ewald</button>
                    <button id="bwt">wt</button>
                    <button id="bdebug">debug</button>
                </div>
                <div id="accordion">
                    
                </div>
                
                <div id="sander-params">
                    <div id="browser" class="browser"></div>
                    <fieldset id="sander-out">
                        <legend>sander protocol</legend>
                        <span id="small">you can load or create your protocol</span>
                    </fieldset>
                    <div id="btemplate">
                        <button id="rp">reset all</button>
                        <button id="lt">load protocol</button>
                        <!--<button id="st" disabled="disabled">save</button>-->
                    </div>
                </div>

                <div id="menu">
                  
                </div>
                <div id="sub_window">
                   
                </div>

        </div><!--tab3 -->
        <div id="tabs-4">
            <form id="submitCalculation" action="/jobs/job_prepare" method="post"  enctype="multipart/form-data" >
                <input type="hidden" name="multij" value="off" />
                <!--<div id="multijobs">-->
                <!--    <label for="multijob">Upload multistructure file</label>-->
                <!--    <div id="multijob_div">-->
                <!--    <input type="file" id="multijob" name="multijob" onchange="uploadMultiJobs(this.id, 'submitCalculation')" /><br/>-->
                <!--    </div>-->
                <!--    <span id="small">(Only .tgz file are accepted)</span>-->
                <!--</div>-->
                <div id="multi-item">
                        
                </div>
            
                
                <br />
                <div id="submitOpt">
		    <!--class="validate[required,custom[noSpecialCaracters],length[1,40]] text-input" -->
                    Choose name for your calculation: <input type="text" name="calc_name" id="calc_name" value="" />
                    &nbsp; <button type="button" id="availability">check availability</button><br />
                    
 <!--                   Select resources for calculation:<br> -->
                    <input type="hidden" name="calccpugpu" id="select-cpugpu" value="" />
             <!--     <input type="radio" name="calccpugpu" id="radio-gpu" value="calcgpu"> Use GRID GPU<br>  -->
             <!--       <input type="radio" name="calccpugpu" id="radio-gpu" value="calclo"> Use FutureGateway<br> -->


                    <input type="hidden" name="prj_id" value="${c.prj_id}" />
                    <input type="hidden" name="tipology" value="${c.tipology}" />
                    <br />
                    <input type="submit" id="submit_calc" value="submit job" onclick="addloading();" disabled="disabled"/>
                </div>
                <br/><br/>
                    Job submission can require some minutes. If the page returns an error, 
                    please check the status of your Job using the menu above before 
                    re-submitting it.
            </form>
        </div><!--tab4-->
    </div><!-- div tabs-->
	

    <ul id="sanderMenu" class="contextMenu">
        <li class="edit"><a href="#edit">Edit</a></li>
        <li class="delete"><a href="#delete">Remove</a></li>
    </ul>

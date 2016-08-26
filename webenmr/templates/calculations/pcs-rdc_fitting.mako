
<%inherit file="/base2.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
    <link href="/global/css/pcs-rdc_fitting.css" rel="stylesheet" type="text/css" />
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/jGrowl-1.2.4/jquery.jgrowl_compressed.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery-ui-1.8/js/jquery-ui-1.8.custom.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.form.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.validate.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.xml.js"></script>
    <script type="text/javascript" src="/global/javascript/pcs-rdc_fitting2.js" ></script>
</%def>
    <br/>
        <div id="compliant" style="text-align:right">
            <!--<a href="http://mozilla-europe.org/en/firefox/" target="_blank"><img src="/global/images/firefox.png" style="border: none" title="Get Mozilla Firefox" alt="Get Mozilla Firefox"></a>-->
            <span class="browser_support">
                <span> Supported browser:</span>
                <span class="browser_logos">
                    <!--<span class="opera supported"></span>
                    <span class="ie"></span>-->
                    <span class="safari supported"></span>
                    <span class="ff supported"></span>
                    <span class="chrome supported"></span>
                </span>
            </span>
        </div>
        <br/>
        <br/>
    <!--<div id="tabs">-->
        <!--<ul>
                <li><a href="#tabs-1">structure upload</a></li>
                <li><a href="#tabs-2">RDC/PCS fitting</a></li>
        </ul>
        <div id="tabs-1">-->
        <dl class="intro">
            <dd class="summary">
               <b>AnisoFIT</b> <br />Fitting of Pseudocontact Shifts and Residual Dipolar couplings -
                The program allows users to fit pseudocontact shift and/or residual
                dipolar couplings measured for a protein against its structure. The
                calculation exploits the SIMPLEX minimization algorithm. . As extensively
                documented in the literature, this procedure allows the determination of
                the magnetic susceptibility tensor anisotropy (for pseudocontact shifts as
                well as residual dipolar couplings induced by the presence of a
                paramagnetic metal center) or of the anisotropy of the diffusion tensor
                (for residual dipolar couplings induced by the presence of orienting media
                in the protein solution). <br />This service has a value either as a preliminary
                step for protein structure refinement or determination using the
                aforementioned NMR data or as a tool to validate structural models such as
                those generated through homology modeling.<br />
                At present, the interface accepts pdb files containing either a single
                structure or a bundle of structures. In the latter case, however, only the
                first model is used. Results are provided in a graphical as well as
                tabular, downloadable form.<br/><br/>
                Please quote the following references when reporting the use of this program:<br/>
                Banci L, Bertini I, Bren KL, Cremonini MA, Gray
                HB, Luchinat C, Turano P, J. Biol. Inorg. Chem. (1996) 1, 117-126.<br/>
                Banci L, Bertini I, Huber JG, Luchinat C, Rosato
                A, J. Am. Chem. Soc. (1998) 120, 12903-12909. 
            </dd>
        </dl>
        <br />
        <br />
        
       <!-- <div id="tabs">
        <ul>
                <li><a href="#tabs-1">structure upload</a></li>
                <li><a href="#tabs-2">constraint specification</a></li>
        </ul>-->
        <div id="tabs-1">
        <form  id="structure" action="${h.url('/structureUpload/submitStructure')}" method="post"  enctype="multipart/form-data" >
            <fieldset>
                <legend>
                    <b>Structure upload</b>                     
                </legend>
                <!--<p>Please complete the form below. Mandatory fields marked <em id="asterix">*</em></p>-->
                
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
                                        <!--<em id="asterix">*</em> -->
                                        </div>
                                        
                                        <br />
                                        <span id="small">(Only .pdb files are accepted)</span>
                                </div>
                                <div id="chain-item">
                                    <!-- trovare un modo per far funzionare il validating -->
                                </div>
                            </fieldset>
                            
                        </div>
                        
                        <div id="column2">
                        
                        </div><!-- column2 -->
                        
                        
                    </div><!-- column1 -->
                    <input type="hidden" name="forcefield" value="AMBER99SB" />
                    <div id="submit">
                        <input type="hidden" value="" id="field" name="field" />
                        <input type="hidden" value="1" id="pcs-rdc_fitting" name="pcs-rdc_fitting" />
                    </div>
                </div><!--div form-item-->
            </fieldset>
        </form>
            <div id="mstruct" style="display: none">
		<h4></h4>
		<div>
		    <center><button type="button" id="mstructyes">Close</button></center>
		    <!--<button type="button" id="mstructno">No</button>-->
		</div>
	    </div>
        </div><!--div tabs-1-->
        <div id="tabs-2">
            <form id="constraint" action="${h.url('/structureUpload/submitConstraint')}" method="post"  enctype="multipart/form-data" >
                <fieldset>
                    <legend><b>Constraint upload</b></legend>
                    <div class="form-item">
                        <div id="rdcUpload">
                            <fieldset id="rdc">
                                <legend>Residue Dipolar Coupling</legend>
                                <div id="rdc-fields">
                                    <label id="startResidue">First residue</label>
                                    <input type="text" id="rdc_number" name="rdc_number" size=4 onkeyup="add_constraintEntry(this.id, 'constraint')"/>
                                    <label id="ltype" for="rdc_cyanaXplor">Type </label>
                                    <select id="rdc_cyanaXplor" name="rdc_cyanaXplor" onchange="add_constraintEntry(this.name, 'constraint')">
                                        <option value="null"></option>
                                        <option value="dyana">DYANA</option>
                                        <option value="cyana">CYANA</option>
                                        <option value="xplor">XPLOR</option>
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
                                    <label id="startResidue">First residue</label>
                                    <input type="text" id="pcs_number" name="pcs_number" size=4 onkeyup="add_constraintEntry(this.id, 'constraint')"/>
                                    <label id="ltype" for="pcs_cyanaXplor">Type </label>
                                    <select id="pcs_cyanaXplor" name="pcs_cyanaXplor"  onchange="add_constraintEntry(this.name, 'constraint')">
                                        <option value="null"></option>
                                        <option value="dyana">DYANA</option>
                                        <option value="cyana">CYANA</option>
                                        <option value="xplor">XPLOR</option>
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
    <!--</div>--><!-- div tabs-->
    <dl class="textblock">
        <dt></dt>
        <dd>
            <center>
                <b>For any questions, problems and informations please <a href="/feedback/index?type=anisofit">contact us</a></b>:<br>
                <!--<a href="http://www.google.com/recaptcha/mailhide/d?k=01xaa_vA_6WIC9HuV_Qub22g==&amp;c=Gr58f4zaPS_Aif4nUEkk4NBAezqgRrAkYjyxhtCMNKQ=" onclick="window.open('http://www.google.com/recaptcha/mailhide/d?k\07501xaa_vA_6WIC9HuV_Qub22g\75\75\46c\75Gr58f4zaPS_Aif4nUEkk4NBAezqgRrAkYjyxhtCMNKQ\075', '', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width=500,height=300'); return false;" title="Reveal this e-mail address">click to view</a>-->
            </center>
        </dd>
    </dl>
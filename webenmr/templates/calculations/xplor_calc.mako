<%inherit file="/base.mako"/>
<%def name="css()">
    <link href="/global/css/xplor.css" rel="stylesheet" type="text/css" />
    <!--<link rel="stylesheet" type="text/css" href="/global/css/validationEngine2.jquery.css"  media="screen" charset="utf-8" />-->
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/xplor.js" ></script>
    <!--<script type="text/javascript" src="/global/javascript/jquery.validationEngine2-en.js" ></script>-->
    <!--<script type="text/javascript" src="/global/javascript/jquery.validationEngine2.js" ></script>-->
</%def>
    
<div id="xplor-div">
    <form id="xplor-form" action="${h.url('/xplor/submitXplor')}" method="post"  enctype="multipart/form-data">
        <div id="tabs-xplor">
            <ul>
                <li><a href="#tabs-xplor-1">Protein structure</a></li>
                <li><a href="#tabs-xplor-2">Constraints</a></li>
                <li><a href="#tabs-xplor-3">Job submission</a></li>
            </ul>
                <div id="tabs-xplor-1">
                    <fieldset>
                        <legend><b>Sequence</b></legend>
                        <div id="xplorseq-div">
                                <div id="xplorseq-item">
                                    <label class="label-item">Select file</label>
                                    <input type="file" name="xplor-seqfile" id="xplor-seqfile" size="7" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('xplor-seqfile')" />
                                    <label class="label-item">Number of first residue</label>
                                    <input type="text" name="xplor-residuenum" id="xplor-residuenum" size="4" value="1" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('xplor-residuenum')" />
                                    <label class="label-item">Chain name</label>
                                    <input type="text" name="xplor-chainname" id="xplor-chainname" size="4"  /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('xplor-chainname')" />
                                    <input type="hidden" id="xplor-posseq" name="xplor-posseq" value="1"/>
                                </div>
                        </div>
                        <a href="javascript:newfield('seq');">upload other sequence</a>
                    </fieldset>
                    <fieldset>
                        <legend><b>Protein properties</b></legend>
                        <div id="nonstd-residues">
                            <label class="label-item">Are there non standard residues?</label>
                            <input type="radio" title=": yes" name="nonstdres" id="nonstdres_yes" class="radiomiddle" value="yes" onclick="shownonstdres()">
                            <label for="nonstdres_yes" class="label-item">Yes</label>
                            <input type="radio" title=": no" name="nonstdres" id="nonstdres_no" class="radiomiddle" value="no" checked onclick="hidenonstdres()">
                            <label for="nonstdres_no" class="label-item">No</label>
                        </div>
                        <div id="nonstdres-div" style="display: none;">
                            <fieldset>
                                <legend><b>Add residues non standard</b></legend>
                                <div id="nonstdres-item">
                                        <label class="label-item">Topology</label></td>
                                        <input type="file" name="xplor-nonstdrestop" id="xplor-nonstdrestop" size="7" />&nbsp;&nbsp;
                                        <label class="label-item">Parameters</label>
                                        <input type="file" name="xplor-nonstdrespar" id="xplor-nonstdrespar" size="7" />
                                </div>
                               <br />
                               <a href="javascript:newfield('nonstdres')">add other residue</a>
                            </fieldset>
                        </div><!--div nonstdres-div -->
                        <br/>
                        <div id="paramagnetic">
                            <label class="label-item">is your protein a paramagnetic system?</label>
                            <input type="radio" title=": yes" name="parcenter" id="parcenter_yes" class="radiomiddle" value="yes" onclick="showparag()">
                            <label for="parcenter_yes" class="label-item">Yes</label>
                            <input type="radio" title=": no" name="parcenter" id="parcenter_no" class="radiomiddle" value="no" checked onclick="hideparag()">
                            <label for="parcenter_no" class="label-item">No</label>
                        </div>
                        <div id="metalprop" style="display: none;">
                            <fieldset>
                                <legend><b>Add metal ion</b></legend>
                                <div id="metal-choice">
                                        <input type="checkbox" id="metal-choice-checkbox" name="metal-choice-checkbox" value="cofactor" onchange="metal_choice(this);"/> metal ion within the cofactor
                                </div>
                                <table id="add-metal">
                                    <tr>
                                        <td><label class="label-item">Atom name</label></td>
                                        <td><input type="text" id="met_atom_name" size="5" maxlength="3" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_atom_name')" /></td>
                                        <td><label class="label-item">Chem. element</label></td>
                                        <td><input type="text" id="met_element" size="5" maxlength="2" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_element')" /></td>
                                        <td><label class="label-item">Residue name</label></td>
                                        <td><input type="text" id="met_res_name" size="5" maxlength="3" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_res_name')" /></td>
                                        <td><label class="label-item">Residue number</label></td>
                                        <td><input type="text" id="met_res_number" size="5" maxlength="3" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_res_number')" /></td>
                                    </tr>
                                    <tr>
                                        <td><label class="label-item">Charge</label></td>
                                        <td><input type="text" id="met_charge" size="5" maxlength="4" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_charge')" /></td>
                                        <td><label class="label-item">VDW radius</label></td>
                                        <td><input type="text" id="met_rvdw" size="5" maxlength="6" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_rvdw')" /></td>
                                        <td><label class="label-item">VDW epsilon</label></td>
                                        <td><input type="text" id="met_eps" size="5" maxlength="6" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_eps')" /></td>
                                        <td><input type="button" value="Add metal" onclick="addmetal()"/></td>
                                    </tr>
                                </table>
                                <br/>
                                <table id="metal-ion" style="display: none">
                                    <tr>
                                        <th>Atom name</th>
                                        <th>Chemical element</th>
                                        <th>Residue name</th>
                                        <th>Residue number</th>
                                        <th>Charge</th>
                                        <th>VDW radius</th>
                                        <th>VDW epsilon</th>
                                        <th>Metal binding residues</th>
                                        <th></th>
                                     </tr>
                                </table>
                            </fieldset><!-- add metal ion-->
                            <div id="hidden-metalfields"></div>
                        </div><!--div metalprop-->
                        <br/>
                        <div id="cofactor">
                            <label class="label-item">Does your protein bind a cofactor?</label>
                            <input type="radio" title=": yes" name="cof" id="cof_yes" class="radiomiddle" value="yes" onclick="showcof()">
                            <label for="cof_yes" class="label-item">Yes</label>
                            <input type="radio" title=": no" name="cof" id="cof_no" class="radiomiddle" value="no" checked onclick="hidecof()">
                            <label for="cof_no" class="label-item">No</label>
                        </div>
                        <div id="cofactorprop" style="display: none;">
                            <fieldset style="padding: 5px;">
                                <legend><b>Add cofactor</b></legend>
                                <div id="cof-item" style="font: 11px Verdana,Sans-serif;">
                                        <label class="label-item">PDB</label>
                                        <input type="file" name="xplor-cofpdb" id="xplor-cofpdb" size="7" />
                                        <label class="label-item">Topology</label></td>
                                        <input type="file" name="xplor-coftop" id="xplor-coftop" size="7" />
                                        <label class="label-item">Parameters</label>
                                        <input type="file" name="xplor-cofpar" id="xplor-cofpar" size="7" />
                                        <a href="javascript:selectPatch(this.parentNode, 1);">Patch molecule</a>
                                        <input type="hidden" id="xplor-poscof" name="xplor-poscof" value="1"/>
                                        <!--<a onclick=""><img src="/global/images/rem.png" /></a>-->
                                </div>
                                <br />
                                <a href="javascript:newfield('cof')">add other cofactor</a>
                            </fieldset>
                        </div>
                        <br/>
                        <div id="disulfide">
                            <label class="label-item">Are there disulfide bridges?</label>
                            <input type="radio" title=": yes" name="dis" id="dis_yes" class="radiomiddle" value="yes" onclick="showdis()">
                            <label for="dis_yes" class="label-item">Yes</label>
                            <input type="radio" title=": no" name="dis" id="dis_no" class="radiomiddle" value="no" checked onclick="hidedis()">
                            <label for="dis_no" class="label-item">No</label>
                        </div>
                        <div id="disulfideprop" style="display: none;">
                            <fieldset>
                                <legend><b>Add disulfide bridge</b></legend>
                                <table>
                                    <tr>
                                        <!--<td><label class="label-item">Atom</label></td>
                                        <td><input type="text" name="xplor-disatoma" id="xplor-disatoma" size="7"/></td>-->
                                        <td><label class="label-item">Residue number</label></td>
                                        <td><input type="text" name="xplor-disresnuma" id="xplor-disresnuma" size="7" /></td>
                                        <td>&lt;--&gt;</td>
                                        <!--<td><label class="label-item">Atom</label></td>
                                        <td><input type="text" name="xplor-disatomb" id="xplor-disatomb" size="7"/></td>-->
                                        <td><label class="label-item">Residue number</label></td>
                                        <td><input type="text" name="xplor-disresnumb" id="xplor-disresnumb" size="7" /></td>
                                        <td></td>
                                    </tr>
                                </table>
                                <a href="javascript:newfield('dis')">add other disulfide bridge</a>
                            </fieldset>
                        </div>
                        <br/>
                        <div id="histidine">
                            <label class="label-item">Do you want to specify His protonation?</label>
                            <input type="radio" title=": yes" name="phis" id="phis_yes" class="radiomiddle" value="yes" onclick="showphis()">
                            <label for="phis_yes" class="label-item">Yes</label>
                            <input type="radio" title=": no" name="phis" id="phis_no" class="radiomiddle" value="no" checked onclick="hidephis()">
                            <label for="phis_no" class="label-item">No</label>
                        </div>
                        <div id="histidineprop" style="display: none;">
                            <fieldset>
                                <legend><b>Specify protonation</b></legend>
                                <span class="note">By <b>default</b> the histidine has hydrogen in the <b>epsilon</b> position.</span><br/><br/>
                                <div id="xplorphis-div">
                                    <div id="xplorphis-item">
                                        <label class="label-item">Residue number</label>
                                        <input type="text" name="xplor-phisresnum" id="xplor-phisresnum" size="7" />
                                        <label class="label-item">Protonation type</label>
                                        <select name='xplor-phistype' >
                                            <option value = '' >Select type</option>
                                            <option value = 'HIED' >Delta</option>
                                            <option value = 'HIEP' >Protonated</option>
                                        </select>
                                    </div>
                                </div>
                                <a href="javascript:newfield('phis')">add other protonation</a>
                            </fieldset>
                        </div>
                    </fieldset>
                    <fieldset>
                        <legend><b>Output structures</b></legend>
                        <div>
                            <label class="label-item">Nro. output structures </label>
                            <input type="text" name="xplor-nrostruct" id="xplor-nrostruct" size="4" value="50"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('xplor-nrostruct')" />
                            <span> only multiple of 10 accepted</span>
                        </div>
                    </fieldset>
                </div>
                <div id="tabs-xplor-2">
                    <fieldset>
                        <legend><b>Restraints</b></legend>
                        <fieldset>
                            <legend>Nuclear Overhauser Effect</legend>
                            <div id="xplornoe-div">
                                <div id="xplornoe-item">
                                    <label class="label-item">Select file</label>
                                    <input type="file" name="xplor-noefile" id="xplor-noefile" />
                                </div>
                            </div>
                            <a href="javascript:newfield('noe');">upload other file</a>
                        </fieldset>
                        <fieldset>
                            <legend>Dihedral angles</legend>
                            <div id="xplordih-div">
                                <div id="xplordih-item">
                                    <label class="label-item">Select file </label>
                                    <input type="file" name="xplor-dihfile" id="xplor-dihfile"/>
                                </div>   
                            </div>
                            <a href="javascript:newfield('dih');">upload other file</a>
                        </fieldset>
                        <fieldset>
                            <legend><!--<span class="stepnumberSlave">2.3</span>-->Residue Dipolar Coupling</legend>
                            <div id="xplorrdc-div">
                                <div id="xplorrdc-item">
                                    <label class="label-item">Reference metal ion</label>
                                    <select id="xplor-rdc-metal" name="xplor-rdc-metal">
                                        <option value="none">None</option>
                                    </select>
                                    <br />
                                    <label class="label-item">Tensor ax </label>
                                    <input type="text" name="xplor-rdctnsax" id="xplor-rdctnsax" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('xplor-rdctnsax')" />
                                    <label class="label-item">Tensor rh </label>
                                    <input type="text" name="xplor-rdctnsrh" id="xplor-rdctnsrh" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('xplor-rdctnsrh')" />
                                    <label class="label-item">Select file </label>
                                    <input type="file" name="xplor-rdcfile" id="xplor-rdcfile" size="12"/>
                                </div>
                            </div>
                            <a href="javascript:newfield('rdc');">upload other file</a>
                        </fieldset>
                        <fieldset>
                            <legend>Pseudocontact Chemical Shift</legend>
                            <div id="xplorpcs-div">
                                <div id="xplorpcs-item">
                                    <label class="label-item">Reference metal ion</label>
                                    <select id="xplor-pcs-metal" name="xplor-pcs-metal">
                                        <option value="">Select metal</option>
                                    </select>
                                    <br />
                                    <label class="label-item">Tensor ax </label>
                                    <input type="text" name="xplor-pcstnsax" id="xplor-pcstnsax" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('numstruct')" />
                                    <label class="label-item">Tensor rh </label>
                                    <input type="text" name="xplor-pcstnsrh" id="xplor-pcstnsrh" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('numstruct')" />
                                    <label class="label-item">Select file </label>
                                    <input type="file" name="xplor-pcsfile" id="xplor-pcsfile" size="12"/>
                                </div>
                            </div>
                            <a href="javascript:newfield('pcs');">upload other file</a>
                        </fieldset>
                    </fieldset>
                </div>
                <div id="tabs-xplor-3">
                    <fieldset>
                        <legend><b>Submit calculation</b></legend>
                        <div>
                            <label class="label-item">Choose name</label>
                            <input type="text" name="xplor-namecalc" id="xplor-namecalc"/>
                            <input type="button" id="availability" value="Check availability" onclick="checkava();">
                            <input type="hidden" name="xplor-prj_id" id="xplor-prj_id" value="${c.prj_id}" />
                            <input type="hidden" name="tipology" value="${c.tipology}" />
                        </div>
                        
                    </fieldset>
                </div>
        </div>
    </form>
    <div id="metal-binding-div" style="display: none">
        <table id="add-metal-binding">
            <tr>
                <td><label class="label-item">Residue number</label></td>
                <td><input type="text" id="met_bin_res_number" size="5" maxlength="3"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_bin_res_number')" /></td>
                <td><label class="label-item">Atom name</label></td>
                <td><input type="text" id="met_bin_atom_name" size="5" maxlength="3"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_bin_atom_name')" /></td>
                <td><label class="label-item">Distance</label></td>
                <td><input type="text" id="met_bin_distance" size="5" maxlength="5"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info('met_bin_distance')" /></td>
            </tr>
        </table>
        <a href="javascript:newfield('bin')">add other residue</a>
        <div style="float: right; padding: 20px 0px 0px 0px">
		    <button type="button" id="bindrescanc" onclick="bindingresiduecancel();">Cancel</button>
		    <button type="button" id="bindresapply" onclick="bindingresidueapply()">Apply</button>
		</div>
    </div>
</div>

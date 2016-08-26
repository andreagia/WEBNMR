<%inherit file="/base.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
    <link href="/global/css/maxocc.css" rel="stylesheet" type="text/css" />
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/maxocc.js" ></script>
</%def>

<div>
       <span>
              MaxOcc analysis is based on RanCh and CALCPARA outputs, hence <b>you have to
               perform the RanCh and CALCPARA calculation</b>, and a tutorial
              to setup them is available <a href="http://wenmr.eu/#">here</a>.
       </span>
       <br /><br />
       <form id="maxocc" action="${h.url('/maxocc/getDataJob')}" method="post"  enctype="multipart/form-data">
              <fieldset>
                     <legend>Choose input source</legend>
                     Select project 
                     <select id="proj_list" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                     <br />
                     <span class="note">After selected a project, if calculations list is empty or partially filled means either not exists one or that some calculations are still running (or completed but some errors occurred).</span>
              </fieldset>
              <div id="maxoccInput">
                     <fieldset>
                       <legend>Parameters for MO calculations</legend>
                       <table>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('numstruct')" /> Structures of which MO is to be calculated </td>
                               <td><input type="text" name="numstruct" id="numstruct" size=7 class="validate[required]"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('weightconf')" /> Weight of the considered conformer </td>
                               <td><input type="text" name="weightconf" id="weightconf" size=7 class="validate[required]" value="0.0001"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('dist1')"/> Expected TF at zero weight (optional)</td>
                               <td><input type="text" name="expavetf" size=7/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('dist2')"/> Standard Deviation (optional)</td>
                               <td><input type="text" name="tfstd" size=7/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('thresholds')" /> TF tresholds (%) (optional)</td>
                               <td><input type="text" name="thresholds" id="thresholds" size=7/></td>
                           </tr>
                       </table>
                   </fieldset>
                   <fieldset>
                       <legend>Parameters for Minimization</legend>
                       <table>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('maxnumstruct')" /> Max number of structures in the completing ensemble</td>
                               <td><input type="text" name="maxnumstruct" id="maxnumstruct" value="45" size=7 class="validate[required]"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('numstructstep')" /> Number of structures added at each step </td>
                               <td><input type="text" name="numstructstep" id="numstructstep" size=7 class="validate[required]" value="4"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('numstepaddstruct')" /> Number of steps in which structures are added</td>
                               <td><input type="text" name="numstepaddstruct" id="numstepaddstruct" size=7 class="validate[required]" value="11"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('initnumens')" /> Initial number of ensembles</td>
                               <td><input type="text" name="initnumens" id="initnumens" size=7 class="validate[required]" value="400"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ensremstep')" /> Ensembles removed at each step</td>
                               <td><input type="text" name="ensremstep" id="ensremstep" size=7 class="validate[required]" value="11"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('starttemp')" /> Starting temperature</td>
                               <td><input type="text" name="starttemp" id="starttemp" size=7 class="validate[required]" value="0.07"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('targetmutrate')" /> Target mutation rate</td>
                               <td><input type="text" name="targetmutrate" id="targetmutrate" size=7 class="validate[required]" value="0.10"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('weightmin')" /> Weight minimization</td>
                               <td><input type="text" name="weightmin" id="weightmin" size=7 class="validate[required]" value="1"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('maxnumcg')" /> Maximum number of conjugate gradients iterations</td>
                               <td><input type="text" name="maxnumcg" id="maxnumcg" size=7 class="validate[required]" value="400"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('cggradtol')" /> Conjugate gradients tolerance (only if previous is 1)</td>
                               <td><input type="text" name="cggradtol" id="cggradtol" size=7 class="validate[required]" value="1E-5"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('satol')" /> Simulated Annealing tolerance</td>
                               <td><input type="text" name="satol" id="satol" size=7 class="validate[required]" value="1E-2"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('target')" /> Lower bound for minimization </td>
                               <td><input type="text" name="target" id="target" size=7 class="validate[required]" value="0.20"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('maxnumiter')" /> Maximum number of iterations</td>
                               <td><input type="text" name="maxnumiter" id="maxnumiter" size=7 class="validate[required]" value="2000"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('numtempstep')" /> Simulated Annealing temperature steps</td>
                               <td><input type="text" name="numtempstep" id="numtempstep" size=7 class="validate[required]" value="10"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('weightSA')" /> Weight MMC criterium for Simulated Annealing</td>
                               <td><input type="text" name="weightSA" id="weightSA" size=7 class="validate[required]" value="5E-3"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('weightinitreplace')" /> Weight MMC criterium for initial replacement</td>
                               <td><input type="text" name="weightinitreplace" id="weightinitreplace" size=7 class="validate[required]" value="0.02"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('weightaddstruct')" /> Weight MMC criterium when adding structures</td>
                               <td><input type="text" name="weightaddstruct" id="weightaddstruct" size=7 class="validate[required]" value="5E-4"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('weightheusteepdesc')" /> Weight MMC criterium for heuristic steepest descent</td>
                               <td><input type="text" name="weightheusteepdesc" id="weightheusteepdesc" size=7 class="validate[required]" value="5E-7"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('iterrestart')" /> Iteration between restart writings</td>
                               <td><input type="text" name="iterrestart" id="iterrestart" size=7 class="validate[required]" value="500"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('relweightpcs')" /> PCS multiplier </td>
                               <td><input type="text" name="relweightpcs" id="relweightpcs" size=7 class="validate[required]" value="1.0"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('relweightrdc')" /> RDC multiplier </td>
                               <td><input type="text" name="relweightrdc" id="relweightrdc" size=7 class="validate[required]" value="1.0"/></td>
                           </tr>
                           <tr id="pre-weight">
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('relweightpre')" /> PRE multiplier </td>
                               <td><input type="text" name="relweightpre" id="relweightpre" size=7 class="validate[required]" value="1.0"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('relweightsax')" /> SAXS multiplier </td>
                               <td><input type="text" name="relweightsax" id="relweightsax" size=7 class="validate[required]" value="0.1"/></td>
                           </tr>
                           <tr>
                               <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('multiharmonic')" /> Multiplier of the harmonic restraint for weights normalization </td>
                               <td><input type="text" name="multiharmonic" id="multiharmonic" size=7 class="validate[required]" value="1000"/></td>
                           </tr>
                       </table>
                   </fieldset>
                   <fieldset>
                     <legend>Experimental SAXS</legend>
                     <table>
                            <tr>
                                   <td>Select SAXS file</td>
                                   <td><input type="file" name="exp-saxs" id="exp-saxs" class="validate[required]" /></td>
                            </tr>
                            <tr>
                                   <td>No. of blind points</td>
                                   <td><input type="text" name="exp-saxs-blind" id="exp-saxs-blind" size="4" class="validate[required]" /></td>
                            </tr>
                     </table>
                   </fieldset>
                   <fieldset id="pre">
                     <legend>Paramagnetic Relaxation Enhancement</legend>
                     <table>
                            <tr>
                                   <td>Constant for transverse paramagnetic relaxation enhancement</td>
                                   <td><input type="text" name="pre-const" id="pre-const" size="7" value="1.37E-10" class="validate[required]" /></td>
                            </tr>
                     </table>
                   </fieldset>
                   <fieldset>
                       <legend>Submit calculation</legend>
                       Choose calculation name <input type="text" name="maxocc-calcname" id="maxocc-calcname"/> <input type="button" id="checkava" onclick="check_calc()" value="Check availability"/>
                       <br/>
                       <input type="submit" id="submit_maxocc" value="Submit calculation" disabled="disabled">
                   </fieldset>
            </div>
        </form>
    </div>

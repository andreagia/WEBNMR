<%inherit file="/base.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
    <link href="/global/css/maxocc.css" rel="stylesheet" type="text/css" />
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/maxoccMerge.js" ></script>
    <script type="text/javascript">
        function add_new(){
            var n = ($("fieldset").find("select").length/2 + 1).toString()
            //var str = 'Select project '+
            //         '<select id="proj_list'+n+'" name="proj_list" class="validate[required] select">'+
            //         '       <option value="none">Select project</option>'+
            //         '</select> &nbsp;&nbsp;&nbsp;'+
            //         'Select calculation: '+
            //         '<select id="calc_list'+n+'" name="calc_list" class="validate[required] select">'+
            //         '       <option value="none">Select calculation</option>'+
            //         '</select>'+
            //         '<br />';
            $("fieldset").find("#projdiv").last().clone().insertBefore("#addprj")
        }
    </script>
</%def>

    <div>
       <span>
              MaxOcc analysis is based on Ranch and CalcAll outputs, hence <b>you have to
               perform the Ranch and CalcAll calculation</b>, and a tutorial
              to setup them is available <a href="http://wenmr.eu/#">here</a>.<br>
       </span>
       <br /><br />
       <span>
              BETA TEST
       </span>
       <form id="maxoccMerge" action="${h.url('/maxocc/merge_do')}" method="post"  enctype="multipart/form-data">
              <fieldset>
                     <legend>Choose input source</legend>
                     <div id="projdiv">
                        Select project 
                        <select id="proj_list0" name="proj_list" class="validate[required] select">
                               <option value="none">Select project</option>
                        </select> &nbsp;&nbsp;&nbsp;
                        Select calculation: 
                        <select id="calc_list0" name="calc_list" class="validate[required] select">
                               <option value="none">Select calculation</option>
                        </select>
                        <br />
                     </div>
                     
                     <!--Select project 
                     <select id="proj_list1" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list1" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                    Select project 
                     <select id="proj_list2" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list2" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                     Select project 
                     <select id="proj_list3" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list3" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                     Select project 
                     <select id="proj_list4" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list4" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                      <br />
                     Select project 
                     <select id="proj_list5" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list5" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                      <br />
                     Select project 
                     <select id="proj_list6" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list6" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                     Select project 
                     <select id="proj_list7" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list7" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                     Select project 
                     <select id="proj_list8" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list8" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                      Select project 
                     <select id="proj_list9" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list9" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br />
                      Select project 
                     <select id="proj_list10" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list10" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>
                     <br/>
                      Select project 
                     <select id="proj_list11" name="proj_list" class="validate[required] select">
                            <option value="none">Select project</option>
                     </select> &nbsp;&nbsp;&nbsp;
                     Select calculation: 
                     <select id="calc_list11" name="calc_list" class="validate[required] select">
                            <option value="none">Select calculation</option>
                     </select>-->
                     <a onclick="add_new();" id="addprj">add project</a>
                     <br/>
                     <br/>
                     Threshold: <input type="text" id="threshold" name="threshold" />
              </fieldset>
              <input type="submit" name="submitMerge" value="Merge and analysis" />
        </form>
    </div>

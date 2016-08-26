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
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Amber Calculation</a>
                </legend>
                <div class="content">
                    <form id="signup" action="${h.url(controller='jobs', action='job_prepare')}" method="post" enctype="multipart/form-data" >
                    <table>
                        <tr>
                            <td class="labelcell">Calculation name:</td>
                            <td class="fieldcell"><input type="text" name="calc_name" id="calc_name" value="${c.calc_name}" /></td>
                        </tr>
                        <tr>
                            <td class="labelcell">Enter the in.tgz file:</td>
                            <td class="fieldcell"><input type="file" name="infile" id="infile" /></td>
                        </tr>
                        <tr>
                            <td class="labelcell">Enter the jdl file:</td>
                            <td class="fieldcell"><input type="file" name="jdl" id="jdl" /></td>
                        </tr>
                        <tr>
                            <td class="labelcell">Enter the run file:</td>
                            <td class="fieldcell"><input type="file" name="run" id="run" /></td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <input type="hidden" name="prj_id" value="${c.prj_id}" />
                                <input type="hidden" name="tipology" value="${c.tipology}" />
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

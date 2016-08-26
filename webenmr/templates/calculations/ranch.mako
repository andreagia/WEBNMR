<%inherit file="/base.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
    <link href="/global/css/maxocc.css" rel="stylesheet" type="text/css" />
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/ranch.js" ></script>
</%def>

    <div>
        <form name="ranchCalcall" action="${h.url('/ranch/submitRanch')}" method="post"  enctype="multipart/form-data">
            <fieldset>
                <legend>RanCh input</legend>
                <table>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchseq')" /> Input sequence filename (.seq)</td>
                        <td><input type="file" name="ranchseq" id="ranchseq" class="validate[required]"/></td>
                    </tr>
                    <tr id="numdomain">
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchnumdomain')" /> Number of domains</td>
                        <td><input type="text" name="ranchnumdomain" id="ranchnumdomain" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchtotstruct')" /> Total number of structures to generate</td>
                        <td><input type="text" name="ranchtotstruct" id="ranchtotstruct" value="50000" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchrefstruct')" /> Reference domain</td>
                        <td><input type="text" name="ranchrefstruct" id="ranchrefstruct"  value="1" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchtypelinkers')" /> Type of linkers: 0-native like, 1-random</td>
                        <td><input type="text" name="ranchtypelinkers"  id="ranchtypelinkers" value="0" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchorder')" /> Order of harmonics (max 50)</td>
                        <td><input type="text" name="ranchorder" id="ranchorder" value="15" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchmaxs')" /> Maximum s value</td>
                        <td><input type="text" name="ranchmaxs"  id="ranchmaxs" value="0.35" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td><img src="/global/images/info.png" class="infoimg" onclick="help_info('ranchnumpoints')" /> Number of points (max 201)</td>
                        <td><input type="text" name="ranchnumpoints" id="ranchnumpoints" size=7 value="51" class="validate[required]"/></td>
                    </tr>
                </table>
            </fieldset>
            <fieldset>
                <legend>CALCPARA input</legend>
                <table id="calcall">
                    <tr>
                        <td>Select RDC filename</td>
                        <td><input type="file" name="calcrdc" id="calcrdc" class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td>Select PCS filename</td>
                        <td><input type="file" name="calcpcs" id="calcpcs" class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td>Select tensor filename</td>
                        <td><input type="file" name="calctensor" id="calctensor" class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td>Field (MHz)</td>
                        <td><input type="text" name="calcfield" id="calcfield" value="700." size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td>Temperature (K)</td>
                        <td><input type="text" name="calctemp" id="calctemp" value="298" size=7 class="validate[required]"/></td>
                    </tr>
                    <tr>
                        <td>Do you use Paramagnetic Relaxation Enhancement?</td>
                        <td><input type="radio" title=": yes" name="pre" id="pre_yes" class="radiomiddle" value="yes" onclick="showpre();">
                            <label for="pre_yes" class="label-item">Yes</label>
                            <input type="radio" title=": no" name="pre" id="pre_no" class="radiomiddle" value="no" checked onclick="hidepre();">
                            <label for="pre_no" class="label-item">No</label>
                        </td>
                    </tr>
                </table>
            </fieldset>
            <fieldset>
                <legend>Submit calculation</legend>
                Choose calculation name <input type="text" name="ranch-calcname" id="ranch-calcname"/> <input type="button" id="checkava" onclick="check_calc();" value="Check availability"/>
                <br/>
                <input type="hidden" name="prj_id" id="prj_id" value="${c.prj_id}" />
                <input type="submit" name="submit_ranch" id="submit_ranch" value="Submit calculation" disabled="disabled">
            </fieldset>
        </form>
    </div>
        
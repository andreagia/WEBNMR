$(document).ready(function() {
    $("form[name=ranchCalcall]").validationEngine();
    var optionsFormRanch = {
        beforeSubmit:   validatorRequest,  // pre-submit callback
        dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
        success:  processFormRanchSuccess   // post-submit callback 
    }; 
    // bind form using 'ajaxForm' 
    $('form[name=ranchCalcall]').ajaxForm(optionsFormRanch);
    $("form[name=ranchCalcall]")[0].reset();
    $("form[name=ranchCalcall]").validationEngine();
    $("input[name=ranchnumdomain]").bind('keyup', function(){buildpdbinput();});
});

function help_info(field){
    $.ajax({
        type: 'POST',
        url: '/maxocc/helpinfo',
        data: {'field': field},
        success: function(data){
            var myWidth = 400;
            var myHeight = 130;
            var option = {
                opacity:70,
                minWidth: myWidth,
                minHeight: myHeight,
                maxWidth: myWidth,
                maxHeight: myHeight
            };
            $.modal(data, option);
        }

    });
}

function showtag(){
    if (!$("#calcall").find("tr[id=coord-met]").lenght){
            var new_tr = '<tr id="coord-met">'+
                '<td>Coordinates of paramagnetic tag</td>'+
                '<td><label class="label-item">x</label> <input type="text" name="tag-x" size="7" id="x-tag" class="validate[required]" /> '+
                '<label class="label-item">y</label> <input type="text" name="tag-y" size="7" id="y-tag" class="validate[required]" /> '+
                '<label class="label-item">z</label> <input type="text" name="tag-z" size="7" id="z-tag" class="validate[required]" />'+
                '</td>'+
                '</tr>';
                $("#calcall").find("tr[id=pre]").prev(new_tr);
    }   
}

function hidetag(){
    if( $("#calcall").find("input[id=pre]").value()=="no"){
          $("#calcall").find("tr[id=coord-met]").remove();      
    }
    var new_trs = '<tr id="par">'+
                        '<td>Name of paramagnetic center</td>'+
                        '<td><input type="text" name="calcparam" id="calcparam"  size=7 class="validate[required]"/></td>'+
                    '</tr>'+
                    '<tr id="par">'+
                        '<td>Corresponding residue number</td>'+
                        '<td><input type="text" name="calcresnum" id="calcresnum"  size=7 class="validate[required]"/></td>'+
                    '</tr>'+
                    '<tr id="par">'+
                        '<td>Last residue (number) before the paramagnetic metal</td>'+
                        '<td><input type="text" name="calclastresnum" id="calclastresnum"  size=7 class="validate[required]"/></td>'+
                    '</tr>'+
                    '<tr id="pre">'+
                        '<td>Do you use Paramagnetic Relaxation Enhancement?</td>'+
                        '<td><input type="radio" title=": yes" name="pre" id="pre_yes" class="radiomiddle" value="yes" onclick="showpre()">'+
                            '<label for="pre_yes" class="label-item">Yes</label>'+
                            '<input type="radio" title=": no" name="pre" id="pre_no" class="radiomiddle" value="no" checked onclick="hidepre()">'+
                            '<label for="pre_no" class="label-item">No</label>'+
                        '</td>'+
                    '</tr>';
     $("#calcall").append(new_trs);
     $("#calcall").find("tr[id=coord-tag]").remove();
}

function check_calc(){
                var calc = $("#ranch-calcname").val();
                var proj = $("#prj_id").val();
                if (calc != ""){
                                $.ajax({
                                                type: 'POST',
                                                url: '/ranch/check_ava',
                                                data: {'proj_id': proj, 'calc_name': calc},
                                                success: function(data){
                                                             if (data == 'Ok'){
                                                                    $("#checkava").remove();
                                                                    $("#ranch-calcname").after('<span class="ok" style="color:  blue;"> OK</span>');
                                                                    $("#submit_ranch").removeAttr("disabled");
                                                             }
                                                             else{
                                                                    $("#checkava").remove();
                                                                    $("#ranch-calcname").after('<span class="no" style="color:  red;"> Already in use in this project</span>');
                                                                    $("#submit_ranch").attr("disabled", "disabled");
                                                             }
                                                }    
                                });
                }
}

function validatorRequest(formData, jqForm, options){
                var isok = true
                if ($("#ranchseq").val() == ""){
                                $.validationEngine.buildPrompt("#ranchseq", "*This field is required","error");
                                isok = false;
                }
                if ($("#ranchpdb").val() == ""){
                                $.validationEngine.buildPrompt("#ranchpdb", "*This field is required","error");
                                isok = false;
                }
                if ($("#calcrdc").val() == ""){
                                $.validationEngine.buildPrompt("#calcrdc", "*This field is required","error");
                                isok = false;
                }
                if ($("#calcpcs").val() == ""){
                                $.validationEngine.buildPrompt("#calcpcs", "*This field is required","error");
                                isok = false;
                }
                if ($("#calctensor").val() == ""){
                                $.validationEngine.buildPrompt("#calctensor", "*This field is required","error");
                                isok = false;
                }
                
                if (isok){
                         waiting();
                         return true       
                }
                else{
                         return false
                }
}

function processFormRanchSuccess(data){
                window.location = '/jobs/show/all';
}

function waiting(){
                var myWidth = 320;
                var myHeight = 240;
                var option = {
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                data = '<img src="/global/images/downloadBundle.gif" />'
                $.modal(data, option);
}

function buildpdbinput(){
                var num = $("input[name=ranchnumdomain]").val();
                var str_temp = '';
                
                if (parseInt(num) > 0){
                                var ranchpdb = $("input[name=ranchpdb]");
                                $(ranchpdb).each(function(){$(this).parent().parent().remove();})
                                for (i=0; i < parseInt(num); i++) {
                                                str_temp += '<tr><td>Select pdb filename (.pdb)</td>';
                                                str_temp += '<td><input type="file" name="ranchpdb" id="ranchpdb" class="validate[required]"/></td></tr>';
                                }
                                $("#numdomain").after(str_temp)
                }
                else{
                                var ranchpdb = $("input[name=ranchpdb]");
                                $(ranchpdb).each(function(){$(this).parent().parent().remove();})
                }
}

function showpre(){
    var new_tr ='<tr id="file-pre">'+
                '<td>Paramagnetic Relaxation Enhancement file</td>'+
                '<td><input type="file" name="prefile" id="prefile" class="validate[required]" /></td>'+
                '</tr>'+
                '<tr id="center-pre">'+
                '<td>Coordinates of paramagnetic center</td>'+
                '<td><label class="label-item">x</label> <input type="text" name="pre-x" size="7" id="x-pre" class="validate[required]" />'+
                '<label class="label-item">y</label> <input type="text" name="pre-y" size="7" id="y-pre" class="validate[required]" />'+
                '<label class="label-item">z</label> <input type="text" name="pre-z" size="7" id="z-pre" class="validate[required]" />'+
                '</td>'+
                '</tr>';
    //$("#calcall").find("tr[id=par]").remove();
    $("#calcall").append(new_tr);
}

function hidepre(){
     $("#calcall").find("tr[id=file-pre]").remove();
     $("#calcall").find("tr[id=center-pre]").remove();
}
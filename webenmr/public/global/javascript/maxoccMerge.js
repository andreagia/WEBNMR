$(document).ready(function() {
                //$("#maxoccInput").hide();
                fill_project_list();
                $("#maxoccMerge").find("select[name=proj_list]").each(function(i){
                    $(this).bind("change", function(){
                            if ($("#proj_list"+i).val() != 'none'){
                                $("#calc_list"+i).removeAttr("disabled");
                                maxocc_calc_list(i);
                            }
                            else{
                                $("#calc_list"+i).empty();
                                $("#calc_list"+i).append('<option value="none">Select calculation</option>');
                                $("#calc_list"+i).attr("disabled", "disabled");
                            }
                    });
                });
                //$("#calc_list").attr("disabled", "disabled");
                //$("#calc_list").bind("change", function(){
                //    if ($("#calc_list").val() != 'none'){
                //        $("#maxoccInput").show();
                //    }
                //    else{
                //        $("#maxoccInput").hide();
                //    }
                //});
    
                //$("#maxocc").validationEngine();
                
               // var optionsFormMaxocc = { 
               //     beforeSubmit:   validatorRequest,  // pre-submit callback
               //     dataType:  'script',        // 'xml', 'script', or 'json' (expected server response type) 
               //     success:  processFormMaxoccSuccess   // post-submit callback 
               // }; 
               //
               // // bind form using 'ajaxForm' 
               // $('#maxocc').ajaxForm(optionsFormMaxocc);
               ////$('#maxocc')[0].reset();
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

function check_calc(){
                var calc = $("#maxocc-calcname").val();
                var proj = $("#proj_list option:selected").val();
                if (calc != ""){
                                $.ajax({
                                                type: 'POST',
                                                url: '/maxocc/check_ava',
                                                data: {'proj_name': proj, 'calc_name': calc},
                                                success: function(data){
                                                             if (data == 'Ok'){
                                                                    $("#checkava").remove();
                                                                    $("#maxocc-calcname").after('<span class="ok" style="color:  blue;"> OK</span>');
                                                                    $("#submit_maxocc").removeAttr("disabled");
                                                             }
                                                             else{
                                                                    $("#checkava").remove();
                                                                    $("#maxocc-calcname").after('<span class="no" style="color:  red;"> Already in use in this project</span>');
                                                                    $("#submit_maxocc").attr("disabled", "disabled");
                                                             }
                                                }    
                                });
                }
}

function validatorRequest(formData, jqForm, options){
                var isok = true
                if ($("#exp-saxs").val() == ""){
                                $.validationEngine.buildPrompt("#exp-saxs", "*This field is required","error");
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

function view_result(){
                var myWidth = 600;
                var myHeight = 630;
                var option = {
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                
                $("#results").modal(option);
}

function stop_remove(c) {
                $("#"+c).remove();
}

function processFormMaxoccSuccess(data){
                $('#maxocc')[0].reset();
                window.location = '/jobs/show/all';
}

function check_status(){
                var calc = new Array();
                $("table[id=jobs]").find('tr[id^=calculation]').each(function(){
                              if ($(this).children('td').eq(1).html() == 'Running'){
                                var item = $(this).children('td').eq(0).html();
                                calc.push(item);
                              }
                });
                $(calc).each(function(){
                                var c = this;
                                $.ajax({
                                                type: 'POST',
                                                dataType: 'script',
                                                url: '/maxocc/check_status',
                                                data: "calcname="+c,
                                                success: function(data){
                                                                if (data == 'True'){
                                                                                changeStatus(c, "Completed")     
                                                                }
                                                }
                                });
                });
}

function changeStatus(calc, cur){
                alert("pippo")
                $("table[id=jobs]").find('tr[id^=calculation]').each(function(){
                                if ($(this).children('td').eq(0).html() == calc){
                                                $(this).children('td').eq(1).fadeOut().html(cur).fadeIn();
                                                $(this).children('td').eq(1).removeClass("running");
                                                $(this).children('td').eq(1).addClass("completed");
                                                $(this).children('td').eq(2).html('<a href="/maxocc/download/'+calc+'">download results</a>')
                                }
                });
}


function refresh_status(status_list){
                //formato item: calc::status
                status_list.each(function(){
                                var item = this.split("::")[0];
                                var status = this.split("::")[1];
                                $("table[id=jobs]").find('tr[id^=calculation]').each(function(){ 
                                                if ($(this).children().eq(0).html() == item){
                                                               if (!$(this).children().eq(1).html() == status){
                                                                                var stat = status.toLowerCase();
                                                                                $(this).children().eq(1).html(stat);
                                                                                $(this).children().eq(1).attr("class", stat);
                                                               }
                                                }
                                });
                });
}

function enableDist(){
                if ($('input[name=dist]').is(':checked')){
                                $("#defintorno1").show();
                                $("#defintorno2").show();
                }
                else{
                                $("#defintorno1").hide();
                                $("#defintorno2").hide();
                }
                
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
                                                str_temp += '<td><input type="file" name="ranchpdb"/></td></tr>';
                                }
                                $("#numdomain").after(str_temp)
                }
                else{
                                var ranchpdb = $("input[name=ranchpdb]");
                                $(ranchpdb).each(function(){$(this).parent().parent().remove();})
                }
}

function fill_project_list(){
    $.ajax({
        type: 'POST',
        url:  '/maxocc/projects_list',
        success: function(data){
            plist = data.split(',');
            $("#maxoccMerge").find("select[name=proj_list]").each(function(){
                var obj = this;
                $(plist).each(function(){
                    $(obj).append('<option value="'+this+'">'+this+'</option>');
                });
            });
        }
    });
}

function fill_calc_list(){
    p = $("#proj_list").val();
    $("#calc_list").empty();
    $("#calc_list").append('<option value="none">Select calculation</option>');
    $.ajax({
        type: 'GET',
        url:  '/maxocc/ranch_calculations_list',
        data: 'proj='+p,
        success: function(data){
            if(data != ''){
                clist = data.split(',');
                $("#calc_list").removeAttr("disabled");
                $(clist).each(function(){
                    $("#calc_list").append('<option value="'+this+'">'+this+'</option>');
                });
            }
        }
    });
}

function maxocc_calc_list(idx){
    p = $("#proj_list"+idx).val();
    $("#calc_list"+idx).empty();
    $("#calc_list"+idx).append('<option value="none">Select calculation</option>');
    $.ajax({
        type: 'GET',
        url:  '/maxocc/calculations_list',
        data: 'proj='+p,
        success: function(data){
            if(data != ''){
                clist = data.split(',');
                $("#calc_list"+idx).removeAttr("disabled");
                $(clist).each(function(){
                    $("#calc_list"+idx).append('<option value="'+this+'">'+this+'</option>');
                });
            }
        }
    });
}
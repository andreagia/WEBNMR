$(function() {
    $("#tabs_restart").tabs();
    $("#tabs_restart").tabs( "option", "disabled", [1, 2] );
    fill_project_list();
    $("#proj_list").bind("change", function(){
        $("#sel_inputs").attr("style", "display: none;");
        if ($("#proj_list").val() != 'none'){
            $("#calc_list").removeAttr("disabled");
            fill_calc_list();
        }
        else{
            $("#calc_list").empty();
            $("#calc_list").append('<option value="none">Select calculation</option>');
            $("#calc_list").attr("disabled", "disabled");
            $("#tabs_restart").tabs( "option", "disabled", [1, 2] );
        }
    });
    $("#calc_list").attr("disabled", "disabled");
    $("#calc_list").bind("change", function(){
        if ($("#calc_list").val() != 'none'){
            $("#job_list").removeAttr("disabled");
            $("#sel_inputs").removeAttr("style");
            fill_job_list();
        }
        else{
            $("#job_list").empty();
            $("#job_list").append('<option value="none">Select job</option>');
            $("#job_list").attr("disabled", "disabled");
            $("#sel_inputs").attr("style", "display: none;");
        }
    });
    
    $("#job_list").attr("disabled", "disabled");
    $("#job_list").bind("change", function(){
        if ($("#calc_list").val() != 'none'){
            $("#tabs_restart").tabs( "option", "disabled", [2] );
            //$("#sel_inputs").removeAttr("style");
        }
        else{
            $("#tabs_restart").tabs( "option", "disabled", [1, 2] );
            //$("#sel_inputs").attr("style", "display: none;");
        }
    });
    
    
    $("select[name=group]").change(function(){
        var g = $(this).val();
        $("span[id=descr]").remove();
        if (g != 'none'){
            $.ajax({
                type: 'POST',
                url: '/calculations/get_protList',
                data: {"group": g},
                success: function(data){
                    var prot_list = data.split(",");
                    $("select[name=protocol]").empty();
                    $("select[name=protocol]").append('<option value="none">Select protocol</option>');
                    $(prot_list).each(function(){
                        $("select[name=protocol]").append('<option value="'+this+'">'+this+'</option>');
                    });
                }
            });
        }
        else{
            $("select[name=protocol]").empty();
            $("select[name=protocol]").append('<option value="none">Select protocol</option>');
            //$("textarea[name=sander]").attr("value", '');
            $("#multistep").attr("style", "display:none;");
        }
        $("textarea[name=sander]").val('');
        $("textarea[name^=step]").remove();
        $("textarea[name=sander]").removeClass("nodisplay");
        
        
    });
    
    $("select[name=protocol]").change(function(){
        var g = $("select[name=group]").val();
        var p = $(this).val();
        if (p != 'none'){
            $.ajax({
                type: 'POST',
                url: '/calculations/isMultistep',
                data: {"protocol": p, "group": g},
                success: function(data){
                    $("textarea[name=sander]").val('');
                    if(parseInt(data) > 1){
                        $("#multistep").children("fieldset").empty();
                        $("#multistep").children("fieldset").append('<legend>Multistep protocol</legend>'+
                            '<p class="multistep_header">Choose what step (also more than one) include in the restart:</p>');
                        for (i = 1; i <= parseInt(data); i = i + 1){
                            $("#multistep").children("fieldset").append('<input type="checkbox" name="chk_step'+i+'" value="'+i+'">step '+i+'<br />')
                        }
                        $("#multistep").removeAttr("style");
                        
                        $("input[name^=chk_step]").click(function(){
                            n = $(this).attr("name").split("_")[1];
                            if ($(this).attr("checked")) {
                                if ($("textarea[name="+n+"]").length){
                                    $("textarea").not(".nodisplay").addClass("nodisplay");
                                    $("textarea[name="+n+"]").removeClass("nodisplay");
                                }
                                else{
                                    $.post("/calculations/get_protContent", {"protocol": p, "group": g, "step": $(this).val()}, function(data){
                                        $("#textarea_sander").append('<textarea name="'+n+'" class="sander_param nodisplay" cols="38" rows="15"></textarea>');
                                        $("textarea").not(".nodisplay").addClass("nodisplay");
                                        $('textarea[name='+n+']').removeClass("nodisplay");
                                        $('textarea[name='+n+']').val(data);
                                        
                                        }
                                    );
                                }
                            }
                            else{
                                $('textarea[name='+n+']').remove();
                                if($('textarea[name^=step]').length){
                                    $('textarea[name^=step]').last().removeClass("nodisplay");
                                }
                                else{
                                    $("textarea[name=sander]").removeClass("nodisplay");
                                }
                                
                                var chk = $("input[name^=chk_step]:checked");
                                var chk_len = chk.length;
                                if(!chk_len){
                                    $("#tabs_restart").tabs( "option", "disabled", [2] );
                                }
                                
                            }
                            var chk = $("input[name^=chk_step]:checked");
                            var chk_len = chk.length;
                            var issequential = true;
                            for(i = 0; i < (chk_len - 1); i = i+1){
                                if(($(chk[i+1]).val() - $(chk[i]).val()) > 1){
                                    issequential = false;
                                }
                            }
                            if(issequential && chk_len){
                                $("#shake").remove();
                                $("#tabs_restart").tabs( "option", "disabled", [] );
                            }
                            else if(!issequential){
                                $("#tabs_restart").tabs( "option", "disabled", [2] );
                                $("#multistep").children("fieldset").append('<div id="shake" class="effect">'+
                                    '<br /><div align="center"><img src="/global/images/war.png" style="cursor: pointer;" onclick="show_note()"></div></div>');
                                $("#multistep").children("fieldset").children("#shake").effect( "bounce", {}, 500 );
                            }
                            else{
                                $("#shake").remove();
                                $("#tabs_restart").tabs( "option", "disabled", [2] );
                            }
                        });
                    }
                    else{
                        $.post('/calculations/get_protContent', {"protocol": p, "group": g, "step": 1}, function(data){
                                $("#multistep").attr("style", "display: none;");
                                $("textarea[name=sander]").val(data);
                                $("#tabs_restart").tabs( "option", "disabled", [] );
                            }
                        );
                    }
                }
            });
            $("#descr").remove();
            $("select[name=protocol]").after('<span id="descr">&nbsp;&nbsp;<img src="/global/images/info.png"'+
                                              'onclick="show_descr()" title="Details on selected protocol" alt="Details on selected protocol"></span>');
        }
        else{
            $("#multistep").attr("style", "display:none;");
            $("#descr").remove();
            $("textarea[name^=step]").remove();
            $("textarea[name=sander]").removeClass("nodisplay");
        }
    });
    $("#restart_form").validationEngine({inlineValidation: false, returnIsValid:true});
//    var optionsSel_inputs = { 
//		//target:        '#output1',   // target element(s) to be updated with server response 
//		beforeSubmit:   validateRequest,  // pre-submit callback
//		dataType:  'script',        // 'xml', 'script', or 'json' (expected server response type) 
//		success:  processSel_inputsSubmit   // post-submit callback 
//    }; 
//	   
//    // bind form using 'ajaxForm' 
//    $('#restart_form').ajaxForm(optionsSel_inputs);
    
    $("textarea[name=sander]").bind("contextmenu", function(e) {
        e.preventDefault();
    });
    
    $("textarea[name=sander]").bind("keyup", function(){
        var count_lines = $("textarea[name=sander]").val().split("\n").length;
        if (count_lines >= 4 ){
            $("#tabs_restart").tabs( "option", "disabled", [] );
            if (!$("#save_prot").length){
                $("textarea[name=sander]").after('<br /><button type="button" id="save_prot">Save as...</button><br /><span id="note" class="note">Note: you can run the simulation with modified protocol also without save it</span>');		    
                $("#save_prot").button();
                $("#save_prot").bind("click", function(){
                    save();
                });
            }
        }
        else if($("textarea[name=sander]").val() == ''){
            $("#tabs_restart").tabs( "option", "disabled", [2] );
            $("#save_prot").remove();
            $("span[id=note]").remove();
            $("span[id=saved]").remove();
        }
        else{
            $("#tabs_restart").tabs( "option", "disabled", [2] );
            $('select[name=group] option:selected').removeAttr("selected");
            $("select[name=protocol]").empty();
            $("select[name=protocol]").append('<option value="none">Select protocol</option>');
        }
        
        if ($("#saved").length)
            $("#saved").removeClass("saved");
            $("#saved").html("(not saved, maybe)")
            $("#saved").addClass("notsaved");
        
    });
    
    $("#top_input").change(function(){
        if ($(this).attr("value") != '')
            $.validationEngine.closePrompt("#top_input");
    });
    $("#coord_input").change(function(){
        if ($(this).attr("value") != '')
            $.validationEngine.closePrompt("#coord_input");
    });
    
    $("#name-restart").bind("keyup", function(){
        if (!$("#check").length){
            $("#fieldname").children("span").remove();
            $("#name-restart").after('<button type="button" id="check" onclick="check_calc_name()">check availability</button>');
        }
    });
});
    
function validateRequest(){
    /*if ($("#top_input").val() == ""){
        $.validationEngine.buildPrompt("input[id=top_input]","Please, a topology file is required","error");
        return false
    }
    if ($("#coord_input").val() == ""){
        $.validationEngine.buildPrompt("input[id=coord_input]","Please, a coordinates file is required","error");
        return false
    }
    
    return true	  */  
}

function processSel_inputsSubmit(data){
   next_tab();
}

function fill_project_list(){
    $.ajax({
        type: 'POST',
        url:  '/filemanager/projects_list',
        success: function(data){
            plist = data.split(',');
            $(plist).each(function(){
                $("#proj_list").append('<option value="'+this+'">'+this+'</option>');
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
        url:  '/filemanager/amber_calculations_list',
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

function fill_job_list(){
    p = $("#proj_list").val();
    c = $("#calc_list").val();
    $("#job_list").empty();
    $("#job_list").append('<option value="none">Select job</option>');
    $.ajax({
        type: 'POST',
        url:  '/calculations/get_jobList',
        data: {'proj': p, 'calc': c},
        success: function(data){
            if (data != ''){
                jlist = data.split(',');
                $("#job_list").removeAttr("disabled");
                $(jlist).each(function(){
                    $("#job_list").append('<option value="'+this+'">'+this+'</option>');
                });
                if(jlist.length == 1){
                    $("#job_list").children('<option[value='+jlist+']').attr("selected", "selected");
                    $("#tabs_restart").tabs( "option", "disabled", [2] );
                }
            }
        }
    });
}

function next_tab(){
    if (typeof( $("#advanced").attr('style') ) == 'undefined'){
        if($("#top_input").attr("value") != '' && $("#coord_input").attr("value") != ''){
            //$.validationEngine.closePrompt(".allmydiv", true);
            $.validationEngine.closePrompt("#top_input");
            $.validationEngine.closePrompt("#coord_input");
            $("#tabs_restart").tabs( "option", "disabled", [2] );
            $("#tabs_restart").tabs( "option", "selected", 1 );
        }
        else{
            if($("#top_input").attr("value") == ''){
                $.validationEngine.buildPrompt("#top_input", "You must upload a topology file", "error");
            }
            if($("#coord_input").attr("value") == ''){
                $.validationEngine.buildPrompt("#coord_input", "You must upload a coordinates file", "error");
            }
            $("#tabs_restart").tabs( "option", "disabled", [2] );
            $("#tabs_restart").tabs( "option", "selected", 0 );
        }
    }
}

function fill_summary(){
    $("#summary_job").html('<b>'+$("select[id=job_list]").val()+'</b>');
    $("#summary_restart").html('<b>'+$("select[id=calc_list]").val()+'</b>');
    $("#summary_project").html('<b>'+$("select[id=proj_list]").val()+'</b>');
    if ($("#top_input").attr("value") != '')
        $("#summary_input").html("<b>uploaded</b>");
    else
        $("#summary_input").html("<b>taken from previous run</b>");
        
    if (!$('textarea[name=sander]').hasClass("nodisplay")){
        name = 'sander';
        $("#summary_sander").empty();
        $("#summary_sander").append('<a href="javascript:show_sander(\''+name+'\');" style="text-decoration: underline; color: blue" >view</a> &nbsp; &nbsp;')
    }
    else{
        $("#summary_sander").empty();
        $('textarea[name^=step]').each(function(i){
            var name = $(this).attr("name");
            $("#summary_sander").append('<a href="javascript:show_sander(\''+name+'\');" style="text-decoration: underline; color: blue" >view '+$(this).attr("name").replace("p", "p ")+'</a> &nbsp; &nbsp;')
        });
    }
}

function expert_mode(){
    $("#advanced").removeAttr("style");
    $("#job_list option:selected").removeAttr("selected");
    //$("#input_file_form").validationEngine({inlineValidation: false});
    //$("#input_file_form").before('<a id="normal_link" href="javascript:normal_mode();" style="text-decoration: underline;">back to default</a>');
    $("#tabs_restart").tabs( "option", "disabled", [1, 2] );
}

function normal_mode(){
    $("#advanced").attr("style", "display: none;");
    $("#normal_link").remove();
    if($("#job_list").children().length == 2){
        $("#job_list").children().last().attr("selected", "selected");
        $("#tabs_restart").tabs( "option", "disabled", [2] );
    }
    else{
        $("#tabs_restart").tabs( "option", "disabled", [1, 2] );
    }
    $.validationEngine.closePrompt("input[id=top_input]");
    $.validationEngine.closePrompt("input[id=coord_input]");
}

function show_example(){
    var myWidth = 600;
    var myHeight = 400;
    var option = {
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    $("#example").modal(option);
}

function show_info(){
    var option = {
            opacity:70,
            overlayCss: {backgroundColor:"#fff"}
        };
    //error due vertical scroll bar, calculated on Firefox browser
    var error_width = 0;
    var myWidth = 400 + error_width;
    var myHeight = 250;
    var h = (myHeight/$(document).height())*100;
    var w = (myWidth/$(document).width())*100;
    var pY = 50 - h/2;
    var pX = 50 - w/2;
    
    $("#info").modal({minWidth: myWidth, minHeight: myHeight, maxWidth: myWidth, maxHeight: myHeight});
    //, position:[pX+"%", pY+"%"] 
}

function show_sander(name){
    var myWidth = 350;
    var myHeight = 300;
    var option = {
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    data = $('textarea[name='+name+']').val();    
    var tmp = data.replace(/\n/g, "<br>");
    $.modal(tmp, option);
}

function show_descr(){
    var myWidth = 450;
    var myHeight = 300;
    var option = {
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    //var data = $('textarea[name=sander]').val();
    //var tmp = data.replace(/\n/g, "<br>");
    var g = $("select[name=group]").val();
    var p = $("select[name=protocol]").val();
    $.post("/calculations/get_protContent", {"group": g, "protocol": p, "step": "dscr"}, function(data){
        $.modal(data, option);
    });
}

function show_note(){
    var myWidth = 550;
    var myHeight = 100;
    var option = {
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    data = '<b>Some notes about the protocol to include in restart</b><br><br> '+
            'If you are selecting more than one step of a multistep protocol <b>must</b> follow '+
            'a simple rule: the list of steps (e.g. from step <b>m</b> to step <b>n</b>) '+ 
            'you can select must be strictly consecutive, that is, for example, the ensemble [step <b>1</b>, step <b>3</b>] isn\'t permitted, '+
            'whereas the ensemble [step <b>1</b>, step <b>2</b>], [step <b>2</b>, step <b>3</b>] or [step <b>1</b>, step <b>2</b>, step <b>3</b>] are possible.';
    $.modal(data, option);
}

function save(){
    var option = {
            opacity:70,
            overlayCss: {backgroundColor:"#fff"}
        };
    //error due vertical scroll bar, calculated on Firefox browser
    var error_width = 0;
    var myWidth = 400 + error_width;
    var myHeight = 250;
    var h = (myHeight/$(document).height())*100;
    var w = (myWidth/$(document).width())*100;
    var pY = 50 - h/2;
    var pX = 50 - w/2;
    
    $("#confirm").button();
    $("#confirm").bind("click", function(){
        if ($("#protname").val() == ''){
            $.validationEngine.buildPrompt("#protname", "You must type a name", "error");
        }
        else{
            var filename = $("#protname").val();
            var data_content = $("textarea[name=sander]").val();
            var descr_content = $("textarea[name=descrprot]").val();
            $.validationEngine.closePrompt("#protname");
            $.ajax({
                type: "POST",
                url: "/calculations/save_protocol",
                data: {"filename": filename, "data_content": data_content, "descr_content": descr_content},
                success: function(){
                    $("#save_prot").after('&nbsp;<span id="saved" class="saved">(saved)</span>');
                    $.modal.close();
                }
            });
        }
        
    });
    $("#close").button();
    $("#close").bind("click", function(){
        $.validationEngine.closePrompt("#protname");
        $("#confirm").unbind("click");
        $.modal.close();
    });
    $("#saveform").modal({minWidth: myWidth, minHeight: myHeight, maxWidth: myWidth, maxHeight: myHeight});
}

function check_calc_name(){
    p = $("select[id=proj_list]").val();
    c = $("#name-restart").val();
    $.ajax({
        url: '/calculations/check_calc_name',
        type: 'POST',
        data: {'calc_name': c, 'proj_name': p},
        success: function(data){
            var c = 'no-available';
            $("#check").remove();
            if (data == 'Ok'){
                $("#submit-button").removeAttr("disabled");
                c = 'available';
            }
            $("#name-restart").after('<span class="'+c+'"> '+data+'</span>')
        }
    });
}
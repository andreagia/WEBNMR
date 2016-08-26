$(document).ready( function() {
                
    $("#keyboard").accordion({
        autoHeight: false,
        collapsible: true
    });
    loadProtocol();
});

function loadProtocol(){
        //group::name
        $.ajax({
                url: '/protocols/laod_protocols',
                type: 'POST',
                success: function(data){
                        if (data) {
                                var l = data.split(";");
                                l.each(function(){
                                        var item = this.split("::");
                                        if (item[0] == 'preset'){
                                                $("#preset").append('<option value="'+item[1]+'">'+item[1]+'</option>');
                                        }
                                        else{
                                                $("#personal").append('<option value="'+item[1]+'">'+item[1]+'</option>');
                                        }
                                });
                        }
                }
        });
}
        
        function modalOnClose(dialog){
            var s = this;
            s.close(); // close the current dialog
            setTimeout(function () { // wait for 1/10ths of a second, then open the next dialog
                var myWidth = 850;
                var myHeight = 430;
                var option = {
                    onShow: modalOnShow2,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                
                $("#protocol").modal(option);
            }, 100);
        }
        
        function modalOnShow(dialog){
            var s = this;
            $('.retcp', dialog.data[0]).click(function () { // use the modal data context
                s.close(); // close the current dialog
               
                setTimeout(function () { // wait for 1/10ths of a second, then open the next dialog
                    var myWidth = 850;
                    var myHeight = 430;
                    var option = {
                        onShow: modalOnShow2,
                        opacity:70,
                        minWidth: myWidth,
                        minHeight: myHeight,
                        maxWidth: myWidth,
                        maxHeight: myHeight
                    };
                    $("#protocol").modal(option);
                }, 100);
                return false;
            });
        }
        
        function show_descr(){
	    var myWidth = 450;
	    var myHeight = 300;
	    var option = {
                onShow: modalOnShow,
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
                $("#infop").prepend(data);
		$("#infop").modal(option);
	    });
	}
        
        function changeGroup(o){
            var g = $(o).val();
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
            $("textarea[name=param-list]").val('');
            $("textarea[name^=step]").remove();
            $("textarea[name=param-list]").removeClass("nodisplay");
        }
        
        function changeProtocol(o){
            var g = $("select[name=group]").val();
            var p = $(o).val();
            if (p != 'none'){
                $.ajax({
                    type: 'POST',
                    url: '/calculations/isMultistep',
                    data: {"protocol": p, "group": g},
                    success: function(data){
                        $("textarea[name=param-list]").val('');
                        if(parseInt(data) > 1){
                            $("#multistep").empty();
                            for (i = 1; i <= parseInt(data); i = i + 1){
                                $("#multistep").append('<input type="checkbox" name="chk_step'+i+'" value="'+i+'"><i>step '+i+'</i> <img id="step'+i+'" class="imgremove" src="/global/images/cancel.png" onclick="remove_step(this.id)" /><br />')
                            }
                            $("#multistep").append('<div><img id="add_step" class="imgplus" src="/global/images/plus.png">&nbsp;<a href="javascript:add_step()" title="Add new step">add step</a></div><br>');
                            $("#multistep").removeAttr("style");
                            $("#parameters-sander").find("p").removeClass("nodisplay")
                            
                            $("input[name^=chk_step]").click(function(){
                                n = $(this).attr("name").split("_")[1];
                                if ($(this).attr("checked")) {
                                    if ($("textarea[name="+n+"]").length){
                                        $("textarea").not(".nodisplay").addClass("nodisplay");
                                        $("textarea[name="+n+"]").removeClass("nodisplay");
                                    }
                                    else{
                                        $.post("/calculations/get_protContent", {"protocol": p, "group": g, "step": $(this).val()}, function(data){
                                            $("#textarea_sander").append('<textarea name="'+n+'" class="txtsander nodisplay" cols="38" rows="15"></textarea>');
                                            $("textarea").not(".nodisplay").addClass("nodisplay");
                                            $('textarea[name='+n+']').removeClass("nodisplay");
                                            $('textarea[name='+n+']').val(data);
                                        });
                                    }
                                }
                                else{
                                    $('textarea[name='+n+']').remove();
                                    if($('textarea[name^=step]').length){
                                        $('textarea[name^=step]').last().removeClass("nodisplay");
                                    }
                                    else{
                                        $("textarea[name=param-list]").removeClass("nodisplay");
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
                                    $("textarea[name=param-list]").val(data);
                                    $("#tabs_restart").tabs( "option", "disabled", [] );
                                }
                            );
                        }
                    }
                });
                $("#descr").remove();
                $("select[name=protocol]").after('<span id="descr">&nbsp;&nbsp;<img id="info" src="/global/images/info.png"'+
                                                  ' title="Details on selected protocol" alt="Details on selected protocol"></span>');
            }
            else{
                $("#multistep").attr("style", "display:none;");
                $("#descr").remove();
                $("textarea[name^=step]").remove();
                $("textarea[name=param-list]").removeClass("nodisplay");
            }
        }
        
        function remove_step(id){
            $("input[name=chk_"+id+"]").nextUntil("input[name^=chk_step]").not("div").remove();
            $("input[name=chk_"+id+"]").remove();
            $("textarea[name="+id+"]").remove();
            $("#"+id).remove();
            var txtactive = $("textarea").not(".nodisplay");
            if (!txtactive.length){
                var chk = $("input[name^=chk_step]:checked");
                var chk_len = chk.length;
                if(chk_len){
                    chk.last().removeClass("nodisplay");
                }
                else{
                    $("#param-list").removeClass("nodisplay");
                }
            }
            
            if(!$("input[name^=chk_step]").length){
                $("#multistep").children("div").remove();
            }
            
        }
        
        function add_step(){
            var chk = $("input[name^=chk_step]");
            var chk_len = chk.length;
            if (chk_len){
                if ($(chk[0]).attr("value") != '1'){
                    $("#multistep").prepend('<input type="checkbox" name="chk_step1" value="1"><i>step 1</i> <img id="step1" src="/global/images/cancel.png" onclick="remove_step(this.id)" /><br />');
                }
                else{
                    var cont = true;
                    $(chk).each(function(i){
                    var s = i+2
                        if(i < (chk_len -1)){
                            if ((Math.abs(parseInt($(this).attr("value")) - parseInt($(chk[i+1]).attr("value"))) > 1) && cont){
                                $(this).nextUntil("br").last().next().after('<input type="checkbox" name="chk_step'+s+'" value="'+s+'"><i>step '+s+'</i> <img id="step'+s+'" src="/global/images/cancel.png" onclick="remove_step(this.id)" /><br />');
                                cont = false;
                            }
                        }
                    });
                    if (cont){
                        var s = chk_len + 1
                        $(chk[chk_len-1]).nextUntil("br").last().next().after('<input type="checkbox" name="chk_step'+s+'" value="'+s+'"><i>step '+s+'</i> <img id="step'+s+'" src="/global/images/cancel.png" onclick="remove_step(this.id)" /><br />');
                    }
                }
            }
            else{
                $("#multistep").children("#add_step").before('<input type="checkbox" name="chk_step1" value="1"><i>step 1</i> <img id="step1" src="/global/images/cancel.png" onclick="remove_step(this.id)" /><br />');
            }
        }
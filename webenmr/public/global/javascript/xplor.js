$(document).ready(function() {
    $("#tabs-xplor").tabs();
    var $radios = $('input:radio');
    $radios.filter('[value=no]').attr('checked', true);
    
    //validazione
    //$("#xplor-form").validationEngine();
    $("#xplor-form").validationEngine(); 
    
    var optionsConstraint = { 
        //target:        '#output1',   // target element(s) to be updated with server response 
        beforeSubmit:   validateFormFields,  // pre-submit callback
        dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
        success:  processSubmit   // post-submit callback 
    };
    
               
    // bind form using 'ajaxForm' 
    $('#xplor-form').ajaxForm(optionsConstraint);
    
    $('#xplor-form')[0].reset();
    
})

function addChainSelector(where, like){
    if ($("#xplorseq-div").children().length > 1){
        var strSelect = '<label class="label-item">Chain name</label> <select id="chain-selector-'+like+'">'
        $("#xplorseq-div").children().each(function(){
            var val = $(this).find("#xplor-chainname").val()
            strSelect += '<option value="'+val+'">'+val+'</option>'
        });
        strSelect += "</select>";
        $("#tabs-xplor").find("#"+where).after(strSelect);
    }
    else if ($("#xplorseq-div").children().find("#xplor-chainname").val() != ""){
            var strSelect = '<label class="label-item">Chain name</label> <select id="chain-selector-'+like+'">'
            var val = $("#xplorseq-div").children().find("#xplor-chainname").val().replace(" ", "")
            strSelect += '<option value="'+val+'">'+val+'</option>'
            strSelect += "</select>";
            $("#"+where+":last").after(strSelect);
    }
}


function processSubmit(response){
    window.location.href = '/jobs/show/all';
}

function metal_choice(obj){
    if ($(obj).is(':checked')){
        $("#met_element").attr("readonly", "readonly")
        $("#met_charge").attr("readonly", "readonly")
        $("#met_rvdw").attr("readonly", "readonly")
        $("#met_eps").attr("readonly", "readonly")
    }
    else{
        $("#met_element").removeAttr("readonly")
        $("#met_charge").removeAttr("readonly")
        $("#met_rvdw").removeAttr("readonly")
        $("#met_eps").removeAttr("readonly")
    }
}

function validateFormFields(formData, jqForm, options){
    var someerror = false;
    $("#xplorseq-div").children("div[id=xplorseq-item]").each(function(){
        if ($(this).find("input[type=file]").val() != ''){
            if($(this).find("input[type=text]").val() == ''){
                someerror = true;
                $("#tabs-xplor").tabs('select', 0);
                obj = $(this).find("input[type=text]")
                $.validationEngine.buildPrompt(obj, 'This value is required!', 'error');
                input_id = $(this).find("input[type=text]").attr("id");
                $(this).find("input[type=text]").keyup(function(){
                   $.validationEngine.closePrompt("#"+input_id)
                });
                
            }
        }
        if ($(this).find("input[type=text]").val() != ''){
            if($(this).find("input[type=file]").val() == ''){
                someerror = true;
                $("#tabs-xplor").tabs('select', 0);
                obj = $(this).find("input[type=file]")
                $.validationEngine.buildPrompt(obj, 'This file is required!', 'error');
                input_id = $(this).find("input[type=file]").attr("id");
                $(this).find("input[type=file]").change(function(){
                   $.validationEngine.closePrompt("#"+input_id)
                });
            }
        }
    });
    
    if ($("input[name=parcenter]:checked").val() == 'yes'){
        if ($("#metal-ion").css('display') == 'none'){
            someerror = true;
            $("#tabs-xplor").tabs('select', 0);
            if($("#metal-choice-checkbox").is(":checked")){
                if ($("input[id=met_atom_name]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_atom_name]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_atom_name]").attr("id");
                    $("input[id=met_atom_name]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_res_name]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_res_name]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_res_name]").attr("id");
                    $("input[id=met_res_name]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_res_number]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_res_number]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_res_number]").attr("id");
                    $("input[id=met_res_number]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
            }
            else{
                if ($("input[id=met_atom_name]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_atom_name]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_atom_name]").attr("id");
                    $("input[id=met_atom_name]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_element]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_element]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_element]").attr("id");
                    $("input[id=met_element]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_res_name]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_res_name]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_res_name]").attr("id");
                    $("input[id=met_res_name]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_res_number]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_res_number]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_res_number]").attr("id");
                    $("input[id=met_res_number]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_charge]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_charge]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_charge]").attr("id");
                    $("input[id=met_charge]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_rvdw]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_rvdw]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_rvdw]").attr("id");
                    $("input[id=met_rvdw]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
                if ($("input[id=met_eps]").val() == ''){
                    $.validationEngine.buildPrompt($("input[id=met_eps]"), 'This value is required!', 'error');
                    input_id = $("input[id=met_eps]").attr("id");
                    $("input[id=met_eps]").keyup(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
            }
        }
    }
    if ($("input[name=cof]:checked").val() == 'yes'){
        $("#cofactorprop").find("table").find("tr").each(function(i){
            if ($("#xplor-cofpdb:eq("+i+")").val() == ''){
                someerror = true;
                $.validationEngine.buildPrompt($("#xplor-cofpdb:eq("+i+")"), 'This file is required!', 'error');
                input_id = $("#xplor-cofpdb:eq("+i+")").attr("id");
                $("#xplor-cofpdb:eq("+i+")").change(function(){
                   $.validationEngine.closePrompt("#"+input_id)
                });
            }
                
            if ($("#xplor-coftop:eq("+i+")").val() == ''){
                someerror = true;
                $.validationEngine.buildPrompt($("#xplor-coftop:eq("+i+")"), 'This file is required!', 'error');
                input_id = $("#xplor-coftop:eq("+i+")").attr("id");
                $("#xplor-coftop:eq("+i+")").change(function(){
                   $.validationEngine.closePrompt("#"+input_id)
                });
                
            }
            if ($("#xplor-cofpar:eq("+i+")").val() == ''){
                someerror = true;
                $.validationEngine.buildPrompt($("#xplor-cofpar:eq("+i+")"), 'This file is required!', 'error');
                input_id = $("#xplor-cofpar:eq("+i+")").attr("id");
                $("#xplor-cofpar:eq("+i+")").change(function(){
                   $.validationEngine.closePrompt("#"+input_id)
                });
            }
        });
    }
    if ($("input[name=dis]:checked").val() == 'yes'){
        $("#disulfideprop").find("table").find("tr").each(function(i){
            if ($("#xplor-disresnuma:eq("+i+")").val() != ''){
                if ($("#xplor-disresnumb:eq("+i+")").val() == ''){
                    someerror = true;
                    $.validationEngine.buildPrompt($("#xplor-disresnumb:eq("+i+")"), 'This value is required!', 'error');
                    input_id = $("#xplor-disresnumb:eq("+i+")").attr("id");
                    $("#xplor-disresnumb:eq("+i+")").change(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
            }
            if ($("#xplor-disresnumb:eq("+i+")").val() != ''){
                if ($("#xplor-disresnuma:eq("+i+")").val() == ''){
                    someerror = true;
                    $.validationEngine.buildPrompt($("#xplor-disresnuma:eq("+i+")"), 'This value is required!', 'error');
                    input_id = $("#xplor-disresnuma:eq("+i+")").attr("id");
                    $("#xplor-disresnuma:eq("+i+")").change(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
            }
        }); 
    }
    
    if ($("input[name=phis]:checked").val() == 'yes'){
        $("#xplorphis-div").find("div[id=xplorphis-item]").each(function(i){
            //alert($(this).find("input[id=xplor-phisresnum]").val())
            if ($(this).find("input[id=xplor-phisresnum]").val() != ''){
                if ($(this).find("select[name=xplor-phistype]").val() == ''){
                    someerror = true;
                    $("#tabs-xplor").tabs('select', 0);
                    $.validationEngine.buildPrompt($(this).find("select[name=xplor-phistype]"), 'This choice is required!', 'error');
                    input_id = $(this).find("select[name=xplor-phistype]").attr("id");
                    $(this).find("select[name=xplor-phistype]").change(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
            }
            else if ($(this).find("input[id=xplor-phisresnum]").val() == '' && $(this).find("select[name=xplor-phistype]").val() == '' && $("#xplorphis-div").find("div[id=xplorphis-item]").length == 1 ){
                someerror = true;
                $("#tabs-xplor").tabs('select', 0);
                $.validationEngine.buildPrompt($(this).find("select[name=xplor-phistype]"), 'This choice is required!', 'error');
                $.validationEngine.buildPrompt($(this).find("input[id=xplor-phisresnum]"), 'This value is required!', 'error');
            }
            if ($(this).find("select[name=xplor-phistype]").val() != ''){
                if ($(this).find("input[id=xplor-phisresnum]").val() == ''){
                    someerror = true;
                    $("#tabs-xplor").tabs('select', 0);
                    $.validationEngine.buildPrompt($(this).find("input[id=xplor-phisresnum]"), 'This value is required!', 'error');
                    input_id = $(this).find("input[id=xplor-phisresnum]").attr("id");
                    $(this).find("input[id=xplor-phisresnum]").change(function(){
                       $.validationEngine.closePrompt("#"+input_id)
                    });
                }
            }
        }); 
    }
    if ($("#xplor-nrostruct").val() == ''){
        someerror = true;
        $("#tabs-xplor").tabs('select', 0);
        $.validationEngine.buildPrompt($("#xplor-nrostruct"), 'This value is required!', 'error');
        input_id = $("#xplor-nrostruct").attr("id");
        $("#xplor-nrostruct").keyup(function(){
           $.validationEngine.closePrompt("#"+input_id)
        });
    }
    //$("#tabs-xplor").tabs('select', 0); // switch to first tab
    //jQuery('#xplor-seqfile').validationEngine('showPrompt', 'Aaaaaah, non si fa!', 'error', true);
    //jQuery('#xplor-residuenum').validationEngine('showPrompt', 'Ancora, ma allora!', 'error', true);
    if(someerror){
        alert("some error occurred")
        return false;
    }
    else{
        return true;
    }
}

function help_info(field){
    $.ajax({
        type: 'POST',
        url: '/xplor/helpinfo',
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




function shownonstdres(){
    $("#nonstdres-div").show()
}

function hidenonstdres(){
    $("#nonstdres-div").find("#nonstdres-item:gt(0)").remove();
    $("#nonstdres-div").find("#xplor-nonstdrestop").val("");
    $("#nonstdres-div").find("#xplor-nonstdrespar").val("");
    $("#nonstdres-div").hide();
    
}

function showparag(){
    $("#metalprop").show()
}

function clear_metalion(){
    $("#metal-ion").find("tr").remove();
    var new_tr = '<tr>'+
                    '<th>Atom name</th>'+
                    '<th>Element</th>'+
                    '<th>Residue name</th>'+
                    '<th>Residue number</th>'+
                    '<th>charge</th>'+
                    '<th>VDW radius</th>'+
                    '<th>VDW epsilon</th>'+
                    '<th>Metal binding residues</th>'+
                    '<th></th>'+
                  '</tr>';
    $("#metal-ion").append(new_tr);
    $("#metal-ion").hide();
}

function hideparag(){
    $("#met_atom_name").val("");
    $("#met_element").val("");
    $("#met_charge").val("");
    $("#met_res_name").val("");
    $("#met_rvdw").val("");
    $("#met_eps").val("");
    $("#metalprop").hide();
    clear_metalion();
}

function showcof(){
    $("#cofactorprop").show()
}

function hidecof(){
    $("#cofactorprop").find("#cof-item").first().siblings("#cof-item").remove();
    $("#cofactorprop").find("#cof-item").find("input").attr("value", "");
    $("#cofactorprop").hide()
}

function showdis(){
    $("#disulfideprop").show()
    addChainSelector("xplor-disresnuma", "disa")
    addChainSelector("xplor-disresnumb", "disb")
}

function hidedis(){
    $("#chain-selector-disa").prev().remove();
    $("#chain-selector-disa").remove();
    $("#chain-selector-disb").prev().remove();
    $("#chain-selector-disb").remove();
    $("#disulfideprop").hide()
}

function showphis(){
    $("#histidineprop").show()
    addChainSelector("xplor-phisresnum", "phis");
}

function hidephis(){
    $("#chain-selector-phis").prev().remove();
    $("#chain-selector-phis").remove();
    $("#histidineprop").hide()
}

function addseq(str){
    var out = '<div id="'+str+'"><img src="/global/images/cancel.png" onclick="removeseq(\'str\');"> '+str+'</div>';
    $("#uploadedseq").append(out);
}

function removeseq(id){
    $.ajax({
        url: '/xplor/removefile',
        data: {'file':id},
        success: function(data){
            $("#"+id).remove();
        }
    });   
}

function upload(form, name){
    var options = {
        url: "/xplor/uploadfile",
        data: {'namefield': name},
        success:  function(data){
            addseq(data)
        }
    };
    $("#"+form).ajaxSubmit(options);
}

function addmetal(){
    var new_str = '';
    if($("#metal-choice-checkbox").is(':checked')){
        if ($("#met_atom_name").val() != '' && $("#met_res_number").val() != '' && $("#met_res_name").val() != ''){
            new_str = '<tr>'+
                    '<td>'+$("#met_atom_name").val()+'</td>'+
                    '<td>n/a</td>'+
                    '<td>'+$("#met_res_name").val()+'</td>'+
                    '<td>'+$("#met_res_number").val()+'</td>'+
                    '<td>n/a</td>'+
                    '<td>n/a</td>'+
                    '<td>n/a</td>'+
                    '<td><a onclick="javascript:addmetbinding(this.parentNode.parentNode);">add residues</a></td>'+
                    '<td><img src="/global/images/rem.png" onclick="remove_metal(this.parentNode)"/></td>'+
                  '</tr>';
        }
    }
    else{
        if ($("#met_atom_name").val() != '' && $("#met_element").val() != '' && $("#met_res_name").val() != '' && $("#met_charge").val() != '' && $("#met_rvdw").val() != '' && $("#met_eps").val() != ''){
            new_str = '<tr>'+
                    '<td>'+$("#met_atom_name").val()+'</td>'+
                    '<td>'+$("#met_element").val()+'</td>'+
                    '<td>'+$("#met_res_name").val()+'</td>'+
                    '<td>'+$("#met_res_number").val()+'</td>'+
                    '<td>'+$("#met_charge").val()+'</td>'+
                    '<td>'+$("#met_rvdw").val()+'</td>'+
                    '<td>'+$("#met_eps").val()+'</td>'+
                    '<td><a onclick="javascript:addmetbinding(this.parentNode.parentNode);">add residues</a></td>'+
                    '<td><img src="/global/images/rem.png" onclick="remove_metal(this.parentNode)"/></td>'+
                  '</tr>';
        }
    }
    if (!$("#metal-ion").is(":visible")){
        $("#metal-ion").show();
    }
    //addtorestraints($("#met_res_name").val(), $("#met_res_number").val());
    if(new_str != ''){
        addtorestraints($("#met_res_name").val(), $("#met_res_number").val());
        $("#met_atom_name").val("");
        $("#met_element").val("");
        $("#met_charge").val("");
        $("#met_res_name").val("");
        $("#met_res_number").val("");
        $("#met_rvdw").val("");
        $("#met_eps").val("");    
        
        $("#metal-ion").append(new_str);
        
    }
}

function remove_metal(obj){
    removefromrestraints(obj);
    $(obj).parent().remove();
    if ($("#metal-ion").find("tr").length == 1){
        $("#metal-ion").hide();
    }
}

function addmetbinding(obj){
    var myWidth = 800;
    var myHeight = 250;
    var option = {
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    var posidx = $("#metal-ion").index(obj)
    var field_tmp = '<input type="hidden" id="hidden-index-tr" value="'+$(obj).find("td:eq(3)").text()+'"/>';
    $("#metal-binding-div").parent().append(field_tmp);
    var field_tmp2 = '<input type="hidden" id="hidden-index-tr2" value="'+$(obj).find("td:eq(2)").text()+'"/>';
    $("#metal-binding-div").parent().append(field_tmp2);
    if ($("#metal-binding-div").find("#chain-selector-met").length == 0){
        var strSelect = '';
        if ($("#xplorseq-div").children().length > 1){
            strSelect = '<label class="label-item">Chain name</label> <select id="chain-selector-met">'
            $("#xplorseq-div").children().each(function(){
                var val = $(this).find("#xplor-chainname").val();
                strSelect += '<option value="'+val+'">'+val+'</option>'
            });
            strSelect += "</select>";
        }
        else if ($("#xplorseq-div").children().find("#xplor-chainname").val() != ""){
                strSelect = '<td><label class="label-item">Chain name</label></td><td><select id="chain-selector-met">'
                var val = $("#xplorseq-div").children().find("#xplor-chainname").val()
                strSelect += '<option value="'+val+'">'+val+'</option>'
                strSelect += "</select></td>";
        }
        $("#metal-binding-div").children("table").find("tr").children("td:eq(3)").after(strSelect);
    }
    
    //addChainSelector("met_bin_atom_name", "met");
    $("#metal-binding-div").modal(option);
}

function bindingresidueapply(){
    var str = '';
    $("#add-metal-binding").find("tr").each(function(){
        var resnum = $(this).find("td:eq(1)").children("input").val();
        var atomname = $(this).find("td:eq(3)").children("input").val();
        if ($("#xplorseq-div").children().find("#xplor-chainname").val() != ""){
            var chainname = $(this).find("td:eq(5)").children("select").val();
            var distance = $(this).find("td:eq(7)").children("input").val();
            str = str + '<b>'+resnum+'</b> '+atomname+' '+chainname+' '+distance+', ';    
        }
        else{
            var distance = $(this).find("td:eq(5)").children("input").val();
            str = str + '<b>'+resnum+'</b> '+atomname+' '+distance+', ';    
        }
        
    });
    var nstr = str.slice(0, str.length-2)
    var numres = $("#hidden-index-tr").val()
    var nameres = $("#hidden-index-tr2").val()
    $("#metal-ion").find("tr").each(function(){
        $(this).find("td").each(function(i){
            if ($(this).text() == numres && i == 3){
                $(this).next().next().next().next().html(nstr);
            }
        });
    })
    $("#hidden-index-tr").remove();
    $("#hidden-index-tr2").remove();
    $.modal.close();
}

function bindingresiduecancel(){
    $("#hidden-index-tr").remove();
    $("#hidden-index-tr2").remove();
    $.modal.close();
}

function addtorestraints(name, number){
    var new_item = '<option value="'+number+'">'+name+' - '+number+'</option>';
    $("#xplor-rdc-metal").append(new_item);
    $("#xplor-pcs-metal").append(new_item);
}

function removefromrestraints(obj){
    //obj rappresenta il td con il cestino
    var tr_row = $(obj).parent();
    var num_res = tr_row.children("td:eq(3)");
    $("#xplor-rdc-metal").children("option[value="+$(num_res).text()+"]").remove();
    $("#xplor-pcs-metal").children("option[value="+$(num_res).text()+"]").remove();
}

function newfield(str){
    if (str == 'seq'){
        numdiv = $("#xplorseq-div").children("#xplorseq-item").length;
        arr = new Array(numdiv);
        $("#xplorseq-div").children("#xplorseq-item").each(function(i){
            arr[i] = parseInt($(this).children("#xplor-posseq").val())
        });
        newnum = (Math.max.apply(Math, arr) + 1).toString();
        var new_str = '<div id="xplorseq-item">'+
                        '<label class="label-item">Select file </label>'+
                        '<input type="file" name="xplor-seqfile" id="xplor-seqfile" size="7"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'xplor-seqfile\')"/> '+
                        '<label class="label-item">Number of first residue </label>'+
                        '<input type="text" name="xplor-residuenum" id="xplor-residuenum" size="4" value="1"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'xplor-residuenum\')" />'+
                        '<label class="label-item"> Chain name </label>'+
                        '<input type="text" name="xplor-chainname" id="xplor-chainname" size="4" /> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'xplor-chainname\')" />'+
                        '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
                        '<input type="hidden" id="xplor-posseq" name="xplor-posseq" value="'+newnum+'"/>'+
                      '</div>';
        $("#xplorseq-div").append(new_str);
    }
    else if (str == 'nonstdres'){
        var new_field = '<div id="nonstdres-item">'+
            '<label class="label-item">Topology </label></td>'+
            '<input type="file" name="xplor-nonstdrestop" id="xplor-nonstdrestop" size="7" />&nbsp;&nbsp;&nbsp;'+
            '<label class="label-item">Parameters </label>'+
            '<input type="file" name="xplor-nonstdrespar" id="xplor-nonstdrespar" size="7" />'+
            '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
        '</div>';
        $("#nonstdres-div").children("fieldset").children("#nonstdres-item").last().after(new_field);
        
    }
    else if (str == 'noe'){
        var new_field = '<div id="xplornoe-item">'+
            '<label class="label-item">Select file </label>'+
            '<input type="file" name="xplor-noefile" id="xplor-noefile"/>'+
            '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
        '</div>';
        $("#xplornoe-div").append(new_field);
        
    }
    else if (str == 'dih'){
        var new_field = '<div id="xplordih-item">'+
            '<label class="label-item">Select file </label>'+
            '<input type="file" name="xplor-dihfile" id="xplor-dihfile"/>'+
            '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
        '</div>';
        $("#xplordih-div").append(new_field);
    }
    else if (str == 'rdc'){
        var new_field = '<div id="xplorrdc-item">'+
            '<label class="label-item">Tensor ax </label>'+
            '<input type="text" name="xplor-rdctnsax" id="xplor-rdctnsax" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'numstruct\')" />'+
            '<label class="label-item"> Tensor rh </label>'+
            '<input type="text" name="xplor-rdctnsrh" id="xplor-rdctnsrh" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'numstruct\')" />'+
            '<label class="label-item"> Select file </label>'+
            '<input type="file" name="xplor-rdcfile" id="xplor-rdcfile"/ size="12">'+
            '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
        '</div>';
        $("#xplorrdc-div").append(new_field);
        $("#xplorrdc-div").children().last().prepend("<br />");
        $("#xplor-rdc-metal").clone().prependTo($("#xplorrdc-div").children().last());
        $("#xplorrdc-div").children().last().prepend('<label class="label-item">Reference metal ion</label>');
    }
    else if (str == 'pcs'){
        var new_field = '<div id="xplorpcs-item">'+
            '<label class="label-item">Tensor ax </label>'+
            '<input type="text" name="xplor-pcstnsax" id="xplor-pcstnsax" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'numstruct\')" />'+
            '<label class="label-item"> Tensor rh </label>'+
            '<input type="text" name="xplor-pcstnsrh" id="xplor-pcstnsrh" size="6"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'numstruct\')" />'+
            '<label class="label-item"> Select file </label>'+
            '<input type="file" name="xplor-pcsfile" id="xplor-pcsfile"/ size="12">'+
            '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
        '</div>';
        $("#xplorpcs-div").append(new_field);
        $("#xplorpcs-div").children().last().prepend("<br />");
        $("#xplor-pcs-metal").clone().prependTo($("#xplorpcs-div").children().last());
        $("#xplorpcs-div").children().last().prepend('<label class="label-item">Reference metal ion</label>');
    }
    else if (str == 'cof'){
        var nextStep = $("#cofactorprop").children("fieldset").children("#cof-item").length + 1;
        numdiv = $("#cofactorprop").children("fieldset").children("#cof-item").length;
        arr = new Array(numdiv);
        $("#cofactorprop").children("fieldset").children("#cof-item").each(function(i){
            arr[i] = parseInt($(this).children("#xplor-poscof").val())
        });
        newnum = (Math.max.apply(Math, arr) + 1).toString();
        var newstr = '<div id="cof-item" style="font: 11px/1.6em Verdana,Sans-serif;">'+
                    '<label class="label-item">PDB</label> '+
                    '<input type="file" name="xplor-cofpdb" id="xplor-cofpdb" size="7"/> '+
                    '<label class="label-item">Topology</label> '+
                    '<input type="file" name="xplor-coftop" id="xplor-coftop" size="7"/> '+
                    '<label class="label-item">Parameters</label> '+
                    '<input type="file" name="xplor-cofpar" id="xplor-cofpar" size="7"/> '+
                    '<a href="javascript:selectPatch(this.parentNode, '+nextStep+');">Patch molecule</a>'+
                    '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
                    '<input type="hidden" id="xplor-poscof" name="xplor-poscof" value="'+newnum+'"/>'+
                 '</div>';
         
         $("#cofactorprop").find("#cof-item").last().after(newstr);
    }
    else if (str == 'dis'){
        var new_tr = '<tr>'+
                //'<td><label class="label-item">Atom</label></td>'+
                //'<td><input type="text" name="xplor-disatoma" id="xplor-disatoma" size="7"/></td>'+
                '<td><label class="label-item">Residue number</label></td>'+
                '<td><input type="text" name="xplor-disresnuma" id="xplor-disresnuma" size="7"/></td>'+
                '<td>&lt;--&gt;</td>';
                //'<td><label class="label-item">Atom</label></td>'+
                //'<td><input type="text" name="xplor-disatomb" id="xplor-disatomb" size="7"/></td>'+
                new_tr += '<td><label class="label-item">Residue number</label></td>'+
                '<td><input type="text" name="xplor-disresnumb" id="xplor-disresnumb" size="7"/></td>'+
                '<td><a onclick="removefield(this.parentNode.parentNode);"><img src="/global/images/rem.png" /></a></td>'+
            '</tr>';
        $("#disulfideprop").find("table").append($("#disulfideprop").find("table").find("tr").last().clone());
        if ($("#disulfideprop").find("table").find("tr").length == 2){
            $("#disulfideprop").find("table").find("tr").last().append('<td><a onclick="removefield(this.parentNode.parentNode);"><img src="/global/images/rem.png" /></a></td>');
        }
        
        //addChainSelector("xplor-disresnuma", "disa")
        //addChainSelector("xplor-disresnumb", "disb")
    }
    else if (str == 'phis'){
        var new_tr = '<div id="xplorphis-item">'+
                        '<label class="label-item">Residue number </label>'+
                        '<input type="text" name="xplor-phisresnum" id="xplor-phisresnum" size="7"/> '+
                        '<label class="label-item">Protonation type </label>'+
                        '<select name=\'xplor-phistype\'>'+
                            '<option value = \'\' >Select type</option>'+
                            '<option value = \'HIED\' >Delta</option>'+
                            '<option value = \'HIEP\' >Protonated</option>'+
                        '</select>'+
                         '<a onclick="removefield(this.parentNode);"><img src="/global/images/rem.png" /></a>'+
                      '</div>';
         
        $("#xplorphis-div").append($("#xplorphis-div").children("#xplorphis-item").clone());
        //addChainSelector("xplor-phisresnum", "phis");
    }
    else if (str == 'bin'){
        var strSelect = '';
        chainfound = true;
        if ($("#xplorseq-div").children().length > 1){
            strSelect = '<label class="label-item">Chain name</label> <select id="chain-selector-met">'
            $("#xplorseq-div").children().each(function(){
                var val = $(this).find("#xplor-chainname").val()
                strSelect += '<option value="'+val+'">'+val+'</option>'
            });
            strSelect += "</select>";
        }
        else if ($("#xplorseq-div").children().find("#xplor-chainname").val() != ""){
                strSelect = '<label class="label-item">Chain name</label> <select id="chain-selector-met">'
                var val = $("#xplorseq-div").children().find("#xplor-chainname").val();
                strSelect += '<option value="'+val+'">'+val+'</option>'
                strSelect += "</select>";
        }
        else{
            chainfound = false;
        }
        var new_tr = '<tr>'+
                '<td><label class="label-item">Residue number</label></td>'+
                '<td><input type="text" id="met_bin_res_number" size="5" maxlength="3"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'met_bin_res_number\')" /></td>'+
                '<td><label class="label-item">Atom name</label></td>'+
                '<td><input type="text" id="met_bin_atom_name" size="5" maxlength="3"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'met_bin_atom_name\')" /></td>';
                if (chainfound){
                    new_tr += '<td><label class="label-item">chain name </label></td><td>'+strSelect+'</td>'
                }
                
                new_tr += '<td><label class="label-item">Distance</label></td>'+
                '<td><input type="text" id="met_bin_distance" size="5" maxlength="5"/> <img src="/global/images/info.png" class="infoimg" onclick="help_info(\'met_bin_distance\')" /></td>'+
                '<td><a onclick="removefield(this.parentNode.parentNode);"><img src="/global/images/rem.png" /></a></td>'+
                '</tr>';
        $("#add-metal-binding").append(new_tr);
    }
}

function removefield(obj){
    $(obj).remove();
}



function checkava(){
    var calc = $("#xplor-namecalc").val();
    var proj = $("#xplor-prj_id").val();
    if (calc != ''){
        $.ajax({
            type: "POST",
            url: "/xplor/isCalcExist",
            data: {"calc": calc, "proj": proj},
            success: function(data){
                if (data == 'ok'){
                    var sub = '<input type="submit" name="submitXplor" id = "submitXplor" value="Submit calculation" onclick="waitMessage();"/>';
                    $("#availability").after(sub);
                    $("#availability").remove();
                }
                else{
                    $("#availability").after('<span id="span-msg" class="no" style="color:  red;"> Already exists, choose another name</span>');
                    $("#span-msg").fadeOut(8000);
                }
            }
        });
        retrieve_metals();
    }
}

function waitMessage(){
    var myWidth = 320;
    var myHeight = 240;
    var option = {
        close: false,
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    $.modal('<img src="/global/images/loading2.gif" />', option);
}

function retrieve_metals(){
    var typelist = ["m_atom_name", "m_element", "m_res_name", "m_res_num", "m_charge", "m_rvdw", "m_eps", "m_bind_res"];
    $("#metal-ion").find("tr").each(function(){
        var tdquattro = '';
        $(this).find("td").each(function(i){
            if (i <= 6){
                hddfield = '<input type="hidden" name="'+typelist[i]+'" value="'+$(this).text()+'"/>';
                $("#hidden-metalfields").append(hddfield);
                if (i == 3){
                    tdquattro = $(this);
                }
            }
            else if (i == 7 && $(this).find("a").length == 0){
               hddfield = '<input type="hidden" name="'+typelist[7]+'" value="'+$(tdquattro).text()+':::'+$(this).text()+'"/>';
               $("#hidden-metalfields").append(hddfield); 
            }
        });
    });
}


function selectPatch(pn, numpos){
    var optionsPatch = { 
        //target:        '#output1',   // target element(s) to be updated with server response
        url: "/xplor/selectPatch",         // override for form's 'action' attribute 
        beforeSubmit:   checkFileFields,  // pre-submit callback
        data: {'pos': numpos},
        /*dataType:  'xml',*/       // 'xml', 'script', or 'json' (expected server response type) 
        success:  function(response, status){
                    listPatch = response.split("::")
                    if (listPatch.length >= 2){
                        sel = '<select id="patchsel" name="patchsel" onchange="patchRequirements(numres, firstres, this.parentNode)"><option value="">Select item</option>'
                        numres = new Array();
                        firstres = new Array();
                        $(listPatch).each(function(i){
                            patchs = this.split(",");
                            if (patchs[0] != ''){
                                sel += '<option value="'+patchs[0]+'">'+patchs[0]+'</option>';
                                numres[patchs[0]] = patchs[1];
                                if (patchs.length > 4){
                                    firstres[patchs[0]] = patchs[2] + ", " + patchs[3] + ", " + patchs[4];
                                }
                                else{
                                    firstres[patchs[0]] = patchs[2] + ", " + patchs[3];
                                }
                            }
                        });
                        sel +='</select>';
                        //alert(sel);
                        var myWidth = 850;
                        var myHeight = 300;
                        var option = {
                            opacity:70,
                            minWidth: myWidth,
                            minHeight: myHeight,
                            maxWidth: myWidth,
                            maxHeight: myHeight
                        };
                        msg = '<div id="patchPanel">'+
                        '<center><h2>Patching the molecular structure</h2></center>'+
                        '<p>You can select a patch to modify or link ligands to protein.</p>'+
                        '<div id="patch-item" style="padding: 10px 0 0 ;"><label for="patchsel" style="display: inline;">Choose patch </label>'+sel+'</div>'+
                        '<a onclick="addPatch();">add patch</a>'+
                        '<br />'+
                        '<br />'+
                        '<input type="button" value="Cancel" onclick="closePatchPanel()"/>&nbsp;&nbsp;<input type="button" value="Apply patch(es)!" onclick="applyPatch('+numpos+')" />'+
                        '</div>';
                        $.modal(msg, option);
                    }
                    else{
                        var myWidth = 320;
                        var myHeight = 240;
                        var option = {
                            opacity:70,
                            minWidth: myWidth,
                            minHeight: myHeight,
                            maxWidth: myWidth,
                            maxHeight: myHeight
                        };
                        msg = '<div>'+listPatch[0]+'</div>';
                        $.modal(msg, option);
                    }
                  }
    }; 
               
    // bind form using 'ajaxForm' 
    $('#xplor-form').ajaxSubmit(optionsPatch);
}

function checkFileFields(formData, jqForm, options){
    if ($("#xplor-cofpdb").val() == '' || $("#xplor-coftop").val() == ''){
        var myWidth = 320;
        var myHeight = 140;
        var option = {
            opacity:70,
            minWidth: myWidth,
            minHeight: myHeight,
            maxWidth: myWidth,
            maxHeight: myHeight
        };
        msg = '<div>There is need both pdb <b>and</b> topology files, please upload them.</div>'
        $.modal(msg, option);
        return false
    }
    return true
}

//function processPatch(data){
//    listPatch = data.split("::")
//    if (listPatch.length >= 2){
//        sel = '<select id="patchsel" name="patchsel" onchange="patchRequirements(numres, firstres, this.parentNode)"><option value="">Select item</option>'
//        numres = new Array();
//        firstres = new Array();
//        $(listPatch).each(function(i){
//            patchs = this.split(",");
//            if (patchs[0] != ''){
//                sel += '<option value="'+patchs[0]+'">'+patchs[0]+'</option>';
//                numres[patchs[0]] = patchs[1];
//                if (patchs.length > 4){
//                    firstres[patchs[0]] = patchs[2] + " " + patchs[3] + " " + patchs[4];
//                }
//                else{
//                    firstres[patchs[0]] = patchs[2] + " " + patchs[3];
//                }
//            }
//        });
//        sel +='</select>';
//        //alert(sel);
//        var myWidth = 800;
//        var myHeight = 300;
//        var option = {
//            opacity:70,
//            minWidth: myWidth,
//            minHeight: myHeight,
//            maxWidth: myWidth,
//            maxHeight: myHeight
//        };
//        msg = '<div id="patchPanel">'+
//        '<center><h2>Patching the molecular structure</h2></center>'+
//        '<p>You can select a patch to modify or link ligands to protein.</p>'+
//        '<div id="patch-item" style="padding: 10px 0 0 ;"><label for="patchsel" style="display: inline;">Choose patch </label>'+sel+'</div>'+
//        '<a onclick="addPatch();">add patch</a>'+
//        '<br />'+
//        '<br />'+
//        '<input type="button" value="Cancel" onclick="$.modal.close();"/>&nbsp;&nbsp;<input type="button" value="Apply patch(es)!" onclick="applyPatch(this.parentNode)"/>'+
//        '</div>';
//        $.modal(msg, option);
//    }
//    else{
//        var myWidth = 320;
//        var myHeight = 240;
//        var option = {
//            opacity:70,
//            minWidth: myWidth,
//            minHeight: myHeight,
//            maxWidth: myWidth,
//            maxHeight: myHeight
//        };
//        msg = '<div>'+listPatch[0]+'</div>';
//        $.modal(msg, option);
//    }
//}

function addPatch(){
    patchItemCloned = $("#patch-item").first().children("select").clone();
    $(patchItemCloned).find('option:first').attr('selected', 'selected');
    new_divItem = '<div id="patch-item" style="padding: 10px 0 0 ;"><label for="patchsel" style="display: inline;">Select patch </label></div>'
    $("#patchPanel").children("#patch-item").last().after(new_divItem);
    $("#patchPanel").children("#patch-item").last().append(patchItemCloned)
}

function patchRequirements(numreslist, resinfo, pn){
    nres = numreslist[$("#patchsel").val()];
    new_field = '<div id="req" style="display:inline"> &nbsp;&nbsp;<label style="display: inline;">1st residue (number) </label><input type="text" id="patchres1" name="patchres1" size="7"/> ';
    if (nres == '2'){
        new_field += '&nbsp;&nbsp;<label style="display: inline;">2st residue (number)</label><input type="text" id="patchres2" name="patchres2" size="4" />';
    }
    new_field += '<a onclick="removePatchItem(this.parentNode);"><img src="/global/images/rem.png" /></a></div>'
    $(pn).children("select").after(new_field);
    addChainSelector("patchres1", "patch1");
    addChainSelector("patchres2", "patch2");
    //div_note = '<div id="patch-note">* if present in your macromolecule system.</div>';
    //$("")
}

function removePatchItem(obj){
    if ($("#patchPanel").children("#patch-item").length > 1){
        $(obj).parent().remove();
    }
    else{
        $(obj).parent().children("select").find('option:first').attr('selected', 'selected');
        $(obj).remove();
    }
}

function applyPatch(n){    
    $("#patchPanel").children("#patch-item").each(function(i){
        if($(this).children("#req").length){
            patchname = $(this).children("#patchsel").val()
            patchres1 = $(this).children("#req").children("#patchres1").val()
            patchres1chain = $(this).children("#req").children("#chain-selector-patch1").val()
            patchres2 = $(this).children("#req").children("#patchres2").val()
            patchres2chain = $(this).children("#req").children("#chain-selector-patch2").val()
            hidden_patchname = '<input type="hidden" name="hpatch-name" value="'+patchname+'"/>';
            hidden_patchres1 = '<input type="hidden" name="hpatch-res1" value="'+patchres1+'"/>';
            hidden_patchres1chain = '<input type="hidden" name="hpatch-res1-chain" value="'+patchres1chain+'"/>';
            hidden_patchres2 = '<input type="hidden" name="hpatch-res2" value="'+patchres2+'"/>';
            hidden_patchres2chain = '<input type="hidden" name="hpatch-res2-chain" value="'+patchres2chain+'"/>';
            $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").append(hidden_patchname)
            $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").append(hidden_patchres1)
            $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").append(hidden_patchres1chain)
            $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").append(hidden_patchres2)
            $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").append(hidden_patchres2chain)
        }
    });
    $.modal.close();
    $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").children('a:eq(0)').html("view patches");
    $("#cofactorprop").find("#cof-item:eq("+(n-1)+")").children('a:eq(0)').attr("href", "javascript:view_patches("+(n-1)+")");
}

function view_patches(n){
    patches_htmllist = '<fieldset><legend><b>The patches of selected cofactor</b></legend>'
    $("#cofactorprop").find("#cof-item:eq("+(n)+")").children('input[name=hpatch-name]').each(function(i){
        patches_htmllist += '<b>patch name</b>: '+$(this).val()+' <b>1st residue (number)</b>: '+$("#cofactorprop").find("#cof-item:eq("+(n)+")").children('input[name=hpatch-res1]:eq('+i+')').val();
        if ($("#xplorseq-div").children().length > 1 || $("#xplorseq-div").children().find("#xplor-chainname").val() != ""){
            patches_htmllist += '&nbsp;<b>chain name</b>: '+$("#cofactorprop").find("#cof-item:eq("+(n)+")").children('input[name=hpatch-res1-chain]:eq('+i+')').val();   
        }
        patches_htmllist += '&nbsp;<b>2st residue (number)</b>: '+$("#cofactorprop").find("#cof-item:eq("+(n)+")").children('input[name=hpatch-res2]:eq('+i+')').val();
        if ($("#xplorseq-div").children().length > 1 || $("#xplorseq-div").children().find("#xplor-chainname").val() != ""){
            patches_htmllist += '&nbsp;<b>chain name</b>: '+$("#cofactorprop").find("#cof-item:eq("+(n)+")").children('input[name=hpatch-res2-chain]:eq('+i+')').val();
        }
        patches_htmllist +='<br />';

    });
    var myWidth = 700;
    var myHeight = 200;
    var option = {
        opacity:70,
        minWidth: myWidth,
        minHeight: myHeight,
        maxWidth: myWidth,
        maxHeight: myHeight
    };
    msg = '<div>'+patches_htmllist+'</div>';
    $.modal(msg, option);
}

function closePatchPanel(){
    $.modal.close()
}

function removeCof(obj){
    $(obj).remove();
}

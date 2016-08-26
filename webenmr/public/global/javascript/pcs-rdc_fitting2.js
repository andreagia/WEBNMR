$(document).ready(function() {
                
                
                $("#header").children("div").first().html("AnisoFIT");
                $("#header").children("div").first().next().html("");
                $("#header").children("div").first().next().css("padding-top", '20px');
                $("#navbar").find("li").removeAttr("class");
                $("#navbar").find("li").eq(11).attr("class", "current");
                $("#path").find("li").eq(1).remove();
                $("#path").children("ul").append('<li><a href="/access/index?type=anisofit">AnisoFIT</a></li>')
                $('#tabs').tabs({ disabled: [1,2,3] });

               //aggiungo metodo unique() ad Array()
               //nomearray.unique() restituisce un array senza ripezioni
                Array.prototype.unique = function(){
                    var vals = this;
                    var uniques = [];
                    for(var i=vals.length;i--;){
                        var val = vals[i];  
                        if($.inArray( val, uniques )=== -1){
                            uniques.unshift(val);
                        }
                    }
                    return uniques;
                }

               var optionsConstraint = { 
                    //target:        '#output1',   // target element(s) to be updated with server response 
                    //beforeSubmit:   validatorRequest,  // pre-submit callback
                    dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                    success:  processConstraintSubmit   // post-submit callback 
                }; 
               
                // bind form using 'ajaxForm' 
                $('#constraint').ajaxForm(optionsConstraint);
               
               
               var validatorStructure = $("#structure").validate({ 
                    rules: { 
                        protein_file_1: {
                            required: true,
                            accept: "pdb"
                        },
                        ligand_file_1: {
                            //required: "required",
                            accept: "pdb"
                        },
                        top_file_1: {
                            //required: "required",
                            accept: "lib|in"
                        },
                        force_fields: {
                            required: true
                        }
                    },
                    errorPlacement: function(error, element) {
                        element.after(error);
                    },
                    invalidHandler: function(form, validator) {
                        var errors = validator.numberOfInvalids();
                        if (errors) {
                          var message = errors == 1
                            ? 'You missed 1 field. It has been marked'
                            : 'You missed ' + errors + ' fields. They have been marked';
                          $("div.error span").html(message);
                          $("div.error").show();
                        } else {
                          $("div.error").hide();
                        }
                    },
                    submitHandler: function() {
                        //$("div.error").hide();
                        var options = { 
                            //target:        '#output1',   // target element(s) to be updated with server response 
                            //beforeSubmit:   validatorRequest,  // pre-submit callback
                            dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                            success:  processStructureSubmit   // post-submit callback 
                        }; 
    
                        // bind form using 'ajaxForm' 
                        $('#structure').ajaxForm(options); 
                    }
                });
            
            
                $("#structure").validationEngine();
                $("#submitCalculation").validationEngine()
                
                $('#constraint')[0].reset();
                
                $('#structure')[0].reset();
               
                //initSander();
               
                var optionsSander = { 
                    //target:        '#output1',   // target element(s) to be updated with server response 
                    //beforeSubmit:   validatorRequest,  // pre-submit callback
                    dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                    success:  processSanderSubmit   // post-submit callback 
                }; 
               
                // bind form using 'ajaxForm' 
                $('#submitSander').ajaxForm(optionsSander);
               
              //var optionsJobs = {
                //    action: "jobs/job_prepare",
                    //target:        '#output1',   // target element(s) to be updated with server response 
                //    beforeSubmit:   addInfoProtocol,  // pre-submit callback
                //    dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                    //success:  processSanderSubmit   // post-submit callback 
                //}; 
               
                // bind form using 'ajaxForm' 
                //$('#submitCalculation').ajaxForm(optionsJobs);
                
               
               $("#subCalc").button();
               $("#subCalc").click(function(){
                    $.ajax({
                        type: "POST",
                        url: "/jobs/job_prepare",
                        dataType: "xml",
                        data: "calc_name="+$("#submitOpt").children("input[name=calcname]").attr("value")+"&prj_id="+"${c.prj_id}"+"&tipology="+"${c.tipology}"+"&numStep="+$("#submitOpt").children("input[name=step]").attr("value")
                    });
               });
               
               $("#availability").button();
               $("#availability").click(function(){
                    checkAvailability($("#calc_name").attr("id"), $("input[name=prj_id]").attr("value"), $("#calc_name").attr("value"));
               });
	       
               $("#calc_name").keyup(function(){
                                if(!$("#availability").length){
                                    $("#calc_name").next().remove();
                                    $("#calc_name").after('<button type="button" id="availability">check availability</button>');
                                                $("#availability").button();
                                                $("#availability").click(function(){
                                                     checkAvailability($("#calc_name").attr("id"), $("input[name=prj_id]").attr("value"), $("#calc_name").attr("value"));
                                                });
                                    $("#submit_calc").attr("disabled", "disabled");
                                }
                    //$("#subCalc").attr("disabled","disabled");
                    //var ava = $("#submitOpt").children("button");
                    //if (ava.length == 1){
                    //    $("#submitOpt").children("span").remove();
                    //    
                    //}
               });
               
               //$("#calc_name").focus(function(){
               //     if($(this).attr("value") == "Type a directory name"){
               //        $(this).attr("value", ""); 
               //     }
               //});
               
               
               
              
               
               
               
		});
		

            function remove_item(obj_id){
                var type = $("#"+obj_id).parent().parent().parent().attr("id").split('-')[0];
                if (type != "bond"){
                    $("#"+type).children("a").removeAttr("style");
                    $("#"+type).children("a").attr("href", "javascript:add_"+type+"();");
                }
                $("#"+obj_id).parent().remove();
            }
    
    
            function check_noparcent(){
                if ($("#noparcent").is(':checked')){
                        $("#rdc_tensor_fit").children().children("#rdc_atmname").attr("disabled", "disabled");
                        $("#rdc_tensor_fit").children().children("#rdc_rsdname").attr("disabled", "disabled");
                        $("#rdc_tensor_fit").children().children("#rdc_rsdnum").attr("disabled", "disabled");
                }
                else{
                        $("#rdc_tensor_fit").children().children("#rdc_atmname").removeAttr("disabled");
                        $("#rdc_tensor_fit").children().children("#rdc_rsdname").removeAttr("disabled");
                        $("#rdc_tensor_fit").children().children("#rdc_rsdnum").removeAttr("disabled");         
                }
            }
            
            function addInfoProtocol(){
                var nrStep = $("#protocol").children("div").length;
                $("#submitCalculation").children("#submitOpt").children("input[name=step]").remove();
                $("#submitCalculation").children("#submitOpt").append('<input type="hidden" value="'+nrStep+'" name="step">');
            }

            
            function processSanderSubmit(response){
                //alert("submit sander OK");
            }
 
            var PROTEIN = 'protein';
            var LIGAND = 'ligand';
            var IMG_PATH = "/global/images/";
            var IMG_PLUS = 'plus.gif';
            var IMG_MINUS = 'minus.gif';
            
            var INPUTFILE_TEMPLATE = '<div id="PREFIX_div_ID"><li>';
            INPUTFILE_TEMPLATE += '<label id="PREFIX_label_ID" for="PREFIX_file_ID">Chain .pdb file: </label>';
            INPUTFILE_TEMPLATE += '<input type="file" class="required" name="PREFIX_file" id="PREFIX_file_ID" onChange="add_plus(this.id);checkUploaded(this.id);remove_warror(this.id)">';
            INPUTFILE_TEMPLATE += '</li></div>';
            var PATH_PLUS = IMG_PATH+IMG_PLUS;
            var PATH_MINUS = IMG_PATH+IMG_MINUS;
            var IMGPLUS_TEMPLATE = '<img src="'+PATH_PLUS+'" id="PREFIX_plus_ID" onClick="add_fileField(this.id)">';
            var IMGMINUS_TEMPLATE = '<img src="'+PATH_MINUS+'" id="PREFIX_minus_ID" onClick="remove(this.id)">';
            
            var ligands = new Array();
            ligands["ligand"] = new Array();
            ligands["top"] = new Array();
            ligands["ligand"][1] = 0;
            ligands["top"][1] = 0;

            function remove_aminoEntry(id){
                //residuo_residue_nomefile

                var inputfile = id.split('_')[1];
                
                
                
                $("#amino-item").children("div[id*="+inputfile+"]").each(function(){
                    var residue = $(this).attr("id").split('_')[0];
                    $('option[value*="'+residue+'"]').remove();
                    $(this).remove();
                });
                
                $("#samino").children().each(function(){
                    if($(this).attr("value").indexOf(inputfile) != -1){
                        $(this).remove();
                        
                    }
                    
                });
                
                if($("#samino").children().length == 0){
                    $("fieldset#amino").remove();
                }
            }
            
 
            function uploadMultiJobs(id, form){
                var filename = $("input[id="+id+"]").attr("value");
                
                    
                var options = {
                        url: "/structureUpload/uploadMultiJobs",
                        dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                        success:  function(response, status){
                            $('#'+id+'_div').html($('#'+id+'_div').html());
                            $("input[id="+id+"]").attr("value", "");
                            var elem = '<a id="'+id+'_a" href="javascript:removeUploadedFile(\''+id+'_a\', \'multijobs.tgz\');"><img src="/global/images/cancel.png" border="0"/></a>'+
                            '<span name="multijob_name"> '+filename+' </span>';
                            $("#multi-item").append(elem);
                        }
                    };
                    $("#"+form).ajaxSubmit(options);    
                
            }
            
            
            function uploadFile(id, form){
                var prefix = id.split('_')[0];
                var id_dest = prefix+"-item";
                var filename = $("input[id="+id+"]").attr("value");
                filename_list = filename.split('\\');
                if (filename_list.length){
                    filename = filename_list[filename_list.length - 1];
                }
                var valid = 1;
                var notfound = 1
                var cntItem = $("#"+prefix+"-item").children("div[id="+prefix+"_"+filename.split('.')[0]+"]");
                if(cntItem.length){
                    notfound = 0;
                }
                if(filename.split('.')[1] != 'pdb'){
                        $.validationEngine.buildPrompt("input[id=chain_file]","upload only .pdb files","error");
                         $('#chain_file_div').html($('#chain_file_div').html());
                        valid = 0;
                }
                else{
                    $.validationEngine.closePrompt("input[name=chain_file]");
                }
                if(notfound && valid){
                    
                    var tagFilename = '<div id="'+prefix+'_'+filename.split('.')[0]+'"><a id="'+prefix+'_a_'+filename.split('.')[0]+'" href="javascript:removeUploadedFile(\''+prefix+'_a_'+filename.split('.')[0]+'\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a>'+
                    '<span name="protein_name"> '+filename+' </span></div>';
                    
                    //inserire la voce nel div chain-item
                    $("#"+id_dest).append(tagFilename);
                    $("#advanced-setting").removeAttr("style");
                    //runEffect();
                   
                    
                    //ajax per l'upload vero e proprio
                    $("#field").attr("value", id);
                    var hdd = '<input type="hidden" value="'+filename+'" name="protein_name">';
                    $("#submit").append(hdd);
                    var options = {
                        url: "/structureUpload/upload",
                        dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                        success:  function(response, status){
                            $('#chain_file_div').html($('#chain_file_div').html());

                            //$('input[id='+id+']').attr("value", "");
                            
                           
                            processUploadedFile(id, response);
                            enableTabs();
                            //$.validationEngine.closePrompt("select[id=force_fields]");
                        }
                    };
                    $("#"+form).ajaxSubmit(options);
                    
                    //$("#"+id).attr("value", "");
                }
                else if(!notfound){
                    $("input[id="+id+"]").attr("value", "");
                    open_dialog("WARNING","You are already uploaded a file with same namefile or use same namefile in different subtree directory filesystem", 570, 150)
                    //piccola dialog che avvisa che file già inserito
                }

            }
            
            function removeUploadedFile(id, filename){
                $.ajax({
                    url: "/structureUpload/removeUploadedFile",
                    data: "file_name="+filename
                });
                //if(id.split('_')[0] == "chain"){
                //    //rimuovo eventuali aminoacidi non standard
                //    remove_aminoEntry($("#"+id).parent().attr("id"));
                //    if(!$("#chain_item").children().length){
                //        $("#advanced-setting").attr("style", "display: none;");
                //    }
                //    enableTabs();
                //}
                var ty = id.split('_')[1];
                if(ty == "ligand"){
                    $("#"+id).parent().parent().remove();
                    enableTabs();
                }
                else if((ty == "rdc") || (ty == "pcs")){
                    $("#"+ty+"_tensor_fit").remove();
                    $("#"+ty+"_tensor_calc").remove();
                    $("a[id="+id+"]").parent().remove();
                    if($("#"+ty+"_selectable").children().length == 0){
                        $("label[id="+ty+"_title]").remove();
                    }
                }
                else if(id.split('_')[0] == 'multijob'){
                    $("a[id="+id+"]").parent().empty();
                }
                else if((ty == "top") || (ty == "par")){
                    if(!$("a[id="+id+"]").parent().siblings("div").length){
                        $("a[id="+id+"]").parent().parent().remove();
                    }
                    else{
                        $("a[id="+id+"]").parent().remove();    
                    }
                    enableTabs();
                }
                else{
                    $("a[id="+id+"]").parent().remove();
                    enableTabs();
                }
                
                $("#submit").children("input[value="+filename+"]").remove();
                $("#submitConstr").children("input[value="+filename+"]").remove();
            }

            
            function checkUploaded(id){
                var value_id = $("#"+id).attr("value");
                
                var allInput = $("input[id^=protein_file_]");
                var exist = -1;
                allInput.each(function(){
                    if ($(this).attr("value") == value_id){
                        exist += 1;
                    }
                });
                
                //$("#"+id).nextUntil("#message").last().next().remove();
                if (!exist){
                    $("#"+id).parent().children("#message").remove();
                    //add_checkButton(id, "away", "structure", "check entry", "checkSubmit(this.name)");
                }
                else{
                    remove_checkButton(id);
                    $("#"+id).parent().children("#message").remove();
                    $("#"+id).nextUntil("div").last().after('<em id="message">&nbsp;'+$("#"+id).attr("value")+' already uploaded or it is uploading!</em>');
                    $("#"+id).parent().children("img[id^="+id.split('_')[0]+"_plus_"+id.split('_')[2]+"]").remove();
                }
            }
            
            
            function validatorRequest(formData, jqForm, options) { 
                // formData is an array; here we use $.param to convert it to a string to display it 
                // but the form plugin does this for you automatically when it submits the data 
                //var queryString = $.param(formData);
                return $("#structure").validate().form();
            } 
            
            
            function processUploadedFile(id, response){
                
                
                //var warnings = $('<warning>', response);
                //var errors = $('<error>', response);
                //var fatals = $('<fatal>', response);
                //if (fatals.length || errors.length || warnings.length){
                //    showMessage('Your .pdb file is bad formatted and/or contains not recognized residues.', 550, 60, 'attention_01');
                //}
                response = $(response).xml();
                var file_list = $('file', response);
                
                
                if(file_list.length){
                    
                    info_pdb = $('Info_PDB', response);
                    info_pdb_num = parseInt($.trim(info_pdb.text().split(":")[1]));
                    if (info_pdb_num > 1){
                        use_multijob(info_pdb_num);
                    }
                    submit('structure');
                }
            }
            
	    function use_multijob(n){
		var myWidth = 400;
		var myHeight = 120;
		var option = {
		    escClose: false,
		    opacity:70,
		    minWidth: myWidth,
		    minHeight: myHeight,
		    maxWidth: myWidth,
		    maxHeight: myHeight
		};
		var txt = "Your .pdb is a bundle of "+ n + " conformers, but only the first conformer will be used."
		$("#mstruct").children("h4").empty()
		$("#mstruct").children("h4").append(txt);
		$("#mstructyes").button();
		$("#mstructyes").click(function(){
		    //$("input[name=multij]").attr("value", "on");
		    $.modal.close();
		});
		//$("#mstructno").button();
		//$("#mstructno").click(function(){
		//    $("input[name=multij]").attr("value", "off");
		//    $.modal.close();
		//});
		
		$("#mstruct").modal(option)
	    }
            
            function showMessage(txt, w, h, icon){
                var myWidth = w;
                var myHeight = h;
                var option = {
                    escClose: true,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                var msg = '<img src="/global/images/'+icon+'.png" /> '+txt;
                $.modal(msg, option);
            }
            //function processCheckedFile(response, statusText){
            //    response = $(response).xml();
            //    var file_list = $('file', response);
            //    
            //    alert(response)
            //    if(file_list){
            //        var mess = "";
            //        var file_bname = $(file_list).attr("BaseName");
            //        //alert(file_bname)
            //        var file_id = $("input[value="+file_bname+"]").attr("id");
            //        //alert(file_id)
            //        var prefix = file_id.split('_')[0];
            //        var id_nr = file_id.split('_')[2];
            //        var loc = "";
            //        if(file_id.split('_')[0] == "protein"){
            //            loc = "away";
            //        }
            //        else{
            //            loc = "near"
            //        }
            //        
            //        
            //        warnings = $('warning_pdb', response);
            //        warn_res = $('warning_res', response);
            //        if((warnings.length) || (warn_res.length)){
            //            var warning_message = "<ol>";
            //            warnings.each(function(){
            //                var war = $(this).text();
            //                warning_message += "<li>"+war+"</li>";
            //            });
            //           
            //            var listWarn = new Array();
            //            warn_res.each(function(i){
            //                var res = $(this).text();
            //                listWarn[i] = res;
            //            });
            //            var listWarnUnique = listWarn.unique();
            //            for (var i=0; listWarnUnique[i]; i++){
            //                var war = listWarnUnique[i];
            //                warning_message += "<li>"+war+"</li>";
            //            }
            //            warning_message += "</ol>"
            //            var title = 'Warning messages of *'+file_bname+'* file';
            //            var file_checked = file_bname.split('.')[0]+"_c.pdb";
            //            add_warning(file_id, title , warning_message, loc);
            //            mess += "Warning messages:<br/> " + warning_message;
            //            
            //            //warn_res = $('warning_res', response);
            //            if(warn_res.length){
            //                var listAmino = new Array();
            //                warn_res.each(function(i){
            //                    var res = $(this).attr("residue");
            //                    listAmino[i] = res;
            //                });
            //                create_aminoEntry(listAmino);
            //                
            //            }
            //            
            //            //abilito submit
            //            enableSubmit();
            //        }
            //    
            //        errors = $('error_pdb', response);
            //        if(errors.length){
            //            var error_message = "<ol>";
            //            errors.each(function(){
            //                var err = $(this).text();
            //                error_message += "<li>"+err+"</li>";
            //            });
            //            error_message += "</ol>"
            //            add_error(file_id, "errors" , error_message, loc);
            //            mess += "Error messages:<br/> " + error_message;
            //        }
            //    }
            //    else{
            //        add_ok(file_id, loc);
            //    }
            //     
            //    open_dialog("IMPORTANT MESSAGE","There are some non-standard residues, you must provide their topologies and parameters", 570, 200)
            //    
            //    var down = '<a href="/structureUpload/download?requested_filename='+file_checked+'"><img src="'+IMG_PATH+'download.png" border="0" title="Download converted file"></a>';
            //    $("#"+file_id).nextUntil("div").last().after(down);
            //    
            //    
            //    remove_checkButton(file_id);
            //    $("#submit_check").attr("value", "");
            //    //var path_dir = '${c.dir}'.split('/')[7]
            //    //var path_dir = '${c.dir}';
            //    //alert(path_dir)
            //    var file = file_bname.split('.')[0]+"_c.pdb";
            //    
            //    
            //    var img_jmol = '<a id="'+prefix+'_'+id_nr+'_a_eye" href="javascript:open_jmolView(\''+file_id+'\');"><img id="'+prefix+'_eye_'+id_nr+'" src="'+IMG_PATH+'jmol.gif" border="0" title="View chemical structure of protein"></a>';
            //    if(loc == "away"){
            //        $("#"+file_id).nextUntil("div").last().after(img_jmol);
            //    }
            //    else{
            //        $("#"+file_id).after(img_jmol);
            //    }
            //}

            function processStructureSubmit(response, statusText){
                //var prot = $('protein', response);
                //var attr = prot.attr("filename");
                //response = $(response).xml();
                //alert(response);
                
                
                //$("#submit_structure").attr("disabled", "disabled");
                
                
                var warnings = $('warning', response);
                var errors = $('error', response);
                var fatals = $('fatal', response);
                alert(warnings.length)
                if (fatals.length || errors.length || warnings.length){
                    showMessage('Your .pdb file is bad formatted and/or contains not recognized residues.', 350, 80, 'no');
                }
                
                if(!fatals.length){
                    var leap = $('leap', response);
                    var chains = $('chain', leap);
                
                    if(chains.length){
                        $("#chain-row").empty();
                        
                        chains.each(function(i){
                            //if((i+1) % 4 == 1){
                               
                               
                                //$("#chain_summary_fieldset").append(tag);
                                var chain_n = $(this).attr("chain_n");
                                var chain_range = $(this).attr("chain_range");
                                var tag =   '<div  class="cell">'+
                                                '<span>Chain </span><span id="lchain_n">'+chain_n+' </span>'+
                                                '<span>(range </span><span id="lchain_range">'+chain_range+')</span>'+
                                            '</div>';
                                $("#chain-row").append(tag);
                            //}
                            //else{
                                //var chain_n = $(this).attr("chain_n");
                                //var chain_range = $(this).attr("chain_range");
                                //var tag =  '<div  class="cell"><label>Chain </label><label id="lchain_n">'+chain_n+'</label>&nbsp;'+
                                //    '<label>range </label><label id="lchain_range">'+chain_range+'</label>&nbsp;'+
                                //    '</div>';
                                //$("#chain-row:last").append(tag);
                            //}
                        });
                    }
                    $('#tabs').tabs("disable", 0 );
                    $('#tabs').tabs("disable", 3 );
                }
                else{
                    $("#tabs").tabs("enable", 0);
                    $("#tabs").tabs( "option", "selected", 0 );
                    $('#tabs').tabs("disable", 1 );
                    $('#tabs').tabs("disable", 2 );
                    $('#tabs').tabs("disable", 3 );
                    
                    if(fatals.length){
                        $("div.jGrowl-notification").trigger("jGrowl.close");
                        $.jGrowl("Amber fatal error. See <em>Amber fatal error</em> to more informations ", {header: 'ERRORS', life: 8000, theme: 'iphone'});
                    }
                    //aggiungere visualizzazione degli errori
                    var txt = '';
                    fatals.each(function(){
                        var txt_list = $(this).text().split('\n')
                        $(txt_list).each(function(i){
                            txt_list[i] = this.replace(/</g, '(');
                            txt_list[i] = txt_list[i].replace(/>/g, ')');
                        });
                        txt += txt_list.join("<br> ");
                        //$.jGrowl($(this).text(), {header: 'ERRORS', life: 8000, theme: 'iphone'});
                    });
                    //txt += $(fatals).xml();
                    //txt = txt.replace(/&lt;/g, '(');
                    //txt = txt.replace(/&gt;/g, ')');
                    //alert(txt)
                    var linkmsg = '<a href="javascript:open_dialog(\'Amber fatal error\', \''+txt+'\', 400, 500);">Amber fatal error</a>';
                    $("#chain-item").children().last().append(linkmsg);  
                }
                
            }
            
            
            function open_jmolView(id, name){
                //alert(id)
                var suffix = id.split('chain_')[1];
                //alert(suffix)
                
                if(name == ""){
                    var file_name = suffix+"_c.pdb";
                }
                else{
                    var file_name = name;
                }
                
                //var xhr = XMLHttpRequest();
                
                $.ajax({
                    url: "/structureUpload/jmol_file",
                    data: "file_name="+file_name,
                    success: function(data){
                        
                        data = data.replace(/\n/g, "|");
                        
                        var obj = '<object name="jmolApplet0" id="jmolApplet0" classid="java:JmolApplet" type="application/x-java-applet" height="500" width="500">'+
                                        '<param name="syncId" value="216291259819275">'+
                                        '<param name="progressbar" value="true">'+
                                        '<param name="progresscolor" value="blue">'+
                                        '<param name="boxbgcolor" value="black">'+
                                        '<param name="boxfgcolor" value="white">'+
                                        '<param name="boxmessage" value="Downloading JmolApplet ...">'+
                                        '<param name="name" value="jmolApplet0">'+
                                        '<param name="archive" value="JmolApplet0.jar">'+
                                        '<param name="mayscript" value="true">'+
                                        '<param name="codebase" value="/global/jmol">'+
                                        '<param name="loadInline" value="'+data+'">';
                                        if (name == ''){
                                            obj += '<param name="script" value="select *">';
                                        }
                                        else{
                                            obj += '<param name="script" value="select atomname=MEX, atomname=AX; connect single;'+
                                            'select atomname=MEX, atomname=AY; connect single;'+
                                            'select atomname=MEX, atomname=AZ; connect single;'+
                                            'select atomname=MEX or atomname=AX or atomname=AY or atomname=AZ;'+
                                            'label %a; select protein; cartoons; color structure;'+
                                            'select protein; spacefill off; wireframe off;">';
                                        }
                                        
                                        obj += '<p style="background-color: yellow; color: black; width: 400px; height: 400px; text-align: center; vertical-align: middle;">'+
                                            'You do not have Java applets enabled in your web browser, or your browser is blocking this applet.<br>'+
                                            'Check the warning message from your browser and/or enable Java applets in<br>'+
                                            'your web browser preferences, or install the Java Runtime Environment from <a href="http://www.java.com">www.java.com</a><br></p>'+
                                            '</object>';
                                    
                         var vdialog = $('<div></div>');
                            vdialog.html(obj);
                            vdialog.dialog({
                                autoOpen: false,
                                title: "Jmol Chemical structure of "+file_name,
                                width: 540,
                                height: 570,
                                modal: true
                            });
                            
                            vdialog.dialog('open');
                            //if(name != ""){
                                //var script= 'select atomname=MEX, atomname=AX; connect single; select atomname=MEX, atomname=AY; connect single; select atomname=MEX, atomname=AZ; connect single; select atomname=MEX or atomname=AX or atomname=AY or atomname=AZ; label %a';
                                //jmolScript(script);
                            //}
                    }
                });

            }
            
            
            function create_aminoEntry(listAmino, filename){
                var listAminoUnique = listAmino.unique();
                //se già ci sono degli aminoacidi non standard
                if($("#aminoUpload").length == 0){
                    var amino_tag = '<fieldset id="amino" class="ui-widget-content ui-corner-all">'+
                                    '<legend>Non-standard residues</legend>'+
                                    '<div id="aminoUpload">'+
                                        '<div id="amino_select">'+
                                            '<ol>'+
                                            '<li>'+
                                            'Select residue: &nbsp;'+
                                            '<select id="samino">'+
                                            '</select>'+
                                            '</li>'+
                                            '<br />'+
                                            '<li>'+
                                            'specify it topology and/or parameters:<br />'+
                                            '<label id="top" for="top_amino">topology file</label>'+
                                            '<div id="top_amino_div">'+
                                            '<input type="file" id="top_amino" class="required" name="top_amino_file" onchange="add_toppar(\'samino\', this.id, \'structure\', \''+filename+'\')">'+
                                            '</div>'+
                                            '<label id="par" for="par_amino">parameters file</label>'+
                                            '<div id="par_amino_div">'+
                                            '<input type="file" id="par_amino" name="par_amino_file" onchange="add_toppar(\'samino\', this.id, \'structure\', \''+filename+'\')"><br />'+
                                            '</div>'+
                                            '</li>'+
                                            '</ol>'+
                                        '</div>'+
                                        '<div id="amino-item">'+
                                        '</div>'+
                                    '</div>'+
                                    '</fieldset>';
                    $("#column2").append(amino_tag);
                    runEffect();
                    $.jGrowl("You have to upload some others files for non-standard residues", {header: 'IMPORTANT', life: 8000, theme: 'iphone'});
                    //enableTabs();
                    //$.validationEngine.closePrompt("input[id=top_amino]");
                    //$.validationEngine.closePrompt("input[name=chain_file]");
                    //$.validationEngine.closePrompt("select[id=force_fields]");
                }
                
                $.each(listAminoUnique, function(i, value){
                    //$("#samino").addOption(value, value);
                    $('<option value="'+value+'_'+filename.split('.')[0]+'">'+value+'</option>').appendTo('#samino');
                });
            }
            
            
            function add_constraintEntry(inputID, form){
                var type = inputID.split('_')[0];
                var field = inputID.split('_')[1];
                
                var cntEntry = $("#"+type+"-item").children().length;
                if((field != "cyanaXplor") && (field != "fit")){
                    var value = $("#"+inputID).attr("value");
                    var value_list = value.split('\\');
                    //alert(value_list.length)
                    if(value_list.length){
                        value = value_list[value_list.length - 1];
                    }
                }
                else{
                    var value = $("#"+inputID).val();
                }
                
                
                if (field == "file"){
                    
                    var start = $("#"+type+"_number").attr("value");
                    var tp = $("#"+type+"_cyanaXplor").val();
                    
                    var notfound = 1
                    var cntItem = $("#"+type+"-item").children("div[id^="+value+"]");
                    var cntItem2 = $("#"+type+"-item").children("div");
                    cntItem2.each(function(){
                        var txt = $(this).children("span").text();
                        //alert(txt)
                        //alert(value)
                        if(txt == value){
                            notfound = 0;
                        }
                    });
                    
                    
                    if (notfound){
                        var fit = '';
                        if((type == "rdc") || (type == "pcs")){
                            var title = '<label id="'+type+'_title">Select a '+type+' item to fit or calculate a tensor:</label>';
                            if($("#"+type+'-item').children("#"+type+"_title").length == 0){
                                $("#"+type+'-item').prepend(title);
                            }
                            //$("#"+type+'-item').append(title);
                            fit = $("#"+type+"_fit").val();
                            var hdd4 = '<input type="hidden" id="'+type+'_fit" value="'+fit+'" name="'+type+'_fit_t">';
                            $("#submitConstr").append(hdd4);
                            $.jGrowl("You have to fit rdc and/or pcs. Select uploaded rdc or pcs to fit.", {header: 'IMPORTANT', life: 8000, theme: 'iphone'});
                        }
                        var no_corr = '';
                        if(type == 'noe'){
                           no_corr = $("#"+type+"_checkbox:checked").val();
                            if (no_corr != 'True'){
                                no_corr = 'False'
                            }
                            var hdd5 = '<input type="hidden" id="'+type+'_noe_corr" value="'+no_corr+'" name="'+type+'_noe_corr_r">';
                            $("#submitConstr").append(hdd5);
                        }
                        //var title_item="<label>Select rdc item to fit or calculate tensor: </label>";
                        //$("#rdc-item").append(title_item)
                        
                        var tag = '<div id="'+value+'_file">'+
                                    '<a id="a_'+type+'_'+value+'" href="javascript:removeUploadedFile(\'a_'+type+'_'+value+'\', \''+value+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                       '<span>['+start+'] ('+tp+') '+no_corr+' '+value+'</span>'+
                                       '&nbsp;&nbsp;&nbsp;<b>click <a onclick="javascript:toFit(\''+type+'\', this)">here</a> to fit</b>'+
                                  '</div>';
                        if (cntItem.length){
                            $("#submitConstr").children("input[id^="+type+"]").remove();
                            //$("input[type='hidden' id^='"+type+"']").remove();
                            //$("input[type='hidden' id="+type+'_cyanaXplor'+"]").remove();
                            //$("input[type='hidden' id="+type+'_number'+"]").remove();
                            //$("input[type='hidden' id="+type+'_fit'+"]").remove();
                            cntItem.replaceWith(tag);
                            
                        }
                        else{
                            if((type == 'rdc') || (type == "pcs")){
                                $("#"+type+"-item").children("#selectable").append('<img src="/global/images/loading.gif">');
                                //$("#"+type+"-item").children("#selectable").append(tag);    
                            }
                            else{
                                $("#"+type+"-item").append('<img src="/global/images/loading.gif">');
                                //$("#"+type+"-item").append(tag);
                            }
                        }
                        //$("#selectable").selectable();
                        //$("#"+type+"-item").children("#selectable").selectable({ filter: 'span' });
                        //$("#"+type+"-item").children("#selectable").selectable( { cancel: 'img, a'} );
                        //$("#"+type+"-item").children("#selectable").selectable( { selected: function(event, ui) {
                        //        
                        //}} );
                        //$("#"+type+"-item").children("#selectable").selectable({
                        //    unselected: function(event, ui) {
                        //            $("#"+type+"_tensor_fit").remove();
                        //            $("#"+type+"_tensor_calc").remove();
                        //        }
                        //}); 
  
                        
                        
                        
                        var hdd1 = '<input type="hidden" id="'+type+'_'+field+'_f" value="'+value+'" name="'+type+'_'+field+'_f">';
                        $("#submitConstr").append(hdd1);
                        var hdd2 = '<input type="hidden" id="'+type+'_number" value="'+start+'" name="'+type+'_number_n">';
                        $("#submitConstr").append(hdd2);
                        var hdd3 = '<input type="hidden" id="'+type+'_cyanaXplor" value="'+tp+'" name="'+type+'_cyanaXplor_c">';
                        $("#submitConstr").append(hdd3);
                        
                        
                    
                        $("#submitConstr").children("#field").attr("value", type);
                        if(type=='rdc'){
                            var len_rdcs = $("#"+type+"-item").children("#selectable").children().length;
                            if(len_rdcs > 3){
                                open_dialog("ATTENTION", "You have already reached "+type+" uploads limit!", 350, 150);
                                $("#"+type+"_number").attr("value", "");
                                $("#"+type+"_file").attr("value", "");
                                $("#"+type+"_file").attr("disabled", "disabled");
                                $("#"+type+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                                $("#"+type+"-item").children("#selectable").children('img').remove();
                                return
                            }
                        }
                        else{
                            var len_pcss = $("#"+type+"-item").children("#selectable").children().length;
                            if(len_pcss > 1){
                                open_dialog("ATTENTION", "You have already reached "+type+" uploads limit!", 350, 150);
                                $("#"+type+"_number").attr("value", "");
                                $("#"+type+"_file").attr("value", "");
                                $("#"+type+"_file").attr("disabled", "disabled");
                                $("#"+type+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                                $("#"+type+"-item").children("#selectable").children('img').remove();
                                return
                            }
                        }
                        var options = {
                            url: "/structureUpload/check_constraint",
                            dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type)
                            success:  function(response, status){
                                $("#"+type+"_number").attr("value", "");
                                $("#"+type+"_file_div").html($("#"+type+"_file_div").html());
                                $("#"+type+"_file").attr("disabled", "disabled");
                                $("#"+type+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                                //$("#"+type+"_fit option[value='null']").attr('selected', 'selected');
                                $("#"+type+"_checkbox").removeAttr("checked");
                                if((type == 'rdc') || (type == "pcs")){
                                    $("#"+type+"-item").children("#selectable").children('img').remove();;
                                    $("#"+type+"-item").children("#selectable").append(tag);    
                                }
                                else{
                                    $("#"+type+"-item").children('img').remove();
                                    $("#"+type+"-item").append(tag);
                                }
                                $.validationEngine.closePrompt('#sander-out');
                            }
                        };
                        $("#"+form).ajaxSubmit(options); 
                        
                    }
                    else{
                        $("#"+type+"_number").attr("value", "");
                        $("#"+type+"_file").attr("value", "");
                        $("#"+type+"_file").attr("disabled", "disabled");
                        $("#"+type+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                        $("#"+type+"_fit option[value='null']").attr('selected', 'selected');
                        $("#"+type+"_checkbox").removeAttr("checked");
                        open_dialog('WARNING', 'File already uploaded', 200, 100)
                    }
                    //$("#"+form).ajaxSubmit();
                }
                else{
                    if(($("#"+type+"_number").attr("value") != "") && ($("#"+type+"_cyanaXplor").val() != "null")){
                        if((type == "rdc") || (type == "pcs")){
                            if($("#"+type+"_fit").val() != "null"){
                                $("#"+type+"_file").removeAttr("disabled");
                                
                            }
                        }
                        else{
                            $("#"+type+"_file").removeAttr("disabled");
                            $('a[href="#tabs-2"]').click(function(){
                               
                            });
                        }
                    
                    }
                    else{
                        $("#"+type+"_file").attr("disabled", "disabled");    
                    }
                }
            }
                
            function startLoading(){
                var myWidth = 320;
                var myHeight = 240;
                var option = {
                    escClose: false,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                var img = '<img src="/global/images/loading2.gif" />';
                $.modal(img, option);
            }
            
            function stopLoading(){
                $.modal.close();
            }
            
            function toFit(type, obj){
                var myWidth = 400;
                var myHeight = 300;
                var option = {
                    escClose: false,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                
                var result = $("#"+type+"_tensor").empty();
                var metals = '<select id="'+type+'_metal"><option value="null"></option>';
                if(type == 'rdc'){
                    type2 = 'pcs';
                }
                else{
                    type2 = 'rdc';
                }
                var tns_fit = '<div id="'+type+'_tensor_fit"><fieldset><legend>Fitting</legend>'+
                                '<label class="ltensor" id="'+type+'_lmetal">Select metal:</label><br />'+
                                '<label class="ltensor">Temperature</label><input id="temperature" type="text" size=10 value=298 />';
                                    //if (type == 'rdc'){
                                tns_fit +=  '&nbsp;&nbsp;<label class="ltensor">B (Mhz)</label><input id="b" type="text" size=10 value=700 />';
                                    //}
                                tns_fit += '&nbsp;&nbsp;<label class="ltensor">Tolerance</label><input id="tolerance" type="text" size=10 value="" />'+
                                            '&nbsp;&nbsp;<button type="button" id="'+type+'_bfit">Fit</button><br />'+
                                    
                              '</fieldset></div>';
                result.append(tns_fit);
                var met = '<label class="ltensor">atom name</label> <input type="text" size="5" id="'+type+'_atmname"/>&nbsp;&nbsp; <label class="ltensor">residue name</label> <input type="text" size="5" id="'+type+'_rsdname"/>&nbsp;&nbsp; <label class="ltensor">residue number</label> <input type="text" size="5" id="'+type+'_rsdnum"/>&nbsp;&nbsp; ';
                $(met).insertAfter("#"+type+"_lmetal");
                if (type == 'rdc'){
                    noparcent = '<label class="ltensor">No par. cent.</label><input type="checkbox" name="noparcent" id="noparcent" value="yes" onClick="check_noparcent()"/> <label class="ltensor"> OR </label>';
                    $(noparcent).insertBefore("#"+type+"_lmetal");
                }
                                            
                var elem = $("#"+type2+"-item").children("#selectable").children();
                if (elem.length > 0){
                    var elem_select = '&nbsp;&nbsp;OR <label class="ltensor" id="rdcpcs_lfile">Select '+type2+'</label><select id="spcs"><option value="null"></option>';
                    elem.each(function(){
                        //if($(this).children("span:contains('dchiax')").length > 0){
                        var name = $(this).attr("id").replace(/_file/, '');
                        elem_select += '<option value="'+$(this).attr("id")+'">'+name+'</option>';
                        //}
                    });
                    elem_select += '</select>';
                    
                    
                    elem_select += '&nbsp;&nbsp;<label class="ltensor">RDC weight</label><input id="'+type+'_weight" type="text" size=10 value="0.02" />';
                    //$(elem_select).insertAfter("#"+type+"_bfit");
                    $("#"+type+"_bfit").next().after(elem_select);
                    var bfitPCS = '<button type="button" id="bfit_'+type+'">Fit with '+type2+'</button>';
                    $("#"+type+"_weight").after(bfitPCS);
                    
                    //$(elem_select).insertAfter("#"+type+"_bcalculate");
                    //var bcalcPCS = '<button id="bcalculate_'+type+'">Calculate with '+type2+'</button>';
                    //$("#"+type+"_weight").after(bcalcPCS);
                    //$("#spcs").clic(function(){
                    //        
                    //});
                }
                
                $("#"+type+"_bfit").button();
                $("#"+type+"_bfit").click(function() {
                    startLoading();
                    var filename = $(obj).parent().prev().text().split(" ")[3];
                    var selected = $(obj).parent().prev();
                    //alert(filename);
                    //alert($("#"+type+"_tensor_fit").children().children("select").val());
                    var resname = $("#"+type+"_tensor_fit").children().children("#"+type+"_rsdname").val();
                    if (resname.length > 3){
                                    resname = resname.substring(0,3)
                    }
                    var fr = parseInt($(obj).parent().prev().text().split("]")[0].replace("[", ""));
                    var resnum = parseInt($("#"+type+"_tensor_fit").children().children("#"+type+"_rsdnum").val());
                    resnum = resnum + 1 - fr;
                    if ($("#noparcent").is(':checked')){
                          var metstr = "No Par. Cent."          
                    }
                    else{
                          var metstr = $("#"+type+"_tensor_fit").children().children("#"+type+"_atmname").val() + " " + resname + " " + resnum
                    }
                    
                    $.ajax({
                        type: "POST",
                        url: "/structureUpload/fit_"+type,
                        data: "protocol=fit"+"&"+type+"_xml=" +$(obj).parent().prev().text().split(" ")[3]+ "&temperature=" +$("#temperature").attr("value")+
                              "&b=" +$("#b").attr("value")+ "&tolerance=" +$("#tolerance").attr("value")+
                              "&metal="+metstr+"&number="+$(obj).parent().prev().text().split("]")[0].replace("[", ""),
                        success: function(data){
                            stopLoading();
                            rows = read_data_fitCalc(data, selected, type);
                            rows = rows.replace(/undefined/g, "");
                            
                            $("div[id="+filename+"_file]").children("a").not("a[href*=remove]").remove();
                            //alert(rows)
                            //rows = rdc_out.text();
                            
                            var fit_info = ' <a href="javascript:open_dialog(\''+type+' output\', \''+rows+'\', 680, 700);">fit info</a>';
                            $("div[id="+filename+"_file]").append(fit_info);
                            //$("#"+filename+"_file").append(fit_info);
                            var jmol_file = $(type+'_pdb', data).text();
                            jmol_file = jmol_file.split("_")[0]+"_"+type+''+jmol_file.split("_")[1]
                            var jmo = '<a id="'+filename+'_a" href="javascript:open_jmolView(\''+filename+'_file\', \''+jmol_file+'\');"><img class="imgconst" id="'+jmol_file+'_eye" src="'+IMG_PATH+'jmol.gif" border="0" title="View pdb with the tensor"></a>';
                            $("div[id="+filename+"_file]").children('a:last').after(jmo);
                            //$("#rdc-item").append(jmo);
                            var tarpdbfanta = type+"outfanta.tar"
                            var down = '<a href="/structureUpload/download?requested_filename='+tarpdbfanta+'"><img class="imgconst" src="'+IMG_PATH+'download.png" border="0" title="Download pdb with the tensor and fitting info"></a>';
                            $("div[id="+filename+"_file]").children('a:last').after(down);
                            $(obj).parent().remove();
                            stopLoading();
                        }
                    });
                    
                    $("#"+type+"_tensor_fit").remove();
                    $("#"+type+"_tensor_calc").remove();
                    //$(obj).parent().prev().removeAttr("class");
                    
                });
                $("#bfit_"+type).button();
                $("#bfit_"+type).click(function() {
                    startLoading();
                    var filename = $(obj).parent().prev().text().split(" ")[3];
                    var selected = $(obj).parent().prev();
                    number = $(obj).parent().prev().text().split("]")[0].replace("[", "");
                    var resname = $("#"+type+"_tensor_fit").children().children("#"+type+"_rsdname").val();
                    if (resname.length > 3){
                                    resname = resname.substring(0,3)
                    }
                    var fr = parseInt($(obj).parent().prev().text().split("]")[0].replace("[", ""));
                    var resnum = parseInt($("#"+type+"_tensor_fit").children().children("#"+type+"_rsdnum").val());
                    resnum = resnum + 1 - fr;
                    if ($("#noparcent").is(':checked')){
                          var metstr = "No Par. Cent."          
                    }
                    else{
                          var metstr = $("#"+type+"_tensor_fit").children().children("#"+type+"_atmname").val() + " " + resname + " " + resnum
                    }
                    $.ajax({
                        type: "POST",
                        url: "/structureUpload/fit_"+type,
                        data: "protocol=fit"+"&"+type+"_xml=" +$(obj).parent().prev().text().split(" ")[3]+ "&rh=" +$("#rh").attr("value")+
                              "&ax=" +$("#ax").attr("value")+ "&x1=" +$("#x1").attr("value")+
                              "&x2=" +$("#x2").attr("value")+ "&x3=" +$("#x3").attr("value")+
                              "&y1=" +$("#y1").attr("value")+ "&y2=" +$("#y2").attr("value")+
                              "&y3=" +$("#y3").attr("value")+ "&z1=" +$("#z1").attr("value")+
                              "&z2=" +$("#z2").attr("value")+ "&z3=" +$("#z3").attr("value")+
                              "&temperature=" +$("#temperature").attr("value")+
                              "&b=" +$("#b").attr("value")+ "&tolerance=" +$("#tolerance").attr("value")+
                              "&metal="+metstr+
                              "&withpcsrdc="+$("#"+type+"_tensor_fit").children().children("select[id=spcs]").val().replace("_file", "")+
                              "&weight="+$("#"+type+'_'+"weight").attr("value")+"&number="+number,
                        success: function(data){
                            //alert($(data).xml());
                            stopLoading();
                            rows = read_data_fitCalc(data, selected, type+'_'+type2);
                            rows = rows.replace(/undefined/g, "");
                            
                            $("div[id="+filename+"_file]").children("a").not("a[href*=remove]").remove();
                            //alert(rows)
                            //rows = rdc_out.text();
                            
                            var fit_info = ' <a href="javascript:open_dialog(\'output\', \''+rows+'\', 680, 700);">fit info</a>';
                            $("div[id="+filename+"_file]").append(fit_info);
                            //$("#"+filename+"_file").append(fit_info);
                            var jmol_file = $(type+'_pdb', data).text();
                            var jmo = '<a id="'+filename+'_a" href="javascript:open_jmolView(\''+filename+'_file\', \''+jmol_file+'\');"><img class="imgconst" id="'+jmol_file+'_eye" src="'+IMG_PATH+'jmol.gif" border="0" title="View pdb with the tensor"></a>';
                            $("div[id="+filename+"_file]").children('a:last').after(jmo);
                            //$("#rdc-item").append(jmo);
                            var taroutfanta = type+"outfanta.tar"
                            var down = '<a href="/structureUpload/download?requested_filename='+taroutfanta+'"><img class="imgconst" src="'+IMG_PATH+'download.png" border="0" title="Download pdb with the tensor and fitting info"></a>';
                            $("div[id="+filename+"_file]").children('a:last').after(down);
                            
                            $("#"+type+"_tensor_fit").remove();
                            $("#"+type+"_tensor_calc").remove();
                            //$(".ui-selected").removeAttr("class");
                            $(obj).parent().remove();
                            stopLoading();
                        }
                    });
                    
                });
 
                var resname = $("#"+type+"_tensor_fit").children().children("#"+type+"_rsdname").val();
                if (resname.length > 3){
                                resname = resname.substring(0,3)
                }
                var fr = parseInt($(".ui-selected").text().split("]")[0].replace("[", ""));
                var resnum = parseInt($("#"+type+"_tensor_fit").children().children("#"+type+"_rsdnum").val());
                resnum = resnum + 1 - fr;
                    
                metals = metals.replace(/id="rdc_metal"/, 'id="pcs_metal"');
                $(metals).insertAfter("#"+type+"_lmetal1");
                
                //$("#"+type+"_bcalculate").button();
                //$("#"+type+"_bcalculate").click(function() {
                //    if ($("#noparcent").is(':checked')){
                //          var metstr = "No Par. Cent."          
                //    }
                //    else{
                //           var metstr = $("#"+type+"_tensor_fit").children().children("#"+type+"_atmname").val() + " " + resname + " " + resnum
                //    }
                //    $.ajax({
                //        type: "POST",
                //        url: "/structureUpload/fit_"+type,
                //        data: "protocol=calc"+"&"+type+"_xml=" +$(".ui-selected").text().split(" ")[3]+ "&rh=" +$("#rh").attr("value")+
                //              "&ax=" +$("#ax").attr("value")+ "&x1=" +$("#x1").attr("value")+
                //              "&x2=" +$("#x2").attr("value")+ "&x3=" +$("#x3").attr("value")+
                //              "&y1=" +$("#y1").attr("value")+ "&y2=" +$("#y2").attr("value")+
                //              "&y3=" +$("#y3").attr("value")+ "&z1=" +$("#z1").attr("value")+
                //              "&z2=" +$("#z2").attr("value")+ "&z3=" +$("#z3").attr("value")+
                //              "&temperature=" +$("#temperature").attr("value")+
                //              "&b=" +$("#b").attr("value")+
                //              "&metal="+metstr,
                //        success: function(data){
                //            //alert($(data).xml());
                //            
                //            rows = read_data_fitCalc(data, selected, type+'_'+type2);
                //            rows = rows.replace(/undefined/g, "");
                //            
                //            $("div[id="+filename+"_file]").children("a").not("a[href*=remove]").remove();
                //            //alert(rows)
                //            //rows = rdc_out.text();
                //            
                //            var fit_info = ' <a href="javascript:open_dialog(\'output\', \''+rows+'\', 680, 700);">fit info</a>';
                //            $("div[id="+filename+"_file]").append(fit_info);
                //            //$("#"+filename+"_file").append(fit_info);
                //            var jmol_file = $(type+'_pdb', data).text();
                //            var jmo = '<a id="'+filename+'_a" href="javascript:open_jmolView(\''+filename+'_file\', \''+jmol_file+'\');"><img class="imgconst" id="'+jmol_file+'_eye" src="'+IMG_PATH+'jmol.gif" border="0" title="View chemical structure of rdc"></a>';
                //            $("div[id="+filename+"_file]").children('a:last').after(jmo);
                //            //$("#rdc-item").append(jmo);
                //            var down = '<a href="/structureUpload/download?requested_filename='+jmol_file+'"><img class="imgconst" src="'+IMG_PATH+'download.png" border="0" title="Download rdc"></a>';
                //            $("div[id="+filename+"_file]").children('a:last').after(down);
                //            
                //            $("#"+type+"_tensor_fit").remove();
                //            $("#"+type+"_tensor_calc").remove();
                //            $(".ui-selected").removeAttr("class");
                //        }
                //    });     
                //});
                        
//                        $(elem_select).insertAfter("#"+type+"_bcalculate");
//                        var bcalcPCS = '<button type="button" id="bcalculate_'+type+'">Calculate with '+type2+'</button>';
//                        $("#"+type+"_tensor_calc").children().children("#"+type+"_weight").after(bcalcPCS);
//					    var number = $(".ui-selected").text().split("]")[0].replace("[", "");
					//    var number_rdc = '';
					//    var number_pcs = '';
					//    if (type2 == 'rdc'){
					//	number_pcs =  $(".ui-selected").text().split("]")[0].replace("[", "");
					//	number_rdc = $("#"+$("#"+type+"_tensor_fit").children().children("select[id=spcs]").val()).children("span").text().split("]")[0].replace("[", "");
					//    }
					//    else{
					//	number_rdc =  $(".ui-selected").text().split("]")[0].replace("[", "");
					//	number_pcs = $("#"+$("#"+type+"_tensor_fit").children().children("select[id=spcs]").val()).children("span").text().split("]")[0].replace("[", "");
					//    }
                    //$("#bcalculate_"+type).button();
                    //$("#bcalculate_"+type).click(function() {
                    //    $.ajax({
                    //        type: "POST",
                    //        url: "/structureUpload/fit_"+type,
                    //        data: "protocol=calc"+"&"+type+"_xml=" +$(".ui-selected").text().split(" ")[3]+ "&rh=" +$("#rh").attr("value")+
                    //              "&ax=" +$("#ax").attr("value")+ "&x1=" +$("#x1").attr("value")+
                    //              "&x2=" +$("#x2").attr("value")+ "&x3=" +$("#x3").attr("value")+
                    //              "&y1=" +$("#y1").attr("value")+ "&y2=" +$("#y2").attr("value")+
                    //              "&y3=" +$("#y3").attr("value")+ "&z1=" +$("#z1").attr("value")+
                    //              "&z2=" +$("#z2").attr("value")+ "&z3=" +$("#z3").attr("value")+
                    //              "&temperature=" +$("#temperature").attr("value")+
                    //              "&b=" +$("#b").attr("value")+
                    //              "&metal="+$("#"+type+"_tensor_calc").children().children("select[id="+type+"_metal]").val()+
                    //              "&withpcsrdc="+$("#"+type+"_tensor_calc").children().children("select[id=spcs]").val().replace("_file", "")+
                    //              "&weight="+$("#"+type+"_tensor_calc").children().children("#"+type+'_'+"weight").attr("value")+"&number="+number,
                    //        success: function(data){
                    //            //alert($(data).xml());
                    //            
                    //            rows = read_data_fitCalc(data, selected, type+'_'+type2);
                    //            rows = rows.replace(/undefined/g, "");
                    //            
                    //            $("div[id="+filename+"_file]").children("a").not("a[href*=remove]").remove();
                    //            //alert(rows)
                    //            //rows = rdc_out.text();
                    //            
                    //            var fit_info = ' <a href="javascript:open_dialog(\'output\', \''+rows+'\', 680, 700);">fit info</a>';
                    //            $("div[id="+filename+"_file]").append(fit_info);
                    //            //$("#"+filename+"_file").append(fit_info);
                    //            var jmol_file = $(type+'_pdb', data).text();
                    //            var jmo = '<a id="'+filename+'_a" href="javascript:open_jmolView(\''+filename+'_file\', \''+jmol_file+'\');"><img class="imgconst" id="'+jmol_file+'_eye" src="'+IMG_PATH+'jmol.gif" border="0" title="View chemical structure of rdc"></a>';
                    //            $("div[id="+filename+"_file]").children('a:last').after(jmo);
                    //            //$("#rdc-item").append(jmo);
                    //            var down = '<a href="/structureUpload/download?requested_filename='+jmol_file+'"><img class="imgconst" src="'+IMG_PATH+'download.png" border="0" title="Download rdc"></a>';
                    //            $("div[id="+filename+"_file]").children('a:last').after(down);
                    //            
                    //            $("#"+type+"_tensor_fit").remove();
                    //            $("#"+type+"_tensor_calc").remove();
                    //            $(".ui-selected").removeAttr("class");
                    //        }
                    //    });     
                    //});
                
            }
            
            function read_sander_flags(){
                //var sander_out = $("fieldset[id=sander-out]");
                //var descr = $(sander_out).children("em").text();
                //var str_post = "";
                //var sander_sections = sander_out.children("div");
                //sander_sections.each(function(){
                    //var name_section = $(this).attr("id");
                    //str_post += name_section+"^";
                    //$(this).children("#flag-items").children("div").each(function(){
                        //var name = $(this).attr("id");
                        //var value = $(this).children("input").attr("value");
                        //str_post += name+"="+value+"^";//include divisorio per singoli parametri
                        
                    //});
                    //str_post += "----"; //divisioro per diverse section
                //});
                //alert(str_post);
                //$.ajax({
                    //type: "POST",
                    //url: "/structureUpload/submitSander",
                    //data: "sout="+str_post+"&description="+descr,
                    //success: function(data){
                        //alert(data);
                    //}
                //});
                
                var protocol = $("#protocol");
                var str_post = "";
                var titles = "";
                $(protocol).children("h2").each(function(){
                    titles += $(this).text()+"??"
                    var sections = $(this).next().children();
                    sections.each(function(){
                        var name_section = $(this).attr("id");
                        str_post += name_section+"^";
                        $(this).children("#flag-items").children("div").each(function(){
                            var name = $(this).attr("id");
                            var value = $(this).children("input").attr("value");
                            str_post += name+"="+value+"^";//include divisorio per singoli parametri    
                        });
                        str_post += "----"; //divisioro per diverse section
                    });
                    str_post += "????";
                });
                
                $.ajax({
                    type: "POST",
                    url: "/structureUpload/submitSander",
                    data: "sout="+str_post+"&description="+titles,
                    success: function(data){
                        //alert(data);
                    }
                });
            }
            
            
            function read_data_fitCalc(data_all, selected, type){
                
                var data_temp = data_all;
                var type_temp = type;
                var type2 = type;
                var rows1 = '';
                var data = data_all;
                var rows='';
                if(type_temp == "rdc_pcs" || type_temp == "pcs_rdc"){
                    var data1 =  $("fanta_"+type_temp.split('_')[0], data_temp);
                    data = $("fanta_"+type_temp.split('_')[1], data_temp);
                    type2 = type_temp.split('_')[1];
                    var qfactor_val = $('qfactor', data1).attr("qfactor_val");
                
                    rows1 += '<label class=litem>qfactor value: '+qfactor_val +'</label> ';
                    var qfactor_num = $('qfactor', data1).attr("num");
                    rows1 += '<label class=litem>qfactor num: '+qfactor_num+'</label> ';
                    var qfactor_den = $('qfactor', data1).attr("den").replace(/\)/, '');
                    rows1 += '<label class=litem>qfactor den: '+qfactor_den+'</label><br />';
                    var eig_val1 = $('RDC_eig', data1).attr("a1val");
                    rows1 += '<label class=litem>eigenvalue a1: '+eig_val1+'</label> ';
                    var eig_val2 = $('RDC_eig', data1).attr("a2val");
                    rows1 += '<label class=litem>eigenvalue a2: '+eig_val2+'</label> ';
                    var eig_val3 = $('RDC_eig', data1).attr("a3val");
                    rows1 += '<label class=litem>eigenvalue a3: '+eig_val3+'</label><br />';
                    var dchirh = $('aniso', data1).attr("dchirh");
                    rows1 += '<label class=litem>aniso dchirx: '+dchirh+'</label> ';
                    var dchiax = $('aniso', data1).attr("dchiax");
                    rows1 += '<label class=litem>aniso dchiax: '+dchiax+'</label><br />';
                    var dchirh_m = $('anisom', data1).attr("dchirh");
                    rows1 += '<label class=litem>anisom dchirx: '+dchirh_m+'</label> ';
                    var dchiax_m = $('anisom', data1).attr("dchiax");
                    rows1 += '<label class=litem>anisom dchiax: '+dchiax_m+'</label><br />';
                    var theta = $('euler', data1).attr("theta");
                    rows1 += '<label class=litem>euler theta: '+theta+'</label> ';
                    var phi = $('euler', data1).attr("phi");
                    rows1 += '<label class=litem>euler phi: '+phi+'</label> ';
                    var omega = $('euler', data1).attr("omega");
                    rows1 += '<label class=litem>euler omega: '+omega+'</label><br />';

                    var graph_file = $(type_temp.split('_')[0]+'_graph', data1).text();
                    
                    //selected.append(" <br />dchiax: "+dchiax+" dchirh: "+dchirh);
                    var rdc_out = $(type_temp.split('_')[0]+'_out', data1);
                   
                    var rdc_out_split = rdc_out.text().split('\n');
                    
                    rows1 += '<img src=/global/img_tmp/'+graph_file+'>';
                    
                    if (type_temp.split('_')[0] == 'rdc'){
                        rows1 += '<label class=cell_rdc><b>Calculated</b></label>'+
                            '<label class=cell_rdc><b>Observed</b></label>'+
                            '<label class=cell_rdc><b>Tolerance</b></label>'+
                            '<label class=cell_rdc><b>Atom 1</b></label>'+
                            '<label class=cell_rdc><b>Atom 2</b></label>'+
                            '<label class=cell_rdc><b>Magn. field</b></label><br />';
                    }
                    else if (type_temp.split('_')[0] == 'pcs'){
                        rows1 += '<label class=cell_pcs><b>Calculated</b></label>'+
                            '<label class=cell_pcs><b>Observed</b></label>'+
                            '<label class=cell_pcs><b>Tolerance</b></label>'+
                            '<label class=cell_pcs><b>Atom</b></label>';
                    }
                    
                    $(rdc_out_split).each(function(){
                        var this_split = this.split(';')
                        if (type_temp.split('_')[0] == 'rdc'){
                            var calc = this_split[0];
                            var obs = this_split[1];
                            var err = this_split[2];
                            var atom1 = this_split[3];
                            atom1 += ' '+ this_split[4];
                            var atom2 = this_split[5];
                            atom2 += ' '+this_split[6];
                            var field = this_split[7];
                            if (Math.abs(obs - calc) > err){
                                var row = '<label class=cell_rdc><span class=errorFit>'+calc+'</span></label> <label class=cell_rdc>' + obs +'</label> <label class=cell_rdc>'+ err+'</label> <label class=cell_rdc>'+atom1 + '</label> <label class=cell_rdc>'+atom2 + '</label> <label class=cell_rdc>'+field+'</label> ';
                                //var row = '<span>'+calc + '</span> ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ field+'<br />';
                            }
                            else{
                                var row = '<label class=cell_rdc>'+calc+'</label> <label class=cell_rdc>' + obs +'</label> <label class=cell_rdc>'+ err+'</label> <label class=cell_rdc>'+atom1 + '</label> <label class=cell_rdc>'+atom2 + '</label> <label class=cell_rdc>'+field+'</label> ';
                                //var row = calc + ' ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ temp+'<br />';
                            }
                        }
                        else{
                            var calc = this_split[0];
                            var obs = this_split[1];
                            var err = this_split[2];
                            var atom1 = this_split[3];
                            atom1 += ' '+ this_split[4];
                            
                            if (Math.abs(obs - calc) > err){
                                var row = '<label class=cell_pcs><span class=errorFit>'+calc+'</span></label> <label class=cell_pcs>' + obs +'</label> <label class=cell_pcs>'+ err+'</label> <label class=cell_pcs>'+atom1+'</label> ';
                                //var row = '<span>'+calc + '</span> ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ field+'<br />';
                            }
                            else{
                                var row = '<label class=cell_pcs>'+calc+'</label> <label class=cell_pcs>' + obs +'</label> <label class=cell_pcs>'+ err+'</label> <label class=cell_pcs>'+atom1 + '</label> ';
                                //var row = calc + ' ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ temp+'<br />';
                            }
                        }
                        
                        rows1 += row;
                        
                    });
                            
                }
                else{
                    var qfactor_val = $('qfactor', data).attr("qfactor_val");
                    rows += '<label class=litem>qfactor value: '+qfactor_val +'</label> ';
                    var qfactor_num = $('qfactor', data).attr("num");
                    rows += '<label class=litem>qfactor num: '+qfactor_num+'</label> ';
                    var qfactor_den = $('qfactor', data).attr("den").replace(/\)/, '');
                    rows += '<label class=litem>qfactor den: '+qfactor_den+'</label><br />';
                    var eig_val1 = $('RDC_eig', data).attr("a1val");
                    rows += '<label class=litem>eigenvalue a1: '+eig_val1+'</label> ';
                    var eig_val2 = $('RDC_eig', data).attr("a2val");
                    rows += '<label class=litem>eigenvalue a2: '+eig_val2+'</label> ';
                    var eig_val3 = $('RDC_eig', data).attr("a3val");
                    rows += '<label class=litem>eigenvalue a3: '+eig_val3+'</label><br />';
                    var dchirh = $('aniso', data).attr("dchirh");
                    rows += '<label class=litem>aniso dchirx: '+dchirh+'</label> ';
                    var dchiax = $('aniso', data).attr("dchiax");
                    rows += '<label class=litem>aniso dchiax: '+dchiax+'</label><br />';
                    var dchirh_m = $('anisom', data).attr("dchirh");
                    rows += '<label class=litem>anisom dchirx: '+dchirh_m+'</label> ';
                    var dchiax_m = $('anisom', data).attr("dchiax");
                    rows += '<label class=litem>anisom dchiax: '+dchiax_m+'</label><br />';
                    var theta = $('euler', data).attr("theta");
                    rows += '<label class=litem>euler theta: '+theta+'</label> ';
                    var phi = $('euler', data).attr("phi");
                    rows += '<label class=litem>euler phi: '+phi+'</label> ';
                    var omega = $('euler', data).attr("omega");
                    rows += '<label class=litem>euler omega: '+omega+'</label><br />';
                }
                //var rows = '';
                //var qfactor_val = $('qfactor', data).attr("qfactor_val");
                
                //rows += '<label class=litem>qfactor value: '+qfactor_val +'</label> ';
                //var qfactor_num = $('qfactor', data).attr("num");
                //rows += '<label class=litem>qfactor num: '+qfactor_num+'</label> ';
                //var qfactor_den = $('qfactor', data).attr("den").replace(/\)/, '');
                //rows += '<label class=litem>qfactor den: '+qfactor_den+'</label><br />';
                //var eig_val1 = $('RDC_eig', data).attr("a1val");
                //rows += '<label class=litem>eigenvalue a1: '+eig_val1+'</label> ';
                //var eig_val2 = $('RDC_eig', data).attr("a2val");
                //rows += '<label class=litem>eigenvalue a2: '+eig_val2+'</label> ';
                //var eig_val3 = $('RDC_eig', data).attr("a3val");
                //rows += '<label class=litem>eigenvalue a3: '+eig_val3+'</label><br />';
                var dchirh = $('aniso', data).attr("dchirh");
                //rows += '<label class=litem>aniso dchirx: '+dchirh+'</label> ';
                var dchiax = $('aniso', data).attr("dchiax");
                //rows += '<label class=litem>aniso dchiax: '+dchiax+'</label><br />';
                //var dchirh_m = $('anisom', data).attr("dchirh");
                //rows += '<label class=litem>anisom dchirx: '+dchirh_m+'</label> ';
                //var dchiax_m = $('anisom', data).attr("dchiax");
                //rows += '<label class=litem>anisom dchiax: '+dchiax_m+'</label><br />';
                //var theta = $('euler', data).attr("theta");
                //rows += '<label class=litem>euler theta: '+theta+'</label> ';
                //var phi = $('euler', data).attr("phi");
                //rows += '<label class=litem>euler phi: '+phi+'</label> ';
                //var omega = $('euler', data).attr("omega");
                //rows += '<label class=litem>euler omega: '+omega+'</label><br />';
                var graph_file = $(type2+'_graph', data).text();
                
                selected.append(" <br />dchiax: "+dchiax+" dchirh: "+dchirh);
                var rdc_out = $(type2+'_out', data);
               
                var rdc_out_split = rdc_out.text().split('\n');
                
                rows += '<img src=/global/img_tmp/'+graph_file+'>';
                
                if (type2 == 'rdc'){
                    rows += '<label class=cell_rdc><b>Calculated</b></label>'+
                        '<label class=cell_rdc><b>Observed</b></label>'+
                        '<label class=cell_rdc><b>Tolerance</b></label>'+
                        '<label class=cell_rdc><b>Atom 1</b></label>'+
                        '<label class=cell_rdc><b>Atom 2</b></label>'+
                        '<label class=cell_rdc><b>Magn. field</b></label><br />';
                }
                else if (type2 == 'pcs'){
                    rows += '<label class=cell_pcs><b>Calculated</b></label>'+
                        '<label class=cell_pcs><b>Observed</b></label>'+
                        '<label class=cell_pcs><b>Tolerance</b></label>'+
                        '<label class=cell_pcs><b>Atom</b></label>';
                        
                }
                
                $(rdc_out_split).each(function(){
                    var this_split = this.split(';')
                    if (type2 == 'rdc'){
                        var calc = this_split[0];
                        var obs = this_split[1];
                        var err = this_split[2];
                        var atom1 = this_split[3];
                        atom1 += ' '+ this_split[4];
                        var atom2 = this_split[5];
                        atom2 += ' '+this_split[6];
                        var field = this_split[7];
                        if (Math.abs(obs - calc) > err){
                            var row = '<label class=cell_rdc><span class=errorFit>'+calc+'</span></label> <label class=cell_rdc>' + obs +'</label> <label class=cell_rdc>'+ err+'</label> <label class=cell_rdc>'+atom1 + '</label> <label class=cell_rdc>'+atom2 + '</label> <label class=cell_rdc>'+field+'</label> ';
                            //var row = '<span>'+calc + '</span> ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ field+'<br />';
                        }
                        else{
                            var row = '<label class=cell_rdc>'+calc+'</label> <label class=cell_rdc>' + obs +'</label> <label class=cell_rdc>'+ err+'</label> <label class=cell_rdc>'+atom1 + '</label> <label class=cell_rdc>'+atom2 + '</label> <label class=cell_rdc>'+field+'</label> ';
                            //var row = calc + ' ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ temp+'<br />';
                        }
                    }
                    else{
                        var calc = this_split[0];
                        var obs = this_split[1];
                        var err = this_split[2];
                        var atom1 = this_split[3];
                        atom1 += ' '+ this_split[4];
                        
                        if (Math.abs(obs - calc) > err){
                            var row = '<label class=cell_pcs><span class=errorFit>'+calc+'</span></label> <label class=cell_pcs>' + obs +'</label> <label class=cell_pcs>'+ err+'</label> <label class=cell_pcs>'+atom1+'</label> ';
                            //var row = '<span>'+calc + '</span> ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ field+'<br />';
                        }
                        else{
                            var row = '<label class=cell_pcs>'+calc+'</label> <label class=cell_pcs>' + obs +'</label> <label class=cell_pcs>'+ err+'</label> <label class=cell_pcs>'+atom1 + '</label> ';
                            //var row = calc + ' ' + obs +' '+ err+' '+atom1 + ' '+ atom2 +' '+ temp+'<br />';
                        }
                    }
                    
                    rows += row;
                    
                });
                
                
                return rows1+rows;
            }
            
            function insertFlagValue(str, section){
                var str_txtArea = $("#txtarea").attr("value");
                alert(str_txtArea)
                var str_txtAreaSections = str_txtArea.split("&");
                var str_flag = str.split("=");
                
                $(str_txtAreaSections).each(function(){
                    this.replace(section+"\n", "").split(",").filter(function(index){
                            return $(str_flag[0], this).length == 1;
                        }).replace(/^\c/, str);
                });
            }
            
            function manage_ligandEntry(inputID, form){
                var ID = inputID.split('_')[0];
                var cntEntry = $("#ligand-item").children().length;
                var filename = $("#"+inputID).attr("value");
                var filename_list = filename.split('\\');
                if (filename_list.length){
                    filename = filename_list[filename_list.length - 1];
                }
                
                var notfound = 1
                var cntItem = $("#ligand-item").children("div[id="+filename.split('.')[0]+"_ligand]");
                if(cntItem.length){
                    notfound == 0;
                }
                
                if(notfound){
                    
                    if(ID != 'ligand'){
                        var name = "ligand_"+ID+"_name";    
                    }
                    else{
                        var name = "ligand_name";
                    }
                    var lig_tag = '<div id="li_'+ID+'_ligand"> <a id="a_'+ID+'_file" href="javascript:removeUploadedFile(\'a_'+ID+'_file\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                        '<span name="ligand_'+ID+'_name" id="l'+ID+filename.split('.')[0]+'">'+filename+'</span><br /></div>';
                    if(!cntEntry){//se non ci sono entry
                        //creo il box e lo inserisco
                        var new_box = '<div id='+filename.split('.')[0]+'_ligand>'+
                                '<li class="drop" id="'+filename.split('.')[0]+'-list">'+
                                '</li>'+
                                '<br />'
                                '</div>';
                        $("#ligand-item").append(new_box);    
                        //inserisco tag ligand
                        $("#"+filename.split('.')[0]+'_ligand').children("li[id="+filename.split('.')[0]+"-list]").append(lig_tag);
                    }
                    else if(cntEntry == 1){
                          var entry_li_div = $("#ligand-item").children().children("li").children("div[id=li_"+ID+"_ligand]");
                          //alert(entry_li_div.length)
                          if ((entry_li_div.length) && (ID != "ligand")){
                            entry_li_div.replaceWith(lig_tag);
                          }
                          else if(ID == "ligand"){
                            var new_box = '<div id='+filename.split('.')[0]+'_ligand>'+
                                '<li class="drop" id="'+filename.split('.')[0]+'-list">'+
                                '</li>'+
                                '<br />'
                                '</div>';
                            $("#ligand-item").append(new_box);    
                            //inserisco tag ligand
                            $("#"+filename.split('.')[0]+'_ligand').children("li[id="+filename.split('.')[0]+"-list]").append(lig_tag);
                          }
                          else{
                            $("#ligand-item").children().children("li").append(lig_tag);
                          }
                    }
                    else{
                        var cntEntryWithID = $("#ligand-item").children().length;
                        var count = cntEntryWithID;
                        var target = $();
                        $("#ligand-item").children().each(function(){
                            var e = $(this).children("li").children("div[id=li_"+ID+"_ligand]");
                            if (e.length){
                                count = count - 1;
                            }
                            else{
                                target = $(this).children("li");
                            }
                        });
                        
                        if (count == 1){
                            target.append(lig_tag);
                        }
                        else{
                            $("#ligand-zombies").append(lig_tag);
                            $("#ligand-zombies").children().addClass("drag");
                        }
                    }
                    if(ID == "ligand"){
                        $("#top_file").removeAttr("disabled");
                    }
                    else if(ID == "top"){
                        $("#par_file").removeAttr("disabled");
                    }
                    
                    $(".drag").draggable();
                    $(".drop").droppable({
                                    accept: ".drag",
                                    activeClass: 'droppable-active',
                                    hoverClass: 'droppable-hover',
                                    drop: function(ev, ui) {
                                            var clone = $(ui.draggable).clone();
                                            clone.removeAttr("style");
                                            clone.removeAttr("class");
                                            var item = $(this).children("#"+clone.attr("id"));
                                            if (item.length){
                                                item.replaceWith(clone);
                                            }
                                            else{
                                                $(this).append(clone);
                                            }
                                            $(ui.draggable).remove();
                                    }
                    });
                    
                    var hdd = '<input type="hidden" value="'+filename+'" name="'+name+'">';
                    $("#submit").append(hdd);
                    
                    $("#field").attr("value", inputID);
                    var options = {
                        url: "/structureUpload/upload",
                        dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                        success:  function(response, status){
                            //alert(inputID)
                            $("#"+inputID).attr("value", "");
                        }
                    };
                    $("#"+form).ajaxSubmit(options); 
                }
                enableTabs();
            }
            
            
            
            
            
            function add_ligandEntry(id_input,form){
                var filename = $("#"+id_input).attr("value");
                var filename_list = filename.split('\\');
                if (filename_list.length){
                    filename = filename_list[filename_list.length - 1];
                }
                var ligand = $("#ligand-item").children().last();
                
                if(id_input.split('_')[0] == "ligand"){
                    var new_label = '<div id="'+id_input.split('_')[0]+'_ligand"> <a id="a_'+id_input.split('_')[0]+'_file" href="javascript:removeUploadedFile(\'a_'+id_input.split('_')[0]+'_file\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                    '<span id="l'+id_input.split('_')[0]+filename.split('.')[0]+'">'+filename+'</span>'+
                                    '<input type="checkbox" name="chbx_'+filename.split('.')[0]+'" value="'+filename.split('.')[0]+'" onclick="manage_chbx_ligand(\'chbx_'+filename.split('.')[0]+'\')">change ligand files<br>'+
                                    '<br /></div>';
                }
                else{
                    var new_label = '<div id="'+id_input.split('_')[0]+'_ligand"> <a id="a_'+id_input.split('_')[0]+'_file" href="javascript:removeUploadedFile(\'a_'+id_input.split('_')[0]+'_file\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                    '<span id="l'+id_input.split('_')[0]+filename.split('.')[0]+'">'+filename+'</span><br /></div>';    
                }
                
                if ((ligand.length == 0) || (id_input.split('_')[0] == "ligand")){
                    var lig_tag = '<div id='+filename.split('.')[0]+'_ligand>'+
                            '<li id="'+filename.split('.')[0]+'-sort">'+
                            '</li>'+
                            '<br />'
                            '</div>';
                    $("#ligand-item").append(lig_tag);
                    $("#"+filename.split('.')[0]+'_ligand').children("li[id="+filename.split('.')[0]+"-sort]").append(new_label);
                }
                else if(ligand.children("a[id^=a_"+id_input.split('_')[0]+"]").length){
                    //ligand.children("span").last().remove();
                    ligand.children("a[id^=a_"+id_input.split('_')[0]+"]").replaceWith(new_label);
                    
                }
                else{
                    ligand.append(new_label);
                } 
                
            }
            
            function add_toppar(select_id, id_input, form, fname){
                var residue = $("#"+select_id).val();
                var filename = $("#"+id_input).attr("value");
                var filename_list = filename.split('\\');
                if (filename_list.length){
                    filename = filename_list[filename_list.length - 1];
                }
                var new_label = '<div id="'+id_input.split('_')[0]+'_'+residue+'" <a id="a_'+id_input.split('_')[0]+'_file" href="javascript:removeUploadedFile(\'a_'+id_input.split('_')[0]+'_file'+'\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                '<span name="amino_'+id_input.split('_')[0]+'_name" id="l'+id_input.split('_')[0]+residue+'">'+filename+'</span><br /></div>';
                
                var notfound = 1
                $("#l"+id_input.split('_')[0]+residue).each(function(){
                    if($(this).attr("value") == filename){
                        notfound == 0;
                    }
                });
                
                
                if(notfound){
                    if($("#"+residue+'_residue_'+fname.split('.')[0]).length == 0){
                        var div_tag = '<div id="'+residue+'_residue_'+fname.split('.')[0]+'">'+
                                    '<label name="amino_name" id="lresidue">'+residue.split('_')[0]+'</label>'+
                              '</div>';
                        $("#amino-item").append(div_tag); 
                        $("#"+residue+'_residue_'+fname.split('.')[0]).append(new_label);
                    }
                    else if( $("#"+residue+'_residue_'+fname.split('.')[0]).children("#"+id_input.split('_')[0]+"_"+residue).length == 0){
                        $("#"+residue+'_residue_'+fname.split('.')[0]).append(new_label);
                    }
                    else{
                        $('#l'+id_input.split('_')[0]+residue).next().remove();
                        $('#l'+id_input.split('_')[0]+residue).remove();
                        $("#"+residue+'_residue_'+fname.split('.')[0]).children("#"+id_input.split('_')[0]+"_"+residue).replaceWith(new_label);
                        
                    }
                    
                    var hdd = '<input type="hidden" value="'+filename+'" name="amino_'+id_input.split('_')[0]+'_name">';
                    $("#submit").append(hdd);
                    
                    $("#field").attr("value", id_input+'_file');
                    var options = {
                        url: "/structureUpload/upload",
                        dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                        success:  function(response, status){
                            $("#"+id_input+"_div").html($("#"+id_input+"_div").html());
                        }
                    };
                    $("#"+form).ajaxSubmit(options);
                    //$.validationEngine.closePrompt("input[id=top_amino]");
                    enableTabs();
                    //$.validationEngine.closePrompt("#force_fields");
                } 
            }
            
            
            
            
            
            function open_dialog(titleDialog, message, w, h){
                var vdialog = $('<div></div>');
		vdialog.html(message);
               
		vdialog.dialog({
                    autoOpen: false,
                    title: titleDialog,
                    width: w,
                    height: h,
                    modal: true,
                    buttons: {
                        "Ok": function() {
                            $(this).dialog("close");
                            }
                    }
		});

                //vdialog.dialog( "option", "position", 'center' );
                vdialog.dialog('open');
            }


            
            
            function add_warning(id, title, message){
                var prefix = id.split('_')[0];
                var id_nr = id.split('_')[2];
                var img_w = '<a id="'+prefix+'_a_'+id_nr+'" href="javascript:open_dialog(\''+title+'\', \''+message+'\', \'550\', \'570\');"><img id="'+prefix+'_war_'+id_nr+'" src="'+IMG_PATH+'warning.png" border="0" title="Some warnings about your input file"></a>';
                
                $("#"+id).append(img_w);
                
            }
            
            function add_Jmolview(id, title, message, loc){
                var prefix = id.split('_')[0];
                var id_nr = id.split('_')[2];
                var img_jmol = '<a id="'+prefix+'_a_'+id_nr+'" href="javascript:open_dialog(\''+title+'\', \''+message+'\', \'550\', \'570\');"><img id="'+prefix+'_eye_'+id_nr+'" src="'+IMG_PATH+'jmol.gif" border="0" title="View chemical structure of protein"></a>';
                if(loc == "away"){
                    $("#"+id).nextUntil("div").last().after(img_jmol);
                }
                else{
                    $("#"+id).after(img_jmol);
                }
                
                
            }
            
            function add_error(id, title, message){
                var prefix = id.split('_')[0];
                var id_nr = id.split('_')[2];
                var img_e = '<a id="'+prefix+'_a_'+id_nr+'" href="javascript:popup(\'\', \''+title+'\', \''+message+'\');"><img id="'+prefix+'_err_'+id_nr+'" src="'+IMG_PATH+'error.png" border="0" title="Some errors about your input file"></a>';
                
                $("#"+id).append(img_e);
                
            }
            
            function add_ok(id, loc){
                var prefix = id.split('_')[0];
                var id_nr = id.split('_')[2];
                var img_ok = '<img id="'+prefix+'_ok_'+id_nr+'" src="/global/images/ok.gif" border="0" title="Your input file is ok" alt="Your input file is ok">';
                if(loc == "away"){
                    $("#"+id).nextUntil("div").last().after(img_ok);
                }
                else{
                    $("#"+id).after(img_ok);
                }
            }
            
            
            function enableSubmit(){
                var proteins_div = $("div[id^=protein_div_]");
                var enabled = 1;
                proteins_div.each(function(){
                        if ($(this).children("input[id^=protein_check]").length > 1){
                            enabled = 0;
                        }
                    });
                if(enabled){
                    $("#submit_structure").removeAttr("disabled");
                }
            }
            
            function checkSubmit(id){
                
                var id_tmp = id.replace(/check/,"file");
                $("#submit_check").attr("value", id_tmp );
                
                
                
                var options = {
                    url: "/structureUpload/check_input_pdb",
                    //target:        '#output1',   // target element(s) to be updated with server response 
                    //beforeSubmit:   
                    dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                    success:  processCheckedFile   // post-submit callback 
                };
                
                $("#structure").ajaxSubmit(options);
                
            }
            
            
            
            
            function popup(head, title, body){
                var w = 700;
                var h = 350;
                var l = Math.floor((screen.width-w)/2);
                var t = Math.floor((screen.height-h)/2);
                option = "\'height="+h+",width="+w+",left="+l+",top="+t+",resizable=yes,scrollbars=yes,toolbar=no,menubar=no,location=no,directories=no,status=yes\'";
                //alert(option)
                var generator=window.open('','name',option);
                generator.document.write('<html>');
                generator.document.write('<head>');
                generator.document.write('<title>'+title+' popup</title>');
                generator.document.write(head);
                generator.document.write('</head>');
                generator.document.write('<body>');
                generator.document.write(body);
                generator.document.write('<p align="center"><a href="javascript:self.close()">Close</a> the popup.</p>');
                generator.document.write('</body>');
                generator.document.write('</html>');
                generator.document.close();
            }
            
            function popupMessage(typeMessage, message){
                var w = 500;
                var h = 350;
                var l = Math.floor((screen.width-w)/2);
                var t = Math.floor((screen.height-h)/2);
                option = "\'height="+h+",width="+w+",left="+l+",top="+t+",resizable=yes,scrollbars=yes,toolbar=no,menubar=no,location=no,directories=no,status=yes\'";
                //alert(option)
                //var generator=window.open("","name","height=" + h + "',width=" + w +",top=" + t + ",left=" + l ",scrollbars=yes'");
                
                var generator=window.open('','name',option);
                generator.document.write('<html><head><title>'+typeMessage+' popup</title>');
                generator.document.write('</head>');

                generator.document.write('<body>');
               
                generator.document.write(message);
                generator.document.write('<p align="center"><a href="javascript:self.close()">Close</a> the popup.</p>');
                generator.document.write('</body></html>');
                generator.document.close();
            }

        
        function checkSubmitConstraint(id){
            
            var type = id.split('_')[0];
            $("#field").attr("value", type);

            var options = {
                url: "/structureUpload/check_constraint",
                //data: type,
                //target:        '#output1',   // target element(s) to be updated with server response 
                //beforeSubmit:   
                dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                success:  processCheckedConstraint   // post-submit callback 
            };
            
            $("#constraint").ajaxSubmit(options);
            
        }
        
        function processCheckedConstraint(response, statusText){
                //response = $(response).xml();
                //alert(response);
                GLOB_RESP = response;
               $("#submit_contraint").removeAttr("disabled");
                //enableSubmit();
        }

        function processConstraintSubmit(response, statusText){
            //var prot = $('protein', response);
            //var attr = prot.attr("filename");
            //response = $(response).xml();
            //alert($(response));
            
        }

        
        function check_nstdres(){
            var ret = true;
            var fieldAmino = $("fieldset[id=amino]");
            if(fieldAmino.length){
                var check = new Array();
                $("select[id=samino]").children().each(function(){
                    var opt = $(this).attr("value").split("_")[0];
                    if($("#amino-item").children().length){
                        $("#amino-item").children().each(function(i){
                            var item = $(this).attr("id");
                            if(item.split("_")[0] == opt){
                                if ($(item).children("div[id^=top]").length){
                                    check[i] = true;
                                }
                                else{
                                    check[i] = false;
                                }
                            }
                        });    
                    }
                    else{
                        ret = false;
                    }
                });
                
                $(check).each(function(){
                    if (!this){
                        ret = false;
                    }
                });
            }
            return ret;
        }
        
        function enableTabs(){
            
            var chain = false;
            //var nstdres = false;
            //var forcef = false;
            if ($("#chain-item").children().length){
                chain = true;
                $.validationEngine.closePrompt("input[name=chain_file]");
                
                //controllo se ci sono amino non standard
                //nstdres = check_nstdres();
                //if(nstdres){
                //    $.validationEngine.closePrompt("input[id=top_amino]");
                //}
            }
            //if($("#force_fields").val() != ""){
            //    forcef = true;
            //    $.validationEngine.closePrompt("#force_fields");
            //}
            
            
            
            //if(($("#chain-item").children().length) && ($("#amino-item").children().length >= ($("#samino").children("option").length - 1)) && ($("#force_fields").val() != "")){
            if(chain){
                //$('#tabs').tabs({ disabled: [] });
                
                $('#tabs').tabs({ disabled: [] });
                $('#tabs').children("ul").children("li").each(function(){
                    if ($(this).children("a").attr("href") == "#tabs-2"){
                        $(this).children("a").bind('click', function(){
                            submit('structure');    
                        });
                        //$(this).children("a").attr("onclick", "submit('structure')");
                    }
                    //else if($(this).children("a").attr("href") == "#tabs-3"){
                    //    if (!$("body").children("input[name=substructure]").length){
                    //        submit('structure');
                    //    }
                    //    $(this).children("a").bind('click', function(){
                    //        submit('constraint');    
                    //    });
                    //    //$(this).children("a").attr("onclick", "submit('constraint')");
                    //    
                    //}
                    //else if($(this).children("a").attr("href") == "#tabs-4"){
                    //    $(this).children("a").bind('click', function(){
                    //        read_sander_flags();    
                    //    });
                    //    //$(this).children("a").attr("onclick", "read_sander_flags()");
                    //    
                    //}
                });
                //$.jGrowl("You are provided a minimum set of structure inputs to continue.", {header: 'INFORMATION', life: 8000, theme: 'iphone'});
                $("div.jGrowl-notification").trigger("jGrowl.close");
                //showMessage('Now, you can specify Constraint inputs.', 350, 80, 'ok2');
                //$.jGrowl("Now, you can specify Constraint inputs.", {header: 'INFORMATION', life: 8000, theme: 'iphone'});
            }
            else{
                //$.validationEngine.closePrompt("input[id=calc_name]");
                $.validationEngine.buildPrompt("input[name=chain_file]","This field is required","error");
                $('#tabs').tabs({ disabled: [1,2,3] });
            }
            //else if (!forcef){
            //    $.validationEngine.buildPrompt("select[id=force_fields]","This field is required","error");
            //    $('#tabs').tabs({ disabled: [1,2,3] });
            //}
            //else if (!nstdres){
            //    $.validationEngine.buildPrompt("input[id=top_amino]","This field is required","error");
            //    $('#tabs').tabs({ disabled: [1,2,3] });
            //}
        }
        
        function submit(form){
            if(form == 'structure'){
//		var pass = true;
//		$.ajax({
//                    type: 'POST',
//                    url: '/structureUpload/checkprmd/id=',
//                    success: function(data){
//                        if (data == 'error'){
//			    pass = false;
//                            $.jGrowl("Some unrecognized error occurred checking your pdb file.", {header: 'ATTENTION', theme: 'iphone'});
//                        }
//                    }
//                });
//		if (pass){
		    var options = { 
				//target:        '#output1',   // target element(s) to be updated with server response 
				//beforeSubmit:   validatorRequest,  // pre-submit callback
				dataType:  'xml'        // 'xml', 'script', or 'json' (expected server response type) 
				/*success:  processStructureSubmit*/   // post-submit callback 
		    };
		    $("#"+form).ajaxSubmit(options);
		    if(!$("body").children("input[name=substructure]").length){
			$("body").append('<input type="hidden" name="substructure" value="1" />');
		    }
		//}
            }
            else{
                if(!$("body").children("input[name=substructure]").length){
                   submit('structure');
                }
                $("#"+form).ajaxSubmit();
            }
        }
        
        
        
        function submitSander(){
            //$.ajax({
            //        type: "POST",
            //        url: "/structureUpload/submitSander",
            //        data: "protocol=calc"+"&"+type+"_xml=" +$(".ui-selected").text().split(" ")[3]+ "&rh=" +$("#rh").attr("value")+
            //              "&ax=" +$("#ax").attr("value")+ "&x1=" +$("#x1").attr("value")+
            //              "&x2=" +$("#x2").attr("value")+ "&x3=" +$("#x3").attr("value")+
            //              "&y1=" +$("#y1").attr("value")+ "&y2=" +$("#y2").attr("value")+
            //              "&y3=" +$("#y3").attr("value")+ "&z1=" +$("#z1").attr("value")+
            //              "&z2=" +$("#z2").attr("value")+ "&z3=" +$("#z3").attr("value")+
            //              "&temperature=" +$("#temperature").attr("value")+
            //              "&b=" +$("#b").attr("value")+
            //              "&metal="+$("#"+type+"_tensor_calc").children().children("select[id="+type+"_metal]").val()+
            //              "&withpcsrdc="+$("#"+type+"_tensor_calc").children().children("select[id=spcs]").val().replace("_file", "")+
            //              "&weight="+$("#"+type+"_tensor_calc").children().children("#"+type+'_'+"weight").attr("value"),
            //        success: function(data){
            //            alert($(data).xml());
                                                        
        }
        
        //run the currently selected effect
        function runEffect(){
            //run the effect
            var options = {};
            
            //$("#amino").effect("slide",options,500,callback);
            $("#amino").effect("highlight",options,500,callback);
        };
        
        //callback function to bring a hidden box back
        function callback(){
                setTimeout(function(){
                        $("#amino:hidden").removeAttr('style').hide().fadeIn();
                }, 1000);
        };

        
        function retrieveCostraints(noe, rdc){
            var str = '<div id="sander_file"><div id="flag-items">';
            var noe_item = $("#noe-item").children("div");
            var dih_item = $("#dihedral-item").children("div");
            if (((noe_item.length > 0) || (dih_item.length > 0))&&(noe=='1')){
                str += '<div id="DISANG">DISANG=<input type="text" id="iflag" readonly="readonly" value="allNOE_allDIH.in" style="border:medium none;" size="8" /></div>';
            }
            
            
            //if (dih_item.length > 0){
            //    dih_item.each(function(){
            //        str += '<div id="DISANG">DISANG=<input type="text" id="iflag" readonly="readonly" value="DIHfiles.in" style="border:medium none;" size="8" /></div>';
            //    });
            //}
            
            var rdc_item = $("#rdc-item").children("#selectable").children();
            if ((rdc_item.length > 0)&&(rdc=='1')){
                rdc_item.each(function(){
                    str += '<div id="DIPOLE">DIPOLE=<input type="text"  id="iflag" readonly="readonly" value="allRDC.in" style="border:medium none;" size="8" /></div>';
                });
            }
            
            var pcs_item = $("#pcs-item").children("#selectable").children();
            if ((pcs_item.length > 0)&&(rdc=='1')){
                pcs_item.each(function(){
                    str += '<div id="PCSHIFT">PCSHIFT=<input type="text" id="iflag" readonly="readonly" value="PCS.in" style="border:medium none;" size="8" /></div>';
                });
            }
            str += '</div>';
            str += '</div>';
            return str;
        }
        
        
        function checkAvailability(id, proj, calc){
	    if (calc != ''){
		$.ajax({
		    type: "POST",
		    url: "/structureUpload/isCalcExist",
		    data: {"calc": calc, "proj": proj},
		    success: function(data){
			//$("#submitOpt").children("img").remove();
			addInfoProtocol();
			if (data == 'False'){
			    //$.validationEngine.closePrompt("input[id=calc_name]");
			    //$.validationEngine.buildPrompt("input[id=calc_name]","it's available ","pass");
			    //$("#"+id).after('<img src="/global/images/ok.png"></img>')
			    $("#availability").remove();
			    $("#"+id).after('<span class="ok">Ok</span>');
			    $("#submit_calc").removeAttr("disabled");
			    //$("#subCalc").removeAttr("disabled");
			    $("#submitOpt").children("input[name=calcname]").remove();
			    $("#submitOpt").append('<input type="hidden" name="calcname" value="'+$('#'+id).attr("value")+'" />');
			}
			else{
			    $("#availability").remove();
			    $("#"+id).after('<span class="no">Already exists</span>');
			    $("#submit_calc").attr("disabled", "disabled");
			    //$("#submitOpt").children("img").remove();
			    //$.validationEngine.buildPrompt("input[id=calc_name]","this directory name already exists","error");
			}
		    }
		});
	    }
	//    else{
	//	if (!$("#availability").length){
	//	    $("#calc_name").next().remove();
	//	    $("#calc_name").after('<button id="availability">check availability</button>');
	//	    $("#availability").button();
	//	    $("#availability").click(function(){
	//		 checkAvailability($("#calc_name").attr("id"), '${c.prj_id}', $("#calc_name").attr("value"));
	//	    });
	//	}
	//    }
            
        }
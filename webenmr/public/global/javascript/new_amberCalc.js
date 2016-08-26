$(document).ready(function() {
                
//              $("#tabs").tabs();
//		$(".tabs-bottom .ui-tabs-nav, .tabs-bottom .ui-tabs-nav > *") 
// 		.removeClass("ui-corner-all ui-corner-top") 
//  		.addClass("ui-corner-bottom");

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
                    dataType:  'xml',  // 'xml', 'script', or 'json' (expected server response type) 
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
                            dataType:  "xml",        // 'xml', 'script', or 'json' (expected server response type) 
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
               
                initSander();
               
                var optionsSander = { 
                    //target:        '#output1',   // target element(s) to be updated with server response 
                    //beforeSubmit:   validatorRequest,  // pre-submit callback
                    dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
                    success:  processSanderSubmit   // post-submit callback 
                }; 
               
                // bind form using 'ajaxForm' 
                $('#submitSander').ajaxForm(optionsSander);
               
              //var optionsJobs = {
              //      action: "jobs/job_prepare",
              //      beforeSubmit:   addloading,  // pre-submit callback
              //      dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type) 
              //      success:  processSanderSubmit   // post-submit callback 
              //  }; 
              // 
              //   //bind form using 'ajaxForm' 
              //  $('#submitCalculation').ajaxForm(optionsJobs);
                
               
               $("#subCalc").button();
               $("#subCalc").click(function(){
                    $.ajax({
                        type: "POST",
                        timeout: 5000,
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
               
               
               
               $("#step1TOstep2").button();
               $("#step1TOstep2").click(function(){
                    //$("#tabs").tabs("enable", 1);
                    //$("#tabs").tabs( "option", "selected", 1 );
                    //$("#tabs").tabs("disable", 0);
               });
               
               $("#browser").hide();
               
               
               var atom1 = $("#atom1"),
			residue1 = $("#residue1"),
			atom2 = $("#atom2"),
                        residue2 = $("#residue2"),
			allFields = $([]).add(atom1).add(residue1).add(atom2).add(residue2),
			tips = $(".validateTips");
            
            

		function updateTips(t) {
			tips
				.text(t)
				.addClass('ui-state-highlight');
			setTimeout(function() {
				tips.removeClass('ui-state-highlight', 1500);
			}, 500);
		}

		function checkLength(o,n,min,max) {

			if ( o.val().length > max || o.val().length < min ) {
				o.addClass('ui-state-error');
				updateTips("Length of " + n + " must be between "+min+" and "+max+".");
				return false;
			} else {
				return true;
			}

		}

		function checkRegexp(o,regexp,n) {

			if ( !( regexp.test( o.val() ) ) ) {
				o.addClass('ui-state-error');
				updateTips(n);
				return false;
			} else {
				return true;
			}

		}

               $("#bond-form").dialog({
			autoOpen: false,
			//height: 360,
			//width: 350,
                        //position: 'center',
			modal: true,
			buttons: {
				'Create a bond': function() {
					var bValid = true;
					allFields.removeClass('ui-state-error');

					bValid = bValid && checkLength(atom1,"atom1",2,4);
					bValid = bValid && checkLength(residue1,"residue1",1,10000);
                                        bValid = bValid && checkLength(atom2,"atom2",2,4);
					bValid = bValid && checkLength(residue2,"residue2",1,10000);
					

					bValid = bValid && checkRegexp(atom1,/^([A-Z0-9])+$/i,"Atom may consist alpha-numeric characters A-Z 0-9.");
                                        bValid = bValid && checkRegexp(atom2,/^([A-Z0-9])+$/i,"Atom may consist of alpha-numeric characters A-Z 0-9.");
                                        bValid = bValid && checkRegexp(residue1,/^([0001-9999])+$/,"Residue field only allow numbers from 0001 to 9999");
                                        bValid = bValid && checkRegexp(residue2,/^([0001-9999])+$/,"Residue field only allow numbers from 0001 to 9999");
                                        
					// From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
					// bValid = bValid && checkRegexp(email,/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i,"eg. ui@jquery.com");
					//bValid = bValid && checkRegexp(password,/^([0-9a-zA-Z])+$/,"Password field only allow : a-z 0-9");
					
					if (bValid) {
                                            var id = residue1.val()+'_'+residue2.val();
                                            $('#bond-item').children("#items").append('<div>' +
                                                '<a id="'+id+'" href="javascript:remove_item(\''+id+'\')"><img src="/global/images/cancel.png" border="0"/></a>'+
                                                '<span>' +
                                                    residue1.val() + '--' + atom1.val() + '</span>' + 
                                                    '&lt;--&gt;' + '<span>' + residue2.val() + '--' + atom2.val() + '</span>' +
                                                    '</div>');
                                            var hdds = '<input type="hidden" name="residue1" value="'+residue1.val()+'"/>';
                                            hdds +=  '<input type="hidden" name="atom1" value="'+atom1.val()+'"/>';
                                            hdds += '<input type="hidden" name="residue2" value="'+residue2.val()+'"/>';
                                            hdds +=  '<input type="hidden" name="atom2" value="'+atom2.val()+'"/>';
                                            $('#bond-item').children("#items").children("div").last().append(hdds);
                                            residue1.attr("value", "");
                                            atom1.attr("value", "");
                                            residue2.attr("value", "");
                                            atom2.attr("value", "");
                                            $(this).dialog('close');
					}
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			},
			close: function() {
				allFields.val('').removeClass('ui-state-error');
			}
		});
                
                
                var solvent = $("#solvent"),
                    geometry = $("#geometry"),
                    distance = $("#distance"),
                    allFields = $([]).add(solvent).add(geometry).add(distance),
                    tips = $(".validateTips");
                
                $("#solvent-form").dialog({
			autoOpen: false,
			height: 450,
			width: 400,
                        position: 'center',
			modal: true,
			buttons: {
				'add a solvent': function() {
					var bValid = true;
					allFields.removeClass('ui-state-error');

					//bValid = bValid && checkLength(atom1,"atom1",2,4);
					//bValid = bValid && checkLength(residue1,"residue1",1,10000);
                                        //bValid = bValid && checkLength(atom2,"atom2",2,4);
					//bValid = bValid && checkLength(residue2,"residue2",1,10000);
					

					//bValid = bValid && checkRegexp(atom1,/^([A-Z])+$/i,"Atom may consist of characters A-Z.");
                                        //bValid = bValid && checkRegexp(atom2,/^([A-Z])+$/i,"Atom may consist of characters A-Z.");
                                        //bValid = bValid && checkRegexp(residue1,/^([0001-9999])+$/,"Residue field only allow numbers from 0001 to 9999");
                                        //bValid = bValid && checkRegexp(residue2,/^([0001-9999])+$/,"Residue field only allow numbers from 0001 to 9999");
                                        
					// From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
					// bValid = bValid && checkRegexp(email,/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i,"eg. ui@jquery.com");
					//bValid = bValid && checkRegexp(password,/^([0-9a-zA-Z])+$/,"Password field only allow : a-z 0-9");
					
					if (bValid) {
                                            $('#solvent-item').children("#items").append('<div>' +
                                                    '<a id="'+solvent.val()+'" href="javascript:remove_item(\''+solvent.val()+'\')"><img src="/global/images/cancel.png" border="0"/></a>'+
                                                    '<span>Solvent: '+solvent.val() + ' Geometry: ' + geometry.val() + ' Distance: '+distance.val()+'</span>' + 
                                                    '</div>');
                                            var hdds = '<input type="hidden" name="solvent" value="'+solvent.val()+'"/>';
                                            hdds +=  '<input type="hidden" name="geometry" value="'+geometry.val()+'"/>';
                                            hdds +=  '<input type="hidden" name="resid" value="'+$("#resid").val()+'"/>';
                                            hdds += '<input type="hidden" name="distance" value="'+distance.val()+'"/>'
                                            $('#solvent-item').children("#items").children("div").last().append(hdds);
                                            $('option:selected', solvent).removeAttr('selected');
                                            $('option:selected', geometry).removeAttr('selected');
                                            distance.attr("value", "");
                                            $(this).dialog('close');
                                            //$("#solv").children("a").removeAttr("href");
                                            $("#solv").children("a").attr("style", "text-decoration: none;");
                
					}
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			},
			close: function() {
				allFields.val('').removeClass('ui-state-error');
			}
		});
                
                var ion = $("#ion"),
			number = $("#number"),
			//allFields = $([]).add(ion).add(number),
			tips = $(".validateTips");
                
                $("#ion-form").dialog({
			autoOpen: false,
			height: 260,
			width: 350,
                        position: 'center',
			modal: true,
			buttons: {
				'add ion': function() {
					var bValid = true;
					allFields.removeClass('ui-state-error');

					//bValid = bValid && checkLength(atom1,"atom1",2,4);
					//bValid = bValid && checkLength(residue1,"residue1",1,10000);
                                        //bValid = bValid && checkLength(atom2,"atom2",2,4);
					//bValid = bValid && checkLength(residue2,"residue2",1,10000);
					

					//bValid = bValid && checkRegexp(atom1,/^([A-Z])+$/i,"Atom may consist of characters A-Z.");
                                        //bValid = bValid && checkRegexp(atom2,/^([A-Z])+$/i,"Atom may consist of characters A-Z.");
                                        //bValid = bValid && checkRegexp(residue1,/^([0001-9999])+$/,"Residue field only allow numbers from 0001 to 9999");
                                        //bValid = bValid && checkRegexp(residue2,/^([0001-9999])+$/,"Residue field only allow numbers from 0001 to 9999");
                                        
					// From jquery.validate.js (by joern), contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
					// bValid = bValid && checkRegexp(email,/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i,"eg. ui@jquery.com");
					//bValid = bValid && checkRegexp(password,/^([0-9a-zA-Z])+$/,"Password field only allow : a-z 0-9");
					
					if (bValid) {
                                            $('#ion-item').children("#items").append('<div>' +
                                                    '<a id="'+ion.val()+'" href="javascript:remove_item(\''+ion.val()+'\')"><img src="/global/images/cancel.png" border="0"/></a>'+
                                                    '<span>Ion: '+ion.val() + ' Number: '+number.val()+'</span>' + 
                                                    '</div>');
                                            var hdds = '<input type="hidden" name="ion" value="'+ion.val()+'"/>';
                                            hdds +=  '<input type="hidden" name="number" value="'+number.val()+'"/>';
                                            $('#ion-item').children("#items").children("div").last().append(hdds);
                                            $('option:selected', ion).removeAttr('selected');
                                            number.val("");
                                            $(this).dialog('close');
                                            //$("#ions").children("a").removeAttr("href");
                                            $("#ions").children("a").attr("style", "text-decoration: none;");
					}
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			},
			close: function() {
				allFields.val('').removeClass('ui-state-error');
			}
		});
		
                
                $("#born-form").dialog({
			autoOpen: false,
			height: 200,
			width: 380,
                        position: 'center',
			modal: true,
			buttons: {
				'Yes': function() {
                                    $('#born-item').children("#items").append('<div>' +
                                            '<a id="born_a_yes" href="javascript:remove_item(\'born_a_yes\')"><img src="/global/images/cancel.png" border="0"/></a>'+
                                            '<span>Born radius: yes </span>' + 
                                            '</div>');
                                    var hdds = '<input type="hidden" name="born" value="yes"/>';
                                    $('#born-item').children("#items").children("div").last().append(hdds);
                                    $(this).dialog('close');
                                    $("#born").children("a").removeAttr("href");
                                    $("#born").children("a").attr("style", "text-decoration: none;");
				},
				
                                'No': function() {
                                    $('#born-item').children("#items").append('<div>' +
                                            '<a id="born_a_no" href="javascript:remove_item(\'born_a_no\')"><img src="/global/images/cancel.png" border="0"/></a>'+
					    '<span>Born radius: no </span></div>');
                                    var hdds = '<input type="hidden" name="born" value="no"/>';
                                    $('#born-item').children("#items").children("div").last().append(hdds);
				    $(this).dialog('close');
                                    $("#born").children("a").attr("disabled", "disabled");
                                },
                                
				Cancel: function() {
					$(this).dialog('close');
				}
			},
			close: function() {
				allFields.val('').removeClass('ui-state-error');
			}
		});
		
		
                
		$('#add-bond')
			.button()
			.click(function() {
				$('#bond-form').dialog('open');
			});

               
               
            });
            function add_bond(){
                    $('#bond-form').dialog('open');
            }
            
            function add_solvent(){
                    $('#solvent-form').dialog('open');
            }
            
            function checkSolvate(id){
                $("#lres").remove();
                $("#residspan").remove();
                $("#resid").remove();
                $("#ldistance").html("Distance (&Aring;)")
                if ($("#"+id).val() == 'scap'){
                    var res = '<label id="lres" for="resid">Center of sphere</label>'+
                        '<input type="text" name="resid" id="resid" /><span id="residspan">(residue number)</span>';
                    $("#"+id).after(res);
                    $("#ldistance").html("Size of sphere radius");
                }
                else if ($("#"+id).val() == 'sshell'){
                    //var res = '<label id="lres" for="resid">Closeness</label>'+
                    //'<input type="text" name="shellclos" id="shellclos" />';
                    //$("#"+id).after(res);
                    $("#ldistance").html("Thickness (&Aring;)");
                }
            }
            
            function add_ion(){
                    $('#ion-form').dialog('open');
            }
            
            function add_born(){
                    $('#born-form').dialog('open');
            }
            
            function remove_item(obj_id){
                var type = $("#"+obj_id).parent().parent().parent().attr("id").split('-')[0];
                if (type != "bond"){
                    $("#"+type).children("a").removeAttr("style");
                    $("#"+type).children("a").attr("href", "javascript:add_"+type+"();");
                }
                $("#"+obj_id).parent().remove();
            }
    
    

    
            
            function addInfoProtocol(){
                var nrStep = $("#protocol").children("div").length;
                $("#submitCalculation").children("#submitOpt").children("input[name=step]").remove();
                $("#submitCalculation").children("#submitOpt").append('<input type="hidden" value="'+nrStep+'" name="step">');
            }
            
            function show_subwindow(id){
                $.ajax({
                    type: "GET",
                    url: "/structureUpload/get_sanderConfig",
                    dataType: "xml",
                    success: function(xml) {
                        var param = $(xml).find('PARAMETER').children("ID").filter(function(index) {
                                return (id == $(this).text());
                        }).parent();
                        var sub = $("#sub_window").empty();
                        $(param).children('FLAG').each(function(){
                                var info = '<a href="javascript:info(\''+$(this).children("NAME").text()+'\')"><img src="/global/images/info.png" border="0" title="click to obtain more info on it" /></a> ';
                                var values = $(this).children('VALUE');
                                
                                if (values.length == 1){
                                    var tag = info + '<label for="ifield" class="lsander">'+$(this).find("NAME").text()+' </label><input id="ifield" class="field" name="'+$(this).find("NAME").text()+'" type="text" size=4 value="'+values.find("AMOUNT").text()+'" /><br />';
                                    var div_item = '<div id="sitem">'+tag+'</div>';
                                    //sub.append(div_item);
                                }
                                else if(values.length == 0){
                                    var tag = info + '<label for="ifield" class="lsander">'+$(this).find("NAME").text()+' </label><input id="ifield" class="field" name="'+$(this).find("NAME").text()+'" type="text" size=4 /><br />';
                                    var div_item = '<div id="sitem">'+tag+'</div>';
                                    //sub.append(div_item);
                                }
                                else{
                                    var tag = info + '<label for="sfield" class="lsander">'+$(this).find("NAME").text()+' </label><select id="sfield" name="'+$(this).find("NAME").text()+'" >';
                                    values.each(function(){
                                        if($(this).attr("default") == 'yes'){
                                            tag += '<option value="'+$(this).find("AMOUNT").text()+'" selected>'+$(this).find("AMOUNT").text()+'</option>';
                                        }
                                        else{
                                            tag += '<option value="'+$(this).find("AMOUNT").text()+'" >'+$(this).find("AMOUNT").text()+'</option>';
                                        }
                                    });
                                    tag += '</select><br />';
                                    var div_item = '<div id="sitem">'+tag+'</div>';
                                    //sub.append(div_item);
                                }
                                sub.append(div_item);
                        });
                    }
                });
            }
            
            function initSander(){
                
                $.ajax({
                    type: "GET",
                    url: "/structureUpload/get_sanderConfig",
                    dataType: "xml",
                    success: function(xml) {
                        //var menu = '<ul id="nav">';
                        //$(xml).find('PARAMETER').each(function(){
                        //    //if($(this).children("TARGET").text() == section){
                        //    var name_par = $(this).children("NAME").text();
                        //    var id = $(this).children("ID").text();
                        //    var title = '<h3><a href="#">'+name_par+'</a></h3>';
                        //    //menu += '<li><a href="javascript:show_subwindow(\''+id+'\')">'+name_par+'</a></li>';
                        //    //$("#some").append('<br />'+name_par+':<br />')
                        //    var div_par = '<div id="sparam"></div>';
                        //    $("#accordion").append(title+div_par);
                        //    
                        //    $(this).children('FLAG').each(function(){
                        //        //if($(this).attr('type') == 'basic'){
                        //        //    $("#some").append($(this).find('NAME').text()+'<BR />');
                        //        //}
                        //        var name = $(this).children("NAME").text();
                        //        
                        //        var info = '<a href="javascript:info(\''+name+'\')"><img src="/global/images/info.png" border="0" title="click to obtain more info on it" /></a> ';
                        //        var values = $(this).children('VALUE');
                        //        
                        //        if (values.length == 1){
                        //            var tag = info + '<label for="ifield" class="lsander">'+name+' </label><input id="i'+name+'" class="field" name="'+name+'" type="text" size=4 value="'+values.find("AMOUNT").text()+'" /><br />';
                        //            var div_item = '<div id="sitem">'+tag+'</div>';
                        //            $("#accordion").children('div').last().append(div_item);
                        //        }
                        //        else if(values.length == 0){
                        //            var tag = info + '<label for="ifield" class="lsander">'+name+' </label><input id="i'+name+'" class="field" name="'+name+'" type="text" size=4 /><br />';
                        //            var div_item = '<div id="sitem">'+tag+'</div>';
                        //            $("#accordion").children('div').last().append(div_item);
                        //        }
                        //        else{
                        //            var tag = info + '<label for="sfield" class="lsander">'+name+' </label><select id="s'+name+'" name="'+name+'" >';
                        //            values.each(function(){
                        //                if($(this).attr("default") == 'yes'){
                        //                    tag += '<option value="'+$(this).find("AMOUNT").text()+'" selected>'+$(this).find("AMOUNT").text()+'</option>';
                        //                }
                        //                else{
                        //                    tag += '<option value="'+$(this).find("AMOUNT").text()+'" >'+$(this).find("AMOUNT").text()+'</option>';
                        //                }
                        //            });
                        //            tag += '</select><br />';
                        //            var div_item = '<div id="sitem">'+tag+'</div>';
                        //            $("#accordion").children('div').last().append(div_item);
                        //        }
                        //    });
                        //    //}
                        //});
                        load_sander_data("cntrl", "basic");
                        var hdd = '<input type="hidden" value="cntrl" name="section">';
                        $("#sander_control").append(hdd);
                        var hdd1 = '<input type="hidden" value="'+$("input[name='mode']:checked").val()+'" name="type">';
                        $("#sander_control").append(hdd1);
                        //menu += '</ul>';
                        //$("#menu").append(menu);
                        
                        $("#accordion").accordion({
                            autoHeight: false,
                            //navigation: true,
                            collapsible: true
                        });
                        
                        $('.accordion .head').click(function() {
                                $(this).next().toggle('slow');
                                return false;
                        }).next().hide();
                    }
                });
                $("#lt").button();
                $("#lt").click(function() {
                    $("#sander-params").children("#sander-out").hide();
                    $("#lt").hide();
                    $("#st").hide();
                    $("#browser").show();
                    $("#browser").fileTree({
                            root: "protocols",
                            script: '/filesystem/dirlist',
                            expandSpeed: 750,
                            collapseSpeed: 750,
                            //folderEvent: 'dbclick',
                            multiFolder: false
                        }, function(file) {
                            var filename= file;
                            $.ajax({
                               type: "POST",
                               url: "/structureUpload/load_template",
                               data: "filename="+filename,
                               dataType: "xml",
                               success: function(xml) {
                                    $("#sander-params").children("#sander-out").show();
                                    show_sander(xml);
                                    $("#browser").empty();
                                    $("#browser").hide();
                                    $("#lt").show();
                                    $("#st").show();
                                    $('#tabs').tabs({ disabled: [] });
                                }
                            });
                        });
                });
                    
                //$("#st").button();
                //$("#st").click(function() {
                //    alert("saving template...")
                //});
                
                $("#rp").button();
                $("#rp").click(function() {
                    if ($("#sander-out").children("div[id=protocol]").length){
                        $("#sander-out").children("a").remove();
                        $("#sander-out").children("img").remove();
                        $("#sander-out").children("div[id=protocol]").remove();
                        $("#sander-out").append('<span id="small">you can load or create your protocol</span>');
                    }
                    if ($("#browser[style=display: none;]").length == 0){
                        $("#browser").attr("style", "display:none;");
                        $("#sander-out").removeAttr("style");
                        $("#lt").removeAttr("style");
                    }
                    else{
                        $("#sander-out").children("a").remove();
                        $("#sander-out").children("div[id=protocol]").remove();
                        $('#tabs').tabs("disable", 3 );
                    }
                    $.validationEngine.closePrompt("fieldset[id=sander-out]");
                });
                
                $("#submitSander").button();
                $("#submitSander").click(function() {
                    //$('#submitSander').ajaxSubmit(); 
                });
                
                $("#bcontrol").button();
                $("#bcontrol").click(function(){
                    $("#sander_control").children("input[type='hidden']").remove();
                    load_sander_data("cntrl", $("input[name='mode']:checked").val());
                    var hdd = '<input type="hidden" value="cntrl" name="section" />';
                    $("#sander_control").append(hdd);
                    var hdd1 = '<input type="hidden" value="'+$("input[name='mode']:checked").val()+'" name="type" />';
                    $("#sander_control").append(hdd1);
                    
                });
                $("#bewald").button();
                $("#bewald").click(function(){
                    $("#sander_control").children("input[type='hidden']").remove();
                    load_sander_data("ewald", $("input[name='mode']:checked").val());
                    var hdd = '<input type="hidden" value="ewald" name="section" />';
                    $("#sander_control").append(hdd);
                    var hdd1 = '<input type="hidden" value="'+$("input[name='mode']:checked").val()+'" name="type" />';
                    $("#sander_control").append(hdd1);
                });
                $("#bwt").button();
                $("#bwt").click(function(){
                    $("#sander_control").children("input[type='hidden']").remove();
                    load_sander_data("wt", $("input[name='mode']:checked").val());
                    var hdd = '<input type="hidden" value="wt" name="section" />';
                    $("#sander_control").append(hdd);
                    var hdd1 = '<input type="hidden" value="'+$("input[name='mode']:checked").val()+'" name="type" />';
                    $("#sander_control").append(hdd1);
                });
                $("#bdebug").button();
                $("#bdebug").click(function(){
                    $("#sander_control").children("input[type='hidden']").remove();
                    load_sander_data("debugf", $("input[name='mode']:checked").val());
                    var hdd = '<input type="hidden" value="debugf" name="section" />';
                    $("#sander_control").append(hdd);
                    var hdd1 = '<input type="hidden" value="'+$("input[name='mode']:checked").val()+'" name="type" />';
                    $("#sander_control").append(hdd1);
                });
                
                $("#bmode").click(function(){
                    load_sander_data($("input[name='section']").attr("value"), "basic");
                });
                
                $("#emode").click(function(){
                    load_sander_data($("input[name='section']").attr("value"), "expert");
                });
            }
            
            function load_sander_data(section, mode){
                $.ajax({
                    type: "GET",
                    url: "/structureUpload/get_sanderConfig",
                    dataType: "xml",
                    success: function(xml) {
                        //var menu = '<ul id="nav">';
                        $("#accordion").remove();
                        $("#tabs-3").append('<div id="accordion"></div>');
                        $(xml).find('PARAMETER').each(function(){
                            if($(this).children("TARGET").text() == section){
                                var name_par = $(this).children("NAME").text();
                                var id = $(this).children("ID").text();
                                var title = '<h3><a href="#">'+name_par+'</a></h3>';
                                //menu += '<li><a href="javascript:show_subwindow(\''+id+'\')">'+name_par+'</a></li>';
                                //$("#some").append('<br />'+name_par+':<br />')
                                var div_par = '<div id="sparam"></div>';
                                $("#tabs-3").children("div[id='accordion']").append(title+div_par);
                                
                                $(this).children('FLAG').filter(function(index){
                                        if(mode == "basic"){
                                            return $(this).attr("type") == mode;
                                        }
                                        else{
                                            return true;
                                        }
                                        
                                    }).each(function(){
                                        var name = $(this).children("NAME").text();
                                        
                                        var info = '<a href="javascript:info(\''+name+'\')"><img src="/global/images/info.png" border="0" title="click to obtain more info on it" /></a> ';
                                        var values = $(this).children('VALUE');
                                        
                                        if (values.length == 1){
                                            var tag = info + '<label for="ifield" class="lsander">'+name+' </label><input id="i'+name+'" class="field" name="'+name+'" type="text" size=4 value="'+values.find("AMOUNT").text()+'" /><br />';
                                            var div_item = '<div id="sitem">'+tag+'</div>';
                                            $("#tabs-3").children("div[id='accordion']").children('div').last().append(div_item);
                                        }
                                        else if(values.length == 0){
                                            var tag = info + '<label for="ifield" class="lsander">'+name+' </label><input id="i'+name+'" class="field" name="'+name+'" type="text" size=4 /><br />';
                                            var div_item = '<div id="sitem">'+tag+'</div>';
                                            $("#tabs-3").children("div[id='accordion']").children('div').last().append(div_item);
                                        }
                                        else{
                                            var tag = info + '<label for="sfield" class="lsander">'+name+' </label><select id="s'+name+'" name="'+name+'" >';
                                            values.each(function(){
                                                if($(this).attr("default") == 'yes'){
                                                    tag += '<option value="'+$(this).find("AMOUNT").text()+'" selected>'+$(this).find("AMOUNT").text()+'</option>';
                                                }
                                                else{
                                                    tag += '<option value="'+$(this).find("AMOUNT").text()+'" >'+$(this).find("AMOUNT").text()+'</option>';
                                                }
                                            });
                                            tag += '</select><br />';
                                            var div_item = '<div id="sitem">'+tag+'</div>';
                                            $("#tabs-3").children("div[id='accordion']").children('div').last().append(div_item);
                                        }
                                        $("#tabs-3").children("div[id='accordion']").children('div').last().last().children().children().filter("input").keyup(function(){
                                            addFlag($(this).attr("name"), $(this).attr("value"));
                                        });
                                        
                                        $("#tabs-3").children("div[id='accordion']").children('div').last().children().last().children().filter("select").change(function(){
                                            
                                            addFlag($(this).attr("name"), $(this).val());
                                        });
                                    });
                                    $("#tabs-3").children("div[id='accordion']").children("div").filter(function(){
                                        if ($(this).children().length == 0){
                                            $(this).prev().remove();
                                            return true;
                                        }
                                        return false;
                                    }).remove();
                            }
                        });
                        $("#tabs-3").children("div[id='accordion']").accordion({
                            autoHeight: false,
                            //navigation: true,
                            collapsible: true
                        });
                        
                        $('.accordion .head').click(function() {
                                $(this).next().toggle('slow');
                                return false;
                        }).next().hide();
                    }
                });
            }
            
            
            function addFlag(name, value){
                $("#tabs").tabs("enable", 3);
                //var charat = rname.charAt(0);
                //var name = rname.split(charat)[1];
                var section = $("input[name='section']").attr("value");
                //se name esiste modifica altrimenti [se non c'è la sezione creala, inserisci]
                var thereisprotocol = $("#sander-out").children("#protocol").length;
                if(thereisprotocol){
                    activestep = $("#sander-out").children("#protocol").accordion( "option", "active" );
                    div_activestep = $("#sander-out").children("#protocol").children("div:eq("+activestep+")");
                    div_section = div_activestep.children("div[id="+section+"]");
                    if (div_section.length){
                        var div_target = div_section.children("#flag-items").children("#"+name.toLowerCase());
                            if(div_target.length){
                                div_target.children("input").attr("value", value);
                            }
                            else{
                                var new_flag = '<div id="'+name.toLowerCase()+'">'+
                                                    name.toLowerCase()+
                                                    ' = <input type="text" readonly="readonly" value="'+value+'" style="border: medium none;" size="5" />'+
                                                '</div>';
                                div_section.children("#flag-items").append(new_flag);
                            }
                    }
                    else{
                        var new_flag = '<div id="'+name.toLowerCase()+'">'+
                                            name.toLowerCase()+
                                            ' = <input type="text" readonly="readonly" value="'+value+'" style="border: medium none;" size="5" />'+
                                        '</div>';
                            //$("#sander-out").children("div").filter("[id="+section+"]").children("#flag-items").append(new_flag);
                            var istheresander = $(div_activestep).find("div[id=sander_file]");
                            if(istheresander.length){
                                $(istheresander).before(new_flag);
                            }
                            else{
                                $(div_activestep).append(new_flag);
                            }
                    }
                        
                }
                else{
                    var new_prot = '<div id="protocol">'+
                                        '<h2><a href="#" tabindex="-1">new protocol</a></h2>'+
                                        '<div>'+
                                            '<div id="'+section+'">'+
                                                '<span>&amp;'+section+'</span>'+
                                                '<div id="flag-items">'+
                                                    '<div id="'+name.toLowerCase()+'">'+name.toLowerCase()+
                                                    ' = <input type="text" readonly="readonly" value="'+value+'" style="border: medium none;" size="5" />'+
                                                '</div>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>';
                    $("#sander-out").children("span").remove();                
                    $("#sander-out").append(new_prot);
                    
                    $("#sander-out").children("#protocol").accordion({
                            autoHeight: false,
                            //navigation: true,
                            collapsible: true
                        });
                        
                        $('.accordion .head').click(function() {
                                $(this).next().toggle('slow');
                                return false;
                        }).next().hide();
                }
                //alert($("#noeUpload").find("#noe-item").children().length);
                //alert($("#sander-out").find("#sander_file").length);
                if((($("#noe-item").children().length) || ($("#dihedral-item").children().length) || ($("#rdc-item").children().length) || ($("#pcs-item").children().length))&&(!$("#sander-out").find("#sander_file").length)){
                    if(($("#noe-item").children().length)||($("#dihedral-item").children().length)){
                        var noe = '1';
                    }
                    else{
                        var noe = '0';
                    }
                    
                    if(($("#rdc-item").children().length)||($("#pcs-item").children().length)){
                        var rdc = '1';
                    }
                    else{
                        var rdc = '0';
                    }
                    var sander = retrieveCostraints(noe, rdc);
                    activestep = $("#sander-out").children("#protocol").accordion( "option", "active" );
                    div_activestep = $("#sander-out").children("#protocol").children("div:eq("+activestep+")");
                    div_activestep.append(sander);
                    
                }
                
                $("#flag-items div").contextMenu({
                    menu: 'sanderMenu'
                    },
                    function(action, el, pos) {
                    //alert(
                    //        'Action: ' + action + '\n\n' +
                    //        'Element ID: ' + $(el).attr('id') + '\n\n' + 
                    //        'X: ' + pos.x + '  Y: ' + pos.y + ' (relative to element)\n\n' + 
                    //        'X: ' + pos.docX + '  Y: ' + pos.docY+ ' (relative to document)'
                    //);
                    if (action == 'edit'){
                        $(el).children("input").removeAttr("readonly");
                        $(el).children("input").removeAttr("style");
                        $(el).children("input").select();
                        $(el).children("input").blur(function(){
                            $(el).children("input").attr("readonly", "readonly");
                            $(el).children("input").attr("style", "border: none");
                        })
                        
                    }
                    else{
                         //se la sezione corrente contiene una sola voce
                            var parent = $(el).parent();
                            if (!$(el).siblings().length){
                                //se ci sono altre sezioni nello step attivo
                                if(parent.parent().siblings().length){
                                    //rimuovi intera sezione
                                    parent.parent().remove();
                                }
                                else{
                                    //rimuovi intero step attivo
                                    grandParent = parent.parent().parent();
                                    grandParent.prev().remove();
                                    grandParent.remove();
                                }
                            }
                            else{
                                $(el).remove();  
                            }
                    }
                });
            }
            
            function show_sander(data){
                var miss_restraint = false;
                var idx = 0;
                var str = '<div id="protocol">';
                $(data).find("calculation").each(function(){
                    idx = idx + 1; 
                    str +='<h2 id="'+idx+'"><a href="#">'+$(this).find('description').text()+'</a></h2>';
                    str += '<div>';
                    str += '<div id="cntrl"><span>&cntrl</span>';
                    str += '<div id="flag-items">';
                    $(this).find('cntrl').find('flag').each(function(){
                        var flag = $(this).children('name').text();
                        var value = $(this).children('value').text();
                        str += '<div id="'+flag+'">'+flag+' = <input type="text" size="10" style="border: none" value="'+value+'" readonly="readonly"</input></div>';
                    });
                    str += '</div>';
                    str += '</div>';
                    if($(this).find('ewald').length){
                        str += '<div id="ewald"><span>&ewald</span>';
                        str += '<div id="flag-items">';
                        $(this).find('ewald').find('flag').each(function(){
                            var flag = $(this).children('name').text();
                            var value = $(this).children('value').text();
                            str += '<div id="'+flag+'">'+flag+' = <input type="text" size="10" style="border: none" value="'+value+'" readonly="readonly"</input></div>';
                        });
                        str += '</div>';
                        str += '</div>';
                    }
                    if($(this).find('wt').length){
                        $(this).find('wt').each(function(){
                            str += '<div id="wt"><span>&wt</span>';
                            str += '<div id="flag-items">';
                            $(this).find('flag').each(function(){
                                var flag = $(this).children('name').text();
                                var value = $(this).children('value').text();
                                str += '<div id="'+flag+'">'+flag+' = <input type="text" size="10" style="border: none" value="'+value+'" readonly="readonly"</input></div>';
                            });
                            str += '</div>';
                            str += '</div>';
                        });
                    }
                    var noe = $(this).children('noe').text();
                    var rdc = $(this).children('rdc').text();
                    var noe_item = $("#noe-item").children();
                    var dih_item = $("#dihedral-item").children();
                    var rdc_item = $("#rdc-item").children();
                    var pcs_item = $("#pcs-item").children();
                    //if (((noe == '1')  && ((!noe_item.length) && (!dih_item.length))) || ((rdc == '1')  && ((!rdc_item.length) && (!pcs_item.length)))){
                    //    miss_restraint = true;
                    //}
                    if (noe == '1'){
                        if (!noe_item.length && !dih_item.length && !rdc_item.length && !pcs_item.length){
                                miss_restraint = true;
                        }        
                    }
                    
                        
                    
                    //alert(noe+' '+rdc);
                    if((noe=='1')|| (rdc=='1')){
                        var sander_constraint = retrieveCostraints(noe, rdc);
                        str += sander_constraint;    
                    }
                    
                    str += '</div>';
                    //str += '<div id="infoSander>"';
                    //var noe = $(this).find('noe').text();
                    //var rdc = $(this).find('rdc').text();
                    //var list = $(this).find('list').text();
                    //str += '<input type="hidden" value="'+noe+'??'+rdc+'??'+list+'" name="infoRestraints">';
                    //str +="</div>";
                });
                str += '</div>';
                
                
                if (!miss_restraint){
                    $("#sander-params").children("fieldset").empty();
                    $("#sander-params").children("fieldset").append("<legend>sander protocol</legend>");
                    $("#sander-params").children("fieldset").append(str);
                    if($(data).find("summary").text() !== ""){
                                //alert("ho letto");
                        $("#sander-out").prepend('<a href="javascript:open_dialog(\'protocol description\', \''+$(data).find("summary").text()+'\', 400, 500);">protocol description</a><img src="/global/images/read.png"</img>');
                    }
                    if($(data).find("gpu").text() !== ""){
                         //var bla =$('#select-cpugpu').val();
                         //alert(bla);
                        $('#select-cpugpu').val('calcgpu');
                        //var bla =$('#select-cpugpu').val();
                         //alert(bla);
                        } else{
                            $('#select-cpugpu').val('calccpu');
                            //var bla =$('#select-cpugpu').val();
                         //alert(bla);
                        }
                    $("#protocol").accordion({
                                autoHeight: false,
                                navigation: false,
                                collapsible: true
                            });
                            
                    $('.accordion .head').click(function() {
                            $(this).next().toggle('slow');
                            return false;
                    }).next().hide();
                    
                    $("#flag-items div").contextMenu({
                        menu: 'sanderMenu'
                        },
                        function(action, el, pos) {
                        //alert(
                        //        'Action: ' + action + '\n\n' +
                        //        'Element ID: ' + $(el).attr('id') + '\n\n' + 
                        //        'X: ' + pos.x + '  Y: ' + pos.y + ' (relative to element)\n\n' + 
                        //        'X: ' + pos.docX + '  Y: ' + pos.docY+ ' (relative to document)'
                        //);
                        if (action == 'edit'){
                            $(el).children("input").removeAttr("readonly");
                            $(el).children("input").removeAttr("style");
                            $(el).children("input").select();
                            $(el).children("input").blur(function(){
                                $(el).children("input").attr("readonly", "readonly");
                                $(el).children("input").attr("style", "border: none");
                            })
                        }
                        else{
                            //se la sezione corrente contiene una sola voce
                            var parent = $(el).parent();
                            if (!$(el).siblings().length){
                                //se ci sono altre sezioni nello step attivo
                                if(parent.parent().siblings().length){
                                    //rimuovi intera sezione
                                    parent.parent().remove();
                                }
                                else{
                                    //rimuovi intero step attivo
                                    grandParent = parent.parent().parent();
                                    grandParent.prev().remove();
                                    grandParent.remove();
                                }
                            }
                            else{
                                $(el).remove();  
                            }
                        }
                    });
                    $("#cntrl").children("#flag-items").sortable();
                    //$("#cntrl").children("#flag-items").disableSelection();
                    $.validationEngine.closePrompt('#sander-out');
                }
                else{
                    if ($("#sander-out").children("div[id=protocol]").length){
                        $("#sander-out").children("a").remove();
                        $("#sander-out").children("img").remove();
                        $("#sander-out").children("div[id=protocol]").remove();
                        $("#sander-out").append('<span id="small">you can load or create your protocol</span>');
                    }
                    if ($("#browser[style=display: none;]").length == 0){
                        $("#browser").attr("style", "display:none;");
                        $("#sander-out").removeAttr("style");
                        $("#lt").removeAttr("style");
                    }
                    else{
                        $("#sander-out").children("a").remove();
                        $("#sander-out").children("div[id=protocol]").remove();
                        $('#tabs').tabs("disable", 3 );
                    }
                    $.validationEngine.buildPrompt("#sander-out", "the selectect protocol requires some restraints file. First upload them.","error");
                }
                
                
                
            }
            
            function info(flag){
                $.ajax({
                       type: "GET",
                       url: "/structureUpload/get_sanderConfig",
                       dataType: "xml",
                       success: function(xml) {
                           $(xml).find('FLAG').each(function(){
                               if ($(this).children("NAME").text() == flag){
                                   var help = $(this).children("HELP").text();
                                   open_dialog("More info on "+flag, help , 600, 400);
                               }
                           });
                       }
                });
            }
            
            
            function processSanderSubmit(response){
                window.location.href = '/jobs/show/all';
            }
    
            
            
            function create_summary(){
                
                $("#structSummary").empty().append("Structures:<br/>");
                $("#structSummary").append($("#chain_protein").children().filter("span[name=protein_name]"));
                
                $("#noStdResSummary").empty().append("Non-standard residues:<br />")
                $("#noStdResSummary").append($("#amino-item").children());
                
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
                //alert(id)
                var inputfile = id.split('--')[1];
                
                
                
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
                var div_chain = $("#"+prefix+"-item");
                var wait = '<img id="loading" src="/global/images/loading.gif">';
                div_chain.append(wait);
                var id_dest = prefix+"-item";
                var filename = $("input[id="+id+"]").attr("value");
                filename_list = filename.split('\\');
                if (filename_list.length){
                    filename = filename_list[filename_list.length - 1];
                }
                var valid = 1;
                var notfound = 1
                var cntItem = $("#"+prefix+"-item").children("div[id="+prefix+"::"+filename.split('.')[0]+"]");
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
                    var tagFilename = '<div id="'+prefix+'--'+filename.split('.')[0]+'"><a id="'+prefix+'--a--'+filename.split('.')[0]+'" href="javascript:removeUploadedFile(\''+prefix+'--a--'+filename.split('.')[0]+'\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a>'+
                    '<span name="protein_name"> '+filename+' </span></div>';
                    
                    //inserire la voce nel div chain-item
                    $("#"+id_dest).append(tagFilename);
                    
                    $("#advanced-setting").removeAttr("style");
                    //runEffect();
                   
                    
                    //ajax per l'upload vero e proprio
                    $("#field").attr("value", id);
                    var hdd = '<input type="hidden" value="'+filename+'" name="protein_name" id="protein_name">';
                    $("#submit").append(hdd);
                    var options = {
                        url: "/structureUpload/upload",
                        dataType:  "xml",        // 'xml', 'script', or 'json' (expected server response type) 
                        success:  function(response, status){
                            $('#chain_file_div').html($('#chain_file_div').html());

                            //$('input[id='+id+']').attr("value", "");
                            if ($.browser.msie){
                                data = response;
                            }
                            else{
                                data = (new XMLSerializer()).serializeToString(response);    
                            }
                            processUploadedFile(id, data);
                            enableTabs();
                            $.validationEngine.closePrompt("select[id=force_fields]");
                        }
                    };
                    $("#"+form).ajaxSubmit(options);
                    
                    //$("#"+id).attr("value", "");
                }
                else if(!notfound){
                    $("input[id="+id+"]").attr("value", "");
                    open_dialog("WARNING","You are already uploaded a file with same filename.", 570, 150)
                    $("#chain-item").children("#loading").remove();
                    //piccola dialog che avvisa che file già inserito
                }
            }
            
            function show_wait(){
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
                $.modal('<div><img src="/global/images/loading2.gif"></div>', option);
            }
            
            function close_modal(){
                $.modal.close();
            }
            
            function removeUploadedFile(id, filename){
                $.ajax({
                    url: "/structureUpload/removeUploadedFile",
                    data: "file_name="+filename
                });
                if(id.split('--')[0] == "chain"){
                    //rimuovo eventuali aminoacidi non standard
                    remove_aminoEntry($("#"+id).parent().attr("id"));
                    if(!$("#chain_item").children().length){
                        $("#advanced-setting").attr("style", "display: none;");
                    }
                    $("#"+id).parent().remove();
                    $("#submit").children("#protein_name").remove();
                    
                    enableTabs();
                }
                var ty = id.split('--')[1];
                if(ty == "ligand"){
                    $("#"+id).parent().parent().remove();
                    enableTabs();
                }
                else if((ty == "rdc") || (ty == "pcs")){
                    $("#"+ty+"_tensor_fit").remove();
                    $("#"+ty+"_tensor_calc").remove();
                    //$("#"+id).parent().remove();
                    
                    $("#submitConstr").children("input").each(function(){
                        if ($(this).attr("id").split("--")[0] == filename){
                            $(this).remove();
                        }
                    });
                    $("#"+ty+"-item").children("#selectable").children().each(function(){
                        if ($(this).attr("id") == filename+"_file"){
                            $(this).remove();
                        }
                    });
                    
                    if($("#"+ty+"-item").children("#selectable").children().length == 0){
                        $("label[id="+ty+"_title]").remove();
                    }
                }
                else if(id.split('--')[0] == 'multijob'){
                    $("a[id="+id+"]").parent().empty();
                }
                else if((ty == "top_amino") || (ty == "par_amino")){
                    
                    if(!$("#"+id).parent().siblings("div").length){
                        $("#"+id).parent().parent().remove();
                    }
                    else{
                        $("#"+id).parent().remove();
                    }
                    if (ty == "top_amino"){
                        $("#amino_top_name").remove();
                    }
                    else{
                        $("#amino_par_name").remove();
                    }
                    enableTabs();
                }
                else if (ty == 'noe' || ty == 'dihedral'){
                    $("#"+ty+"-item").children().each(function(){
                        if ($(this).attr("id") == filename+"--file"){
                            $(this).remove();
                            $("#submitConstr").children("input").each(function(){
                                if ($(this).attr("id").split("--")[0] == filename){
                                    $(this).remove();
                                }
                            });
                        }
                    });
                    
                }
                
                else if(ty == 'a'){
                    /*$("#chain--"+id.split("--")[2]).remove(); */   $("#"+id).parent().remove();    
                }
                //else if(ty == 'noe' || ty == 'dihedral'){
                //    //alert(id)
                //    //alert("#"+id.split("--")[2] + '--file')
                //    $("#"+id).parent().remove();    //$("a[id="+id+"]").parent().remove();    
                //}
                else{
                    $("#"+id.split("--")[2]).remove();    //$("a[id="+id+"]").parent().remove();    
                }
                
                //$("#submitConstr").children("input[value="+filename+"]").remove();
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
                //response = $(response).xml();
                //var file_list = $('file', response);
                var file_list = $(response).find('File');
                //if ($.browser.msie){
                //                var file_list = $(response).find('File');
                //                alert(file_list.length);
                //                var file_list = $('File', response);
                //                alert(file_list.length);
                //}
                if(file_list.length){
                    //info_pdb = $('Info_PDB', response);
                    info_pdb = $(response).find('Info_PDB');
                    info_pdb_num = parseInt($.trim(info_pdb.text().split(":")[1]));
                    if (info_pdb_num > 1){
                        use_multijob(info_pdb_num);
                    }
                    var mess = "";
                    var file_bname = $(file_list).attr("BaseName");
                    var file_checked = file_bname.split('.')[0]+"_c.pdb";
                    //alert(file_bname)
                    var prefix = id.split('_')[0];
                    var div_file = $("#"+prefix+"-item").children().last();
                    //alert(file_id)
                    var id_nr = id.split('_')[1];
                    //warnings = $('warning_pdb', response);
                    warnings = $(response).find('Warning_pdb');
                    //warn_res = $('warning_res', response);
                    warn_res = $(response).find('Warning_res');
                    if((warnings.length) || (warn_res.length)){
                        var warning_message = "<ol>";
                        warnings.each(function(){
                            var war = $(this).text();
                            warning_message += "<li>"+war+"</li>";
                        });
                        var listWarn = new Array();
                        warn_res.each(function(i){
                            //var res = $(this).text();
                            var res = $(this).attr("Residue");
                            //if(res.substr(0, 2) != 'DA' && res.substr(0, 2) != 'DT' && res.substr(0, 2) != 'DC' && res.substr(0, 2) != 'DG' && res.substr(0, 3) != 'DA3' && res.substr(0, 3) != 'DT3' && res.substr(0, 3) != 'DC3' && res.substr(0, 3) != 'DG3' && res.substr(0, 3) != 'DA5' && res.substr(0, 3) != 'DT5' && res.substr(0, 3) != 'DC5' && res.substr(0, 3) != 'DG5' && res.substr(0, 3) != 'RG5' && res.substr(0, 3) != 'RA5' && res.substr(0, 3) != 'RC5' && res.substr(0, 3) != 'RU5' && res.substr(0, 3) != 'RG3' && res.substr(0, 3) != 'RA3' && res.substr(0, 3) != 'RC3' && res.substr(0, 3) != 'RU3' && res.substr(0, 3) != 'RGN' && res.substr(0, 3) != 'RAN' && res.substr(0, 3) != 'RCN' && res.substr(0, 3) != 'RUN' && res.substr(0, 3) != 'RG' && res.substr(0, 2) != 'RA' && res.substr(0, 2) != 'RC' && res.substr(0, 2) != 'RU'){
                            //    listWarn[i] = res;
                            //}
                            if (res != 'DA' && res != 'DT' && res != 'DC' && res != 'DG' && res != 'DA3' && res != 'DT3' && res != 'DC3' && res != 'DG3' && res != 'DA5' && res != 'DT5' && res != 'DC5' && res != 'DG5'  && res != 'RG5' && res != 'RA5' && res != 'RC5' && res != 'RU5' && res != 'RG3' && res != 'RA3' && res != 'RC3' && res != 'RU3' && res != 'RGN' && res != 'RAN' && res != 'RCN' && res != 'RUN' && res != 'RG' && res != 'RA' && res != 'RC' && res != 'RU'){
                                listWarn[i] = res;
                            }
                            
                        });
                        if(listWarn.length){
                                var listWarnUnique = listWarn.unique();
                                for (var i=0; listWarnUnique[i]; i++){
                                    var war = listWarnUnique[i];
                                    warning_message += "<li>"+war+"</li>";
                                }
                        }
                        
                        warning_message += "</ol>"
                        var title = 'Warning messages of *'+file_bname+'* file';
                        //var file_checked = file_bname.split('.')[0]+"_c.pdb";
                        if(warnings.length || listWarn.length){
                                add_warning(div_file.attr("id"), title , warning_message);
                                mess += "Warning messages:<br/> " + warning_message;
                        }
                        
                        
                        //warn_res = $('warning_res', response);
                        if(warn_res.length){
                            var listAmino = new Array();
                            warn_res.each(function(i){
                                var res = $(this).attr("Residue");
                                if (res != 'DA' && res != 'DT' && res != 'DC' && res != 'DG' && res != 'DA3' && res != 'DT3' && res != 'DC3' && res != 'DG3' && res != 'DA5' && res != 'DT5' && res != 'DC5' && res != 'DG5'  && res != 'RG5' && res != 'RA5' && res != 'RC5' && res != 'RU5' && res != 'RG3' && res != 'RA3' && res != 'RC3' && res != 'RU3' && res != 'RGN' && res != 'RAN' && res != 'RCN' && res != 'RUN' && res != 'RG' && res != 'RA' && res != 'RC' && res != 'RU'){
                                    listAmino[i] = res;
                                }
                            });
                            if (listAmino.length){
                                $.jGrowl("See warning messages clicking on icon <img id='imgPopup' src='"+IMG_PATH+"warning.png' border='0'>.", {header: 'WARNING', life: 15000, theme: 'iphone'});
                                create_aminoEntry(listAmino, file_bname);
                            }
                            
                        }
                        
                        //abilito submit
                        //enableSubmit();
                    }
                
                    //errors = $('error_pdb', response);
                    errors = $(response).find('error_pdb');
                    if(errors.length){
                        var error_message = "<ol>";
                        errors.each(function(){
                            var err = $(this).text();
                            error_message += "<li>"+err+"</li>";
                        });
                        error_message += "</ol>"
                        add_error(div_file.attr("id"), "errors" , error_message);
                        mess += "Error messages:<br/> " + error_message;
                         $.jGrowl("See error messages clicking on icon <img id='imgPopup' src='"+IMG_PATH+"error.png' border='0'>.", {header: 'ERROR', life: 15000, theme: 'iphone'});
                    }
                    
                    $("#submit_check").attr("value", "");
                    //var path_dir = '${c.dir}'.split('/')[7]
                    //var path_dir = '${c.dir}';
                    //alert(path_dir)
                    var file = file_bname.split('.')[0]+"_c.pdb";
                    var down = '<img src="'+IMG_PATH+'download.png" border="0" title="Download converted file" alt="Download converted file" onClick="download_pdb(\'/structureUpload/download?requested_filename='+file_checked+'\')" />';
                    div_file.append(down);
                    var img_jmol = '<img id="'+prefix+'_joml_'+id_nr+'" onClick="open_jmolView(\''+div_file.attr("id")+'\', \'\')" src="'+IMG_PATH+'jmol.gif" border="0" title="View chemical structure of protein" alt="View chemical structure of protein" />';
                    div_file.append(img_jmol);
                }
                $("#chain-item").children("#loading").remove();
                //close_modal();
            }
            
        function download_pdb(url){
                window.location = url;        
        }   
        
	    function use_multijob(n){
		var myWidth = 400;
		var myHeight = 170;
		var option = {
		    escClose: false,
		    opacity:70,
		    minWidth: myWidth,
		    minHeight: myHeight,
		    maxWidth: myWidth,
		    maxHeight: myHeight
		};
		var txt = "Your .pdb is a bundle of "+ n + " conformers. <br>Do you want to refine all of them? If you choose 'No', only the first conformer will be used."
		$("#mstruct").children("h4").empty()
		$("#mstruct").children("h4").append(txt);
		$("#mstructyes").button();
		$("#mstructyes").click(function(){
		    $("input[name=multij]").attr("value", "on");
		    $.modal.close();
		});
		$("#mstructno").button();
		$("#mstructno").click(function(){
		    $("input[name=multij]").attr("value", "off");
		    $.modal.close();
		});
		
		$("#mstruct").modal(option)
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
            function showchain(chain){
                var myWidth = 600;
                var myHeight = 400;
                var option = {
                    escClose: true,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                $.modal(chain, option);
                
            }
            function processStructureSubmit(response, statusText){
                //var prot = $('protein', response);
                //var attr = prot.attr("filename");
                
                //response = $(response).xml();
                //alert(response);
                
                
                //$("#submit_structure").attr("disabled", "disabled");
                
                
                //var errors = $('error', response);
                var errors = $(response).find('Error');
                //var fatals = $('fatal', response);
                var fatals = $(response).find('fatal');
                if(!fatals.length){
                    var leap = $(response).find('leap');
                    var chains = $(response).find('chain');
                    $("#chain-row").empty();
                    if(chains.length){
                        $("#chain-row").empty();
                        var tag = '';
                        chains.each(function(i){
                            //if((i+1) % 4 == 1){
                               
                               
                                //$("#chain_summary_fieldset").append(tag);
                                var chain_n = $(this).attr("chain_n");
                                var chain_range = $(this).attr("chain_range");
                                tag =  tag + '<div  class=\'cell\'>'+
                                                '<span>Chain </span><span id=\'lchain_n\'>'+chain_n+' </span>'+
                                                '<span>[range </span><span id=\'lchain_range\'>'+chain_range+']</span>'+
                                            '</div>';
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
                        
                        if (chains.length > 5){
                                tag = '';
                                chains.each(function(i){
                                    var chain_n = $(this).attr("chain_n");
                                    var chain_range = $(this).attr("chain_range");
                                    tag =  tag + ' Chain '+chain_n+' range: '+chain_range;
                                    if ((i % 3 == 0) && (i > 0)){
                                        tag = tag + '<br />';
                                    }
                                    
                                });
                                var link = 'click <a style="text-decoration: underline; cursor: pointer; color: blue;" onclick="javascript:showchain(\''+tag+'\');">here</a> to view info about chains'
                                $("#chain-row").append(link);
                        }
                        else{
                                $("#chain-row").append(tag);        
                        }
                        
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
                var suffix = id.split('--')[1];
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
                       
                                var obj = '<object name="jmolApplet0" id="jmolApplet0" type="application/x-java-applet" height="500" width="500">';
                        
                        
                                obj += '<param name="syncId" value="216291259819275">'+
                                '<param name="progressbar" value="true">'+
                                '<param name="progresscolor" value="blue">'+
                                '<param name="boxbgcolor" value="black">'+
                                '<param name="boxfgcolor" value="white">'+
                                '<param name="boxmessage" value="Downloading JmolApplet ...">'+
                                '<param name="name" value="jmolApplet0">'+
                                '<param name="archive" value="JmolApplet0.jar">'+
                                '<param name="mayscript" value="true">'+
                                '<param name="code" value="JmolApplet.class">'+
                                '<param name="codebase" value="/global/jmol-12.0.39">'+
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
                                            '<label id="par" for="atmtype_amino">Atom type file</label>'+
                                            '<div id="atmtype_amino_div">'+
                                            '<input type="file" id="atmtype_amino" name="atmtype_amino_file" onchange="add_toppar(\'samino\', this.id, \'structure\', \''+filename+'\')"><br />'+
                                            '</div>'+
                                            '</li>'+
                                            '</ol>'+
                                        '</div>'+
                                        '<div id="amino-item">'+
                                        '</div>'+
                                    '</div>'+
                                    '<br/><br/> If recognized non-standard residue(s) represent a small organic molecule or metal ion click <a style="text-decoration: underline; cursor: pointer; color: blue;" href="http://web-enmr.cerm.unifi.it/load/index" target="_blank">here</a> to use Antechamber Web Portal to build its topology and parameters files.'+
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
                var txt = '<img src="/global/images/loading2.gif" />';
                $.modal(txt, option);
                
                
                //var myWidth = 320;
                //var myHeight = 240;
                //var option = {
                //    escClose: false,
                //    opacity:70,
                //    minWidth: myWidth,
                //    minHeight: myHeight,
                //    maxWidth: myWidth,
                //    maxHeight: myHeight
                //};
                //var img = '<img src="/global/images/loading2.gif" />';
                //$.modal(img, option);
            }
            
            function stopLoading(){
                $.modal.close();
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
            
            
            function toFit(type, p){
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
                    var filename_list = $(p).parent().prev().text().replace(/\s\s+/, ' ').split(" ");
                    var filename = filename_list[2];
                    var selected = $(p).parent().prev();
                    //alert(filename);
                    //alert($("#"+type+"_tensor_fit").children().children("select").val());
                    var resname = $("#"+type+"_tensor_fit").children().children("#"+type+"_rsdname").val();
                    if (resname.length > 3){
                                    resname = resname.substring(0,3)
                    }
                    var fr_list = $(p).parent().prev().text().split("]")
                    var fr = parseInt(fr_list[0].replace("[", ""));
                    var resnum = parseInt($("#"+type+"_tensor_fit").children().children("#"+type+"_rsdnum").val());
                    resnum = resnum + 1 - fr;
                    if ($("#noparcent").is(':checked')){
                          var metstr = "No Par. Cent."          
                    }
                    else{
                          var metstr = $("#"+type+"_tensor_fit").children().children("#"+type+"_atmname").val() + " " + resname + " " + resnum
                    }
                    var num_list = $(p).parent().prev().text().split("]");
                    var num = num_list[0].replace("[", "");
                    $.ajax({
                        type: "POST",
                        url: "/structureUpload/fit_"+type,
                        data: "protocol=fit"+"&"+type+"_xml=" +filename+ "&temperature=" +$("#temperature").attr("value")+
                              "&b=" +$("#b").attr("value")+ "&tolerance=" +$("#tolerance").attr("value")+
                              "&metal="+metstr+"&number="+num,
                        success: function(data){
                            stopLoading();
                            rows = read_data_fitCalc(data, selected, type);
                            if (rows == 'error'){
                                var myWidth = 350;
                                var myHeight = 240;
                                var option = {
                                    escClose: false,
                                    opacity:70,
                                    minWidth: myWidth,
                                    minHeight: myHeight,
                                    maxWidth: myWidth,
                                    maxHeight: myHeight
                                };
                                var txt = '<div><h2>Selected Metal is not present in pdb.</h2></div>';
                                $.modal(txt, option);
                            }
                            else{
                                rows = rows.replace(/undefined/g, "");
                                
                                $("#"+filename+"_file").find("a").not("a[href*=remove]").remove();
                                //alert($("#"+type+"-item").find("#selectable").length)
                                //rows = rdc_out.text();
                                var fit_info = ' <a href="javascript:open_dialog(\''+type+' output\', \''+rows+'\', 680, 700);"><b>fit info</b></a>';
                                $("#"+type+"-item").children("#selectable").children().each(function(){
                                    if ($(this).attr("id") == filename+"_file"){
                                        $(this).append(fit_info);
                                    }    
                                });
                                
                                var jmol_file = $(type+'_pdb', data).text();
                                jmol_file = jmol_file.split("_")[0]+"_"+type+''+jmol_file.split("_")[1]
                                var jmo = '<a id="'+filename+'_a" href="javascript:open_jmolView(\''+filename+'_file\', \''+jmol_file+'\');"><img class="imgconst" id="'+jmol_file+'_eye" src="'+IMG_PATH+'jmol.gif" border="0" title="View pdb with the tensor"></a>';
                                $("#"+type+"-item").children("#selectable").children().each(function(){
                                    if ($(this).attr("id") == filename+"_file"){
                                        $(this).append(jmo);
                                    }    
                                });
                                //$("#"+filename+"_file").children('a:last').after(jmo);
                                //$("#rdc-item").append(jmo);
                                //var tarpdbfanta = type+"outfanta.tar"
                                var tarpdbfanta = type+"outfanta.tar"
                                var down = '<a href="/structureUpload/download?requested_filename='+tarpdbfanta+'"><img class="imgconst" src="'+IMG_PATH+'download.png" border="0" title="Download pdb with the tensor and fitting info"></a>';
                                //$("div[id="+filename+"_file]").children('a:last').after(down);
                                $("#"+type+"-item").children("#selectable").children().each(function(){
                                    if ($(this).attr("id") == filename+"_file"){
                                        $(this).append(down);
                                    }    
                                });
                                //$("#"+filename+"_file").children('a:last').after(down);
                                $(p).parent().remove();
                                
                            }
                            
                        }
                    });
                    
                    $("#"+type+"_tensor_fit").remove();
                    $("#"+type+"_tensor_calc").remove();
                    //$(obj).parent().prev().removeAttr("class");
                    //stopLoading();
                    
                });
                $("#bfit_"+type).button();
                $("#bfit_"+type).click(function() {
                    startLoading();
                    var filename_list = $(p).parent().prev().text().replace(/\s\s+/, ' ').split(" ");
                    var filename = filename_list[2];
                    var selected = $(p).parent().prev();
                    var num_list = $(p).parent().prev().text().split("]");
                    var num = num_list[0].replace("[", "");
                    var resname = $("#"+type+"_tensor_fit").children().children("#"+type+"_rsdname").val();
                    if (resname.length > 3){
                                    resname = resname.substring(0,3)
                    }
                    
                    var fr_list = $(p).parent().prev().text().split("]")
                    var fr = parseInt(fr_list[0].replace("[", ""));
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
                        data: "protocol=fit"+"&"+type+"_xml=" +$(p).parent().prev().text().split(" ")[3]+
                              "&temperature=" +$("#temperature").attr("value")+
                              "&b=" +$("#b").attr("value")+ "&tolerance=" +$("#tolerance").attr("value")+
                              "&metal="+metstr+
                              "&withpcsrdc="+$("#"+type+"_tensor_fit").children().children("select[id=spcs]").val().replace("_file", "")+
                              "&weight="+$("#"+type+'_'+"weight").attr("value")+"&number="+num,
                        success: function(data){
                            //alert($(data).xml());
                            stopLoading();
                            rows = read_data_fitCalc(data, selected, type+'_'+type2);
                            if (rows == 'error'){
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
                                var txt = '<div><h2>Selected Metal is not present in pdb.</h2></div>';
                                $.modal(txt, option);
                            }
                            else{
                                stopLoading();
                                rows = rows.replace(/undefined/g, "");
                                
                                $("div[id="+filename+"_file").children("a").not("a[href*=remove]").remove();
                                //alert(rows)
                                //rows = rdc_out.text();
                                
                                var fit_info = ' <a href="javascript:open_dialog(\'output\', \''+rows+'\', 680, 700);">fit info</a>';
                                $("div[id="+filename+"_file").append(fit_info);
                                //$("#"+filename+"_file").append(fit_info);
                                var jmol_file = $(type+'_pdb', data).text();
                                var jmo = '<a id="'+filename+'_a" href="javascript:open_jmolView(\''+filename+'_file\', \''+jmol_file+'\');"><img class="imgconst" id="'+jmol_file+'_eye" src="'+IMG_PATH+'jmol.gif" border="0" title="View chemical structure of rdc"></a>';
                                $("div[id="+filename+"_file").children('a:last').after(jmo);
                                //$("#rdc-item").append(jmo);
                                var down = '<a href="/structureUpload/download?requested_filename='+jmol_file+'"><img class="imgconst" src="'+IMG_PATH+'download.png" border="0" title="Download rdc"></a>';
                                $("div[id="+filename+"_file").children('a:last').after(down);
                                
                                $("#"+type+"_tensor_fit").remove();
                                $("#"+type+"_tensor_calc").remove();
                                //$(".ui-selected").removeAttr("class");
                                $(p).parent().remove();
                                
                            }
                        }
                    });
                    //stopLoading();
                    
                });
 
                var resname = $("#"+type+"_tensor_fit").children().children("#"+type+"_rsdname").val();
                if (resname.length > 3){
                                resname = resname.substring(0,3)
                }
                var fr_list = $(".ui-selected").text().split("]")
                var fr = parseInt(fr_list[0].replace("[", ""));
                var resnum = parseInt($("#"+type+"_tensor_fit").children().children("#"+type+"_rsdnum").val());
                resnum = resnum + 1 - fr;
                    
                metals = metals.replace(/id="rdc_metal"/, 'id="pcs_metal"');
                $(metals).insertAfter("#"+type+"_lmetal1");
                
                
            }
            
            function add_constraintEntry(inputID, form){
                var type = inputID.split('_')[0];
                var field = inputID.split('_')[1];
                var cntEntry = $("#"+type.substring(0,3)+"-item").children().length;
                if(field == "file"){ //if(field != "cyanaXplor" && field != "fit"){
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
                    
                    if (type != 'dihedral'){
                        var start = $("#"+type.substring(0,3)+"_number").attr("value");
                        var tp = $("#"+type.substring(0,3)+"_cyanaXplor").val();
                    }
                    else{
                        var start = $("#"+type+"_number").attr("value");
                        var tp = $("#"+type+"_cyanaXplor").val();
                    }
                    
                    
                    var notfound = 1
                    var cntItem = $("#"+type.substring(0,3)+"-item").children("div[id="+value+"_file]");
                    var cntItem2 = $("#"+type.substring(0,3)+"-item").children("div");
                    cntItem2.each(function(){
                        var txt = $(this).children("span").text();
                        //alert(txt)
                        //alert(value)
                        if(txt == value){
                            notfound = 0;
                        }
                    });
                    
                    //var cntItem3 = $("#"+type.substring(0,3)+"-item").children("#selectable").children();
                    //cntItem3.each(function(){
                    //    var txt = $(this).children("span").text();
                    //    alert(txt.split().lenght)
                    //    alert(txt.split())
                    //    txt = txt.split()[2]
                    //    if(txt == value){
                    //        notfound = 0;
                    //    }
                    //});
                    
                    
                    
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
                        if(type == 'noe' || type == 'noeLol'){
                           no_corr = $("#"+type.substring(0,3)+"_checkbox:checked").val();
                            if (no_corr != 'True'){
                                no_corr = 'False'
                            }
                            var hdd5 = '<input type="hidden" id="'+value+'--'+type.substring(0,3)+'--noe--corr" value="'+no_corr+'" name="'+type.substring(0,3)+'_nocorr_r">';
                            $("#submitConstr").append(hdd5);
                        }
                        //var title_item="<label>Select rdc item to fit or calculate tensor: </label>";
                        //$("#rdc-item").append(title_item)
                        if (type == 'pcs' || type == 'rdc'){
                                var tag = '<div id="'+value+'_file">'+
                                    '<a id="a--'+type+'--'+value+'" href="javascript:removeUploadedFile(\'a--'+type+'--'+value+'\', \''+value+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                       '<span>['+start+'] ('+tp+') '+no_corr+' '+value+'</span>'+
                                       '&nbsp;&nbsp;&nbsp;<b>click <a style="color: blue;" onclick="javascript:toFit(\''+type+'\', this)">here</a> to fit</b>'+
                                  '</div>';
                        }
                        else{
                            if (type != 'dihedral'){
                                var tag = '<div id="'+value+'--file">'+
                                            '<a id="a--'+type.substring(0,3)+'--'+value+'" href="javascript:removeUploadedFile(\'a--'+type.substring(0,3)+'--'+value+'\', \''+value+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                               '<span>['+start+'] ('+tp+') '+no_corr+' '+value+'</span>'+
                                          '</div>';
                            }
                            else{
                                var tag = '<div id="'+value+'--file">'+
                                            '<a id="a--'+type+'--'+value+'" href="javascript:removeUploadedFile(\'a--'+type+'--'+value+'\', \''+value+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
                                               '<span>['+start+'] ('+tp+') '+no_corr+' '+value+'</span>'+
                                          '</div>';
                            }
                        }
                        //if (cntItem.length){
                            //$("#submitConstr").children("input[id^="+type.substring(0,3)+"]").remove();###########################################
                            //$("input[type='hidden' id^='"+type+"']").remove();
                            //$("input[type='hidden' id="+type+'_cyanaXplor'+"]").remove();
                            //$("input[type='hidden' id="+type+'_number'+"]").remove();
                            //$("input[type='hidden' id="+type+'_fit'+"]").remove();
                            
                            //cntItem.replaceWith(tag); 9 MARZO PER PROBLEMA CIOFI
                            
                        //}
                        //else{
                            if((type == 'rdc') || (type == "pcs")){
                                $("#"+type+"-item").children("#selectable").append('<img src="/global/images/loading.gif">');
                                //$("#"+type+"-item").children("#selectable").append(tag);    
                            }
                            else{
                                $("#"+type.substring(0,3)+"-item").append('<img src="/global/images/loading.gif">');
                                //$("#"+type+"-item").append(tag);
                            }
                            
                        //}

                        var hdd1 = '<input type="hidden" id="'+value+'--'+type.substring(0,3)+'--'+field+'--f" value="'+value+'" name="'+type.substring(0,3)+'_'+field+'_f">';
                        $("#submitConstr").append(hdd1);
                        var hdd2 = '<input type="hidden" id="'+value+'--'+type.substring(0,3)+'--number" value="'+start+'" name="'+type.substring(0,3)+'_number_n">';
                        $("#submitConstr").append(hdd2);
                        var hdd3 = '<input type="hidden" id="'+value+'--'+type.substring(0,3)+'--cyanaXplor" value="'+tp+'" name="'+type.substring(0,3)+'_cyanaXplor_c">';
                        $("#submitConstr").append(hdd3);
                        
                        
                    
                        $("#submitConstr").children("#field").attr("value", type);
                        if(type=='rdc'){
                            var len_rdcs = $("#"+type+"-item").children("#selectable").children().length;
                            if(len_rdcs > 3){
                                open_dialog("ATTENTION", "You have already reached "+type+" uploads limit!", 350, 150);
                                $("#"+type+"_number").attr("value", "");
                                $("#"+type+"_file").attr("value", "");
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
                                $("#"+type+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                                $("#"+type+"-item").children("#selectable").children('img').remove();
                                return
                            }
                        }
                        var options = {
                            url: "/structureUpload/check_constraint",
                            dataType:  'xml',        // 'xml', 'script', or 'json' (expected server response type)
                            success:  function(response, status){
                                typenew = ''
                                if (type != 'dihedral'){
                                    typenew = type.substring(0,3)
                                }
                                else{
                                    typenew = type
                                }
                                $("#"+typenew+"_number").attr("value", "");
                                //$("#"+type+"_file_div").html($("#"+type+"_file_div").html());
                                $("#"+typenew+"_file").attr("value", "");
                                $("#"+typenew+"_file").attr("disabled", "disabled");

                                $("#noeLol_file").attr("disabled", "disabled");
                                $("#"+typenew+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                                //$("#"+type+"_fit option[value='null']").attr('selected', 'selected');
                                $("#"+typenew+"_checkbox").removeAttr("checked");
                                if((type == 'rdc') || (type == "pcs")){
                                    $("#"+type+"-item").children("#selectable").children('img').remove();;
                                    $("#"+type+"-item").children("#selectable").append(tag);    
                                }
                                else{
                                    if (type != 'dihedral'){
                                        $("#"+typenew+"-item").children('img').remove();
                                        $("#"+typenew+"-item").append(tag);
                                    }
                                    else{
                                        $("#"+type+"-item").children('img').remove();
                                        $("#"+type+"-item").append(tag);
                                    }
                                    
                                }
                                $.validationEngine.closePrompt('#sander-out');
                                
                                if (typenew == 'noe'){
                                    warn_noe = '<div id="warn--'+value+'" style="display:none;"><b>NOEs don\'t match any residues and/or atoms in the pdb</b><br/><br/>';
                                    if ($(response).find("Res1_not_found").length){
                                        warn_noe += '<i>Residue 1 not found</i>:';
                                    }
                                    $(response).find("Res1_not_found").each(function(){
                                            warn_noe += "<br/>"+$(this).text();
                                    });
                                    if ($(response).find("Res2_not_found").length){
                                        warn_noe += '<br/><br/><i>Residue 2 not found</i>:';
                                    }
                                    $(response).find("Res2_not_found").each(function(){
                                            warn_noe += "<br/>"+$(this).text();
                                    });
                                    
                                    if ($(response).find("Atom1_not_found").length){
                                        warn_noe += '<br/><br/><i>Atom 1 not found</i>:';
                                    }
                                    $(response).find("Atom1_not_found").each(function(){
                                            warn_noe += "<br/>"+$(this).text();
                                    });
                                    if ($(response).find("Atom2_not_found").length){
                                        warn_noe += '<br/><br/><i>Atom 2 not found</i>:';
                                    }
                                    $(response).find("Atom2_not_found").each(function(){
                                            warn_noe += "<br/>"+$(this).text();
                                    });
                                    warn_noe += "</div>"
                                    if ($(response).find("Res1_not_found").length || $(response).find("Res12_not_found").length || $(response).find("Atom1_not_found").length || $(response).find("Atom2_not_found").length ){
                                        tag_warning = '<a href="javascript:show_warning(\''+typenew+'\',\''+value+'--file\');"><img src="'+IMG_PATH+'warning.png"></img></a>'
                                        $("#"+typenew+"-item").children("div[id="+value+"--file]").append(tag_warning);
                                        $("#"+typenew+"-item").children("div[id="+value+"--file]").append(warn_noe);
                                    }
                                }
                                else if (typenew == 'dihedral'){
                                    warn_dih = '<div id="warn--'+value+'" style="display:none;"><b>Dihedral angles don\'t match any residues and/or atoms in the pdb</b><br/><br/>';
                                    if ($(response).find("Angle_not_found").length){
                                        warn_dih += '<i> Angle not found</i>:';
                                    }
                                    $(response).find("Angle_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    if ($(response).find("Res1_not_found").length){
                                        warn_dih += '<i>Residue 1 not found</i>:';
                                    }
                                    $(response).find("Res1_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    if ($(response).find("Res2_not_found").length){
                                        warn_dih += '<br/><br/><i>Residue 2 not found</i>:';
                                    }
                                    $(response).find("Res2_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    $(response).find("Res3_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    
                                    $(response).find("Res4_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    
                                    if ($(response).find("Atom1_not_found").length){
                                        warn_dih += '<br/><br/><i>Atom 1 not found</i>:';
                                    }
                                    $(response).find("Atom1_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    if ($(response).find("Atom2_not_found").length){
                                        warn_dih += '<br/><br/><i>Atom 2 not found</i>:';
                                    }
                                    $(response).find("Atom2_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    $(response).find("Atom3_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    $(response).find("Atom4_not_found").each(function(){
                                            warn_dih += "<br/>"+$(this).text();
                                    });
                                    warn_dih += "</div>"
                                    if ($(response).find("Res1_not_found").length || $(response).find("Res12_not_found").length || $(response).find("Atom1_not_found").length || $(response).find("Atom2_not_found").length || $(response).find("Angle_not_found").length){
                                        tag_warning = '<a href="javascript:show_warning(\''+typenew+'\',\''+value+'--file\');"><img src="'+IMG_PATH+'warning.png"></img></a>'
                                        $("#"+typenew+"-item").children("div[id="+value+"--file]").append(tag_warning);
                                        $("#"+typenew+"-item").children("div[id="+value+"--file]").append(warn_dih);
                                    }
                                }
                                
                                
                            }
                        };
                        $("#"+form).ajaxSubmit(options); 
                        
                    }
                    else{
                        $("#"+type+"_number").attr("value", "");
                        $("#"+type+"_file").attr("value", "");
                        $("#"+type+"_file").attr("disabled", "disabled");
                        if (type=="noe"){
                            $("#"+type+"Lol_file").attr("value", "");
                            $("#"+type+"Lol_file").attr("disabled", "disabled");
                        }
                        $("#"+type+"_cyanaXplor option[value='null']").attr('selected', 'selected');
                        $("#"+type+"_fit option[value='null']").attr('selected', 'selected');
                        $("#"+type+"_checkbox").removeAttr("checked");
                        open_dialog('ATTENTION', 'File already uploaded!', 200, 100)
                    }
                    //$("#"+form).ajaxSubmit();
                }
                else{
                    typenew = ''
                    if(type != 'dihedral'){
                        typenew = type.substring(0,3)
                    }
                    else{
                        typenew = type
                    }
                    if(($("#"+typenew+"_number").attr("value") != "") && ($("#"+typenew+"_cyanaXplor").val() != "null")){
                        if((type == "rdc") || (type == "pcs")){
                            if($("#"+type+"_fit").val() != "null"){
                                $("#"+type+"_file").removeAttr("disabled");
                                
                            }
                        }
                        else{
                            $("#"+typenew+"_file").removeAttr("disabled");
                            if (type == "noe"){
                                $("#"+type+"Lol_file").removeAttr("disabled");
                            }
                            $('a[href="#tabs-2"]').click(function(){
                               
                            });
                        }
                    
                    }
                    else{
                        $("#"+typenew+"_file").attr("disabled", "disabled");
                        if (type == "noe"){
                            $("#"+type+"Lol_file").attr("disabled", "disabled");
                        }
                    }
                }
            }
            
            
            function show_warning(where, id){
                var myWidth = 450;
                var myHeight = 600;
                var option = {
                    escClose: true,
                    opacity:70,
                    onShow: function (d) {
                        $(hiddenElement).show();
                    },
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                $("#"+where+'-item').children("div[id="+id+"]").children("div[id^=warn]").modal(option);   
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
                var error = $(data_temp).find("error")[0]
                if (error){
                    return "error";
                }
                else{
                    if(type_temp == "rdc_pcs" || type_temp == "pcs_rdc"){
                        var data1 =  $(data_temp).find("fanta_"+type_temp.split('_')[0])
                        data = $(data_temp).find("fanta_"+type_temp.split('_')[1]);
                        type2 = type_temp.split('_')[1];
                        var qfactor_val = $(data1).find('qfactor').attr("qfactor_val");
                        rows1 += '<label class=litem>qfactor value: '+qfactor_val +'</label> ';
                        var qfactor_num = $(data1).find('qfactor').attr("num");
                        rows1 += '<label class=litem>qfactor num: '+qfactor_num+'</label> ';
                        var qfactor_den = $(data1).find('qfactor').attr("den").replace(/\)/, '');
                        rows1 += '<label class=litem>qfactor den: '+qfactor_den+'</label><br />';
                        var eig_val1 = $(data1).find('RDC_eig').attr("a1val");
                        rows1 += '<label class=litem>eigenvalue a1: '+eig_val1+'</label> ';
                        var eig_val2 = $(data1).find('RDC_eig').attr("a2val");
                        rows1 += '<label class=litem>eigenvalue a2: '+eig_val2+'</label> ';
                        var eig_val3 = $(data1).find('RDC_eig').attr("a3val");
                        rows1 += '<label class=litem>eigenvalue a3: '+eig_val3+'</label><br />';
                        var dchirh = $(data1).find('aniso').attr("dchirh");
                        rows1 += '<label class=litem>aniso dchirx: '+dchirh+'</label> ';
                        var dchiax = $(data1).find('aniso').attr("dchiax");
                        rows1 += '<label class=litem>aniso dchiax: '+dchiax+'</label><br />';
                        var dchirh_m = $(data1).find('anisom').attr("dchirh");
                        rows1 += '<label class=litem>anisom dchirx: '+dchirh_m+'</label> ';
                        var dchiax_m = $(data1).find('anisom').attr("dchiax");
                        rows1 += '<label class=litem>anisom dchiax: '+dchiax_m+'</label><br />';
                        var theta = $(data1).find('euler').attr("theta");
                        rows1 += '<label class=litem>euler theta: '+theta+'</label> ';
                        var phi =$(data1).find('euler').attr("phi");
                        rows1 += '<label class=litem>euler phi: '+phi+'</label> ';
                        var omega = $(data1).find('euler').attr("omega");
                        rows1 += '<label class=litem>euler omega: '+omega+'</label><br />';
    
                        var graph_file = $(data1).find(type_temp.split('_')[0]+'_graph').text();
                        
                        //selected.append(" <br />dchiax: "+dchiax+" dchirh: "+dchirh);
                        var rdc_out = $(data1).find(type_temp.split('_')[0]+'_out');
                       // var rdc_out = $(type_temp.split('_')[0]+'_out', data1);
                       
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
                        data1 = $("fanta_"+type, data)
                        var qfactor_val = $('qfactor', data1).attr("qfactor_val");
                        //alert(qfactor_val)
                        rows += '<label class=litem>qfactor value: '+qfactor_val +'</label> ';
                        var qfactor_num = $(data1).find('qfactor').attr("num");
                        rows += '<label class=litem>qfactor num: '+qfactor_num+'</label> ';
                        var qfactor_den = $(data1).find('qfactor').attr("den").replace(/\)/, '');
                        rows += '<label class=litem>qfactor den: '+qfactor_den+'</label><br />';
                        var eig_val1 = $(data1).find('RDC_eig').attr("a1val");
                        rows += '<label class=litem>eigenvalue a1: '+eig_val1+'</label> ';
                        var eig_val2 = $(data1).find('RDC_eig').attr("a2val");
                        rows += '<label class=litem>eigenvalue a2: '+eig_val2+'</label> ';
                        var eig_val3 = $(data1).find('RDC_eig').attr("a3val");
                        rows += '<label class=litem>eigenvalue a3: '+eig_val3+'</label><br />';
                        var dchirh = $(data1).find('aniso').attr("dchirh");
                        rows += '<label class=litem>aniso dchirx: '+dchirh+'</label> ';
                        var dchiax = $(data1).find('aniso').attr("dchiax");
                        rows += '<label class=litem>aniso dchiax: '+dchiax+'</label><br />';
                        var dchirh_m = $(data1).find('anisom').attr("dchirh");
                        rows += '<label class=litem>anisom dchirx: '+dchirh_m+'</label> ';
                        var dchiax_m = $(data1).find('anisom').attr("dchiax");
                        rows += '<label class=litem>anisom dchiax: '+dchiax_m+'</label><br />';
                        var theta = $(data1).find('euler').attr("theta");
                        rows += '<label class=litem>euler theta: '+theta+'</label> ';
                        var phi = $(data1).find('euler').attr("phi");
                        rows += '<label class=litem>euler phi: '+phi+'</label> ';
                        var omega = $(data1).find('euler').attr("omega");
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
                    var dchirh = $(data).find('aniso').attr("dchirh");
                    //rows += '<label class=litem>aniso dchirx: '+dchirh+'</label> ';
                    var dchiax = $(data).find('aniso').attr("dchiax");
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
                    var graph_file = $(data).find(type2+'_graph').text();
                    
                    selected.append(" <br />dchiax: "+dchiax+" dchirh: "+dchirh);
                    var rdc_out = $(data).find(type2+'_out');
                   
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
                    
                    //alert("read");
                    
                    return rows1+rows;
                }
            }
            
            function insertFlagValue(str, section){
                var str_txtArea = $("#txtarea").attr("value");
                //alert(str_txtArea)
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
                                '<br />'+
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
                                '<br />'+
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
                            '<br />'+
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
                var new_label = '<div id="'+id_input.split('_')[0]+'_'+residue+'"> <a id="a--'+id_input.split('--')[0]+'--file" href="javascript:removeUploadedFile(\'a--'+id_input.split('_')[0]+'_amino--file'+'\', \''+filename+'\');"><img src="/global/images/cancel.png" border="0"/></a> '+
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
                    
                    var hdd = '<input type="hidden" value="'+filename+'" name="amino_'+id_input.split('_')[0]+'_name" id="amino_'+id_input.split('_')[0]+'_name">';
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
            var nstdres = false;
            var forcef = false;
            
            if ($("#chain-item").children().length){
                chain = true;
                $.validationEngine.closePrompt("input[name=chain_file]");
                
                //controllo se ci sono amino non standard
                nstdres = check_nstdres();
                if(nstdres){
                    $.validationEngine.closePrompt("input[id=top_amino]");
                }
            }
            
            if($("#force_fields").val() != ""){
                forcef = true;
                $.validationEngine.closePrompt("#force_fields");
            }
            
            
            
            //if(($("#chain-item").children().length) && ($("#amino-item").children().length >= ($("#samino").children("option").length - 1)) && ($("#force_fields").val() != "")){
            if(chain && nstdres && forcef){
                //$('#tabs').tabs({ disabled: [] });
                
                $('#tabs').tabs({ disabled: [3] });
                $('#tabs').children("ul").children("li").each(function(){
                    if ($(this).children("a").attr("href") == "#tabs-2"){
                        $(this).children("a").bind('click', function(){
                            submit('structure');    
                        });
                        //$(this).children("a").attr("onclick", "submit('structure')");
                    }
                    else if($(this).children("a").attr("href") == "#tabs-3"){
                        if (!$("body").children("input[name=substructure]").length){
                            submit('structure');
                        }
                        $(this).children("a").bind('click', function(){
                            submit('constraint');    
                        });
                        //$(this).children("a").attr("onclick", "submit('constraint')");
                        
                    }
                    else if($(this).children("a").attr("href") == "#tabs-4"){
                        $(this).children("a").bind('click', function(){
                            read_sander_flags();    
                        });
                        //$(this).children("a").attr("onclick", "read_sander_flags()");
                        
                    }
                });
                //$.jGrowl("You are provided a minimum set of structure inputs to continue.", {header: 'INFORMATION', life: 8000, theme: 'iphone'});
                $("div.jGrowl-notification").trigger("jGrowl.close");
                $.jGrowl("Now, you can specify Constraint inputs and/or  set Sander parameters.", {header: 'INFORMATION', life: 8000, theme: 'iphone'});
            }
            else if (!chain){
                //$.validationEngine.closePrompt("input[id=calc_name]");
                $.validationEngine.buildPrompt("input[name=chain_file]","This field is required","error");
                $('#tabs').tabs({ disabled: [1,2,3] });
            }
            else if (!forcef){
                $.validationEngine.buildPrompt("select[id=force_fields]","This field is required","error");
                $('#tabs').tabs({ disabled: [1,2,3] });
            }
            else if (!nstdres){
                $.validationEngine.buildPrompt("input[id=top_amino]","This field is required","error");
                $('#tabs').tabs({ disabled: [1,2,3] });
            }
        }
        
        function submit(form){
            if(form == 'structure'){
		var pass = true;
		$.ajax({
                    type: 'POST',
                    url: '/structureUpload/checkprmd',
                    success: function(data){
                        if (data == 'error'){
			    pass = false;
                            $.jGrowl("Some unrecognized error occurred checking your pdb file.", {header: 'ATTENTION', theme: 'iphone'});
                        }
                    }
                });
		if (pass){
		    var options = {
                type: 'GET',
				//target:        '#output1',   // target element(s) to be updated with server response 
				//beforeSubmit:   validatorRequest,  // pre-submit callback
				dataType:  'xml',     // 'xml', 'script', or 'json' (expected server response type) 
				success:  processStructureSubmit   // post-submit callback 
		    };
		    $("#"+form).ajaxSubmit(options);
		    if(!$("body").children("input[name=substructure]").length){
			$("body").append('<input type="hidden" name="substructure" value="1" />');
		    }
		}
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
			    $("#"+id).after('<span class="ok" style="color:  blue;"> OK</span>');
			    $("#submit_calc").removeAttr("disabled");
			    //$("#subCalc").removeAttr("disabled");
			    $("#submitOpt").children("input[name=calcname]").remove();
			    $("#submitOpt").append('<input type="hidden" name="calcname" value="'+$('#'+id).attr("value")+'" />');
			}
			else{
			    $("#availability").remove();
			    $("#"+id).after('<span class="no" style="color:  red;"> Already exists</span>');
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
        
        function addloading(){
                
                var myWidth = 270;
                var myHeight = 60;
                var option = {
                    escClose: true,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                //$.modal('<div><img src="/static/images/pleasewait.gif" /></div>', option);
                $.modal('<div><center><h2>Please wait...</h2></center></div>', option);
                
                /*var myWidth = 320;
                var myHeight = 240;
                var option = {
                    close: false,
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                // Increase compatibility with unnamed functions  
                window.setTimeout(  
                    function() {  
                        $.modal('<img src="/global/images/loading2.gif" />', option);
                    },  
                    1000  
                ); */ // will work with every browser 
                
                //$('#submitOpt').append('&nbsp;&nbsp;&nbsp;<img src="/global/images/loading.gif">');
                //$('#submit_calc').after('&nbsp;&nbsp;&nbsp; Please wait, I\'m submitting job(s)...');
                //$('#submit_calc').attr("disabled", "disabled");
        }

ChiliBook.recipeFolder="/global/javascript/syntax/";ChiliBook.automaticSelector="pre";ChiliBook.lineNumbers=true;function messageFade()
{$("#message").hide().fadeIn("slow",function(){setTimeout("$('#message').fadeOut('slow');",2000);});}
function checkDocUpload()
{if(!$("#doctitle").val()){jAlert("You have to enter a document title<br />");return false;}
if(!$("#filename").val()){jAlert("You have to enter a file to upload<br />");return false;}}
function checkUpload()
{if(!$("#filename").val()){jAlert("You have to enter a file to upload<br />");return false;}}
function taskAdd(task_task_list_id)
{$("#task-loading").show();task_member_id=$("#task-add-member_id").val();task_description=$("#task-add-description").val();task_estimated_duration=$("#task-add-estimated_duration").val();task_estimated_duration_type=$("#task-add-estimated_duration_type").val();$.post("/task/ajax_save/",{task_list_id:task_task_list_id,member_id:task_member_id,description:task_description,estimated_duration:task_estimated_duration,estimated_duration_type:task_estimated_duration_type},function(data,textStatus){if(textStatus=='success'&&data>0){$("#new-task-holder").load("/task/ajax_new/"+data+"/",function(){$("#task-"+data).remove().appendTo("#list-open");});}
else{alert('There was a problem adding your task.');}
$("#task-add-member_id").val(0);$("#task-add-description").val("");$("#task-add-estimated_duration").val("");$("#task-add-estimated_duration_type").val("minutes");taskAddCancel();$("#task-loading").hide();});}
function taskAddCancel()
{$("#task-add-form-holder").slideUp('slow',function(){$("#section-links").show();});}
function taskAddShow()
{$("#section-links").hide();$("#task-add-form-holder").slideDown('slow');}
function taskToggle(subject,task_id,theme_name)
{$(subject+" > div.list-mark > a > img").attr("src","/"+theme_name+"/images/task_throbber.gif");him=$(subject);if(him.parent().attr("id")=="list-open")
{$.get("/task/toggle/"+task_id+"/",function(responseText,textStatus,XMLHttpRequest){$(subject).remove().prependTo("#list-closed");$(subject+" > div.list-mark > a > img").attr("src","/"+theme_name+"/images/checked.png");});}
else
{$.get("/task/toggle/"+task_id+"/",function(responseText,textStatus,XMLHttpRequest){$(subject).remove().appendTo("#list-open");$(subject+" > div.list-mark > a > img").attr("src","/"+theme_name+"/images/unchecked.png");});}}
function taskEdit(subject,task_id)
{$("#task-"+task_id+"-loading").show();$(subject+" > div.list-item").load("/task/ajax_edit/"+task_id+"/");}
function taskView(subject,task_id)
{$("#task-"+task_id+"-loading").show();$(subject+" > div.list-item").load("/task/ajax_view/"+task_id+"/");}
function taskSave(subject,task_id,form_id)
{$("#task-"+task_id+"-loading").show();task_member_id=$("#task-"+task_id+"-member_id").val();task_description=$("#task-"+task_id+"-description").val();task_estimated_duration=$("#task-"+task_id+"-estimated_duration").val();task_estimated_duration_type=$("#task-"+task_id+"-estimated_duration_type").val();task_actual_duration=$("#task-"+task_id+"-actual_duration").val();task_actual_duration_type=$("#task-"+task_id+"-actual_duration_type").val();$.post("/task/ajax_save/"+task_id+"/",{task_id:task_id,member_id:task_member_id,description:task_description,estimated_duration:task_estimated_duration,estimated_duration_type:task_estimated_duration_type,actual_duration:task_actual_duration,actual_duration_type:task_actual_duration_type},function(){$(subject+" > div.list-item").load("/task/ajax_view/"+task_id+"/");});}
function taskDelete(task_id,task_holder)
{if(confirm('Are you sure you want to delete this task?'))
{$.get('/task/delete/'+task_id+'/',function(){$(task_holder).remove();});}
return false;}
function revisionAddCancel()
{$("#revision-add-form-holder").slideUp('slow',function(){$("#section-links").show();});}
function revisionAddShow()
{$("#section-links").hide();$("#revision-add-form-holder").slideDown('slow');}
function componentAdd(component_project_id)
{$("#component-add-loading").show();component_name=$("#component-add-name").val();$.post("/component/ajax_save/",{project_id:component_project_id,name:component_name},function(data,textStatus){if(textStatus=='success'&&data>0){$("#component-list").append($("<option>").val(data).text(component_name));}
else{alert('There was a problem adding your component.');}
$("#component-add-name").val("");$("#component-add-loading").hide();});}
function componentEdit()
{$("#component-list > option").each(function(){opt=$(this);if(opt.attr("selected")){$("#component-edit-id").val(opt.val());$("#component-edit-name").val(opt.text());$("#component-edit-holder").slideDown("slow");return false;}});}
function componentEditSave(component_project_id)
{$("#component-edit-loading").show();component_id=$("#component-edit-id").val();component_name=$("#component-edit-name").val();$.post("/component/ajax_save/"+component_id+"/",{project_id:component_project_id,name:component_name},function(data,textStatus){if(textStatus=='success'&&data>0){$("#component-list > option").each(function(){opt=$(this);if(opt.val()==data){opt.text(component_name);return false;}});}
else{alert('There was a problem editing your component.');}
componentEditCancel();});}
function componentEditCancel()
{$("#component-edit-holder").slideUp('slow');$("#component-edit-name").val("");$("#component-edit-id").val(0);$("#component-edit-loading").hide();}
function componentDelete()
{if(confirm("Warning: This will delete all of the selected components! Are you sure you want to continue?"))
{$("#component-delete-loading").show();errors=false;removed_ids=new Array();$("#component-list > option").each(function(){opt=$(this);if(opt.attr("selected"))
{$.get("/component/ajax_delete/"+opt.val()+"/",function(data,textStatus){if(textStatus=="success"&&data>0){removed_ids[data]=data;}
else{errors=true;}});}});$("#component-list > option").each(function(){opt=$(this);for(id in removed_ids)
{if(opt.val()==id)
{opt.remove();}}});$("#component-delete-loading").hide();if(errors)
{alert("There was a problem deleting one or more components.");}}}
function confirmDelete(entity)
{if(confirm('Are you sure you want to delete this '+entity+'?'))
{return true;}
else
{return false;}}
function reverseList(listElementId)
{listElement=document.getElementById(listElementId);listOptions=Array();for(i=0;i<listElement.options.length;i++)
{listOptions[i]=listElement.options[i];}
listOptions.reverse();for(i=0;i<listOptions.length;i++)
{listElement.options[i]=listOptions[i];}}
function checkPassword(new_password,conf_password)
{if($('#'+new_password).val()==$('#'+conf_password).val())
{return true;}
else
{alert('Your new passwords do not match!');document.getElementById(new_password).focus();return false;}}
function setActiveProject(selectElementId)
{$('#project-selector > div.content').hide();$('#project-throbber').show();project_id=$('#'+selectElementId).val();$.get('/dashboard/ajax_project/'+project_id+'/',function(){window.location.reload();});}
function fieldsetToggle(fieldset)
{content=$('> div',fieldset);if(fieldset.is('.collapsed'))
{fieldset.removeClass('collapsed');content.slideDown('normal');}
else
{content.slideUp('normal',function(){fieldset.addClass('collapsed');});}}
function toggleFieldset()
{fieldset=$(this).parent().parent();fieldsetToggle(fieldset);return false;}
function increase(elem)
{$(elem).val(parseInt($(elem).val())+1);return false;}
function decrease(elem)
{$(elem).val(parseInt($(elem).val())-1);return false;}
function removeAttachment(button)
{$(button).parent().remove();return false;}
function addAttachment()
{$("#attachments-list").append($("<div>").attr("class","form-item").append('<input type="file" class="form-file" name="attachment" /> <input type="button" class="form-button" value="Remove" onclick="return removeAttachment(this);" />'));return false;}
$(document).ready(function()
{$("fieldset.collapsible > legend").each(function(){legend=$(this);legend_text=legend.text();legend.text("");legend.append($("<a>").attr("href","#").text(legend_text).bind("click",toggleFieldset));});$("fieldset.collapsed").each(function(){$("> div.content",this).slideUp("normal");});$("textarea").elastic();if($("#message"))
{setTimeout("messageFade()",500);}});
function checkAddMemberForm(){
if(!$('#email').val()){jAlert('<b>You have to enter the Email','Warning');return false;}if(!$('#logname').val()){jAlert('<b>You have to enter the Logname','Warning');return false;}if(!$('#password').val()){jAlert('<b>You have to enter the Password','Warning');return false;}}

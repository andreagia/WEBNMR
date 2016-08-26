<%inherit file="/base.mako"/>
<%def name="js()">
    <script  type="text/javascript"> 
      $(document).ready(function() {
       $("#formID").validationEngine()
      })
    </script>
    
</%def>
<fieldset>
<legend>Create Account</legend>
<form name="formID" id="formID" action="${h.url('/admin/save_user')}" method="POST">
<table id="signup">
    <tr>    
        <td class="labelcell">Firstname</td>
        <td class="fieldcell"><input type="text" name="firstname" class="validate[required,custom[onlyLetter],length[2,30]]" id="firstname" maxlength="30" /></td>
        <td class="labelcell">Lastname</td>
        <td class="fieldcell"><input type="text" name="lastname" class="validate[required,custom[onlyLetter],length[2,30]]" id="lastname" maxlength="30" /></td>
    </tr>
    <tr>
        <td class="labelcell">Email</td>
        <td class="fieldcell"><input type="text" name="email" class="validate[required,custom[email],length[1,50]]" id="email" maxlength="50" /></td>
        <td class="labelcell">Logname</td>
        <td class="fieldcell"><input type="text" name="logname" class="validate[required,custom[onlyLetter],length[5,20]]" id="logname" maxlength="20" /></td>
    </tr>
    <tr>
        <td class="labelcell">Password</td>
        <td class="fieldcell"><input type="password" name="password" class="validate[required,length[5,10]]" id="password" maxlength="10" /></td>
    <tr>
        <td colspan="4"><center><input type="submit" id="submit" class="button" name="Submit" value="Add User"></center></td>      
    </tr>
</table>
</fieldset>
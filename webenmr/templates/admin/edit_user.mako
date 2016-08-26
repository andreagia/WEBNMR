<%inherit file="/base.mako"/>
<%def name="js()">
    <script  type="text/javascript"> 
      $(document).ready(function() {
       $("#formID").validationEngine()
      })
    </script>
    
</%def>
<fieldset>
<legend>Edit Account</legend>
<form name="formID" id="formID" action="${h.url(controller=u'admin', 
                                                action='save_user',
                                                id=unicode(c.user.id)
                                                )}"
                                 method="POST">
<table id="signup">
    <tr>    
        <td class="labelcell">Firstname</td>
        <td class="fieldcell"><input type="text" name="firstname" class="validate[required,custom[onlyLetter],length[2,30]]" id="firstname" maxlength="30" value="${c.user.firstname}" /></td>
        <td class="labelcell">Lastname</td>
        <td class="fieldcell"><input type="text" name="lastname" class="validate[required,custom[onlyLetter],length[2,30]]" id="lastname" maxlength="30" value="${c.user.lastname}" /></td>
    </tr>
    <tr>
        <td class="labelcell">Email</td>
        <td class="fieldcell"><input type="text" name="email" class="validate[required,custom[email],length[4,50]]" id="email" maxlength="50" value="${c.user.email}" /></td>
        <td class="labelcell">Logname</td>
        <td class="fieldcell"><input type="text" name="logname" class="validate[required,custom[onlyLetter],length[4,20]]" id="logname" maxlength="20" value="${c.user.logname}" /></td>
    </tr>
    <tr>
        <td class="labelcell">Password (if you leave it empty, the password don't change)</td>
        <td class="fieldcell"><input type="password" name="password"  id="password" maxlength="10" /></td>
    <tr>
        <td colspan="4"><center><input type="submit" id="submit" class="button" name="Submit" value="Add User"></center></td>      
    </tr>
</table>
</fieldset>
<%inherit file="/base.mako"/>
<fieldset>
<legend>Account Edit</legend>
<form name="form1"  action="${h.url('/access/account_create_db')}" method="POST" onSubmit="return checkAddMemberForm(this)" >

<table id="signup">
    <tr>
        <td class="labelcell">Email</td>
        <td class="fieldcell"><input type="text" name="email" id="email" maxlength="50" value="${c.user.email}" /></td>
        <td class="labelcell">Logname</td>
        <td class="fieldcell"><input type="text" name="logname" id="logname" maxlength="20" value="${c.user.logname}" /></td>
    </tr>
    <tr>
        <td class="labelcell">New Password</td>
        <td class="fieldcell"><input type="password" name="password" id="password" maxlength="10" /></td>
    </tr>
    <tr>
        <td colspan="4"><center><input type="submit" id="submit" class="button" name="Submit" value="Change Profile"></center></td>      
    </tr>
</table>
<input type="hidden" name="from" value="modify" />
</form>
</fieldset>
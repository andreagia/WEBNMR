<%inherit file="/base.mako"/>
<%def name="js()">
    <script  type="text/javascript"> 
      $(document).ready(function() {
       $("#formID").validationEngine();
      })
    </script>
</%def>
<fieldset>
    <legend>Account Creation</legend>
    <form name="formID"  action="${h.url('/access/account_create_db')}" method="POST" >

        <table id="signup">

            <tr>
                <td class="labelcell">Email</td>
                <td class="fieldcell"><input type="text" class="validate[required,custom[email],length[5,50]]" name="email" id="email" maxlength="50" /></td>
                <td class="labelcell">Logname</td>
                <td class="fieldcell"><input type="text" class="validate[required,custom[onlyLetter],length[4,20]]" name="logname" id="logname" maxlength="20" /></td>
            </tr>
            <tr>
                <td class="labelcell">Password</td>
                <td class="fieldcell"><input type="password" class="validate[required,length[6,10]]" name="password" id="password" maxlength="10" /></td>
            </tr>
            <tr>
                <td colspan="4"><center><input type="submit" id="submit" class="button" name="Submit" value="Create Login"></center></td>      
            </tr>
        </table>
        <input type="hidden" name="from" value="creation" />
    </form>
</fieldset>
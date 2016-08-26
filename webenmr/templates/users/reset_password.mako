<%inherit file="/base2.mako"/>
    <h2>Forgotten Password</h2>
    <form id="formID" action="${h.url(controller='users', action='pass_reset')}" method="post" >
    <fieldset>
        <legend>Password Reset</legend>
	<label>To obtain a new password, please enter the email address you initially used to sign up for your account. </label>
<br>
        <div class="form-item" style="background: none repeat scroll 0% 0% rgb(206, 227, 246);">
            <label class="lmail" for="addmail">Enter your email address:</label>
            <input type="text" name="yourv3ry3ma1l"  maxlength="50" id="addmail" class="validate[required,custom[email],length[5,50]]" />
        </div>
    <br>
    <div class="form-buttons">
            <input type="submit" value="Send Request" class="form-button" />
            <input type="reset" value="Cancel" id="Cancel" class="form-button" onClick="window.location.href = 'http://py-enmr.cerm.unifi.it:8000';" />
    </div>
	</fieldset>
	<br>
	If you would like further assistance, please <a href="/feedback/index">contact us</a>
</form>

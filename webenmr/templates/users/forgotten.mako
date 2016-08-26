<%inherit file="/base2.mako"/>
 % if h.flash.has_message():
	    <div id="message-wrapper"><div id="message"><p
	    class="${h.flash.get_message_type()}">${h.flash.get_message_text()}</p></div></div>
 % endif
<fieldset>
    <legend><h2>Forgotten your username/password?</h2></legend>
    If you have forgotten your username and/or password, we can reset the password and send the login details to your email address. <br />
    Please enter the email address you used when you created your AMPS-NMR, Xplor-NIH or MaxOcc account.<br />
    <form id="forgotten" action="${h.url(controller='users', action='pass_reset')}" method="POST">
        E-mail address: <input type="text" name="3m61l" id="3m61l" />
        <input type="hidden" name="email" id="email" />
        <input type="submit" name="submit" value="Send Email" />
        
        <br />
	    <div style="color: red;">
        %if 'pass_reset' in session:
            ${session['pass_reset']}
        %endif
        </div>
    </form>
</fieldset>


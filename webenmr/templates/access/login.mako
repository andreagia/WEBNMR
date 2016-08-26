<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <title>Login @ WebENMR</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <link rel="stylesheet" type="text/css" href="/global/styles/behaviour.css" />
    <LINK REL="stylesheet" TYPE="text/css" HREF="/webenmr/styles/webenmr.css" />
    <script type="text/javascript" src="/global/javascript/jquery.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.elastic.js"></script>
    <script type="text/javaScript" src="/global/javascript/jquery.chili.js"></script>
    <script type="text/javascript" src="/global/javascript/functions.js"></script>
</HEAD>
<BODY onLoad="window.focus();document.login.user.focus();">
<br /><br /><br /><br />
<center>
<div id="container">
    % if h.flash.has_message():
       <div id="message-wrapper"><div id="message"><p class="${h.flash.get_message_type()}">${h.flash.get_message_text()}</p></div></div>
    % endif
</div>

<div class="sidebox">
    <div class="boxhead"><h2>:: Access Form to WebENMR ::</h2></div>
        <div class="boxbody">
        
        <p>Access verification:</p>
        <p>
             <form name="login" id="login" method="post" action="${h.url('/access/login')}" > 
             <label>Username:
            <input name="user_name" type="text" id="user" tabindex="1" class="text"  />  
             </label>
             <label>Password:  
            <input name="user_pwd" type="password" id="password" tabindex="2" class="text" />
             <input type="submit" tabindex="3" value="Submit" class="buttons" />
             </label> 
            </form>
            <p>If you have a certificate click <a href="https://py-enmr.cerm.unifi.it">here</a></p>
        </p>
        <br />
        </div>
        <!--[if lt IE 7]>
      <div>&nbsp;</div>
        <div id="item-list">
          <div class="item-box item-overdue">
            <h4>WARNING: You are running an unsupported browser</h4>
            <div class="item-content">
              <p><strong>Amber Web Portal</strong> has been written for Mozilla Firefox,
              Opera, Apple Safari, and Microsoft Internet Explorer 7.0 and higher.
              Your version of Internet Explorer is not supported, and may not work.
              Please upgrade your browser to one of those listed above.</p>
            </div>
            <div class="item-links">&nbsp;</div>
          </div>
        </div>
      </div>
      <![endif]-->
</div>
</BODY>
</HTML>

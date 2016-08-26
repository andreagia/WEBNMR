<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
   <title>e-NMR web portal :: Amber introduction ::</title>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8\n\n">
  <meta name="description" content="Deploying and unifying the NMR e-Infrastructure in System Biology">
  <meta name="author" content="Ferella, Giachetti, Morelli, CERM research infrastructure, Florence University">
  <meta name="keywords" content="eNMR,NMR,Amber,grid">
  <!--<link rel="stylesheet" type="text/css" media="print" href="../Main/print.css"/>-->

  <link rel="stylesheet" type="text/css" media="screen, projection" href="/global/css/mainstyle.css">
  <link rel="stylesheet" href="/global/css/my.css" type="text/css" media="all">
  <link rel="stylesheet" type="text/css" href="/global/css/validationEngine.jquery.css"  media="screen" charset="utf-8" />
  <link rel="stylesheet" href="/global/javascript/jquery-ui-1.8/development-bundle/themes/base/jquery.ui.all.css" type="text/css" media="screen" />
  
  <!--<link rel="alternate" type="application/rss+xml" title="RSS" href="http://haddock.chem.uu.nl/Main/haddock.rss" />-->
  <link rel="home" href="http://haddock.chem.uu.nl/enmr" title="Home">
  <link rel="Shortcut icon" href="/global/images/favicon.ico">


  <!-- Page specific modification to the general CSS style -->
  <style type="text/css">
    .blue body { background-image:url("/global/images/body-background.gif"); }
	.blue #path { background-image:url("/global/images/path-blue.png"); }
	.blue #header { height:150px; background-image:url("/global/images/header-enmr.png"); }
	.blue #navbar { background-image:url("/global/images/navbar-blue.png"); }
	.blue #navbar a:hover { color:#EBF8C9; background-image:url("/global/images/navbarshadow-blue.png"); }
	.blue #navbar .current a { color:#FFFFFF; background-image:url("/global/images/navbarshadow-blue.png"); }
	.blue #subheader { background-image:url("/global/images/subheader-blue.png"); }
	.blue #footer { background:#96ACC4; }
	.blue .container { background-image:url("/global/images/container-blue.png"); }
	.blue #path a:hover { color:#EBF8C9; }
	.blue #path a, #path strong, #path li { color:#99CCD5; }
	.blue #navbar a { color:#99CCD5; }
	.blue #navbar { border-color:#001A3B; }
	.blue #rssfeed { background:url(../Images/rssicon-blue.png) no-repeat 0 0; }
	.blue .onsitelink, .onsitelink:visited { background:url("../Images/docicon-blue-off.png") no-repeat 0 0; }
	.blue .offsitelink, .offsitelink:visited { background:url("../Images/linkicon-blue-off.png") no-repeat 0 0; }
	.blue .emaillink, .emaillink:visited { background:url("../Images/emailicon-blue-off.png") no-repeat 0 0; }
	.blue a.onsitelink:hover { background:url("../Images/docicon-blue-on.png") no-repeat 0 0; }
	.blue a.offsitelink:hover { background:url("../Images/linkicon-blue-on.png") no-repeat 0 0; }
	.blue a.emaillink:hover { background:url("../Images/emailicon-blue-on.png") no-repeat 0 0; }
	.blue dt, dt a { color:#001A3B }
	.blue #subheader span, #subheadersidebar { color:#001A3B }
	.blue .topItem  { background-color:#001C47 }

  </style>
  
    <!--<script type="text/javascript" src="/global/javascript/jquery.easing.js"></script>-->
    <script type="text/javascript" src="/global/javascript/jquery-1.4.2.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.form.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.validationEngine-en.js" ></script>
    <script type="text/javascript" src="/global/javascript/jquery.validationEngine.js" ></script>
    <script type="text/javascript" src="http://www.google.com/recaptcha/api/js/recaptcha_ajax.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery-ui-1.8/js/jquery-ui-1.8.custom.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery-ui-1.8/development-bundle/ui/jquery.effects.core.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery-ui-1.8/development-bundle/ui/jquery.ui.dialog.js"></script>
    <script  type="text/javascript">
	$(document).ready( function() {
	    $("#contact").validationEngine();
	    Recaptcha.create("6Leg-LwSAAAAANVnkLR5QQd1b3hnILUXZMlG7TJ3 ", "r3c6p7ch6", {theme: "white"});
	    
		%if c.title == "AnisoFIT":
			$("#navbar").find("li").removeAttr("class");
            $("#navbar").find("li").eq(10).attr("class", "current");
		 %endif
		
		%if c.subtitle == "":
			$("#header").children("div").first().next().css("padding-top", '20px');
		 %endif
		 
		
	    var optionsContact = { 
			//target:        '#output1',   // target element(s) to be updated with server response 
			beforeSubmit:   validateRequest,  // pre-submit callback
			dataType:  'script',        // 'xml', 'script', or 'json' (expected server response type) 
			success:  processContactSubmit   // post-submit callback 
		}; 
		   
	    // bind form using 'ajaxForm' 
	    $('#contact').ajaxForm(optionsContact);
	    
	    $("#popup-success").dialog({
			autoOpen: false,
			height: 200,
			width: 600,
            position: 'center',
			modal: true,
			buttons: {
				'Close': function() {
					 var loc = window.location.href;
					 var lloc = loc.split("/");
					 var len = lloc.length;
					 var query = lloc[len-1]
                      window.location = "/access/index/"+query;
				},
			},
			close: function() {
			   var loc = window.location.href;
					 var lloc = loc.split("/");
					 var len = lloc.length;
					 var query = lloc[len-1]
				window.location = "/access/index"+query;
			}
		});
	    //$("#popup-success").dialog('open');
	});
    </script>
    
    <script  type="text/javascript">
	function validateRequest(){
	    return $("#contact").validationEngine({returnIsValid:true});
	}
	
	function processContactSubmit(data){
	   var isValid = data.split("__")[0]
	   var errcode = data.split("__")[1]
	   if(isValid == "False"){
	     $("#r3c6p7ch6").prepend('<span id="error" style="color: red;">Error. Fill field below with two new words.</span>');
	     Recaptcha.reload();
	   }
	   else{
	     $("#error").remove();
	     //magari è meglio un popup che avvisa che la mail è stata mandata
	     //window.location = "/access/index";
		 $("#popup-success").dialog('open');
	   }
	}
    </script>
    
</head>
 
<body class="blue">
 <div id="col2" class="container">
   <div id="path">
     <ul>
       <li><a href="http://haddock.chem.uu.nl/enmr/index.php">home &gt;&gt;</a></li>
       <li><a href="/access/index?type=${c.breadcrump}">${c.title}</a></li>
     </ul> 
   </div>
   <div id="header">
    <div style="padding-top:40px; padding-left:30px; color:white; font-size:350%; font-weight:bold; z-index:2">${c.title}</div>
    <div style="padding-left:44px; color:white; font-size:100%; z-index:2">${c.subtitle}</div>
    <div style="padding-top:5px; padding-left:50px; color:white; font-size:200%; z-index:2">e-NMR GRID-enabled web portal</div>
   </div>
   <div id="navbar">
    <ul>
        <li><a href="http://haddock.chem.uu.nl/enmr/index.php">Home</a></li>
        <li><a href="http://haddock.chem.uu.nl/enmr/haddock.php">HADDOCK</a></li>
        <li><a href="http://haddock.chem.uu.nl/enmr/xplor-nih.html">Xplor-NIH</a></li>
        <li class="current"><a href="http://py-enmr.cerm.unifi.it">AMBER</a></li>
        <li><a href="http://www.enmr.eu/webportal/cyana.html">CYANA</a></li>
        <li><a href="http://haddock.chem.uu.nl/enmr/csrosetta.php">CS-ROSETTA</a></li>
        <li><a href="http://haddock.chem.uu.nl/enmr/services/TALOS/">TALOS+</a></li>
        <li><a href="http://nmr.cabm.rutgers.edu/autoassign/cgi-bin/aaenmr.py">AutoAssign</a></li>
        <li><a href="http://www.enmr.eu/webportal/mars.html">MARS</a></li>
        <li><a href="http://www.enmr.eu/webportal/mdd.html">MDD</a></li>
		<li><a href="http://py-enmr.cerm.unifi.it/access/index?type=anisofit">AnisoFIT</a></li>
        <li><a href="http://haddock.chem.uu.nl/enmr/format-converter.html">FormatConverter</a></li>
        <li><a href="http://haddock.chem.uu.nl/enmr/services/3DDART/">3D-DART</a></li>	
        <li><a href="http://haddock.chem.uu.nl/enmr/gridice.html">eNMR-Grid</a></li>
        <li><a href="http://www.enmr.eu/WIKI">eNMR Wiki</a></li>
    </ul>
   </div>
   <div id="subheader">
    <ul>
        <li><span>Leave feedback</span></li>
    </ul>
    <!--<p id="subheadersidebar">Login</p>-->

   </div>
    
    <div id="content">
        <div id="maincol">
	 % if h.flash.has_message():
                    <div id="message-wrapper"><div id="message"><p
                    class="${h.flash.get_message_type()}">${h.flash.get_message_text()}</p></div></div>
            % endif
            <form id="contact" class="formular" method="post" action="${h.url(controller='feedback', action='sendMail')}">
                Use the contact form below to submit your request and/or feedback. All fields are required.
                    <fieldset>
                            <legend>User informations</legend>
            
                                <label for="firstname" class="feedback">First name</label>
                                <input value=""  class="validate[required,custom[onlyLetter],length[2,50]] text-input" type="text" name="firstname" id="firstname" />
                        
                                <label for="lastname" class="feedback">Last name</label>
                                <input value=""  class="validate[required,custom[onlyLetter],length[2,50]] text-input" type="text" id="lastname" name="lastname"  />
                        
                                <label for="university" class="feedback">University OR Organization</label>
                                <input value=""  class="validate[required,custom[onlyLetter],length[5,100]] text-input" type="text" id="university" name="university"  />
                        
                                <label for="department" class="feedback">Department</label>
                                <input value=""  class="validate[required,custom[onlyLetter],length[4,100]] text-input" type="text" id="department" name="department"  />
                        
                                <!--<label for="address" class="feedback">Address (optional)</label>-->
                                <!--<input value=""  class="validate[optional, length[0,100]] text-input" type="text" id="address" name="address"  />-->
                                <!---->
                                <!--<label for="postalcode" class="feedback">Postal code (optional)</label>-->
                                <!--<input value=""  class="validate[optional,custom[onlyNumber],length[3,10]] text-input" type="text" id="postalcode" name="postalcode"  />-->
                                <!---->
                                <!--<label for="city" class="feedback">City (optional)</label>-->
                                <!--<input value=""  class="validate[optional,custom[onlyLetter],length[2,100]] text-input" type="text" id="city" name="city"  />-->
                                <!---->
                                <!--<label for="country" class="feedback">Country (optional)</label>-->
                                <!--<input value=""  class="validate[optional,custom[onlyLetter],length[3,100]] text-input" type="text" id="country" name="country"  />-->
                                <!---->
                    </fieldset>
                    <fieldset>
                            <legend>Email</legend>
                                    <label for="email" class="feedback">Email address</label>
                                    <input value=""  class="validate[required,custom[email]] text-input" type="text" name="email" id="email"  />
                            
                                    <label for="email2" class="feedback">Confirm email address</label>
                                    <input value="" class="validate[required,confirm[email]] text-input" type="text" name="email2"  id="email2" />
                    </fieldset>
                    <fieldset>
            
                            <legend>Message</legend>
				    <label for="subject" class="feedback">subject</label>
				    <select class="validate[required] select" name="subject" id="subject">
				      <option value="">--------------- Please Select ---------------</option>
				      <option value="Feedback">Leave a feedback</option>
				      <option value="Access">Report a access problem</option>
				      <option value="Registration">Report a registration problem</option>
				      <option value="Password">Report a password recovery problem</option>
				      <option value="Bug">Report a bug</option>
				      <option value="Other">Other query</option>
				    </select>
                                    <label for="comments" class="feedback">Message</label>
                                    <textarea value="" class="validate[required,length[6,300]] text-input" name="comments" id="comments" /> </textarea>
                    </fieldset>
                    <fieldset>
                            <legend>Conditions</legend>
                            <div class="infos">
                                We inform you that the protection of the privacy of your personal details 
                                will be treated under the current regulations and with only aim regarding your feedback/query.
                                <br />
                                <br />
                                Checking this box indicates that you are agree to accept uses of your personal data. You must accept these terms  to send this feedback/query.
                            </div>
                            <div id="agree">
                                <input class="validate[required] checkbox" type="checkbox"  id="agree"  name="agree"/>
                                <span>I agree.</span>
                            </div>
                    </fieldset>
		    <fieldset>
                            <legend>Captcha</legend>
                            <div id="r3c6p7ch6">
                                
                            </div>
                    </fieldset>
            
                    <input class="submit" type="submit" value="Send"/>
                    <hr/>
            </form>
        </div>
	<div id="popup-success" title="Mail is sent">
	   <!--<img src="/global/images/ok2.png" alt="Mail is sent correctly" title="Mail is correctly sent">-->
	   <h4>The mail has sent. Please, wait while your request is being processed. A reply will be send you as soon as possible.</h4>
	</div>
	 <div id="subcol">
	 </div>
    </div>
 
    
  
    <div id="navbar">
        <ul>
            <li><a href="http://haddock.chem.uu.nl/enmr/index.php">Home</a></li>
            <li><a href="http://haddock.chem.uu.nl/enmr/haddock.php">HADDOCK</a></li>
            <li><a href="http://haddock.chem.uu.nl/enmr/xplor-nih.html">Xplor-NIH</a></li>
            <li class="current"><a href="http://py-enmr.cerm.unifi.it">AMBER</a></li>
            <li><a href="http://www.enmr.eu/webportal/cyana.html">CYANA</a></li>
            <li><a href="http://haddock.chem.uu.nl/enmr/csrosetta.php">CS-ROSETTA</a></li>
            <li><a href="http://haddock.chem.uu.nl/enmr/services/TALOS/">TALOS+</a></li>
            <li><a href="http://nmr.cabm.rutgers.edu/autoassign/cgi-bin/aaenmr.py">AutoAssign</a></li>
            <li><a href="http://www.enmr.eu/webportal/mars.html">MARS</a></li>
            <li><a href="http://www.enmr.eu/webportal/mdd.html">MDD</a></li>
			<li><a href="http://py-enmr.cerm.unifi.it/access/index?type=anisofit">AnisoFIT</a></li>
            <li><a href="http://haddock.chem.uu.nl/enmr/format-converter.html">FormatConverter</a></li>
            <li><a href="http://haddock.chem.uu.nl/enmr/services/3DDART/">3D-DART</a></li>	
            <li><a href="http://haddock.chem.uu.nl/enmr/gridice.html">eNMR-Grid</a></li>
            <li><a href="http://www.enmr.eu/WIKI">eNMR Wiki</a></li>
        </ul>
     </div>
    <div id="footer">
       <p>2008 &copy; NMR Department Utrecht. All rights reserved<br>
	<a href="http://validator.w3.org/check/referer" title="Validate this page as XHTML 1.0 Strict." rel="external">XHTML | </a>
   
	<a href="http://jigsaw.w3.org/css-validator/check/referer?warning=no&amp;profile=css2" title="Validate the CSS used on this page." rel="external" >CSS</a></p>
    </div>
  </div>
 </body>
</html>


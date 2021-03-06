
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <%def name="show_current_base(page_base)">\
    % if c.page_base == page_base:
     class="current"\
    % endif
    </%def>
    <%def name="show_current_page(page_title)">\
    % if c.page_title == page_title:
     class="current"\
    % endif
    </%def>
    <%def name="css()"></%def>
    <%def name="js()"></%def>
    
    <title>${c.page_base}: ${c.page_title} @ We-NMR</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <meta name="description" content="Deploying and unifying the NMR e-Infrastructure in System Biology"/>
    <meta name="author" content="Ferella, Giachetti, Morelli, CIRMMP-CERM, Florence University"/>
    <meta name="keywords" content="eNMR,WeNMR,NMR,Amber,AMPS-NMR,grid"/>
	<meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content=" -1">
    <meta http-equiv="Cache-Control" content="no-cache, must-revalidate">


  
    <link rel="stylesheet" type="text/css" media="screen, projection" href="/global/css/mainstyle.css"/>
    <link rel="home" href="http://haddock.chem.uu.nl/enmr" title="Home" />
    <link rel="Shortcut icon" href="/global/images/favicon.ico" />
    
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
	  .sidebox {
		width: 113%;
	  }
    </style>
   
    
    <link rel="stylesheet" href="/global/css/my.css" type="text/css" media="all" />
    <link rel="stylesheet" href="/global/javascript/jquery-ui-1.8/development-bundle/themes/base/jquery.ui.all.css" type="text/css" media="screen" />
    <link rel="stylesheet" href="/global/javascript/jqueryFileTree/jqueryFileTree.css"  type="text/css" media="screen" />
    <link rel="stylesheet" href="/global/javascript/jquery.contextMenu/jquery.contextMenu.css"  type="text/css" />
    <!--<link rel="stylesheet" type="text/css" href="/webenmr/styles/webenmr.css" /> -->

    <link rel="stylesheet" type="text/css" href="/webenmr/styles/jquery.alerts.css" />
    <link rel="stylesheet" type="text/css" href="/global/css/validationEngine.jquery.css"  media="screen" charset="utf-8" /> 
    ${self.css()}
	
    <script type="text/javascript" src="/global/javascript/jquery-1.4.2.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.elastic.js"></script>
    <script type="text/javaScript" src="/global/javascript/jquery.chili.js"></script>

    
    <script type="text/javascript" src="/global/javascript/jquery.validationEngine-en.js" ></script>
    <script type="text/javascript" src="/global/javascript/jquery.validationEngine.js" ></script>
	
	<script  type="text/javascript"> 
      $(document).ready(function() {
       $("#formID").validationEngine()
	   
      })
    </script>
    ${self.js()}
  </head>
  
  
<body class="blue">
  <div id="col2" class="container">
    <div id="path">
   	<ul>
	  <li><a href="http://www.wenmr.eu">home &gt;&gt;</a></li>
	  <li><a href="http://py-enmr.cerm.unifi.it/access/index/${session['PORTAL']}">${session['PORTAL'].upper()}</a></li>
	</ul> 
    </div>
    <div id="header">
        <div style="padding-top:40px; padding-left:30px; color:white; font-size:350%; font-weight:bold; z-index:2">${session['PORTAL'].upper()}</div>
		%if session['PORTAL'] == 'amps-nmr':
			  <div style="padding-left:44px; color:white; font-size:100%; z-index:2">(including paramagnetic restraints plugin)</div>
			  <div style="padding-top:5px; padding-left:50px; color:white; font-size:200%; z-index:2">WeNMR GRID-enabled web portal</div>
	    %elif session['PORTAL'] == 'oops!':
		  <div style="padding-left:44px; padding-top: 20px; color:white; font-size:100%; z-index:2"></div>
		%else:
		  <div style="padding-left:44px; padding-top: 20px; color:white; font-size:100%; z-index:2"></div>
		  <div style="padding-top:5px; padding-left:50px; color:white; font-size:200%; z-index:2">WeNMR GRID-enabled web portal</div>
		%endif
        
    </div>
    <div id="navbar">
      <ul>
		<li><a href="http://www.wenmr.eu">WeNMR home</a></li>
		<li><a href="http://www.wenmr.eu/wenmr/nmr-services">NMR services</a></li>
		<li><a href="http://www.wenmr.eu/wenmr/saxs-services">SAXS services</a></li>
		<li><a href="http://www.wenmr.eu/wenmr/support/wenmr-support">WeNMR Support Center</a></li>
    </ul>
    </div>
    <div id="subheader">
      <ul>
        <li><span>Welcome to ${session['PORTAL'].upper()} web portal</span></li>
	  </ul>
	  <p id="subheadersidebar">Profile &gt;&gt;</p>
    </div>
   <div id="content">

      <!--<div>
          <br style="clear: left" />
	</div>-->
      
      
      % if h.flash.has_message():
	    <div id="message-wrapper"><div id="message"><p
	    class="${h.flash.get_message_type()}">${h.flash.get_message_text()}</p></div></div>
      % endif

      <!--<br />
      <br />-->
	${next.body()}
   </div>

	

  <div id="navbar">
    <ul id="navbarul">
        <li><a href="http://www.wenmr.eu">WeNMR home</a></li>
		<li><a href="http://www.wenmr.eu/wenmr/nmr-services">NMR services</a></li>
		<li><a href="http://www.wenmr.eu/wenmr/saxs-services">SAXS services</a></li>
		<li><a href="http://www.wenmr.eu/wenmr/support/wenmr-support">WeNMR Support Center</a></li>
    </ul>
  </div>
  <div id="footer">
    <p>2008 &copy; NMR Department Utrecht. All rights reserved<br />
     <a href="http://validator.w3.org/check/referer" title="Validate this page as XHTML 1.0 Strict." rel="external">XHTML | </a>

     <a href="http://jigsaw.w3.org/css-validator/check/referer?warning=no&amp;profile=css2" title="Validate the CSS used on this page." rel="external" >CSS</a></p>
  </div>
   
</div>
 </body>
</html>

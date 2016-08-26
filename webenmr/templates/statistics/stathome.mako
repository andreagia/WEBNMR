<%inherit file="/base.mako"/>
<%def name="css()">
    <!--<link href="/global/css/statistics.css" rel="stylesheet" type="text/css" />-->
</%def>

<%def name="js()">
    <!--<script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/statistics.js" ></script>-->
</%def>
    
<h3>Statistics for AMPS-NMR portal since the opening of the portal</h3>
    <div id="opening"></div>
    <script type="text/javascript">
        var str = '${c.stringResults | n}'
        //str = str.replace("&lt;", "<")
        //str = str.replace("&gt;", ">")
        $("#opening").html(str)
    </script>
    
    <br/>
    <br/>
<h3>Statistics for AMPS-NMR portal since November 1st 2010 (start of WeNMR)</h3>
    <div id="November2010"></div>
    <script type="text/javascript">
        var str = '${c.stringResults2 | n}'
        //str = str.replace("&lt;", "<")
        //str = str.replace("&gt;", ">")
        $("#November2010").html(str)
    </script>

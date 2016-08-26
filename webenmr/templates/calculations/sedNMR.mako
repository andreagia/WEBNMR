
<%inherit file="/base2.mako"/>
<%def name="css()">
    <link href="/global/styles/jqueryFileTree.css" rel="stylesheet" type="text/css" />
    <link href="/global/css/pcs-rdc_fitting.css" rel="stylesheet" type="text/css" />
    <link rel="stylesheet" type="text/css" href="/global/javascript/jquery.jqplot.1.0.3r1117/jquery.jqplot.css" />
    <style>
        /*.slider_line {
            text-align: center;
            font: normal normal bold 0.9em Arial, sans-serif;
            color: black;
        }
        .label {
            display: block;
            float: left;    
            width: 170px;
            text-align: right;  
        }
        .px {
            float: right;
            display: block;
            text-align: left;
            margin: -24px 132px 0 0;
        }*/
        #slider_box {
            width: 410px;
            float:left;
        }
        .slider {
            width: 300px;
        }
        
        .device-schema {
            float:right;
            width:300px;
        }
        
	</style>
</%def>

<%def name="js()">
    <script type="text/javascript" src="/global/javascript/jquery.simplemodal-1.4.1.js" ></script>
    <script type="text/javascript" src="/global/javascript/jGrowl-1.2.4/jquery.jgrowl_compressed.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery-ui-1.8/js/jquery-ui-1.8.custom.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.form.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.validate.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.xml.js"></script>
    <!--[if lt IE 9]><script language="javascript" type="text/javascript" src="/global/javascript/jquery.jqplot.1.0.3r1117/excanvas.js"></script><![endif]-->
    <script type="text/javascript" src="/global/javascript/jquery.jqplot.1.0.3r1117/jquery.jqplot.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.jqplot.1.0.3r1117/plugins/jqplot.canvasTextRenderer.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.jqplot.1.0.3r1117/plugins/jqplot.canvasAxisLabelRenderer.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.jqplot.1.0.3r1117/plugins/jqplot.highlighter.min.js"></script>
    <script type="text/javascript" src="/global/javascript/jquery.jqplot.1.0.3r1117/plugins/jqplot.cursor.min.js"></script>

    <!--<script type="text/javascript" src="/global/javascript/pcs-rdc_fitting2.js" ></script>-->
    <script>
        var maxFreq = {}
        maxFreqA = {
            "7.9502": 5500,
            "5.969": 7000,
            "4.4958": 9000,
            "3.429": 12000,
            "4.3942": 7000,
            "2.4638": 18000,
            "3.2258": 10000,
            "2.032": 25000,
            "2.6162": 15000,
            "1.5748": 30000,
            "1.143": 40000,
            "0.625": 60000
        }

        maxFreqB = {
            "5.6": 7000,
            "3.0": 15000,
            "2.6": 24000,
            "1.7": 35000,
            "1.5": 42000,
            "0.9": 67000
        }

        maxFreqJ = {
            "6.4": 8000,
            "2.6": 19000,
            "2.2": 24000,
            "1.7": 35000,
            "0.5": 80000,
            "0.35": 110000
        }
        
        maxFreqD = {
            "2.2": 28000,
            "2.90": 18000,
            "3.2990": 12000,
            "2.9": 24000,
            "3.299": 11000,
            "3.5990": 18000,
            "3.599": 13000,
            "4.10950": 16000,
            "4.1095": 9000,
            "5.410": 12000,
            "5.41": 8000,
            "6.0170": 11000,
            "6.017": 7000
        }
        
        $(function() {
            jQuery.expr[':'].focus = function( elem ) {
                return elem === document.activeElement && ( elem.type || elem.href );
            };/*Questa versione di jquery non supporta il :focus  in questo modo l'ho implementato io.*/
            
            rotselected = $("#rotradius option:selected").parent().attr("label")
            if ( rotselected == 'Agilent'){
                maxFreq = maxFreqA
            }
            else if (rotselected == 'Bruker'){
                maxFreq = maxFreqB
            }
            else if (rotselected == "JEOL"){
                maxFreq = maxFreqJ
            }
            else{
                maxFreq = maxFreqD
            }
            
            $.ajax({
                type: "GET",
                url: "/sedNMR/initPlots",
                success: function(data){
                    var tr = parseFloat($("#treshold").slider("option", "value"))
                    var lc = parseFloat($( "#limitconc" ).slider("value"))
                    var p1line = []
                    var p2line = []
                    plotslist = data.split("::")
                    var plot1 = plotslist[0];
                    
                    datalist = plot1.split(";")
                    $(datalist).each(function(){
                        coords = this.split(",")
                        itempl1 = [parseFloat(coords[0]), parseFloat(coords[1])]
                        p1line.push(itempl1)
                    });
                    $.jqplot('chartdiv',  [p1line],
                    {
                        seriesDefaults: {
                            rendererOptions: {
                                //////
                                // Turn on line smoothing.  By default, a constrained cubic spline
                                // interpolation algorithm is used which will not overshoot or
                                // undershoot any data points.
                                //////
                                smooth: true
                            },
                            showMarker:false
                        },
                        axes:{
                            xaxis:{
                              label:'Distance from rotation axis (mm)',
                              labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                              min: 0,
                              max: parseFloat($("#rotradius option:selected").val())/2
                            },
                            yaxis:{
                              label:'Concentration (mg/ml)',
                              labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                              min: 0,
                              max: parseFloat($("#limitconc").slider("value"))*1.1
                            }},
                            highlighter: {
                                show: true,
                                sizeAdjust: 7.5
                            },
                            cursor: {
                                show: false
                            },
                            series:[{color:'#FF9933'}]
                    }).replot();
                    var plot2 = plotslist[1];
                    datalist2 = plot2.split(";")
                    $(datalist2).each(function(){
                        coords = this.split(",")
                        itempl2 = [parseFloat(coords[0]), parseFloat(coords[1])]
                        p2line.push(itempl2)
                    });
                    $.jqplot('chart2div',  [p2line],
                    {
                        seriesDefaults: {
                            rendererOptions: {
                                //////
                                // Turn on line smoothing.  By default, a constrained cubic spline
                                // interpolation algorithm is used which will not overshoot or
                                // undershoot any data points.
                                //////
                                smooth: true
                            },
                            showMarker:false
                        },
                        axes:{
                            xaxis:{
                              label:'MAS frequency (Hz)',
                              labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                              min: 0,
                              max: parseFloat(maxFreq[$( "#rotradius option:selected" ).val()])
                            },
                            yaxis:{
                              label:'Fraction of immobilized protein',
                              labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                              min: 0,
                              max: 1.1
                            }},
                            highlighter: {
                                show: true,
                                sizeAdjust: 7.5
                            },
                            cursor: {
                                show: false
                            }
                    }).replot();
                }
            });
            
            
            $( "#treshold" ).slider({
                value: 0.85,
                orientation: "horizontal",
                min: 0.5,
                max: 1.00,
                step: 0.05,
                animate: true,
                slide: function( event, ui ) {
                    $("#treshold-amount").html( ui.value );
			    },
                change: updatePlots
            });
            $( "#temperature" ).slider({
                value: 274,
                orientation: "horizontal",
                min: 227,
                max: 373,
                step: 1,
                animate: true,
                slide: function( event, ui ) {
                    $( "#temperature-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#protmw" ).slider({
                value: 100,
                orientation: "horizontal",
                min: 1,
                max: 1000,
                step: 1,
                animate: true,
                slide: function( event, ui ) {
                    $( "#protmw-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#initconc" ).slider({
                value: 30.00,
                orientation: "horizontal",
                min: 5,
                max: 700,
                step: 5,
                animate: true,
                slide: function( event, ui ) {
                    $( "#initconc-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#limitconc" ).slider({
                value: 700.00,
                orientation: "horizontal",
                min: 200,
                max: 1800,
                step: 5,
                animate: true,
                slide: function( event, ui ) {
                    $( "#limitconc-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#protdens" ).slider({
                value: 1.23,
                orientation: "horizontal",
                min: 1.2,
                max: 1.8,
                step: 0.01,
                animate: true,
                slide: function( event, ui ) {
                    $( "#protdens-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#solvdens" ).slider({
                value: 0.99,
                orientation: "horizontal",
                min: 0.89,
                max: 1.42,
                step: 0.01,
                animate: true,
                slide: function( event, ui ) {
                    $( "#solvdens-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#masfreq" ).slider({
                value: 12000,
                orientation: "horizontal",
                min: 100,
                max: parseFloat(maxFreq[$( "#rotradius option:selected" ).val()]),
                step: 100,
                animate: true,
                slide: function( event, ui ) {
                    $( "#masfreq-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#censpeed" ).slider({
                value: 32000,
                orientation: "horizontal",
                min: 2000,
                max: 120000,
                step: 100,
                animate: true,
                slide: function( event, ui ) {
                    $( "#censpeed-amount" ).html( ui.value );
                },
                change: updatePlots
            });
            $( "#rotradius" ).change(function() {
                
                var val = $( "#rotradius option:selected" ).val();
                $("#masfreq").slider("option", "max", parseFloat(maxFreq[val]));
                tmpval = $( "#masfreq" ).slider("value")
                if (parseFloat($( "#masfreq" ).slider("value")) >= maxFreq[val]){
                    $( "#masfreq" ).slider("value", maxFreq[val]);
                    $("#masfreq-amount").html(maxFreq[val])
                }
                else{
                    $( "#masfreq" ).slider("value", tmpval);
                    $("#masfreq-amount").html(tmpval)
                }
                //updatePlots();
            });
            $(".device-data").hide();
            $(".device-schema").hide();
            $("input[name=rot-dev]").bind('click', function() {
                if ($("input[name=rot-dev]:checked").val() == 'device'){
                    $(".rotor-data").hide();
                    $(".device-data").show();
                    $(".device-schema").show();
                    updatePlots();
                    
                }
                else{
                    $(".rotor-data").show();
                    $(".device-data").hide();
                    $(".device-schema").hide();
                    $( "#masfreq" ).slider({min: 100, max: parseFloat(maxFreq[$( "#rotradius option:selected" ).val()]), value: 12000});
                    $("#masfreq-amount").html("12000");
                }
            });
            
            $(document).keypress(function(e) {
                if(e.which == 13) {
                    if ($("#hmax").is(":focus") || $("#htot").is(":focus") ||
                        $("#hfun").is(":focus") || $("#h3").is(":focus") ||
                        $("#h2").is(":focus") || $("#h1").is(":focus") ||
                        $("#r3").is(":focus") || $("#r2").is(":focus") ||
                        $("#r1").is(":focus")){
                            updatePlots();
                    }
                }
            });
            
        });
        function updatePlots(){
            var tr = parseFloat($("#treshold").slider("option", "value"))
            var lc = parseFloat($( "#limitconc" ).slider("value"))
            if ($("input[name=rot-dev]:checked").val() == "rotor"){
                rotselected = $("#rotradius option:selected").parent().attr("label")
                if ( rotselected == 'Agilent'){
                    maxFreq = maxFreqA
                }
                else if (rotselected == 'Bruker'){
                    maxFreq = maxFreqB
                }
                else if (rotselected == "JEOL"){
                    maxFreq = maxFreqJ
                }
                else{
                    maxFreq = maxFreqD
                }
                $.ajax({
                    type: "GET",
                    url: "/sedNMR/updateRotor",
                    data: {
                        "tr": $( "#treshold" ).slider("value"),
                        "pd": $( "#protdens" ).slider("value"),
                        "sd": $( "#solvdens" ).slider("value"),
                        "t": $( "#temperature" ).slider("value"),
                        "pmw": $( "#protmw" ).slider("value"),
                        "ic": $( "#initconc" ).slider("value"),
                        "lc": $( "#limitconc" ).slider("value"),
                        "mf": $( "#masfreq" ).slider("value"),
                        "rr": $( "#rotradius option:selected" ).val(),
                        "rt": $( "#rotradius option:selected" ).parent().attr("label"),
                        "devrot":$("input[name=rot-dev]:checked").val()
                        },
                    success: function(data){
                        var p1line = []
                        var p2line = []
                        plotslist = data.split("::")
                        var plot1 = plotslist[0];
                        datalist = plot1.split(";")
                        $(datalist).each(function(){
                            coords = this.split(",")
                            itempl1 = [parseFloat(coords[0]), parseFloat(coords[1])]
                            p1line.push(itempl1)
                        });
                        $.jqplot('chartdiv',  [p1line],
                        {
                            seriesDefaults: {
                                rendererOptions: {
                                    //////
                                    // Turn on line smoothing.  By default, a constrained cubic spline
                                    // interpolation algorithm is used which will not overshoot or
                                    // undershoot any data points.
                                    //////
                                    smooth: true
                                },
                                showMarker:false
                            },
                            axes:{
                                xaxis:{
                                  label:'Distance from rotation axis (mm)',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: parseFloat($("#rotradius option:selected").val())/2
                                  
                                },
                                yaxis:{
                                  label:'Concentration (mg/ml)',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: parseFloat($("#limitconc").slider("value"))*1.1
                                }},
                                highlighter: {
                                    show: true,
                                    sizeAdjust: 7.5
                                },
                                cursor: {
                                    show: false
                                },
                                series:[{color:'#FF9933'}]
                        }).replot();
                        var plot2 = plotslist[1];
                        datalist2 = plot2.split(";")
                        $(datalist2).each(function(){
                            coords = this.split(",")
                            itempl1 = [parseFloat(coords[0]), parseFloat(coords[1])]
                            p2line.push(itempl1)
                        });
                        $.jqplot('chart2div',  [p2line],
                        {
                            seriesDefaults: {
                                rendererOptions: {
                                    //////
                                    // Turn on line smoothing.  By default, a constrained cubic spline
                                    // interpolation algorithm is used which will not overshoot or
                                    // undershoot any data points.
                                    //////
                                    smooth: true
                                },
                                showMarker:false
                            },
                            axes:{
                                xaxis:{
                                  label:'MAS frequency (Hz)',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: parseFloat(maxFreq[$( "#rotradius option:selected" ).val()])
                                },
                                yaxis:{
                                  label:'Fraction of immobilized protein',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: 1.1
                                }},
                                highlighter: {
                                    show: true,
                                    sizeAdjust: 7.5
                                },
                                cursor: {
                                    show: false
                                }
                        }).replot();
                    }
                });
            }//close if rotor/device
            else{
                var myWidth = 320;
                var myHeight = 240;
                var option = {
                    opacity:70,
                    close: false,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                $.modal('<img src="/global/images/loading2.gif">', option);
                $.ajax({
                    type: "GET",
                    url: "/sedNMR/updateDevice",
                    data: {
                        "tr": $( "#treshold" ).slider("value"),
                        "pd": $( "#protdens" ).slider("value"),
                        "sd": $( "#solvdens" ).slider("value"),
                        "t": $( "#temperature" ).slider("value"),
                        "pmw": $( "#protmw" ).slider("value"),
                        "ic": $( "#initconc" ).slider("value"),
                        "lc": $( "#limitconc" ).slider("value"),
                        "cs": $( "#censpeed" ).slider("value"),
                        "rr": $( "#rotradius option:selected" ).val(),
                        "rt": $( "#rotradius option:selected" ).parent().attr("label"),
                        "devrot":$("input[name=rot-dev]:checked").val(),
                        "hmax": $("#hmax").val(),
                        "htot": $("#htot").val(),
                        "hfun": $("#hfun").val(),
                        "h1": $("#h1").val(),
                        "h2": $("#h2").val(),
                        "h3": $("#h3").val(),
                        "r1": $("#r1").val(),
                        "r2": $("#r2").val(),
                        "r3": $("#r3").val(),
                        },
                    success: function(data){
                        $.modal.close();
                        var p1line = []
                        var p2line = []
                        plotslist = data.split("::")
                        var plot1 = plotslist[0];
                        datalist = plot1.split(";")
                        $(datalist).each(function(){
                            coords = this.split(",")
                            itempl1 = [parseFloat(coords[0]), parseFloat(coords[1])]
                            p1line.push(itempl1)
                        });
                        $.jqplot('chartdiv',  [p1line],
                        {
                            seriesDefaults: {
                                rendererOptions: {
                                    //////
                                    // Turn on line smoothing.  By default, a constrained cubic spline
                                    // interpolation algorithm is used which will not overshoot or
                                    // undershoot any data points.
                                    //////
                                    smooth: true
                                },
                                showMarker:false
                            },
                            axes:{
                                xaxis:{
                                  label:'Distance from rotation axis (cm)',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: parseFloat($("#hmax").val()) - parseFloat($("#htot").val()),
                                  max: parseFloat($("#hmax").val()) - parseFloat($("#htot").val()) + parseFloat($("#hfun").val()) + parseFloat($("#h3").val())
                                  
                                },
                                yaxis:{
                                  label:'Concentration (mg/ml)',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: parseFloat($("#limitconc").slider("value"))*1.1
                                }},
                                highlighter: {
                                    show: true,
                                    sizeAdjust: 7.5
                                },
                                cursor: {
                                    show: false
                                },
                                series:[{color:'#FF9933'}]
                        }).replot();
                        var plot2 = plotslist[1];
                        datalist2 = plot2.split(";")
                        $(datalist2).each(function(){
                            coords = this.split(",")
                            itempl1 = [parseFloat(coords[0]), parseFloat(coords[1])]
                            p2line.push(itempl1)
                        });
                        $.jqplot('chart2div',  [p2line],
                        {
                            seriesDefaults: {
                                rendererOptions: {
                                    //////
                                    // Turn on line smoothing.  By default, a constrained cubic spline
                                    // interpolation algorithm is used which will not overshoot or
                                    // undershoot any data points.
                                    //////
                                    smooth: true
                                },
                                showMarker:false
                            },
                            axes:{
                                xaxis:{
                                  label:'Centrifugation speed (rpm)',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: 120000
                                },
                                yaxis:{
                                  label:'Fraction of protein in the rotor',
                                  labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                                  min: 0,
                                  max: 1.1
                                }},
                                highlighter: {
                                    show: true,
                                    sizeAdjust: 7.5
                                },
                                cursor: {
                                    show: false
                                }
                        }).replot();
                    }
                });
            }//close else rotor/device
        }
        
        function canvas2Image(plot){
            var canvas = $("#"+plot).find('canvas');
            var w = canvas[0].width;
            var h = canvas[0].height;
            var newCanvas = $('<canvas id="tempcanvas" />').attr('width',w).attr('height',h)[0];
            var newContext = newCanvas.getContext("2d");
            $(canvas).each(function() {
              newContext.drawImage(this, 0, 0);
            });
            imgdata = newCanvas.toDataURL("image/png"); // Base64 encoded data url string
            window.open(imgdata)
            //$.ajax({
            //    type: "POST",
            //    url: "/sedNMR/canvas2img",
            //    data: {"img": imgdata}
            //});
        }
        
        function download_data(){
            var myWidth = 320;
                var myHeight = 240;
                var option = {
                    opacity:70,
                    close: false,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
            $.modal('<img src="/global/images/loading2.gif">', option);
            $.ajax({
                type: "POST",
                url: "/sedNMR/prepare_download",
                dataType: "script",
                data: {
                    "tr": $( "#treshold" ).slider("value"),
                    "pd": $( "#protdens" ).slider("value"),
                    "sd": $( "#solvdens" ).slider("value"),
                    "t": $( "#temperature" ).slider("value"),
                    "pmw": $( "#protmw" ).slider("value"),
                    "ic": $( "#initconc" ).slider("value"),
                    "lc": $( "#limitconc" ).slider("value"),
                    "mf": $( "#masfreq" ).slider("value"),
                    "rr": $( "#rotradius option:selected" ).val(),
                    "rt": $( "#rotradius option:selected" ).parent().attr("label"),
                    "devrot":$("input[name=rot-dev]:checked").val(),
                    "hmax": $("#hmax").val(),
                    "htot": $("#htot").val(),
                    "hfun": $("#hfun").val(),
                    "cs": $("#censpeed").slider("value"),
                    "h1": $("#h1").val(),
                    "h2": $("#h2").val(),
                    "h3": $("#h3").val(),
                    "r1": $("#r1").val(),
                    "r2": $("#r2").val(),
                    "r3": $("#r3").val()
                },
                success: function(data){
                    $.modal.close();
                    window.location = "/sedNMR/download?path="+data;
                }
            });
        }
        
        function help_info(field){
            $.ajax({
                type: 'POST',
                url: '/sedNMR/helpinfo',
                data: {'field': field},
                success: function(data){
                    var myWidth = 400;
                    var myHeight = 130;
                    var option = {
                        opacity:70,
                        minWidth: myWidth,
                        minHeight: myHeight,
                        maxWidth: myWidth,
                        maxHeight: myHeight
                    };
                    $.modal(data, option);
                }   
            });
        }

	</script>
</%def>
    <br/>
        <div id="compliant" style="text-align:right">
            <!--<a href="http://mozilla-europe.org/en/firefox/" target="_blank"><img src="/global/images/firefox.png" style="border: none" title="Get Mozilla Firefox" alt="Get Mozilla Firefox"></a>-->
            <span class="browser_support">
                <span> Supported browser:</span>
                <span class="browser_logos">
                    <!--<span class="opera supported"></span>
                    <span class="ie"></span>-->
                    <span class="safari supported"></span>
                    <span class="ff supported"></span>
                    <span class="chrome supported"></span>
                </span>
            </span>
        </div>
        <br/>
        <br/>
        <dl class="intro">
            <dd class="summary">
                <b>Introduction</b><br/>
               <div style="display: inline;">
                    We have proposed sedimented solute NMR method to prepare samples for
                    Magic-angle-Spinning (MAS) of biomolecules without the need of
                    crystallization or other sample manipulation. The sedimented solute NMR
                    can be regarded as a simple way to select the best of solution and solid
                    state NMR: the sample can be kept in the buffer that is used for the
                    solution studies; the system is always hydrated enough and its size turns
                    from foe to friend. Sedimentation can be achieved by the large centrifugal
                    fields that are obtained in the MAS rotors<sup>1</sup> or via usual
                    ultracentrifugation<sup>2</sup>.
                    This web tool (sedNMR) allows for simple calculation of the relevant
                    parameters for the success of the experiment, either in the rotor or with
                    ultracentrifugal devices.<sup>2-4</sup>
                    <br/>
                    1 Bertini, I.; Luchinat, C.; Parigi, G.; Ravera, E.; Reif, B.; Turano, P.
                    Proc.Natl.Acad.Sci.USA 2011, 108, 10396-10399.<br>
                    2 Bertini, I.; Engelke, F.; Luchinat, C.; Parigi, G.; Ravera, E.; Rosa,
                    C.; Turano, P. Phys.Chem.Chem.Phys. 2012, 14, 439-447.<br>
                    3 Bertini, I.; Engelke, F.; Gonnelli, L.; Knott, B.; Luchinat, C.; Osen,
                    D.; Ravera, E. J.Biomol.NMR 2012, 54, 123-127.<br>
                    4 Gardiennet, C.; Schütz, A. K.; Hunkeler, A.; Kunert, B.; Terradot, L.;
                    Böckmann, A.; Meier, B. H. Angew.Chem.Int.Ed 2012, 51, 7855-7858.
                    
               </div>
            </dd>
        </dl>
        <br />
        <br />
         <center>
        <div id="chartdiv" style="height:200px;width:700px; "></div>
        <br/>
        <br/>
        <div id="chart2div" style="height:200px;width:700px; "></div>
         </center>        
            
        <fieldset>
            <legend>Setup parameters</legend>
            <div id="slider_box">
                <div class="rotor-device">
                    <span class="label">Set paramaters for: </span>
                    <input type="radio" name="rot-dev" value="rotor" checked> Rotor
                    <input type="radio" name="rot-dev" value="device"> Device<br>
                </div>
                <div class="rotor-data">
                    <div class="rotradius">
                        <span class="label">Rotor radius (mm):</span>
                        <select id="rotradius">
                            <optgroup label="Agilent">
                                <option value="7.9502">9.5 mm, std.</option>
                                <option value="5.969">7.5 mm, std.</option>
                                <option value="4.4958">6.0 mm, std.</option>
                                <option value="3.429">5.0 mm, std.</option>
                                <option value="4.3942">5.0 mm, thinWall</option>
                                <option value="2.4638">4.0 mm, std.</option>
                                <option value="3.2258">4.0 mm, thinWall</option>
                                <option value="2.032">3.2 mm, std.</option>
                                <option value="2.6162">3.2 mm, thinWall</option>
                                <option value="1.5748">2.5 mm, std.</option>
                                <option value="1.143">1.6 mm, std.</option>
                                <option value="0.625">1.2 mm, std.</option>
                            </optgroup>
                            <optgroup label="Bruker">
                                <option value="5.6">MAS 7 mm</option>
                                <option value="3.0">MAS 4 mm</option>
                                <option value="2.6" selected="selected">MAS 3.2 mm</option>
                                <option value="1.7">MAS 2.5 mm</option>
                                <option value="1.5" >MAS 1.9 mm</option>
                                <option value="0.9" >MAS 1.3 mm</option>
                            </optgroup>
                            <optgroup label="JEOL">
                                <option value="6.4">8 mm</option>
                                <option value="2.6">4 mm</option>
                                <option value="2.2">3.2 mm</option>
                                <option value="1.7">2.5 mm</option>
                                <option value="0.5" >1 mm</option>
                                <option value="0.35" >0.75 mm</option>
                            </optgroup>
                            <optgroup label="Doty">
                                <option value="2.2">DI3 3mm</option>
                                <option value="2.90">DI4 Thick 4mm</option>
                                <option value="3.2990">DI Thin 4mm</option>
                                <option value="2.9">XC4 Thick 4mm (Silicon nitride)</option>
                                <option value="3.299" >XC4 Thin 4mm (Zirconia)</option>
                                <option value="3.5990" >XC5 Thick 5.01mm (Silicon Nitride)</option>
                                <option value="3.599" >XC5 Thick 5.01mm (Zirconia)</option>
                                <option value="4.10950" >XC5 Thin 5.01mm (Silicon Nitride)</option>
                                <option value="4.1095" >XC5 Thin 5.01mm (Zirconia)</option>
                                <option value="5.410" >XC7 Thick 7.01mm (Silicon Nitride)</option>
                                <option value="5.41" >XC7 Thick 7.01mm (Zirconia)</option>
                                <option value="6.0170" >XC7 Thin 7.01mm (Silicon Nitride)</option>
                                <option value="6.017" >XC7 Thin 7.01mm (Zirconia)</option>
                            </optgroup>
                        </select>
                    </div>
                    <div class="slider_line">
                        <span class="label">MAS frequency (Hz):</span>
                        <span class="val" id="masfreq-amount">12000</span>
                        <div class="slider" id="masfreq"></div>
                    </div>
                </div>
                <div class="device-data">
                    <table>
                        <tr>
                            <td><span class="label">h<sub>max</sub> (cm):</span></td>
                            <td><input type="text" id="hmax" name="hmax" size="5" value="15.2"/></td>
                            <td><span class="label">h<sub>tot</sub> (cm):</span></td>
                            <td><input type="text" id="htot" name="htot" size="5" value="6.3"/></td>
                           <td><span class="label">h<sub>fun</sub> (cm):</span></td>
                            <td><input type="text" id="hfun" name="hfun" size="5" value="3"/></td>
                        </tr>
                        <tr>
                            <td><span class="label">h<sub>1</sub> (cm):</span></td>
                            <td><input type="text" id="h1" name="h1" size="5" value="0"/></td>
                            <td><span class="label">h<sub>2</sub> (cm):</span></td>
                            <td><input type="text" id="h2" name="h2" size="5" value="0.1"/></td>
                            <td><span class="label">h<sub>3</sub> (cm):</span></td>
                            <td><input type="text" id="h3" name="h3" size="5" value="1.5"/></td>
                        </tr>
                        <tr>
                            <td><span class="label">r<sub>1</sub> (cm):</span></td>
                            <td><input type="text" id="r1" name="r1" size="5" value="6.05"/></td>
                            <td><span class="label">r<sub>2</sub> (cm):</span></td>
                            <td><input type="text" id="r2" name="r2" size="5" value="0.1"/></td>
                            <td><span class="label">r<sub>3</sub> (cm):</span></td>
                            <td><input type="text" id="r3" name="r3" size="5" value="1.055"/></td>
                        </tr>
                    </table>
                    <div class="slider_line">
                        <span class="label">Centrifugation speed (rpm):</span>
                        <span class="val" id="censpeed-amount">32000</span>
                        <div class="slider" id="censpeed"></div>
                    </div>
                </div>
                
                <div class="slider_line">
                    <span class="label">Molecular weight (kDa):</span>
                    <span class="val" id="protmw-amount">100</span>
                    <div class="slider" id="protmw"></div>
                </div>
                <div class="slider_line">
                    <span class="label">Initial concentration (mg/ml):</span>
                    <span class="val" id="initconc-amount">30.00</span>
                    <div class="slider" id="initconc"></div>
                </div>
                <div class="slider_line">
                    <img src="/global/images/info.png" class="infoimg" onclick="help_info('solventdensity')" />
                    <span class="label">Solvent density (g/ml):</span>
                    <span class="val" id="solvdens-amount">0.99</span>
                    <div class="slider" id="solvdens"></div>
                </div>
                <div class="slider_line">
                    <img src="/global/images/info.png" class="infoimg" onclick="help_info('macromoleculardensity')" />
                    <span class="label">Macromolecular density (g/ml):</span>
                    <span class="val" id="protdens-amount">1.23</span>
                    <div class="slider" id="protdens"></div>
                </div>
                <div class="slider_line">
                    <span class="label">Temperature (K):</span>
                    <span class="val" id="temperature-amount">274.00</span>
                    <div class="slider" id="temperature"></div>
                </div>
                <div class="slider_line">
                    <img src="/global/images/info.png" class="infoimg" onclick="help_info('limitingconcentration')" />
                    <span class="label">Limiting concentration (mg/ml):</span>
                    <span class="val" id="limitconc-amount">700.00</span>
                    <div class="slider" id="limitconc"></div>
                </div>
                <div class="slider_line">
                    <img src="/global/images/info.png" class="infoimg" onclick="help_info('thresholdforimmobilization')" />
                    <span class="label">Threshold for immobilization:</span>
                    <span class="val" id="treshold-amount">0.86</span>
                    <div class="slider" id="treshold"></div>
                </div>
            </div>
            <div class="device-schema">
                <img src="/global/images/device2.jpg"/>
            </div>
        </fieldset>
        <br/>
        <fieldset>
            <legend>Get the results</legend>
            Download the <a href="javascript:download_data();">raw data and all NMR relevant parameters</a>
        </fieldset>
        <br>
        <br>
        
        
    <dl class="textblock">
        <dt></dt>
        <dd>
           <b>When using this web portal please cite:</b>
            <br />
            Ferella,L.; Luchinat,C.; Ravera,E.; Rosato,A. “SEDNMR: A web tool for
            optimizing sedimentation of samples for SSNMR”, in press
            <br/><br/>
            <b>General references about sedimentation</b>
            <br />
            Bertini,I.; Luchinat,C.; Parigi,G.; Ravera,E.; Reif,B.; Turano,P.
            “Solid-state NMR of proteins sedimented by ultracentrifugation”,  PNAS
            2011, 108, 10396-10399<br>
            Bertini,I.; Engelke,F.; Luchinat,C.; Parigi,G.; Ravera,E.; Rosa,C.;
            Turano,P. “NMR properties of sedimented solutes”, PCCP 2012, 14, 439-447<br>
            Bertini,I.; Luchinat,C.; Parigi,G.; Ravera,E. “SedNMR: on the edge between
            solution and solid state NMR”, Acc. Chem. Res. 2013, in press
            <br><br>
            <b>References about ultracentrifugal devices</b>
            <br>
            Bertini,I.; Engelke,F.; Gonnelli,L.; Knott,B.; Luchinat,C.; Osen,D.;
            Ravera,E. “On the use of ultracentrifugal devices for sedimented solute
            NMR”, J. Biomol. NMR 2012, 54,123-127<br>
            Gardiennet,C.; Schütz,A.K.; Hunkeler,A.; Kunert,B.; Terradot,L.;
            Böckmann,A; Meier,B.H. “A Sedimented Sample of a 59 kDa Dodecameric
            Helicase Yields High-Resolution Solid-State NMR Spectra”, Angew Chem Int
            Ed 2012, 51, 7855-7858<br>
            Gelis,I.; Vitzthum,V.; Dhimole,N.; Caporini,M.A.; Schedlbauer,A.;
            Carnevale,D.; Connell,S.R.; Fucini,P.; Bodenhausen,G. “Solid-state NMR
            enhanced by dynamic nuclear polarization as a novel tool for ribosome
            structural biology”, J. Biomol. NMR 2013, 56, 85-93<br>
        </dd>
    </dl>
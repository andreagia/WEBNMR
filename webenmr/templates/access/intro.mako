<%inherit file="/base2.mako"/>
    <div id="maincol">
        <div id="compliant" style="text-align:right">
            <a href="/feed/feed.rss" target="_blank"><img src="/global/images/ico_feed_rss.gif" style="border: none" title="Subscribe to rss feed" alt="Subscribe to rss feed" ></a>
            <a href="/feed/atom.xml" target="_blank"><img src="/global/images/ico_feed_atom.gif" style="border: none" title="Subscribe to atom feed" alt="Subscribe to atom feed" ></a>
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
        <dl class="intro">
		 % if session['PORTAL'] == 'maxocc':
			   <br>
			   <br>
			   <br>
			   <dt>Introduction to Maxocc web portal</dt>
			   <dd><b>Maximum Occurrence</b> (MaxOcc) refers to a method for making rigorous numerical assessments 
				 about the maximum percent of time that a conformer of a flexible macromolecule can exist and
				 still be compatible with the experimental data. Maximum Occurrence of a conformer is defined
				 as the maximum weight that it can have in one ensemble that matches the average experimental data.
				 To evaluate the Maximum Occurrence, an ensemble is sought so that the conformation under investigation
				 is contained up to a certain value. At the Maximum Occurrence, no solution will be found fulfilling
				 both the requisites of containing the desired conformation and of being compatible with the experimental
				 data. Such process is exemplified in figure: the four boxes represent 4 different ensembles, containing
				 the desired conformation (represented as a red star) at different weight (represented by the dimension of
				 the red star): the fourth one is no more compatible with the experimental data.
				 <br>
				 <img src="/global/images/maxocc/maxocc_ex.png">
			   </dd>
			   <br/>
			   <br/>
			   <br/>
			   <br/>
			   <b>Reference for use of the MaxOcc server</b>:<br>
               Journal of Biomolecular NMR, 2012 <br/>
			    <i>MaxOcc: a web portal for maximum occurrence analysis</i><br/>
                Ivano Bertini, Lucio Ferella, Claudio Luchinat, Giacomo Parigi, Maxim V. Petoukhov, Enrico Eavera, Antonio Rosato, Dmitri I. Svergun<br/>
                PMID:<a href="http://www.ncbi.nlm.nih.gov/pubmed/22639196">22639196</a> doi:<a href="http://dx.doi.org/10.1007/s10858-012-9638-1">10.1021/ja1063923</a>
			   <br/>
			   <br/>
			   J Am Chem Soc. 2010 Sep 7.<br/>
			   <i>Conformational Space of Flexible Biological Macromolecules from Average Data</i>.<br/>
			   Bertini I, Giachetti A, Luchinat C, Parigi G, Petoukhov MV, Pierattelli R, Ravera E, Svergun DI.<br/>
			   PMID:<a href="http://www.ncbi.nlm.nih.gov/pubmed/20822180">20822180</a> doi:<a href="http://dx.doi.org/10.1021/ja1063923">10.1021/ja1063923</a>
		  % elif session['PORTAL'] == 'amps-nmr':
			  <br>
			  <br>
			  <br>
			  <dt>AMBER-based Portal Server for NMR structures (AMPS-NMR)</dt>
			  <dd>
				  Amber (acronym to Assisted Model Building with Energy Refinement) is a suite of programs
				  <img width="256" height="128" src="/global/images/pro_small.png" class="right" title="1N3L" alt="1N3L"> that allow users
				  to perform molecular dynamics (MD) simulations on biological
				  systems. <br>This web portal makes available the entire functionality of AMBER, in particular (but not only)
				  using NMR-derived information as restraints for MD.
				  <br>
				  <br>
				  To use AMPS-NMR you have to register to WeNMR <a href="http://www.wenmr.eu/wenmr/access/registration">grid infrastructure</a>
				  <br>
				  <br>
				  You can access a trial version of the service using username <i>guest</i> and password <i>guest</i>
		  
				  <br>
				  <b>NB</b>: the trial version will not allow you to submit jobs on the WeNMR grid.
			  </dd>
			  <br/>
			  <br/>
			  <br/>
			  <br/>
			  <b>Reference for use of the AMPS-NMR server</b>:<br>
			  Bioinformatics, 27, 2384-2390 (2011).<br/>
			  <i>A Grid-enabled web portal for NMR structure refinement with AMBER</i>.<br/>
			  Bertini I, Case DA, Ferella L, Giachetti A, Rosato A.<br/>
			  <a href="http://www.ncbi.nlm.nih.gov/pubmed/21757462">Pubmed link</a>
		  % elif session['PORTAL'] == 'xplor-nih':
			  <br>
			  <br>
			  <br>
			  <dt>Xplor-NIH</dt>
			  <dd>
				  Xplor-NIH is a generalized software for biomolecular structure determination
				  from experimental NMR data combined with geometric data. This is achieved by
				  seeking the minimum of a target function comprising terms for the experimental
				  NMR restraints, covalent geometry and non-bonded contacts using a variety of
				  optimization procedures including molecular dynamics in Cartesian and torsion
				  angle space, Monte Carlo methods and conventional gradient-based minimization.
				  <br>
				  <br>
				  To use Xplor-NIH you have to register to WeNMR <a href="http://www.wenmr.eu/wenmr/access/registration">grid infrastructure</a>
				  <br>
				  <br>
				  You can access a trial version of the service using username <i>guest</i> and password <i>guest</i>
		  
				  <br>
				  <b>NB</b>: the trial version will not allow you to submit jobs on the WeNMR grid.
			  </dd>
          % elif session['PORTAL'] == 'oops!':
            <br>
			  <br>
			  <br>
			  <dt>Single Sign On issue</dt>
			  <dd>
				  Your request is expired. Please come back in the <b>My services</b> page on the <a href="http://www.wenmr.eu">Wenmr community portal</a> and reload the page.
				  <br>
				  <br>
			  </dd>
		  % endif
		
		 </dl>
        <br>
        <!--&nbsp;&nbsp;&nbsp;&nbsp;Recommended web browser: <b>Mozilla Firefox</b>-->
        <br>
        
        <center>Please <a href="/feedback/index?type=${session['PORTAL']}">contact us</a> for any suggestion and/or feedback.</center>
    </div>
   
    <div id="subcol">
        <dl class="sidebar firstsidebaritem">
            <dd class="sidetext"><a target="_blank" href="http://www.wenmr.eu"><img src="/global/images/WeNMR.png" alt="WeNMR" width="206" ></a></dd>
			<dd class="sidetext"><a target="_blank" href="https://portal.west-life.eu/"><img src="/global/images/westlife-logo.png" alt="westlife" width="206" ></a></dd>
            <dd class="sidetext"><a target="_blank" href="http://cordis.europa.eu/fp7/ict/e-infrastructure/home_en.html"><img src="/global/images/e-infrastructure-logo.png" alt="e-Infrastructure" width="206"></a></dd>
        </dl>
    
        <div class="sidebox">
            % if h.flash.has_message():
                    <div id="message-wrapper"><div id="message"><p
                    class="${h.flash.get_message_type()}">${h.flash.get_message_text()}</p></div></div>
            % endif

            <div class="boxhead">
                <h2>: Access to ${c.title} :</h2>
            </div>
                
                <div class="boxbody">

                    <form id="login" method="post" action="${h.url('/access/login')}" > 
                        <label>Username:
                            <input name="user_name" type="text" id="user" tabindex="1" class="text"  >  
                        </label>
                        <label>Password:  
                            <input name="user_pwd" type="password" id="password" tabindex="2" class="text" >
                            <input type="submit" tabindex="3" value="Sign In" class="buttons" >
                        </label> 
                    </form>
                    <br/>
					<input id="btnGetResponseIAM" type="button" value="RedirectIAM" />
					<script type="text/javascript">
						$(function () {
							$("#btnGetResponseIAM").click(function () {
							$.get("${h.url('/access/loginIAM')}", function(data, status){
							//alert("IAM TEST TEST TEST" + "\nStatus: " + status);
							window.location = data;
						});
									
							});
						});
					</script>
					
					</br>
					
                    <p><a href="/users/forgotten" target="_blank">Forgot your password?</a><br/><a href="/access/newaccount" target="_blank">New to ${c.title.upper()}? Sign up.</a></p>
                </div>
                <!--[if lt IE 7]>
                <div>&nbsp;</div>
                <div id="item-list">
                    <div class="item-box item-overdue">
                        <h4>WARNING: You are running an unsupported browser</h4>
                        <div class="item-content">
                            <p><strong>${c.title}</strong> has been written for Mozilla Firefox,
                            Opera, Apple Safari, and Microsoft Internet Explorer 7.0 and higher.
                            Your version of Internet Explorer is not supported, and may doesn't work.
                            Please upgrade your browser to one of those listed above.</p>
                        </div>
                        <div class="item-links">&nbsp;</div>
                    </div>
                </div>
            </div>
            
                <![endif]-->
        </div>
        <dl>
            <dd>
                <!--Please, you must provide your username and password or access with your digital certificate.-->
                If you don't have credentials but want try ${c.title} functionality please enter username <em>guest</em>
                and password <em>guest</em>.
            </dd>
        </dl>
     
    </div>

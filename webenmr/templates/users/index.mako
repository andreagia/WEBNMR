<%inherit file="/base.mako"/>


<div id="maincol">
        <dl class="intro">
            <dt>How to start? (Quick run)</dt>
            <dd>
                % if session['PORTAL'] == 'amps-nmr':
                        To quickly create a new calculation, use the Amber drop
                        down menu from the blue bar above and select
                        New calculation. Then follow the four-steps procedure
                        to input all of your data. Check also the AMPS-NMR
                        paper in Bioinformatics. <a href="http://www.ncbi.nlm.nih.gov/pubmed/21757462">Pubmed link</a>
                % elif session['PORTAL'] == 'maxocc':
                        You can create a new project to collect your MaxOcc calculation (<i>Projects-->Create</i>)
                        OR directly create a MaxOcc calculation (<i>MaxOcc-->New calculation</i>).
                        In the latter automatically will be create a generic project to collect all informations about your calculation.
                % elif session['PORTAL'] == 'xplor-nih':
                        To quickly create a new calculation, use the Xplor-NIH drop
                        down menu from the blue bar above and select
                        New calculation. Then follow the four-steps procedure
                        to input all of your data. 
                %endif
            </dd>
        </dl>
        <dl class="intro">
            <dt>Tutorial</dt>
            <dd>
                We would like to show the very basic of ${session['PORTAL'].capitalize()} in a short, simple and interactive tutorial.
                This tutorial is designed to give you a good basic understanding of the use of mainly functionality of this web portal
               without loading you down with too much technical details.<br />
                Click
                        % if session['PORTAL'] == 'amps-nmr':
                                <a href="http://www.wenmr.eu/wenmr/tutorials/nmr-tutorials/amber">here</a>
                        %elif session['PORTAL'] == 'maxocc':
                                <a href="http://www.wenmr.eu/wenmr/tutorials/nmr-tutorials/maxocc">here</a>
                        %elif session['PORTAL'] == 'maxocc':
                                <a href="http://www.wenmr.eu/wenmr/tutorials/nmr-tutorials/xplor-nih">here</a>

                        %endif
                to read this tutorial.
            </dd>
        </dl>
</div>
<div id="subcol">
     <dl class="sidebar firstsidebaritem">
        % if session['PORTAL'] == 'amps-nmr':
                <dd class="sidetext"><img src="/global/images/newprojSM.png" alt="New Project" width="200" title="New Project"></dd>
                <dd class="sidetext"><img src="/global/images/amberSM.png" alt="Amber calculation" width="200" title="Amber calculation"></dd>
        %elif session['PORTAL'] == 'maxocc':
                <dd class="sidetext"><img src="/global/images/MO.png" alt="TF curves" width="200" title="TF curves"></dd>
        %endif
    </dl>
</div>

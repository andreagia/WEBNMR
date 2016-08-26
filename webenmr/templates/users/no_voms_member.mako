<%inherit file="/base2.mako"/>

<div id="maincol">
    <dl class="intro">
           <dt>Registration is not successful</dt>
           <dd>
            We couldn't process correctly your registration request. There are a number of reasons for this but they could be caused by:
            <ol>
                <li>you didn't load digital personal certificate into your web browser</li>
                <li>you aren't registered with the enmr.eu VO</li>
                <li>we are not receiving any response from the enmr.eu VO Management System server that we are attempting to connect to check your affiliation.</li>
            </ol>
            Please, check if the steps 1 and 2 have been completed properly, and <a href="http://py-enmr.cerm.unifi.it/feedback/index?type=${session['PORTAL'].lower()}">contact us</a> if you still encounter some problems. 
           </dd>
    </dl>
</div>
<div id="subcol">
    <dl class="sidebar firstsidebaritem">
        <dd class="sidetext"><a target="_blank" href="http://www.wenmr.eu"><img src="/global/images/WeNMR.png" alt="WeNMR" width="206" ></a></dd>
        <dd class="sidetext"><a target="_blank" href="http://cordis.europa.eu/fp7/ict/e-infrastructure/home_en.html"><img src="/global/images/e-infrastructure-logo.png" alt="e-Infrastructure" width="206"></a></dd>
    </dl>
</div>
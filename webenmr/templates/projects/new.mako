<%inherit file="/base.mako"/>
<%def name="css()">
   
</%def>

<%def name="js()">
<script type="text/javascript" src="/global/javascript/jquery.easing.js"></script>

<script  type="text/javascript">
    $(document).ready( function() {
        $("#signup").validationEngine();
    });
</script>

<script type="text/javascript">
    
</script>

</%def>


<div id="maincol">
    <dl class="intro">
        <dt>About project creation</dt>
        <dd>
            The project name is used throughout the project to organize and distinguish project content. So, choose a project name that will uniquely identify and describe the project. 
            Once a project has been created, you cannot change the name.<br>
            On left section you can read some advice to correctly assign name to your new project. 
        </dd>
    </dl>
    <form id="signup" action="${h.url(controller='projects', action='project_create')}"  method="post" >
        <fieldset>
            <legend>Creation of a new project</legend>
            <div id="newproj">
                    <label for="project" class="lproject">Project name:</label>
                    <input type="text" name="project" id="project" class="validate[required,custom[noSpecialCaracters],length[1,40]]"/>
            </div>
            <input type="submit" name="submit" value="create it"/>
        </fieldset>
    </form>
</div>
<div id="subcol">
           
        <dl>
            <dt>Rules for project names:</dt>
            <dd>
                <ul>
                    <li>A project name should be a single string of characters that include letters (a-z, A-Z) and digits (0-9).</li>
                    <li>The project name should not exceed forty (40) characters.</li>
                    <li>Do not use accented or non-roman characters.</li>
                    <li>Do not use punctuation or spaces.</li>
                    <li>Do not use local language characters or non-English characters. For example, even if you set the language settings in your web-browser or keyboard to Chinese,
                    you will still not be allowed to give a project name with characters in Chinese.</li>
                </ul> 
            </dd>
        </dl>
     
    </div>

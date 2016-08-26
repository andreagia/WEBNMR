<%inherit file="/base2.mako"/>
    <h2>Amber GRID-enabled Web Portal</h2>
    <fieldset>
        <legend>Server Error ${c.code}</legend>
        <div class="form-item">
            <label for="Error">
                <font color="red">${c.message}</font>
            </label>
            <label for="Explain">
                % if c.code == '404':
                    <h3>The server has not found anything matching the request URI</h3>
                    Sorry, we couldn't find page you were looking for. <br />
                    <br />
                    Things to try:
                    <ul>
                        <li> check that the URL you entered is correct. </li>
                        <li> return to our home page and use the navigation menu to find what you need. </li>
                        <li> contact us and we'll see if we can point you in the right direction. </li>
                    </ul>
                % elif c.code == '401':
                    <h3>This page is for authorized users only.</h3>
                    <br />
                    <br />
                    It is possible that the URL you typed was not correct wrong or that
                    the link you clicked on points to the wrong URL.
                    <ul>
                        <li>
                            If you are sure the URL is valid, visit the website's main page and look for
                        a link that says Login. Enter your credentials there and then try the page again.
                        If you don't have credentials, follow the instructions provided on the website for setting up an account.
                        </li>
    
                        <li>
                            If you are sure the page you are trying to reach shouldn't need authorization, this error message may be a mistake.
                        Moreover, this Unauthorized error can also appear immediately after login which is an indication that the web site
                        received your user name and password but found something about them to be invalid (i.e. your password is incorrect).
                        At this point it is probably in your best interest to <a href="/feedback/index">contact us</a> and inform us about the problem.
                        </li>
                    </ul>
                % elif c.code == '403':
                    The server won't let you to access, perhaps because you don't have appropriate permissions
                % elif c.code == '500':
                    <h3>The server was unable to complete your request.</h3><br />
                    <br />
                    This might be because:
                    <ul>
                        <li> there has been a problem with your input or</li>
                        <li> we are experiencing an abnormal traffic to our network or </li>
                        <li> the service or servers it is on is not currently available. </li>
                    </ul>
                    <br />
                    
                    Please try the following options:
                    
                    <ul>
                        <li> please control carefully your input format against our example (link)</li>
                        <li> <a href="/feedback/index">contact us</a> and we'll see if we can point you in the right direction</li>
                        <li> try again later (if you have been through this before please do contact us).</li>
                    </ul>
                % endif
            </label>
        </div>   
    </fieldset>
    
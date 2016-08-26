<%inherit file="/base.mako"/>

<h2></h2>
<div class="item-list">
    <div  class="item-project">
        <div class="item-content">
            <fieldset class="collapsible">
                <legend><a href="#" title="Expand/collapse details" onclick="toggleFieldset(this); return false;">Actions</a>
                </legend>
                <div class="content">
                   <p>In this page you can chose which kind of proxy certificate use to access to Grid resources <br/>
<br/></p>
                    <table style='text-align:left;'>
                        <tr>
                            <th></th><th>Personal Certificate</th>
                        </tr>
                        <tr>
                            <td>
                                ${h.link_to(
                                    "Create a Voms Proxy",
                                    h.url(
                                    controller=u'access',
                                    action='create_voms_proxy',
                                ))}
                            </td>
                            <td>Create a Voms Proxy  </td>
                        </tr>
                        <tr>
                            <td>
                             ${h.link_to(
                                    "Create MyProxy",
                                    h.url(
                                    controller=u'access',
                                    action='create_myproxy',
                                ))}
                            </td>
                            <td>Create MyProxy  </td>
                        </tr>
                        <tr>
                            <td><a href='' onClick=\"window.open('https://web-enmr.cerm.unifi.it/alfa/eric/applet2/index.html','','width=600,height=300,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=no')\">  Create Proxy from  Applet</a></td>
                            <td> Use your Personal Certificate to create a Proxy using a Java applet</td>
                        </tr>
                        <tr>
                            <td>
                                 ${h.link_to(
                                    "Remove a Proxy",
                                    h.url(
                                    controller=u'access',
                                    action='remove_proxy',
                                ))}
                            </td>
                            <td>Remove a Proxy </td>
                        </tr>
                        <tr><th></th><th>Robot  Certificate</th></tr>
                        <tr>
                            <td>
                                ${h.link_to(
                                    "Create Proxy Robot",
                                    h.url(
                                    controller=u'access',
                                    action='create_proxy_robot',
                                ))}
                            </td>
                            <td>Use a Robot certificate to create a  Proxy </td>
                        </tr>
                        <tr>
                            <td>
                                ${h.link_to(
                                    "Robo Proxy Info",
                                    h.url(
                                    controller=u'access',
                                    action='robot_proxy_info',
                                ))}
                            </td>
                            <td>Show info about the validity of you Robot proxy </td>
                        </tr>
                        <tr>
                            <td>
                                ${h.link_to(
                                    "Delegate to MyProxy",
                                    h.url(
                                    controller=u'access',
                                    action='delegate_to_myproxy',
                                ))}
                            </td>
                            <td>Store your Robot proxy in a Myproxy server</td>
                        </tr>
                        <tr>
                            <td>
                                ${h.link_to(
                                    "Info MyProxy",
                                    h.url(
                                    controller=u'access',
                                    action='info_myproxy',
                                ))}
                            </td>
                            <td> Show info about a Proxy stored in a Myproxy server</td>
                        </tr>
                    </table>                  
                </div>
            </fieldset>           
        </div>
    </div>
</div>

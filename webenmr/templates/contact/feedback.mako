<%inherit file="/base.mako"/>
<%def name="css()">
   
</%def>

<%def name="js()">
<script type="text/javascript" src="/global/javascript/jquery.easing.js"></script>

<script  type="text/javascript">
    $(document).ready( function() {
        $("#contact").validationEngine()
	
    });
</script>

<script type="text/javascript">
    
</script>

</%def>

<form id="contact" class="formular" method="post" action="${h.url('/feedback/sendMail')}">
    Use the contact form below to submit your request and/or feedback.
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
            
                    <label for="address" class="feedback">Address (optional)</label>
                    <input value=""  class="validate[optional, length[0,100]] text-input" type="text" id="address" name="address"  />
            
                    <label for="postalcode" class="feedback">Postal code (optional)</label>
                    <input value=""  class="validate[optional,custom[onlyNumber],length[3,10]] text-input" type="text" id="postalcode" name="postalcode"  />
            
                    <label for="city" class="feedback">City (optional)</label>
                    <input value=""  class="validate[optional,custom[onlyLetter],length[2,100]] text-input" type="text" id="city" name="city"  />
            
                    <label for="country" class="feedback">Country (optional)</label>
                    <input value=""  class="validate[optional,custom[onlyLetter],length[3,100]] text-input" type="text" id="country" name="country"  />
            
        </fieldset>
        <fieldset>
                <legend>Email</legend>
                        <label for="email" class="feedback">Email address</label>
                        <input value=""  class="validate[required,custom[email]] text-input" type="text" name="email" id="email"  />
                
                        <label for="email2" class="feedback">Confirm email address</label>
                        <input value="" class="validate[required,confirm[email]] text-input" type="text" name="email2"  id="email2" />
        </fieldset>
        <fieldset>

                <legend>Comments</legend>
                        <label for="comments" class="feedback">Comments</label>
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

        <input class="submit" type="submit" value="Send"/>
        <hr/>
</form>




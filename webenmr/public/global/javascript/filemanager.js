        var selright
        var selleft
        var prev_selleft
        var portal = ""
	$(document).ready( function() {
            //$("#wait-modal").dialog({
            //    closeOnEscape: false,
            //    position: 'center',
            //    width: 450,
            //    height: 450,
            //    modal: true,
            //    resizable: false,
            //    draggable: false,
            //    open: function(event, ui) { $(".ui-dialog-titlebar-close").hide();},
            //    autoOpen: false
            //});
//            $("#help").dialog({
//                title: "Amber Web Portal Filemanager documentation",
//                autoOpen: false,
//                height: 450,
//                width: 500,
//                position: 'center',
//                modal: true,
//                buttons: {
//                        Ok: function() {
//                                $(this).dialog('close');
//                        }
//                }
//	    });
            $("#toolbar").find("li").filter(".help").removeClass("disabled").bind("click", function(){
                var myWidth = 650;
                var myHeight = 300;
                var option = {
                    opacity:70,
                    minWidth: myWidth,
                    minHeight: myHeight,
                    maxWidth: myWidth,
                    maxHeight: myHeight
                };
                $("#help").modal(option);
                //$("#help").dialog('open')
            });
            $("#toolbar").find("li").filter(".project").removeClass("disabled").bind("click", function(){window.location = "/projects/project_create";});
            $("textarea").live("click", function(){
                $("#contentlist").children("li").filter(".ui-selected")
                    .removeClass("ui-selected").children("textarea")
                    .removeClass("selected");
                $(this).parent().addClass("ui-selected");
                $(this).addClass("selected");
                $(this).addClass("selected");
                update_toolbar($(this).parent());
            });
            
            $("textarea").bind("blur", function(){
                $(this).parent().removeClass("ui-selected");
                $(this).removeClass("selected"); 
            });
            selleft = $("#menufinder").children("li").children("a");
            //var menu1 = [
            //    {'open': function(menuItem,menu) {
            //        location.href = "http://www.google.it/";
            //        }
            //    },
            //    $.contextMenu.separator,
            //    {'delete':{
            //        onclick:function(menuItem,menu) {  location.href = "http://www.Wikipedia.it/";  },
            //        icon:'/global/images/cancel.gif',
            //        disabled:true
            //        }
            //    },
            //    {'rename': function(menuItem,menu) { location.href = "http://www.altervista.it/";   } },
            //    $.contextMenu.separator,
            //    {'download':{ onclick:function(menuItem,menu) { location.href = "http://codesnippet.altervista.it/";}, icon:'/global/images/compress.png', disabled:false} },
            //    {'info': function(menuItem,menu) { location.href = "http://codesnippet.altervista.it/";    } }
            //];
            //$('#menulist').find("a").each(function(){
            //    $(this).contextMenu(menu1,{theme:'vista', shadow:false});
            //});
            
            $("#contentlist").children("li").each(function(){
                if($(this).children("p").hasClass("dir_big")){
                    //$(this).contextMenu(menu1, {theme:'vista', shadow:false});
                }
            });
            
            $("#menufinder").selectable({ filter: 'a' });
            $("#menufinder").selectable({
                selected: function(event, ui) {
                    var totsel = $("#menufinder").find(".ui-selected").length;
                    if (totsel > 1){
                        selected_list = $("#menufinder").find(".ui-selected");
                        reset_toolbar();
                        //$("li").filter(".download").removeClass("disabled")
                        //    .bind('click', function(){
                        //        download();    
                        //    });
                        update_toolbar(selleft);
                        var path = '';
                        $(selected_list).each(function(i){
                            if (i == 1){
                                path = 'path='+ makepath(this);
                            }
                            else{
                                path = path +'&path='+ makepath(this);    
                            }
                        });
                        //$.ajax({
                        //    type: "POST",
                        //    url: "/filemanager/get_dir_size",
                        //    data: path,
                        //    success: function(data){
                        //        $("#statusbar").children(".el-finder-sel").empty();
                        //        $("#statusbar").children(".el-finder-sel").append("selected item(s): "+totsel+" size: "+data);
                        //    }
                        //});
                    }
                    else{
                        //if (selleft != ''){
                        //    prev_selleft = selleft;    
                        //}
                        $("#contentlist").find(".ui-selected").removeClass("ui-selected");
                        selright = ''
                        selleft = $(ui.selected);
                        reset_toolbar();
                        initialize_toolbar();
                        $("#menufinder").find("p").filter(".open").each(function(){
                            if(!$(this).closest("li").children("ul").length){
                                $(this).removeClass("open");
                                $(this).addClass("close");
                                $(this).siblings("div").removeClass("expanded");
                                $(this).siblings("div").addClass("collapsed");
                            }
                        });
                        var isopen = $(ui.selected).children("p").hasClass("open");
                        if(isopen){
                            var li_root = $(ui.selected).parent();
                            var collapse = true;
                            //if(selleft.siblings("ul").length){
                            //    var u_sibling = selleft.siblings("ul");
                            //    u_sibling.children("li").each(function(){
                            //        if($(this).children("a").children("p").hasClass("open")){
                            //            collapse = false;
                            //        }
                            //    });
                            //}
                            if(collapse && ($(selleft).children("i").text() != 'amber' && $(selleft).children("i").text() != 'maxocc')){
                                $(ui.selected).children("p").removeClass("open");
                                $(ui.selected).children("p").addClass("close");
                                $(ui.selected).children("div").removeClass("expanded");
                                $(ui.selected).children("div").addClass("collapsed");
                                $(ui.selected).parent().children("ul").remove();
                                $("#contentlist").empty();
                                var path = makepath(selleft);
                                $("#statusbar").children(".el-finder-path").empty();
                                $("#statusbar").children(".el-finder-path").append(path);
                                //var tmp = $(selleft).siblings("ul");
                                //tmp.remove();
                                //if ($(selleft).children("i").text() == 'Home'){
                                //    
                                //    list_home();
                                //}
                                //else{
                                //    var level = $(selleft).parentsUntil("#leftmenu").filter("li").length;
                                //    if (level == 2){
                                //        list_proj(selleft);
                                //    }
                                //    else{
                                //        list_calc(selleft);
                                //    }
                                //}
                                
                                
                                //$(dir).addClass("ui-selectee ui-selected");
                            }
                            else if(($(selleft).children("i").text() != 'amber' && $(selleft).children("i").text() != 'maxocc')) {
                                selleft.parent().children("ul").remove();
                                //list_proj($(ui.selected));
                            }
                            //else{
                            //    $(selleft).removeClass("ui-selected");
                            //}
                            if ($(selleft).children("i").text() != 'amber' || $(selleft).children("i").text() != 'maxocc'){
                                $(selleft).removeClass("ui-selected");
                                selleft = prev_selleft;
                                $(selleft).addClass("ui-selected");
                            }
                        }
                        else{
                            var totsel = $("#leftmenu").find(".ui-selected").length;
                            var path = makepath(selleft);
                            //$.ajax({
                            //    type: "POST",
                            //    url: "/filemanager/get_dir_size",
                            //    data: "path="+path,
                            //    success: function(data){
                            //        $("#statusbar").children(".el-finder-sel").empty();
                            //        $("#statusbar").children(".el-finder-sel").append("selected item(s): "+totsel+" size: "+data);
                            //    }
                            //});
                            $(ui.selected).children("div").removeClass("collapsed");
                            $(ui.selected).children("div").addClass("expanded");
                            //dipende dal livello
                            // > 3 si tratta dei files del calcolo
                            var level = $(ui.selected).parentsUntil("#leftmenu").filter("li").length;
                            if(level > 3){
                                list_calc(ui.selected);
                            }
                            else{
                                if ($(selleft).children("i").text() == 'Projects'){
                                    list_home();
                                }
                                else{
                                    list_proj($(ui.selected));
                                }
                                 //$("#statusbar").children(".el-finder-sel").empty();
                            }
                            
                        }
                        update_toolbar(selleft);
                        //$("#finder").removeClass("trans-box");
                    }
                },
                unselected: function(event, ui) {
                    prev_selleft = ui.unselected;
                    selleft = "";
                    reset_toolbar();
                    //$("#statusbar").children(".el-finder-sel").empty();
                    if($(ui.unselected).children("input[name=old-value]").length){
                        var oldname = $(ui.unselected).children("input[name=old-value]").attr("value");
                        var val = $(ui.unselected).children("input").attr("value");
                        $(ui.unselected).children("input[type=text]").replaceWith("<i>"+val+"</i>");
                        var oldpath = makepath(ui.unselected);
                        oldpath = oldpath.replace(val, oldname);
                        var newname = $(ui.unselected).children("i").text();
                        $.ajax({
                            type: 'POST',
                            url: '/filemanager/rename',
                            data: 'curName='+oldpath+'&newName='+newname,
                            success: function(data){
                                $(ui.unselected).children("input[name=old-value]").remove();
                            }
                        }); 
                    }
                }
            });
            
            $("#contentlist").selectable({filter: 'li'});
            $("#contentlist").selectable({
                selected: function(event, ui) {
                    selright = $(ui.selected);
                    var valtext = $(selright).children("textarea").text();
                    if (valtext.length > 22){
                        var totrows = Math.ceil(valtext.length / 11) + 1;
                        $(selright).children("textarea").attr("rows", totrows);
                    }
              
                    $(selright).children("textarea").addClass("selected");
                    var totsel = $("#contentlist").find(".ui-selected").length;
                    if (totsel > 1){
                        selected_list = $("#contentlist").find(".ui-selected");
                        reset_toolbar();
                        //$("li").filter(".download").removeClass("disabled")
                        //    .bind('click', function(){
                        //        download();    
                        //    });
                        //in questo caso selright non serve a niente
                        update_toolbar(selright);
                        var path = '';
                        if (selleft == ''){
                            selleft = prev_selleft;
                        }
                        var root = makepath(selleft)
                        $(selected_list).each(function(i){
                            if (i == 0){
                                path = 'path='+ root + $(this).children("textarea").text();
                            }
                            else{
                                path = path +'&path='+ root + $(this).children("textarea").text();    
                            }
                        });
                        //$.ajax({
                        //    type: "POST",
                        //    url: "/filemanager/get_dir_size",
                        //    data: path,
                        //    success: function(data){
                        //        $("#statusbar").children(".el-finder-sel").empty();
                        //        $("#statusbar").children(".el-finder-sel").append("selected item(s): "+totsel+" size: "+data);
                        //    }
                        //});
                    }
                    else{
                        //selright = $(ui.selected);
                        //$(selright).children("textarea").addClass("selected");
                        //var totsel = $("#contentlist").find(".ui-selected").length;
                        var obj = '';
                        var trueobj = false;
                        $("#menulist").find("a").each(function(){
                            if ($(this).children("i").text() == selright.children("textarea").text()){
                                obj = this;
                                trueobj = true;
                            }
                        });
                        var path = '';
                        if (selleft == ''){
                            selleft = prev_selleft;
                        }
                        if(trueobj){
                            path = makepath(obj);
                        }
                        else{
                            path = makepath(selleft) + $(selright).children("textarea").text();
                        }
                        $("#statusbar").children(".el-finder-path").empty();
                        $("#statusbar").children(".el-finder-path").append(path);
                        //$.ajax({
                        //    type: "POST",
                        //    url: "/filemanager/get_dir_size",
                        //    data: "path="+path,
                        //    success: function(data){
                        //        $("#statusbar").children(".el-finder-sel").empty();
                        //        $("#statusbar").children(".el-finder-sel").append("selected item(s): "+totsel+" size: "+data);
                        //    }
                        //});
                        
                        update_toolbar(selright);
                    }
                },
                unselected: function(event, ui) {
                    selright = "";
                    $(ui.unselected).children("textarea").attr("rows", 2);
                    $(ui.unselected).children("textarea").removeClass("selected");
                    $(ui.unselected).children("textarea").attr("readonly", "readonly");
                    reset_toolbar();
                    //$("#statusbar").children(".el-finder-sel").empty();
                    if($(ui.unselected).children("input[name=old-value]").length){
                        if ($(ui.unselected).children("textarea").length){
                            var oldname = $(ui.unselected).children("input[name=old-value]").attr("value");
                            var obj = '';
                            $("#menulist").find("a").each(function(){
                                if ($(this).children("i").text() == oldname){
                                    obj = this;
                                }
                            });
                            var oldpath = makepath(obj);
                            var newname = $(ui.unselected).children("textarea").attr('value');
                            $.ajax({
                                type: 'POST',
                                url: '/filemanager/rename',
                                data: 'curName='+oldpath+'&newName='+newname,
                                success: function(data){
                                    $(ui.unselected).children("input[name=old-value]").remove();
                                    //renameSuccessProcessing(data);
                                    //$(ui.unselected).children("input").replaceWith('<label>'+newname+'</label>');
                                }
                            });  
                        }
                    }
                }
            });
            
            //$("#contentlist").children("li").each(function(){
            //    var o = this;
            //    $(o).bind('dblclick', function(){
            //        dispatch(o);
            //    });
            //});
        });
            
            
        
        //function renameSuccessProcessing(data){
        //    alert("unable to rename. Maybe already exist with same name!");
        //}
        
        
        function rename(){
            if (selright){
                var val = $(selright).children("textarea").text();
                $(selright).children("textarea").removeAttr("readonly");
                $(selright).children("textarea").select();
                $(selright).children("textarea").removeClass("selected");
                $(selright).children("textarea").css("cursor", "text");
                $(selright).append('<input type="hidden" name="old-value" value="'+val+'"');
                $(selright).children("textarea").bind("keydown", function(e) {
                    if(e.keyCode == 13) {
                        e.preventDefault();
                        var oldname = $(this).parent().children("input[name=old-value]").attr("value");
                        var obj = '';
                        $("#menulist").find("a").each(function(){
                            if ($(this).children("i").text() == oldname){
                                obj = this;
                            }
                        });
                        var oldpath = makepath(obj);
                        var newname = $(this).parent().children("textarea").attr('value');
                        $.ajax({
                            type: 'POST',
                            url: '/filemanager/rename',
                            data: 'curName='+oldpath+'&newName='+newname,
                            success: function(data){
                                $("#menulist").find("i").each(function(){
                                    if ($(this).text() == oldname){
                                        $(this).text(newname);
                                    }
                                });
                                $(selright).children("textarea").addClass("selected");
                                $(selright).children("textarea").attr("readonly", "readonly");
                                $(selright).children("textarea").select();
                                $(selright).children("textarea").unbind("keydown");
                                $(selright).children("textarea").css("cursor", "hand")
                                $(this).parent().children("input[name=old-value]").remove();
                                //renameSuccessProcessing(data);
                                //$(ui.unselected).children("input").replaceWith('<label>'+newname+'</label>');
                            }
                        });  
                    }
                });
            }
            else{
                var val = $(selleft).children("i").text();
                $(selleft).children("i").replaceWith('<input type="text" size="19" value="'+val+'" />');
                $(selleft).children("input[type=text]").select();
                $(selleft).append('<input type="hidden" name="old-value" value="'+val+'" />');
                $(selleft).children("input[type=text]").bind("keyup", function(e) {
                    if(e.keyCode == '13') {
                        e.preventDefault();
                        var oldname = $("input[name=old-value]").attr("value");
                        var val = $(this).parent().children("input[type=text]").attr("value");
                        var par = $(this).parent();
                        $(this).parent().children("input[type=text]").replaceWith("<i>"+val+"</i>");
                        var oldpath = makepath(par);
                        oldpath = oldpath.replace(val, oldname);
                        var newname = $(par).children("i").text();
                        $.ajax({
                            type: 'POST',
                            url: '/filemanager/rename',
                            data: 'curName='+oldpath+'&newName='+newname,
                            success: function(data){
                                //var old = $(par).children("input[name=old-value]").attr("value");
                                $("#contentlist").children().each(function(){
                                    if ($(this).children("textarea").text() == oldname){
                                        $(this).children("textarea").attr("value", newname);
                                    }
                                });
                                $("input[name=old-value]").remove();
                            }
                        }); 
                    }
                    //e se aggiungiamo gestione key ESC, per annullare modifica in corso? Mica male!
                    else if(e.keyCode == '27'){
                        e.preventDefault();
                        var oldname = $("input[name=old-value]").attr("value");
                        $(this).children("textarea").attr("value", oldname);
                        $("input[name=old-value]").remove();
                        $(selleft).children("input").replaceWith("<i>"+oldname+"</i>");
                    }
                });
            }
        }
        
        function mkdir(){
            var path = makepath(selleft);
            $.ajax({
                type: "POST",
                url: "/filemanager/mkdir",
                data: "path="+path,
                success: function(data){
                    var datalist = data.split("::");
                    if(datalist[0] == "True" &&  datalist[1] == "True"){
                        var itemdx = '<li class="ui-selectee ui-selected"><p class="dir_big manual"></p><textarea rows="1" cols="11" selected="selected">untitled folder</textarea></li>';
                        $("#contentlist").append(itemdx);
                        var itemsx = '';
                        var thereisul = true;
                        if(!$(selleft).children("ul").length){
                            itemsx = '<ul>'
                            thereisul = false;
                        }
                        itemsx = itemsx + '<li class="ui-selectee ui-selected"><a href="#"><div class="collapsed"></div><p id="menuleft" class="dir_small manual close collapsed"></p><input type="text" size="22" value="untitled folder" /></a></li>';
                        if (!thereisul){
                            itemsx = itemsx + '</ul>';
                            $(selleft).parent().append(itemsx);
                        }
                        else{
                            $(selleft).children("ul").append(itemsx);
                        }
                        $(selleft).parent().find("ul").css('list-style-type','none');
                    }
                }
            });
        }
        
        function mkfile(){
            var path = makepath(selleft);
            $.ajax({
                type: "POST",
                url: "/filemanager/mkfile",
                data: "path="+path,
                success: function(data){
                    var item = '<li class="ui-selectee ui-selected"><p class="mimetypes txt"></p><textarea rows="1" cols="11" selected="selected">new file.txt</textarea></li>';
                    $("#contentlist").append(item);
                }
            });
        }
        
        function removeitem(){
            var removeit = false;
            var path = '';
            //if (selright && $(selright).children("p").hasClass("manual")){
            //    removeit = true;
            //}
            //se si tratta di selleft ed è un progetto o calcolo o dir creata da user
            var level = $(selleft).parentsUntil("#leftmenu").filter("li").length;
            if( (level == 2 || level == 4)){ //|| (level > 4 && $(selleft).children("p").hasClass("manual"))
                //if (removeit && $(selright).children("p").hasClass("mimetypes")){
                //    path = makepath(selleft) + $(selright).children("textarea").text();
                //}
                //else{
                removeit = true;
                path = makepath(selleft);
                if (selright){
                    var addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                    path = path + addtopath +'/' + $(selright).children("textarea").attr("value");
                }
                //}
                
            }
            if(removeit){
                $.ajax({
                    type: 'POST',
                    url: '/filemanager/remove',
                    data: 'path='+path,
                    success: function(data){
                        if (selright){
                            if ($(selright).children("p").hasClass("dir_big")){
                                $(selright).remove();
                                $(selleft).parent().children("ul").find("li").each(function(){
                                    if ($(this).children("a").children("i").text() == $(selright).children("textarea").text()){
                                        $(this).remove();
                                        //se amber è vuoto cancellarlo
                                    }
                                });
                            }
                        }
                        else{
                            $(selleft).parent().remove();
                            $("#contentlist").children().remove();
                        }
                        
                    }
                });
            }
        }
        
        function download(){
            if (selright){
                var selected_list = $("#contentlist").find(".ui-selected");   
            }
            else{
                var selected_list = $("#menufinder").find(".ui-selected");
            }
            selleft = $("#menufinder").find(".ui-selected");
            var path = '';
            var root = '';
            $(selected_list).each(function(i){
                if (selright){
                    var item = $(this).children("textarea").text()
                    root = makepath(selleft)
                }
                else{
                    var item = makepath(selleft)
                }
                if (i == 0){
                    path = 'path='+ root + item;
                }
                else{
                    path = path +'&path='+ root + item;    
                }
            });
            window.open("/filemanager/download?"+path)
            window.back
            //$.ajax({
            //    type: "GET",
            //    url: "/filemanager/download",
            //    data: path,
            //    complete: function (){window.open(location);}
            //});
        }
        
        
        function makepath(obj){
            var par = $(obj).parentsUntil("#leftmenu");
            var li_list = par.filter("li");
            var len_li_list = li_list.length;
            var str_path = "";
            $(li_list).each(function(){
                str_path =  $(this).children("a").children("i").text() + "/" + str_path;    
            });
            //alert(str_path)
            return str_path
        }

        function dispatch(o){
            //viene chiamata solo dal menu dx
            //deve discriminare se si tratta di file o dir:
            //          - dir: chiamare list_proj(oggetto selezionato)
            //          - file: scegliere tra le diverse azioni possibili in base al tipo di file
            //                  prima abilitare le possibili azioni nella toolbar
            
            //$("#menulist").find("a").removeClass("ui-selected");
            if ($(o).children("p").hasClass("dir_big")){
                //bisogna capire a quale elemento del menu sx si riferisce
                selright = o;
                var obj = '';
                $("#menulist").find("a").each(function(){
                    if ($(this).children("i").text() == $(selright).children("textarea").text()){
                        obj = this;
                    }
                });
                selleft = obj;
                $("#menulist").find("a").removeClass("ui-selected");
                $(selleft).addClass("ui-selected");
                //capire se è progetto calcolo o interno calcolo
                var par = $(obj).parentsUntil("#leftmenu");
                var ul_list = par.filter("ul");
                var level = ul_list.length;
                //alert(level)
                if(level >= 4){//interno calcolo o calcolo
                    list_calc(obj);    
                }
                else if(level == 2){//progetto
                    list_proj(obj)
                }
                
            }
            else{
                selleft = $("#menufinder").find(".ui-selected")
                selright = o;
                file_action(o);
            }
        }
        
        
        function file_action(obj_sel){
            if ($(obj_sel).children("p").hasClass("tgz") || $(obj_sel).children("p").hasClass("png")){
                download();
            }
            else if($(obj_sel).children("p").hasClass("pdb")){
                var path = makepath(selleft);
                var pdbname = $(obj_sel).children("textarea").text()
                path = path + pdbname;
                open_jmolView(path, pdbname);
            }
            else{
                quicklook();
            }
            
        }
        
        function list_home(){
            $.ajax({
                    type: "GET",
                    url: "/filemanager/projects_list",
                    success: function(data){
                        update_leftmenu($("#menufinder").children("li").children("a"), data);
                        //update_rightmenu(data, 1);
                        update_statusbar("Projects/", data);
                    }
            });
        }
        
        function list_proj(obj_sel){
            var path = makepath(obj_sel);
            var proj = $(obj_sel).children("i").text();
            $.ajax({
                    type: "GET",
                    url: "/filemanager/calculations_list",
                    data: "proj="+proj,
                    success: function(data){
                        update_leftmenu(obj_sel, data);
                        update_rightmenu(data, 2);
                        update_statusbar(path, data);
                    }
            });
        }
        
        function list_calc(obj_sel){
            var path = makepath(obj_sel);
            
            $.ajax({
                type: "GET",
                url: "/filemanager/dircontent",
                data: "path="+path,
                success: function(data){
                    if (data){
                        var items = data.split(",");
                        var newitemsleft = '<ul>';
                        var thereisdir = false;
                        $(items).each(function(){
                            var val  = '';
                            if(this.split("::")[0] == 'dir'){
                                thereisdir = true;
                                val = this.split("::")[1];
                                newitemsleft = newitemsleft +
                                '<li>'+
                                    '<a>'+
                                        '<div class="collapsed" ></div>'+
                                        '<p id="menuleft" class="dir_small close collapsed"></p>'+
                                        '<i>'+val+'</i>'+
                                    '</a>'+
                                '</li>';
                            }
                        });
                        if(thereisdir){
                            newitemsleft = newitemsleft + '</ul>'
                            $(obj_sel).parent().append(newitemsleft);
                            //$(obj_sel).children("div").removeClass("collapsed");
                            //$(obj_sel).children("div").addClass("expanded");
                            $(obj_sel).parent().find("ul").css('list-style-type','none');       
                        }
                        $(obj_sel).children("p").removeClass("close");
                        $(obj_sel).children("p").addClass("open");
                        //$(obj_sel).children("div").removeClass("collapsed");
                        //$(obj_sel).children("div").addClass("expanded");
                        update_rightmenu(data, 3);
                        update_statusbar(path, data);    
                    }
                    else{
                        $("#contentlist").empty();
                    }
                }
            });
        }
        
        function update_statusbar(bread, data){
            //ajax per restituire il numero totale degli elementi e size
            //                    mostrare il path (breadcrump)
            //                    mostrare elem sel e size
            $(".el-finder-path").empty();
            $(".el-finder-path").append(bread);
            if (data){
                var items = data.split(",");    
            }
            else{
                var items = [];
            }
            $(".el-finder-stat").empty();
            //$.ajax({
            //    type: "POST",
            //    url: "/filemanager/get_dir_size",
            //    data: "path="+bread,
            //    success: function(data){
            //        $(".el-finder-stat").append("items: "+items.length +", size: " + data);
            //    }   
            //});
        }
        
        function update_rightmenu(data, level){
            //creo la parte di DOM necessaria
            //aggiungendo una azione per il doppio clic
            $("#contentlist").empty();
            if(data){
                var it = data.split(";;");
                if (it.length == 1){
                        var type = '';
                        items = data.split(",");
                        var newitemsleft = "<ul>";
                        var thereisdir = false;
                        $(items).each(function(){
                            if(level > 2){
                                var elemlt =  $.trim(this.split("::")[0]);
                                var elemdx =  $.trim(this.split("::")[1]);
                                if(elemlt == "dir"){
                                    type = 'class="'+$.trim(this.split("::")[0])+'_big"';
                                }
                                else{
                                    var dotdx = elemdx.split(".");
                                    var lendotdx = dotdx.length;
                                    type = 'class="mimetypes '+dotdx[lendotdx - 1]+'"';
                                }
                                $("#contentlist").append('<li><p '+type+'></p><textarea readonly="readonly" cols=11 rows=2>'+elemdx+'</textarea></li>');
                                $("#contentlist").children("li:last").bind('dblclick', function(){
                                    dispatch(this);
                                });
                                /*$("#contentlist").children("li:last").children("textarea").bind('dblclick', function(){
                                    dispatch($(this).parent());
                                })*/;
                            }
                            else{
                                $("#contentlist").append('<li><p class="dir_big" ></p><textarea readonly="readonly" cols=11 rows=2>'+this+'</textarea></li>');
                                $("#contentlist").children("li:last").bind('dblclick', function(){
                                    dispatch(this);
                                });
                                //$("#contentlist").children("li:last").children("textarea").bind('dblclick', function(){
                                //    dispatch($("#contentlist").children("li:last"));
                                //    
                                //});
                            }
                        });
                }
                else{
                        var count = 0;
                        var elem
                        $(it).each(function(){
                                itlist = this.split("::")
                                if (itlist[1] != ''){
                                        count = count + 1;
                                        elem = itlist[1]
                                }
                        });
                        if (count == 1){
                                elemlist = elem.split(',')
                                $(elemlist).each(function(){
                                        $("#contentlist").append('<li><p class="dir_big" ></p><textarea readonly="readonly" cols=11 rows=2>'+this+'</textarea></li>');
                                        $("#contentlist").children("li:last").bind('dblclick', function(){
                                            dispatch(this);
                                        });        
                                });
                        }
                }
                
            }
        }
        
        function update_leftmenu(sel, data){
            //creo la parte di DOM necessaria MA solo per le directory
            //se la dir è già open
            //      controllo se c'è qualche sottodir aperta
            //          se si chiudo la sottodir open
            //          se no chiudo dir
            //altrimenti procedo nel processare <data>
            if(data){
                var newitemsleft
                var it = data.split(";;");
                if (it.length == 1){
                        //si tratta di progetti
                        newitemsleft = '<ul id="menulist">';
                        items = it[0].split(",")
                        $(items).each(function(){
                            newitemsleft = newitemsleft +
                            '<li>'+
                                '<a><div class="collapsed" ></div>'+
                                '<p id="menuleft" class="dir_small close collapsed"></p>'+
                                '<i>'+this+'</i>'+
                                '</a></li>';
                            });
                        newitemsleft = newitemsleft + '</ul>'
                        $(sel).parent().append(newitemsleft);
                        $(sel).parent().find("ul").css('list-style-type','none');   
                }
                else{
                        //visualizzo i calcoli
                        something = false
                        newitemsleft = '';
                        $(it).each(function(i){
                                itlist = this.split("::")
                                if (itlist[1] != 0){
                                        something = true;
                                        //if (i){
                                        //        newitemsleft = newitemsleft + "<ul>"+
                                        //        '<li>'+
                                        //            '<a><div class="expanded" ></div>'+
                                        //                '<p id="menuleft" class="dir_small open collapsed"></p>'+
                                        //                '<i>'+itlist[0]+'</i>'+
                                        //            '</a>'+
                                        //            '<ul>';
                                        //}
                                        //else{
                                        newitemsleft += "<ul>"+
                                         '<li>'+
                                             '<a><div class="expanded" ></div>'+
                                                 '<p id="menuleft" class="dir_small open collapsed"></p>'+
                                                 '<i>'+itlist[0]+'</i>'+
                                             '</a>'+
                                             '<ul>'; 
                                        //}
                                        //newitemsleft = newitemsleft + "<ul>"+
                                        //'<li>'+
                                        //    '<a><div class="expanded" ></div>'+
                                        //        '<p id="menuleft" class="dir_small open collapsed"></p>'+
                                        //        '<i>'+itlist[0]+'</i>'+
                                        //    '</a>'+
                                        //    '<ul>';
                                        items = itlist[1].split(",")
                                        $(items).each(function(){
                                                newitemsleft = newitemsleft +
                                                '<li>'+
                                                    '<a><div class="collapsed" ></div>'+
                                                    '<p id="menuleft" class="dir_small close collapsed"></p>'+
                                                    '<i>'+this+'</i>'+
                                                '</a></li>';
                                        });
                                        newitemsleft = newitemsleft + '</ul></li>';
                                }
                        });
                        if (something){
                                newitemsleft = newitemsleft + '</ul>'
                                $(sel).parent().append(newitemsleft);
                                $(sel).parent().find("ul").css('list-style-type','none');    
                        }
                }
                $(sel).children("p").removeClass("close");
                $(sel).children("p").addClass("open");
            //        //visualizzo i calcoli
            //        items.pop();
            //        var newitem
            //        $(items).each(function(){
            //            newitemsleft = newitemsleft +
            //            '<li>'+
            //                '<a><div class="collapsed" ></div>'+
            //                '<p id="menuleft" class="dir_small close collapsed"></p>'+
            //                '<i>'+this+'</i>'+
            //            '</a></li>';
            //            });
            //        //if items[0].split()
            //        var newitemsleft = "<ul>"+
            //        '<li>'+
            //            '<a><div class="expanded" ></div>'+
            //                '<p id="menuleft" class="dir_small open collapsed"></p>'+
            //                '<i>amber</i>'+
            //            '</a>'+
            //            '<ul>';
            //    }
            //    $(items).each(function(){
            //            newitemsleft = newitemsleft +
            //            '<li>'+
            //                '<a><div class="collapsed" ></div>'+
            //                '<p id="menuleft" class="dir_small close collapsed"></p>'+
            //                '<i>'+this+'</i>'+
            //            '</a></li>';
            //           
            //    });
            //   
            //    newitemsleft = newitemsleft + '</ul>'
            //    $(sel).parent().append(newitemsleft);
            //    $(sel).parent().find("ul").css('list-style-type','none');        
            //    
            //}
            //$(sel).children("p").removeClass("close");
            //$(sel).children("p").addClass("open");
            //$(sel).children("div").removeClass("collapsed");
            //$(sel).children("div").addClass("expanded");
            }
        }
        
        function initialize_toolbar(){
            var level = $(selleft).parentsUntil("#leftmenu").filter("li").length;
            //if(level >= 4){
            //    $("li").filter(".mkdir").removeClass("disabled")
            //        .bind("click", function(){
            //            mkdir();    
            //        });
            //    $("li").filter(".mkfile").removeClass("disabled")
            //        .bind("click", function(){
            //            mkfile();    
            //        });
            //}
        }
        
        function update_toolbar(o){
            reset_toolbar();
            if (o){
                if($("#contentlist").find(".ui-selected").length == 1){
                    var level = $(selleft).parentsUntil("#leftmenu").filter("ul").length;
                        if(level == 2){
                            $("li").filter(".rm").removeClass("disabled").bind("click", function(){
                                removeitem();
                            });
                            $("li").filter(".rename").removeClass("disabled").bind("click", function(){
                                rename();    
                            });
                            $("li").filter(".downloadbundle").removeClass("disabled").bind("click", function(){
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
                                        $.modal('<img src="/global/images/downloadBundle.gif">', option);    
                                    var path = makepath(selleft);
                                    path_splitted = path.split("/")
                                    //if (path_splitted.length == 3){//selezionato progetto!
                                        addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                        path = path + addtopath + "amber/" + $(o).children("textarea").text()
                                    //} 
                                    //path = path + "/amber/" + $(o).children("textarea").text()
                                    //alert(path)
                                    $.ajax({
                                        type: "POST",
                                        url: "/filemanager/prepare_results",
                                        data: "path=" + path,
                                        success: function(data){
                                                $.modal.close();
                                                if (data) {
                                                        window.open("/filemanager/download_results?name="+data)
                                                }
                                                else{
                                                        var myWidth = 550;
                                                        var myHeight = 50;
                                                        var option = {
                                                            opacity:70,
                                                            minWidth: myWidth,
                                                            minHeight: myHeight,
                                                            maxWidth: myWidth,
                                                            maxHeight: myHeight
                                                        };
                                                        $.modal('<img src="/global/images/attention_01.png"> Selected calculation isn\'t completed, probably is running or scheduled', option);    
                                                }
                                                
                                        }
                                    }); 
                                    
                                })
                            cpath = makepath(selleft);
                            if (cpath.indexOf("amber") > 0){
                                $("li").filter(".violations").removeClass("disabled").bind("click", function(){
                                    var path = makepath(selleft);
                                    path_splitted = path.split("/")
                                    //if (path_splitted.length == 3){//selezionato progetto!
                                        addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                        path = path + addtopath + '/' + $(o).children("textarea").text()
                                    //} 
                                    //path = path + "/amber/" + $(o).children("textarea").text()
                                    $.ajax({
                                        type: "POST",
                                        url: "/filemanager/prepare_violations",
                                        data: "path=" + path,
                                        success: function(data){
                                                $.modal.close();
                                                if (data) {
                                                        window.open("/filemanager/download_violations?name="+data)
                                                }
                                                else{
                                                        var myWidth = 550;
                                                        var myHeight = 50;
                                                        var option = {
                                                            opacity:70,
                                                            minWidth: myWidth,
                                                            minHeight: myHeight,
                                                            maxWidth: myWidth,
                                                            maxHeight: myHeight
                                                        };
                                                        $.modal('<img src="/global/images/attention_01.png"> Selected calculation isn\'t completed, probably is running or scheduled', option);    
                                                }
                                                
                                        }
                                    });        
                                })
                            }
                            
                            $("li").filter(".downloadbundlexplor").removeClass("disabled").bind("click", function(){
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
                                        $.modal('<img src="/global/images/downloadBundle.gif">', option);    
                                    var path = makepath(selleft);
                                    path_splitted = path.split("/")
                                    //if (path_splitted.length == 3){//selezionato progetto!
                                        addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                        path = path + addtopath + "xplor-nih/" + $(o).children("textarea").text()
                                    //} 
                                    //path = path + "/amber/" + $(o).children("textarea").text()
                                    $.ajax({
                                        type: "POST",
                                        url: "/filemanager/prepare_results_xplor",
                                        data: "path=" + path,
                                        success: function(data){
                                                $.modal.close();
                                                if (data) {
                                                        window.open("/filemanager/download_results?name="+data)
                                                }
                                                else{
                                                        var myWidth = 550;
                                                        var myHeight = 50;
                                                        var option = {
                                                            opacity:70,
                                                            minWidth: myWidth,
                                                            minHeight: myHeight,
                                                            maxWidth: myWidth,
                                                            maxHeight: myHeight
                                                        };
                                                        $.modal('<img src="/global/images/attention_01.png"> Selected calculation isn\'t completed, probably is running or scheduled', option);    
                                                }
                                                
                                        }
                                    }); 
                                    
                                })
                            cpath = makepath(selleft);
                            if (cpath.indexOf("xplor-nih") > 0){
                                $("li").filter(".analysisxplor").removeClass("disabled").bind("click", function(){
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
                                            $.modal('<img src="/global/images/downloadBundle.gif">', option);    
                                        var path = makepath(selleft);
                                        path_splitted = path.split("/")
                                        //if (path_splitted.length == 3){//selezionato progetto!
                                            addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                            
                                        //} 
                                        //path = path + "/amber/" + $(o).children("textarea").text()
                                        $.ajax({
                                            type: "POST",
                                            url: "/filemanager/exec_analysis",
                                            data: "path=" + path,
                                            success: function(data){
                                                    $.modal.close();
                                                    //alert($(selleft).next("ul").children().length)
                                                    if($(selleft).next("ul").children().length == 2){
                                                        $(selleft).next("ul").append('<li><a><div class="collapsed"></div><p id="menuleft" class="dir_small close collapsed"></p><li>analysis</li></a></li>')
                                                    }
                                            }
                                        }); 
                                        
                                });
                            }
                        }
                        if (level == 4){
                            $("li").filter(".jobs").removeClass("disabled").bind('click', function(){
                                var path = makepath(selleft);
                                var addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                path = path + addtopath + '/' +$(selright).children("textarea").attr("value");
                                window.location = '/jobs/show_calc?path='+path; 
                            });
                            
                        }
                        $("li").filter(".download").removeClass("disabled").bind('click', function(){download();});
                        $("li").filter(".info").removeClass("disabled");
                }
                else if ($("#contentlist").find(".ui-selected").length > 1){
                    reset_toolbar();
                    var level = $(selleft).parentsUntil("#leftmenu").filter("ul").length;
                    if(level == 2){
                        $("li").filter(".rm").removeClass("disabled").bind("click", function(){
                            removeitem();
                        });
                    }
                    $("li").filter(".download").removeClass("disabled").bind('click', function(){download();});
                    $("li").filter(".info").addClass("disabled");
                }
                else{
                    if ($("#leftmenu").find(".ui-selected").length == 1){
                        var level = $(o).parentsUntil("#leftmenu").filter("ul").length;
                        if (level == 5 && (makepath(selleft).indexOf("xplor-nih") > 0) && (makepath(selleft).indexOf("amber"))){
                            level = 4
                        }
                        
                        if(level == 2 || level == 4){
                            $("li").filter(".rename").removeClass("disabled").bind("click", function(){
                                rename();    
                            });
                            $("li").filter(".rm").removeClass("disabled").bind("click", function(){
                                removeitem();
                            });
                            $("li").filter(".download").removeClass("disabled").bind('click', function(){download();});
                            $("li").filter(".info").removeClass("disabled");
                            if(level == 2){
                                $("li").filter(".amber").removeClass("disabled").bind("click", function(){
                                    var nameproj = $(o).children("i").text();
                                    $.ajax({
                                        type: "POST",
                                        url: "/projects/get_idproj",
                                        data: "name=" + nameproj,
                                        success: function(data){
                                            if (data){
                                                window.location = "/calculations/newcalc/"+data; 
                                            }
                                            
                                        }
                                    }); 
                                    
                                });
                               
                            }
                            if(level == 4){
                                $("li").filter(".jobs").removeClass("disabled").bind('click', function(){
                                    var path = makepath(o);
                                    var root = path.split('/')[1]
                                    var path = root + '::' + $(o).children("i").text();
                                    window.location = '/jobs/show_calc?path='+path; 
                                    //$.ajax({
                                    //    type: 'POST',
                                    //    url: "/jobs/show_calc",
                                    //    data: "path="+path
                                    //});
                                });
                                cpath = makepath(selleft);
                                if (cpath.indexOf("amber") > 0){
                                    $("li").filter(".downloadbundle").removeClass("disabled").bind("click", function(){
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
                                            $.modal('<img src="/global/images/downloadBundle.gif">', option);
                                        
                                        var path = makepath(selleft);
                                        
                                        $.ajax({
                                            type: "POST",
                                            url: "/filemanager/prepare_results",
                                            data: "path=" + path,
                                            success: function(data){
                                                    $.modal.close();
                                                    if (data) {
                                                            window.open("/filemanager/download_results?name="+data)
                                                    }
                                                    else{
                                                            var myWidth = 550;
                                                            var myHeight = 50;
                                                            var option = {
                                                                opacity:70,
                                                                minWidth: myWidth,
                                                                minHeight: myHeight,
                                                                maxWidth: myWidth,
                                                                maxHeight: myHeight
                                                            };
                                                            $.modal('<img src="/global/images/attention_01.png"> Selected calculation isn\'t completed, probably is running or scheduled', option);    
                                                    }
                                                    
                                            }
                                        }); 
                                        
                                    });
                                }
                                cpath = makepath(selleft);
                                if (cpath.indexOf("amber") > 0){
                                    $("li").filter(".violations").removeClass("disabled").bind("click", function(){
                                        var path = makepath(selleft);
                                        path_splitted = path.split("/")
                                        //if (path_splitted.length == 3){//selezionato progetto!
                                            addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                            path = path + addtopath + '/' + $(o).children("textarea").text()
                                        //} 
                                        //path = path + "/amber/" + $(o).children("textarea").text()
                                        $.ajax({
                                            type: "POST",
                                            url: "/filemanager/prepare_violations",
                                            data: "path=" + path,
                                            success: function(data){
                                                    $.modal.close();
                                                    if (data) {
                                                            window.open("/filemanager/download_violations?name="+data)
                                                    }
                                                    else{
                                                            var myWidth = 550;
                                                            var myHeight = 50;
                                                            var option = {
                                                                opacity:70,
                                                                minWidth: myWidth,
                                                                minHeight: myHeight,
                                                                maxWidth: myWidth,
                                                                maxHeight: myHeight
                                                            };
                                                            $.modal('<img src="/global/images/attention_01.png"> Selected calculation isn\'t completed, probably is running or scheduled', option);    
                                                    }
                                                    
                                            }
                                        }); 
                                        
                                    })
                                }
                                cpath = makepath(selleft);
                                if (cpath.indexOf("xplor-nih") > 0){
                                    $("li").filter(".downloadbundlexplor").removeClass("disabled").bind("click", function(){
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
                                            $.modal('<img src="/global/images/downloadBundle.gif">', option);    
                                        var path = makepath(selleft);
                                        path_splitted = path.split("/")
                                        //if (path_splitted.length == 3){//selezionato progetto!
                                            addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                            path = path + addtopath  + $(o).children("textarea").text()
                                        //} 
                                        //path = path + "/amber/" + $(o).children("textarea").text()
                                        $.ajax({
                                            type: "POST",
                                            url: "/filemanager/prepare_results_xplor",
                                            data: "path=" + path,
                                            success: function(data){
                                                    $.modal.close();
                                                    if (data) {
                                                            window.open("/filemanager/download_results?name="+data)
                                                    }
                                                    else{
                                                            var myWidth = 550;
                                                            var myHeight = 50;
                                                            var option = {
                                                                opacity:70,
                                                                minWidth: myWidth,
                                                                minHeight: myHeight,
                                                                maxWidth: myWidth,
                                                                maxHeight: myHeight
                                                            };
                                                            $.modal('<img src="/global/images/attention_01.png"> Selected calculation isn\'t completed, probably is running or scheduled', option);    
                                                    }
                                                    
                                            }
                                        }); 
                                        
                                    });
                                }
                                cpath = makepath(selleft);
                                if (cpath.indexOf("xplor-nih") > 0){
                                    $("li").filter(".analysisxplor").removeClass("disabled").bind("click", function(){
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
                                            $.modal('<img src="/global/images/downloadBundle.gif">', option);    
                                        var path = makepath(selleft);
                                        path_splitted = path.split("/")
                                        //if (path_splitted.length == 3){//selezionato progetto!
                                            addtopath = $(selleft).parent().parent().children("u").first().children("a").children("i").text()
                                            
                                        //} 
                                        //path = path + "/amber/" + $(o).children("textarea").text()
                                        $.ajax({
                                            type: "POST",
                                            url: "/filemanager/exec_analysis",
                                            data: "path=" + path,
                                            success: function(data){
                                                    $.modal.close();
                                                    if($(selleft).next("ul").children().length == 2){
                                                        $(selleft).next("ul").append('<li><a><div class="collapsed"></div><p id="menuleft" class="dir_small close collapsed"></p><li>analysis</li></a></li>')
                                                    }
                                            }
                                        }); 
                                        
                                    });
                                }   
                            }
                            else if (level > 4){
                                $("li").filter(".download").removeClass("disabled").bind('click', function(){download();});
                                $("li").filter(".info").removeClass("disabled");
                            }
                        }
                        
                    }
                    else if($("#leftmenu").find(".ui-selected").length > 1){
                        var islevelok = true;
                        $("#leftmenu").find(".ui-selected").each(function(){
                            var level = $(this).parentsUntil("#leftmenu").filter("ul").length;
                            if (level != 4){
                                islevelok = false;
                            }
                        });
                        if (islevelok){
                            $("li").filter(".download").removeClass("disabled").bind('click', function(){download();});
                            $("li").filter(".rm").removeClass("disabled").bind("click", function(){
                                removeitem();
                            });
                        }
                        else{
                            reset_toolbar();
                        }
                    }
                }
            }
        }
        
        function reset_toolbar(){
            $("#toolbar").find("li").addClass("disabled");
            $("#toolbar").find("li").filter(".delim").removeClass("disabled");
            $("#toolbar").find("li").filter(".project").unbind("click");
            $("#toolbar").find("li").filter(".project").removeClass("disabled").bind("click", function(){window.location = "/projects/project_create";});
            $("#toolbar").find("li").filter(".download").unbind("click");
            $("#toolbar").find("li").filter(".rename").unbind("click");
            $("#toolbar").find("li").filter(".rm").unbind("click");
            $("#toolbar").find("li").filter(".amber").unbind("click");
            $("#toolbar").find("li").filter(".help").removeClass("disabled");
            $("#toolbar").find("li").filter(".downloadbundle").unbind("click");
            $("#toolbar").find("li").filter(".downloadbundle").addClass("disabled");
            $("#toolbar").find("li").filter(".downloadbundlexplor").unbind("click");
            $("#toolbar").find("li").filter(".downloadbundlexplor").addClass("disabled");
            $("#toolbar").find("li").filter(".analysisxplor").unbind("click");
            $("#toolbar").find("li").filter(".analysisxplor").addClass("disabled");
            $("#toolbar").find("li").filter(".violations").unbind("click");
            $("#toolbar").find("li").filter(".violations").addClass("disabled");
            //var level = $(selleft).parentsUntil("#leftmenu").filter("li").length;
            //if(level >= 4){
            //    $("li").filter(".mkdir").removeClass("disabled")
            //    $("li").filter(".mkfile").removeClass("disabled");
            //}
        }
        
        function open_jmolView(path, filename){
            $.ajax({
                type: 'POST',
                url: "/filemanager/read_jmol",
                data: "path="+path,
                success: function(data){
                    alert(data);
                    data = data.replace(/\n/g, "|");
                    
                    var obj = '<object name="jmolApplet0" id="jmolApplet0" classid="java:JmolApplet" type="application/x-java-applet" height="500" width="500">'+
                                    '<param name="syncId" value="216291259819275">'+
                                    '<param name="progressbar" value="true">'+
                                    '<param name="progresscolor" value="blue">'+
                                    '<param name="boxbgcolor" value="black">'+
                                    '<param name="boxfgcolor" value="white">'+
                                    '<param name="boxmessage" value="Downloading JmolApplet ...">'+
                                    '<param name="name" value="jmolApplet0">'+
                                    '<param name="archive" value="JmolApplet0.jar">'+
                                    '<param name="mayscript" value="true">'+
                                    '<param name="codebase" value="/global/jmol">'+
                                    '<param name="loadInline" value="'+data+'">';
                                    if (name == ''){
                                        obj += '<param name="script" value="select *">';
                                    }
                                    else{
                                        obj += '<param name="script" value="select atomname=MEX, atomname=AX; connect single;'+
                                        'select atomname=MEX, atomname=AY; connect single;'+
                                        'select atomname=MEX, atomname=AZ; connect single;'+
                                        'select atomname=MEX or atomname=AX or atomname=AY or atomname=AZ;'+
                                        'label %a; select protein; cartoons; color structure;'+
                                        'select protein; spacefill off; wireframe off;">';
                                    }
                                    
                                    obj += '<p style="background-color: yellow; color: black; width: 400px; height: 400px; text-align: center; vertical-align: middle;">'+
                                        'You do not have Java applets enabled in your web browser, or your browser is blocking this applet.<br>'+
                                        'Check the warning message from your browser and/or enable Java applets in<br>'+
                                        'your web browser preferences, or install the Java Runtime Environment from <a href="http://www.java.com">www.java.com</a><br></p>'+
                                        '</object>';
                                
                    var vdialog = $('<div></div>');
                        vdialog.html(obj);
                        vdialog.dialog({
                            autoOpen: false,
                            title: "Jmol Chemical structure of "+filename,
                            width: 540,
                            height: 570,
                            modal: true
                        });
                        
                        vdialog.dialog('open');
                        //if(name != ""){
                            //var script= 'select atomname=MEX, atomname=AX; connect single; select atomname=MEX, atomname=AY; connect single; select atomname=MEX, atomname=AZ; connect single; select atomname=MEX or atomname=AX or atomname=AY or atomname=AZ; label %a';
                            //jmolScript(script);
                        //}
                }
            });
        }
        
        //function quicklook(p, o){
        //    $.ajax({
        //        type: 'POST',
        //        url: '/filemanager/read_jmol',
        //        data: 'path='+p,
        //        success: function(data){
        //            var el = '<a id="ql" class="top_up">'+data+'</a>';
        //            $("body").append(el);
        //            //TopUp.displayTopUp("#ql", {title: 'titolo'});
        //        }
        //    });
        //}
        
        function quicklook(){
            var path = makepath(selleft);
            var f = $(selright).children("textarea").text();
            path = path + f
            $.ajax({
                type: 'POST',
                url: '/calculations/read_file',
                data: {'path': path},
                success: function(data){
                    var myWidth = 650;
                    var myHeight = 400;
                    var option = {
                        opacity:70,
                        minWidth: myWidth,
                        minHeight: myHeight,
                        maxWidth: myWidth,
                        maxHeight: myHeight
                    };
                    var tmp = data.replace(/\n/g, "<br>");
                    $.modal(tmp, option);
                }
            });
        }
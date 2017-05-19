/**
 * Created by linky on 2017/5/2.
 */
$(function(){
    // 初始化用户表单
    var select_ids = []
    var select2_data = [];
    var select2_data_all = [];
    var full_user = []
    var pid = $('.task-content').attr('pid');
    $.ajax({
        url: '/get_project_user/', //远程数据地址
        type: 'GET',
        data: {'pid': pid},
        dataType: 'json',
        success: function (data) {
            select2_data = data['message'];
            //初始化通知群组的下拉框
            $('#participant-task').select2({
                placeholder: '请选择选项',
                allowClear: true,
                tags: true,
                cache: false,
                data: select2_data  //数据
            });
            // 存储项目人员id
            for (var item in select2_data){
                select_ids.push(select2_data[item]['id'])
            }


            $.ajax({
                url: '/get_all_user/', //远程数据地址
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    select2_data_all = data['message'];
                    console.log(select_ids)
                    //初始化通知群组的下拉框
                    $('#inputProUser').select2({
                        placeholder: '请选择选项',
                        allowClear: true,
                        tags: true,
                        cache: false,
                        data: select2_data_all  //数据
                    }).val(select_ids).trigger('change');
                }
            })

        }
    })


    //初始化日期控件
     $('#participant-finishtime').datetimepicker({
        format: 'yyyy-mm-dd',
        minView: 2,
        pickerPosition: "top-right"
    });
    $('#participant-createtime').datetimepicker({
        format: 'yyyy-mm-dd',
        minView: 2,
        pickerPosition: "top-right"
    });
    //创建任务
    $('#create-task-btn').click(function(){
        var name = $('#inputTaskName').val(),
            intro = $('#inputTaskIntro').val(),
            part = $('#participant-task').val(),
            begin_time = $('#participant-createtime').val(),
            finish_time = $('#participant-finishtime').val(),
            level = $('#task-level').val();
        var pid = $('.task-content').attr('pid');


        console.log(name)
        var data = new FormData();
        data.append('name', name);
        data.append('intro', intro);
        data.append('part', part);
        data.append('begin_time', begin_time);
        data.append('finish_time', finish_time);
        data.append('level', level);
        data.append('pid', pid);

        $.ajax({
            url: "/create_task/",
            type: 'POST',
            dataType: 'json',
            data: data,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    $('#myModal').modal('hide');
                    layer.msg('任务创建成功', {icon: 6, time: 2000},function(){
                        window.location.reload()
                    });
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })
    })

    //删除任务
    $('.delete_task').click(function(){
        var $this = $(this)
        layer.confirm('确认删除该任务？', {
          btn: ["确定",'取消'] //按钮
        }, function(){
            var tid = $this.attr('tid')
            var data = new FormData()
            data.append('tid', tid)
            $.ajax({
                url: '/delete_task/',
                data: data,
                type: "POST",
                dataType: 'json',
                processData: false,  // tell jQuery not to process the data
                contentType: false,  // tell jQuery not to set contentType
                success:function(res){
                    if (res.result){
                        $('#myModal').modal('hide');
                        layer.msg('任务删除成功', {icon: 6, time: 2000},function(){
                            window.location.reload()
                        });
                    }else{
                         layer.msg(res.message, {icon: 5});
                    }
                }
            })

        });
    })

    //获取甘特图数据
    $.ajax({
        url:"/get_gantt_project/" +  $('.task-content').attr('pid'),
        dataType: "json",
        type: "GET",
        success:function(res){
            if (res.result){
                console.log(res.data)
                if(res.empty == false) {
                    init_gantt(res.data)
                    console.log("dsasad")
                }else{
                    console.log("11111111")
                    var str = '<p style="text-align: center; margin-top: 50px;">暂无数据</p>'
                    $('#project-gant').append(str)
                    $('.gantt').remove()
                }
            }else{
                console.log("dasda")
                 init_gantt([])
            }
        }
    })

     //甘特图
    var init_gantt = function(data){
        $(".gantt").gantt({
        source: data,
        navigate: "scroll",
        scale: "days",
        maxScale: "weeks",
        minScale: "days",
        itemsPerPage: 10,
        onRender: function() {
            if (window.console && typeof console.log === "function") {
                console.log("chart rendered");
            }
            $('#project-gant').append($('.gantt'))
            $(".bar .fn-label").mouseover(function(){
                var content = $(this).text()
                console.log(content)
                $(this).popover({
                    content:content,
                    placement: "top",
                    trigger:"hover"
                })
            })
        }
    });
    }

    // 上传项目封面时实现预览效果
    $('#reload-f').on('change', change);

    function change() {
        var pic = document.getElementById("preview"),
            file = document.getElementById("reload-f");

        var ext = file.value.substring(file.value.lastIndexOf(".") + 1).toLowerCase();

        // gif在IE浏览器暂时无法显示
        if (ext != 'png' && ext != 'jpg' && ext != 'jpeg') {
            layer.msg("图片的格式必须为png或者jpg或者jpeg格式！", {icon: 5});
            return;
        }
        var isIE = navigator.userAgent.match(/MSIE/) != null,
            isIE6 = navigator.userAgent.match(/MSIE 6.0/) != null;

        if (isIE) {
            file.select();
            var reallocalpath = document.selection.createRange().text;

            // IE6浏览器设置img的src为本地路径可以直接显示图片
            if (isIE6) {
                pic.src = reallocalpath;
            } else {
                // 非IE6版本的IE由于安全问题直接设置img的src无法显示本地图片，但是可以通过滤镜来实现
                pic.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='image',src=\"" + reallocalpath + "\")";
                // 设置img的src为base64编码的透明图片 取消显示浏览器默认图片
                pic.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
            }
        } else {
            html5Reader(file);
        }
    }

    function html5Reader(file) {
        var file = file.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
            var pic = document.getElementById("preview");
            pic.src = this.result;
        }
    }

    // 修改项目信息
    var update_project = function(){
        var pro_name = $('#inputProName').val(),
            pro_intro = $('#inputProIntro').val(),
            pro_part = $('#inputProUser').val(),
            file = document.getElementById("reload-f");
        console.log(file.files[0])
        var data = new FormData();
        data.append('pro_name',pro_name);
        data.append('pro_intro', pro_intro);
        data.append('pro_part', pro_part);
        data.append('pro_img', file.files[0]);
        data.append('pid', pid);
        $.ajax({
            url: '/update_project_info/',
            type:'POST',
            dataType:'json',
            data: data,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    var host = document.location.href;
                    var index = host.indexOf('#')
                    var new_host = host;
                    if(index){
                        new_host = host.substring(0, index) + '#setting-project'
                        console.log(new_host)
                    }

                    layer.msg('项目信息更新成功', {icon: 6, time: 2000},function(){
                        window.location.href = new_host
                    });
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })
    }
    $('#project-info-save').click(update_project)

    //删除项目
    $('#project-info-delete').click(function(){
        layer.confirm('确认删除该项目？', {
          btn: ["确定",'取消'] //按钮
        }, function(){
            var data = new FormData()
            data.append('pid', pid)
            $.ajax({
                url: '/delete_project/',
                data: data,
                type: "POST",
                dataType: 'json',
                processData: false,  // tell jQuery not to process the data
                contentType: false,  // tell jQuery not to set contentType
                success:function(res){
                    if (res.result){
                        layer.msg('项目删除成功', {icon: 6, time: 2000},function(){
                            window.location.href='/index'
                        });
                    }else{
                         layer.msg(res.message, {icon: 5});
                    }
                }
            })

        });
    })

    //任务详情
    $.ajax({
        url: '/get_full_user/', //远程数据地址
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            full_user = data['message'];
        }
    })

    $('.task-name').click(function(){
        var tid = $(this).attr('tid')
            $.ajax({
                url: '/get_task_info/' + tid,
                type: "GET",
                dataType: 'json',
                processData: false,  // tell jQuery not to process the data
                contentType: false,  // tell jQuery not to set contentType
                success:function(res){
                    console.log(res.data['task_part'])
                    if (res.result){
                        //初始化通知群组的下拉框
                        $('#infoTaskParticipant').select2({
                            placeholder: '请选择选项',
                            allowClear: true,
                            tags: true,
                            cache: false,
                            data: full_user  //数据
                        }).val(res.data['task_part']).trigger('change');
                        //初始化任务信息
                        $('#infoTaskName').text(res.data['task_name'])
                        $('#infoTaskofPro').text(res.data['project_name'])
                        $('#infoTaskIntro').val(res.data['task_intro'])
                        $('#infoTaskLevel').val(res.data['task_level'])
                        $('#update-task-btn').attr('tid', res.data['tid'])
                        //初始化日期控件
                        $('#infoTaskCreatetime').datetimepicker({
                            format: 'yyyy-mm-dd',
                            minView: 2,
                            pickerPosition: "top-right"
                        }).val(res.data['task_begintime']);
                        $('#infoTaskFinishtime').datetimepicker({
                            format: 'yyyy-mm-dd',
                            minView: 2,
                            pickerPosition: "top-right"
                        }).val(res.data['task_finishtime']);
                        if(res.data['task_status'] == 2){
                             $('#check-input').iCheck('check')
                        }else{
                            $('#check-input').iCheck('uncheck');
                        }
                        $('#infoTask').modal('show');
                    } else {
                         layer.msg(res.message, {icon: 5});
                    }
                }
            })
    })

    $('#check-input').iCheck({
        checkboxClass: 'icheckbox_minimal-red',
        radioClass: 'iradio_minimal-red',
        increaseArea: '20%' // optional
    });

    //修改任务信息
    $('#update-task-btn').click(function(){
        var intro = $('#infoTaskIntro').val(),
            part = $('#infoTaskParticipant').val(),
            begin_time = $('#infoTaskCreatetime').val(),
            finish_time = $('#infoTaskFinishtime').val(),
            level = $('#infoTaskLevel').val();
        var tid = $(this).attr('tid');
        var status = $('#check-input').is(':checked')

        var data = new FormData();
        data.append('intro', intro);
        data.append('part', part);
        data.append('begin_time', begin_time);
        data.append('finish_time', finish_time);
        data.append('level', level);
        data.append('tid', tid);
        data.append('pid', pid);
        data.append('status', status);

        $.ajax({
            url: "/update_task_info/",
            type: 'POST',
            dataType: 'json',
            data: data,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    $('#infoTask').modal('hide');
                    layer.msg('更新任务信息成功', {icon: 6, time: 2000},function(){
                        window.location.reload()
                    });
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })
    })

    /// 上传项目文件
    $('#upload-project-file').on('change', change_file);

    function change_file() {
           var file = document.getElementById("upload-project-file");
           fileReader(file);
    }

    function fileReader(file) {
        var file = file.files[0];
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
        var data = new FormData();
        data.append('file', file);
        data.append('pid', pid);
        $.ajax({
            url: '/upload_project_file/',
            type:'POST',
            dataType:'json',
            data: data,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    console.log(res.data)
                    layer.msg('上传文件成功', {icon: 6, time: 2000},function(){
                        var type = 'fa-file'
                        var color = 'gray'
                        for (var index in res.data) {
                            console.log(res)
                            if (res.data[index]["ext"] == 'doc' || res.data[index]["ext"] == 'docx' || res.data[index]["ext"] == 'wps') {
                                color = 'blue'
                                type = "fa-file-word-o"
                            } else if (res.data[index]["ext"] == 'xls' ||res.data[index]["ext"] == 'xlsx') {
                                color = 'green'
                                type = "fa-file-excel-o"
                            } else if (res.data[index]["ext"] == 'pdf') {
                                color = 'red'
                                type = "fa-file-pdf-o"
                            }

                            $('#file-table tbody').append(
                                '<tr> ' +
                                '<td><i class="fa ' + type + ' fa-2x" style="color:' + color + ';"></i>' +
                                '<span class="ml10">' + res.data[index]["name"] + '</span></td>' +
                                ' <td>' + res.data[index]["size"] + '</td>' +
                                ' <td>' + res.data[index]["user"] + '</td> ' +
                                '<td>' + res.data[index]["create_time"] + '</td>' +
                                ' <td><a href="/downloadFile?fid=' + res.data[index]["fid"] + '" class="mr10" title="下载">' +
                                '<span class="glyphicon glyphicon-download"></span></a>' +
                                ' <a href="###" title="删除" fid='+ res.data[index]["fid"]+' class="delete_file"><span class="glyphicon glyphicon-remove"></span>' +
                                '</a> </td> </tr>'
                            )
                        }
                        $('.delete_file').click(delete_file)
                    });
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })
        }
    }
    //获取项目文件
    $.ajax({
            url: "/get_project_file/" + pid,
            type: 'GET',
            dataType: 'json',
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    $('#file-table tbody').html('')
                    console.log(res.data)
                    var type = 'fa-file'
                    var color = 'gray'
                        for(var index in res.data) {
                        if(res.data[index]["ext"] == 'doc' || res.data[index]["ext"] == 'docx'|| res.data[index]["ext"] == 'wps'){
                            color = 'blue'
                            type = "fa-file-word-o"
                        }else if(res.data[index]["ext"] == 'xls' || res.data[index]["ext"] == 'xlsx'){
                            color = 'green'
                            type = "fa-file-excel-o"
                        }else if(res.data[index]["ext"] == 'pdf'){
                            color = 'red'
                            type = "fa-file-pdf-o"
                        }

                        $('#file-table tbody').append(
                                '<tr> ' +
                                '<td><i class="fa '+type+' fa-2x" style="color:'+color+';"></i>' +
                                '<span class="ml10">'+res.data[index]["name"]+'</span></td>' +
                                ' <td>'+res.data[index]["size"]+'</td>' +
                                ' <td>'+res.data[index]["user"]+'</td> ' +
                                '<td>'+res.data[index]["create_time"]+'</td>' +
                                ' <td><a href="/downloadFile?fid='+res.data[index]["fid"]+'" class="mr10" title="下载">' +
                                '<span class="glyphicon glyphicon-download"></span></a>' +
                                ' <a href="###" title="删除" fid='+ res.data[index]["fid"] +' class="delete_file"><span class="glyphicon glyphicon-remove"></span>' +
                                '</a> </td> </tr>'
                            )
                        }
                         $('.delete_file').click(delete_file)
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })
    // 删除文件
    var delete_file = function(event){
        var fid = $(this).attr("fid")
        var data = new FormData();
        var $this = $(this)

        data.append('fid', fid);

        $.ajax({
            url: "/delete_file/",
            type: 'POST',
            dataType: 'json',
            data: data,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    layer.msg('删除文件成功', {icon: 6, time: 2000},function(){
                        $($this.parents('tr')).remove()
                    });
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })
    }
})
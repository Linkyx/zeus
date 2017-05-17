/**
 * Created by linky on 2017/5/16.
 */
$(function(){
    var full_user = []
    var pid = ''
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
                        pid = res.data['pid']
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
})
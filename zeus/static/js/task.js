/**
 * Created by linky on 2017/5/2.
 */
$(function(){
    // 初始化用户表单
    $('#participant-task').select2({
        tags: true,
        placeholder: "请选择用户",
    })

    var select2_data = [];
    $.ajax({
        url: '/get_all_user/', //远程数据地址
        type: 'GET',
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
        }
    })

    //初始化日期控件
     $('#participant-finishtime').datetimepicker({
        format: 'yyyy-mm-dd',
        minView: 2,
        pickerPosition: "top-right"
    });

    //创建任务
    $('#create-task-btn').click(function(){
        var name = $('#inputTaskName').val(),
            intro = $('#inputTaskIntro').val(),
            part = $('#participant-task').val(),
            finish_time = $('#participant-finishtime').val(),
            level = $('#task-level').val();
        var pid = $('.task-content').attr('pid');


        console.log(name)
        var data = new FormData();
        data.append('name', name);
        data.append('intro', intro);
        data.append('part', part);
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
})
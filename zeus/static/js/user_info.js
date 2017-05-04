/**
 * Created by linky on 2017/5/4.
 */

$(function(){
    $('#user-info-save').click(function(){
        var name = $('#inputName'),
            email = $('#inputEmail'),
            phone = $('#inputPhone'),
            workplace = $('#inputWorkPlace'),
            job = $('#inputJob'),
            qq = $('#inputQq'),
            wechat = $('#inputWeChat');
        var data = new FormData();
        data.append('name', name.val())
        data.append('email', email.val())
        data.append('phone', phone.val())
        data.append('workplace', workplace.val())
        data.append('job', job.val())
        data.append('qq', qq.val())
        data.append('wechat', wechat.val())

        $.ajax({
            url: '/change_user_info/',
            type: "POST",
            data: data,
            dataType:'json',
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if(res.result) {
                    layer.msg('修改信息成功', {icon: 6, time: 2000}, function () {
                        window.location.href = '/user_info/'
                    });
                }else{
                    layer.msg(res.message, {icon: 5, time: 2000});
                }
            }
        })
    })
})